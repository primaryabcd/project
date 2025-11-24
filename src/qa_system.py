"""
问答系统模块
"""
import torch
from transformers import BitsAndBytesConfig
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma


def load_llm_model(model_id="Qwen/Qwen2.5-1.5B-Instruct",
                   max_new_tokens=512,
                   temperature=0.1):
    """
    加载大语言模型（使用4bit量化）
    
    Args:
        model_id: 模型ID
        max_new_tokens: 最大生成token数
        temperature: 温度参数
    
    Returns:
        HuggingFacePipeline: LLM管道对象
    """
    print(f"正在加载{model_id}模型（这可能需要几分钟，首次运行需要下载模型）...")
    
    # 配置4位量化
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )
    
    llm = HuggingFacePipeline.from_model_id(
        model_id=model_id,
        task="text-generation",
        device=0 if torch.cuda.is_available() else -1,
        model_kwargs={
            "torch_dtype": torch.float16,
            "quantization_config": quantization_config,
        },
        pipeline_kwargs={
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "do_sample": True,
        }
    )
    print("模型加载完成")
    return llm


def create_medical_prompt_template():
    """
    创建医学专用提示模板
    
    Returns:
        PromptTemplate: 提示模板对象
    """
    medical_prompt_template = """你是一个专业的医学研究助手。请根据以下医学文献内容回答问题。如果文献中没有相关信息，请如实告知。

相关文献内容：
{context}

问题：{question}

请基于文献内容提供专业、准确的回答，并注明信息来源。"""
    
    return PromptTemplate(
        template=medical_prompt_template,
        input_variables=["context", "question"]
    )


def format_docs(docs):
    """格式化文档列表为字符串"""
    return "\n\n".join(doc.page_content for doc in docs)


def create_qa_chain(vectorstore: Chroma, llm, k=3):
    """
    创建问答链
    
    Args:
        vectorstore: 向量库对象
        llm: 大语言模型
        k: 检索的文档数量
    
    Returns:
        Runnable: 问答链对象
    """
    # 创建检索器
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    
    # 创建提示模板
    PROMPT = create_medical_prompt_template()
    
    # 检索并格式化函数
    def retrieve_and_format(question_dict):
        """检索文档并格式化"""
        question = question_dict["question"]
        docs = retriever.invoke(question)
        return {
            "context": format_docs(docs),
            "question": question
        }
    
    # 构建问答链
    qa_chain = (
        RunnablePassthrough()
        | retrieve_and_format
        | PROMPT
        | llm
        | StrOutputParser()
    )
    
    return qa_chain, retriever


def ask_question(qa_chain, retriever, question):
    """
    提问函数
    
    Args:
        qa_chain: 问答链
        retriever: 检索器
        question: 问题文本
    
    Returns:
        dict: 包含回答和来源文献的字典
    """
    print(f"\n问题: {question}")
    print("-" * 50)
    
    # 获取相关文档
    docs = retriever.invoke(question)
    
    # 使用链进行问答
    result = qa_chain.invoke({"question": question})
    print(f"回答: {result}")
    
    # 显示来源文献
    print("\n来源文献:")
    sources = []
    for i, doc in enumerate(docs):
        source_info = {
            "index": i + 1,
            "title": doc.metadata.get('title', 'Unknown'),
            "pmid": doc.metadata.get('pmid', 'Unknown')
        }
        sources.append(source_info)
        print(f"{i + 1}. {source_info['title']} (PMID: {source_info['pmid']})")
    
    return {
        "question": question,
        "answer": result,
        "sources": sources
    }

