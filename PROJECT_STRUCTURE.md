# 项目结构说明

## 目录结构

```
homework/
├── README.md                    # 项目主文档
├── requirements.txt             # Python依赖包
├── setup.py                     # 安装配置文件
├── .gitignore                   # Git忽略文件
├── PROJECT_STRUCTURE.md         # 本文件
│
├── src/                         # 源代码目录
│   ├── __init__.py             # 包初始化文件
│   ├── utils.py                # 工具函数模块
│   │   ├── setup_http_protocol()      # HTTP协议设置
│   │   ├── validate_date()            # 日期验证
│   │   ├── extract_publication_date()  # 提取出版日期
│   │   ├── extract_authors()           # 提取作者信息
│   │   └── extract_journal_info()      # 提取期刊信息
│   │
│   ├── data_loader.py          # PubMed数据抓取模块
│   │   ├── search()                    # 搜索PubMed文章
│   │   ├── fetch_details()             # 获取文章详情（含重试）
│   │   ├── extract_article_info()       # 提取文章信息
│   │   └── get_pubmed_data()           # 主抓取函数
│   │
│   ├── data_loader_cli.py      # 数据抓取命令行入口
│   │   └── main()                      # CLI主函数
│   │
│   ├── data_processor.py       # 数据处理模块
│   │   ├── json_to_documents()         # JSON转Document
│   │   └── load_json_data()            # 加载JSON文件
│   │
│   ├── vector_store.py         # 向量库构建模块
│   │   ├── create_text_splitter()      # 创建文本切分器
│   │   ├── load_embedding_model()      # 加载嵌入模型（主备切换）
│   │   ├── create_vector_store()       # 创建向量库
│   │   └── build_vector_store_from_json()  # 完整构建流程
│   │
│   ├── qa_system.py            # 问答系统模块
│   │   ├── load_llm_model()            # 加载LLM模型（4bit量化）
│   │   ├── create_medical_prompt_template()  # 创建提示模板
│   │   ├── create_qa_chain()           # 创建问答链
│   │   └── ask_question()              # 提问函数
│   │
│   └── main.py                 # 主程序入口
│       └── main()                      # 主函数
│
├── scripts/                    # 运行脚本目录
│   └── run.sh                 # 一键运行脚本
│
├── data/                       # 数据目录
│   ├── raw/                   # 原始数据
│   │   ├── .gitkeep
│   │   └── pubmed_articles.json  # PubMed原始数据
│   └── processed/             # 处理后的数据
│       ├── .gitkeep
│       └── medical_papers.json  # 示例数据
│
├── results/                    # 结果文件目录
│   └── .gitkeep
│
└── chroma_medical_papers_db/   # 向量库目录（自动生成）
    ├── chroma.sqlite3
    └── [UUID目录]/
```

## 模块说明

### 1. utils.py - 工具函数
提供通用的工具函数，包括：
- HTTP协议设置
- 日期验证
- 文献信息提取（日期、作者、期刊）

### 2. data_loader.py - 数据抓取
负责从PubMed API抓取医学文献：
- 支持日期范围检索
- 批量下载（200篇/批次）
- 自动重试机制
- 数据清洗与结构化

### 3. data_processor.py - 数据处理
将JSON数据转换为LangChain Document对象：
- 过滤无摘要文献
- 构建元数据
- 文本格式化

### 4. vector_store.py - 向量库
构建和管理向量数据库：
- 文本切分（chunk_size=1000, overlap=100）
- 嵌入模型加载（主备切换）
- Chroma向量库创建与持久化

### 5. qa_system.py - 问答系统
实现RAG问答功能：
- LLM模型加载（4bit量化）
- 提示模板设计
- 检索-生成链路
- 来源追溯

### 6. main.py - 主程序
整合所有模块，提供完整的运行流程：
1. 构建向量库
2. 加载LLM模型
3. 创建问答链
4. 运行测试问题
5. 交互式问答（可选）

## 数据流

```
PubMed API
    ↓
data_loader.py (抓取)
    ↓
pubmed_articles.json (原始数据)
    ↓
data_processor.py (处理)
    ↓
Document对象列表
    ↓
vector_store.py (向量化)
    ↓
Chroma向量库
    ↓
qa_system.py (检索+生成)
    ↓
专业医学回答 + 文献来源
```

## 使用流程

### 开发模式
```bash
# 1. 下载数据
python -m src.data_loader_cli --output_json data/raw/pubmed_articles.json

# 2. 运行系统
python -m src.main --data_file data/raw/pubmed_articles.json --interactive
```

### 生产模式
```bash
# 一键运行
bash scripts/run.sh
```

## 扩展建议

1. **添加测试**：在 `tests/` 目录下添加单元测试
2. **配置管理**：使用 `config.yaml` 管理配置参数
3. **日志系统**：添加 `logging` 模块记录运行日志
4. **API服务**：使用 FastAPI 创建 Web API
5. **前端界面**：使用 Streamlit 或 Gradio 创建可视化界面

