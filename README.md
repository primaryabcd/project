# 基于RAG与大模型技术的医疗问答系统

一个基于检索增强生成（RAG）技术的医学文献智能问答系统，能够从PubMed数据库抓取医学文献，构建向量知识库，并基于大语言模型提供专业的医学问答服务。

## 项目特点

- 🔍 **自动数据抓取**：从PubMed批量下载医学文献，支持日期范围检索
- 📚 **向量知识库**：使用Chroma构建持久化向量库，支持语义检索
- 🤖 **智能问答**：基于Qwen2.5-1.5B-Instruct模型，提供专业医学问答
- 📖 **可追溯性**：每个回答都附带文献来源（PMID），确保可验证性
- 🛡️ **低幻觉**：通过RAG技术，基于真实文献生成回答，降低模型幻觉

## 项目结构

```
homework/
├── README.md                 # 项目说明文档
├── requirements.txt         # Python依赖包列表
├── .gitignore               # Git忽略文件配置
├── src/                     # 源代码目录
│   ├── __init__.py
│   ├── utils.py             # 工具函数模块
│   ├── data_loader.py       # PubMed数据抓取模块
│   ├── data_loader_cli.py   # 数据抓取命令行入口
│   ├── data_processor.py    # 数据处理模块
│   ├── vector_store.py      # 向量库构建模块
│   ├── qa_system.py         # 问答系统模块
│   └── main.py              # 主程序入口
├── scripts/                 # 运行脚本目录
│   └── run.sh              # 一键运行脚本
├── data/                    # 数据目录
│   ├── raw/                # 原始数据
│   │   └── pubmed_articles.json
│   └── processed/          # 处理后的数据
│       └── medical_papers.json
├── results/                 # 结果文件目录
└── chroma_medical_papers_db/ # 向量库目录（自动生成）
```

## 环境要求

- Python 3.9+
- CUDA 11.8+ (可选，用于GPU加速)
- 16GB+ RAM
- 20GB+ 可用磁盘空间（用于模型和向量库）

## 安装步骤

### 1. 克隆仓库

```bash
git clone <your-repo-url>
cd homework
```

### 2. 创建虚拟环境

```bash
# 使用venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法1：使用脚本运行（推荐）

```bash
bash scripts/run.sh
```

### 方法2：分步运行

#### 步骤1：下载PubMed文献数据

```bash
python -m src.data_loader_cli \
  --output_json data/raw/pubmed_articles.json \
  --start_date 2023/11/01 \
  --end_date 2023/11/30 \
  --num_articles 500 \
  --email your_email@example.com
```

**参数说明：**
- `--output_json`: 输出JSON文件路径
- `--start_date`: 开始日期 (YYYY/MM/DD)
- `--end_date`: 结束日期 (YYYY/MM/DD)
- `--num_articles`: 最大文章数量
- `--email`: 邮箱地址（NCBI API要求）

#### 步骤2：构建向量库并启动问答系统

```bash
python -m src.main \
  --data_file data/raw/pubmed_articles.json \
  --vector_db_path ./chroma_medical_papers_db \
  --interactive
```

**参数说明：**
- `--data_file`: 输入JSON文件路径
- `--vector_db_path`: 向量库保存目录
- `--chunk_size`: 文本切分大小（默认1000）
- `--chunk_overlap`: 文本重叠大小（默认100）
- `--k`: 检索文档数量（默认3）
- `--model_id`: LLM模型ID（默认Qwen2.5-1.5B-Instruct）
- `--interactive`: 启用交互式问答模式

## 使用示例

### 示例1：基本问答

系统启动后会自动运行三个测试问题：
1. 什么是生物类似药？它们在皮肤病学中的应用如何？
2. 阿尔茨海默病的最新治疗方法有哪些？
3. 辐射烧伤的治疗原则有哪些？

### 示例2：交互式问答

启用 `--interactive` 参数后，可以输入自定义问题：

```
请输入您的医学问题: 什么是心包异位甲状旁腺腺瘤？
```

系统会返回：
- 基于文献的专业回答
- 引用文献列表（标题+PMID）

输入 `退出`、`exit` 或 `quit` 结束对话。

## 技术架构

### 数据流程

1. **数据抓取**：使用Bio.Entrez API从PubMed下载文献
2. **数据清洗**：提取标题、摘要、作者、期刊等结构化信息
3. **文本切分**：使用RecursiveCharacterTextSplitter切分长文本
4. **向量化**：使用BGE-small-en-v1.5或MiniLM模型生成向量
5. **存储**：使用Chroma持久化向量库
6. **检索**：基于余弦相似度检索相关文献
7. **生成**：使用Qwen模型基于检索结果生成回答

### 核心技术

- **RAG (Retrieval Augmented Generation)**: 检索增强生成
- **LangChain**: 用于构建RAG应用链
- **Chroma**: 轻量级向量数据库
- **HuggingFace Transformers**: 模型加载与推理
- **BitsAndBytes**: 4bit量化降低显存占用

## 性能指标

- 数据抓取成功率: >95%
- 批量下载速度: ~0.26秒/篇
- 数据过滤率: ~38%（过滤无摘要文献）
- 文本切分效率: ~3.07块/篇
- 单次问答延迟: 3-5秒
- 检索召回数: 3篇文献/问题

## 注意事项

1. **邮箱配置**：NCBI API要求提供有效的邮箱地址
2. **网络环境**：首次运行需要下载模型，确保网络畅通
3. **显存要求**：使用4bit量化后，最低需要4GB显存（GPU）或8GB内存（CPU）
4. **数据更新**：向量库重建会删除旧数据库，注意备份重要数据

## 常见问题

### Q: 模型下载失败怎么办？

A: 系统会自动重试3次，失败后会切换到备用模型（all-MiniLM-L6-v2）。也可以手动指定模型ID。

### Q: 如何更新知识库？

A: 重新运行数据抓取脚本，然后重建向量库（默认会删除旧数据库）。

### Q: 支持中文问答吗？

A: 当前版本主要支持英文文献，中文问答功能在开发中。

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 作者

- 姓名：谢馨
- 学号：25125402

## 致谢

- PubMed数据库
- LangChain社区
- HuggingFace团队
- Qwen模型团队

# project
