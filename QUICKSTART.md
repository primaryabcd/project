# 快速开始指南

## 5分钟快速上手

### 前置要求
- Python 3.9+
- 网络连接（用于下载模型和数据）
- 4GB+ 可用内存

### 步骤1：安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 步骤2：下载数据（首次运行）

```bash
python -m src.data_loader_cli \
  --output_json data/raw/pubmed_articles.json \
  --start_date 2023/11/01 \
  --end_date 2023/11/30 \
  --num_articles 500 \
  --email your_email@example.com
```

**注意**：将 `your_email@example.com` 替换为您的真实邮箱地址。

### 步骤3：运行问答系统

```bash
python -m src.main \
  --data_file data/raw/pubmed_articles.json \
  --interactive
```

### 或者：一键运行

```bash
bash scripts/run.sh
```

## 常见问题

### Q: 模型下载很慢怎么办？
A: 首次运行需要下载约2GB的模型文件，请耐心等待。也可以使用国内镜像加速。

### Q: 内存不足怎么办？
A: 系统已使用4bit量化，最低需要4GB内存。如果仍然不足，可以减少 `--num_articles` 参数。

### Q: 如何更新知识库？
A: 重新运行数据抓取脚本，然后运行主程序（会自动重建向量库）。

## 下一步

- 阅读 [README.md](README.md) 了解详细功能
- 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) 了解代码结构
- 尝试修改参数进行实验

