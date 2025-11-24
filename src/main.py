"""
主程序入口
"""
import argparse
import os
from .vector_store import build_vector_store_from_json
from .qa_system import load_llm_model, create_qa_chain, ask_question


def main():
    parser = argparse.ArgumentParser(description='Medical RAG QA System')
    parser.add_argument(
        '--data_file',
        type=str,
        default='data/raw/pubmed_articles.json',
        help='Path to the JSON data file'
    )
    parser.add_argument(
        '--vector_db_path',
        type=str,
        default='./chroma_medical_papers_db',
        help='Path to the vector database directory'
    )
    parser.add_argument(
        '--chunk_size',
        type=int,
        default=1000,
        help='Chunk size for text splitting'
    )
    parser.add_argument(
        '--chunk_overlap',
        type=int,
        default=100,
        help='Chunk overlap for text splitting'
    )
    parser.add_argument(
        '--k',
        type=int,
        default=3,
        help='Number of documents to retrieve'
    )
    parser.add_argument(
        '--model_id',
        type=str,
        default='Qwen/Qwen2.5-1.5B-Instruct',
        help='LLM model ID'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    # 检查数据文件是否存在
    if not os.path.exists(args.data_file):
        print(f"错误: 数据文件不存在: {args.data_file}")
        print("请先运行数据抓取脚本: python -m src.data_loader")
        return
    
    # 1. 构建向量库
    print("=" * 60)
    print("步骤1: 构建向量库")
    print("=" * 60)
    vectorstore, embeddings = build_vector_store_from_json(
        json_file_path=args.data_file,
        persist_directory=args.vector_db_path,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        force_recreate=True
    )
    
    # 2. 加载LLM模型
    print("\n" + "=" * 60)
    print("步骤2: 加载大语言模型")
    print("=" * 60)
    llm = load_llm_model(model_id=args.model_id)
    
    # 3. 创建问答链
    print("\n" + "=" * 60)
    print("步骤3: 创建问答链")
    print("=" * 60)
    qa_chain, retriever = create_qa_chain(vectorstore, llm, k=args.k)
    
    # 4. 测试问题
    print("\n" + "=" * 60)
    print("步骤4: 运行测试问题")
    print("=" * 60)
    test_questions = [
        "什么是生物类似药？它们在皮肤病学中的应用如何？",
        "阿尔茨海默病的最新治疗方法有哪些？",
        "辐射烧伤的治疗原则有哪些？"
    ]
    
    for question in test_questions:
        ask_question(qa_chain, retriever, question)
    
    # 5. 交互式问答
    if args.interactive:
        print("\n" + "=" * 60)
        print("医疗文献RAG系统已启动")
        print("输入 '退出'、'exit' 或 'quit' 来结束对话")
        print("=" * 60)
        
        while True:
            user_question = input("\n请输入您的医学问题: ")
            if user_question.lower() in ['退出', 'exit', 'quit']:
                print("感谢使用！")
                break
            ask_question(qa_chain, retriever, user_question)


if __name__ == "__main__":
    main()

