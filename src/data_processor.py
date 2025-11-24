"""
数据处理模块：将JSON数据转换为LangChain Document对象
"""
import json
from langchain_core.documents import Document


def json_to_documents(json_data):
    """
    将JSON数据转换为Document对象
    
    Args:
        json_data: JSON格式的文献数据列表
    
    Returns:
        List[Document]: LangChain Document对象列表
    """
    documents = []
    for paper in json_data:
        # 跳过没有摘要的文章
        if not paper.get('abstract') or paper.get('abstract').strip() == '':
            continue

        # 组合标题和摘要作为内容
        content = f"Title: {paper.get('title', '')}\nAbstract: {paper.get('abstract', '')}"

        # 创建元数据
        metadata = {
            "pmid": paper.get("pmid", ""),
            "title": paper.get("title", ""),
            "authors": ", ".join(paper.get("authors", [])),
            "journal": paper.get("journal", {}).get("title", ""),
            "pub_date": f"{paper.get('pub_date', {}).get('year', '')}-{paper.get('pub_date', {}).get('month', '')}",
            "source": "medical_literature"
        }

        documents.append(Document(page_content=content, metadata=metadata))

    return documents


def load_json_data(json_file_path):
    """
    从JSON文件加载数据
    
    Args:
        json_file_path: JSON文件路径
    
    Returns:
        List[dict]: 文献数据列表
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

