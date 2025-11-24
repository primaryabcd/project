"""
向量库构建模块
"""
import os
import shutil
import time
import torch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


def create_text_splitter(chunk_size=1000, chunk_overlap=100):
    """
    创建文本切分器
    
    Args:
        chunk_size: 每个chunk的最大长度
        chunk_overlap: chunk之间的重叠长度
    
    Returns:
        RecursiveCharacterTextSplitter: 文本切分器对象
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )


def load_embedding_model(max_retries=3):
    """
    加载嵌入模型，支持主备切换
    
    Args:
        max_retries: 最大重试次数
    
    Returns:
        HuggingFaceEmbeddings: 嵌入模型对象
    """
    retry_count = 0
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    while retry_count < max_retries:
        try:
            # 优先尝试使用 BGE 模型
            embeddings = HuggingFaceEmbeddings(
                model_name="BAAI/bge-small-en-v1.5",
                model_kwargs={'device': device},
                encode_kwargs={'normalize_embeddings': True}
            )
            print("嵌入模型加载成功 (BAAI/bge-small-en-v1.5)")
            return embeddings
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"模型下载失败，正在重试 ({retry_count}/{max_retries})...")
                time.sleep(5)
            else:
                print("使用备用模型...")
                try:
                    # 备用方案：使用更小的模型
                    embeddings = HuggingFaceEmbeddings(
                        model_name="sentence-transformers/all-MiniLM-L6-v2",
                        model_kwargs={'device': device}
                    )
                    print("备用嵌入模型加载成功 (all-MiniLM-L6-v2)")
                    return embeddings
                except Exception as e2:
                    print(f"所有嵌入模型加载失败: {e2}")
                    raise


def create_vector_store(documents: list[Document], 
                       embeddings: HuggingFaceEmbeddings,
                       persist_directory: str = "./chroma_medical_papers_db",
                       force_recreate: bool = False):
    """
    创建Chroma向量库
    
    Args:
        documents: Document对象列表
        embeddings: 嵌入模型
        persist_directory: 持久化目录
        force_recreate: 是否强制重建（删除旧数据库）
    
    Returns:
        Chroma: 向量库对象
    """
    # 如果数据库已存在，先删除（避免维度不匹配）
    if force_recreate and os.path.exists(persist_directory):
        print("检测到旧的向量数据库，正在删除以避免维度不匹配...")
        shutil.rmtree(persist_directory)
        print("旧数据库已删除")
    
    print("正在创建向量数据库...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print("向量数据库创建完成")
    return vectorstore


def build_vector_store_from_json(json_file_path: str,
                                persist_directory: str = "./chroma_medical_papers_db",
                                chunk_size: int = 1000,
                                chunk_overlap: int = 100,
                                force_recreate: bool = True):
    """
    从JSON文件构建向量库（完整流程）
    
    Args:
        json_file_path: JSON文件路径
        persist_directory: 向量库持久化目录
        chunk_size: chunk大小
        chunk_overlap: chunk重叠大小
        force_recreate: 是否强制重建
    
    Returns:
        tuple: (vectorstore, embeddings) 向量库和嵌入模型
    """
    from .data_processor import load_json_data, json_to_documents
    
    # 1. 加载JSON数据
    print("正在加载医学文献数据...")
    medical_papers = load_json_data(json_file_path)
    print(f"成功加载 {len(medical_papers)} 篇医学文献")
    
    # 2. 转换为Document对象
    documents = json_to_documents(medical_papers)
    print(f"成功处理 {len(documents)} 篇有效文献（已过滤无摘要的文章）")
    
    # 3. 分割文本
    text_splitter = create_text_splitter(chunk_size, chunk_overlap)
    texts = text_splitter.split_documents(documents)
    print(f"成功分割 {len(texts)} 个文本块")
    
    # 4. 加载嵌入模型
    print("正在加载嵌入模型...")
    embeddings = load_embedding_model()
    
    # 5. 创建向量库
    vectorstore = create_vector_store(
        texts, 
        embeddings, 
        persist_directory, 
        force_recreate
    )
    
    return vectorstore, embeddings

