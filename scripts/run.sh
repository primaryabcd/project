#!/bin/bash

# Medical RAG QA System - 一键运行脚本
# 使用方法: bash scripts/run.sh

set -e  # 遇到错误立即退出

echo "=========================================="
echo "医疗问答系统 - 一键运行脚本"
echo "=========================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.9+"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "检查并安装依赖..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p results

# 检查数据文件是否存在
if [ ! -f "data/raw/pubmed_articles.json" ]; then
    echo ""
    echo "=========================================="
    echo "步骤1: 下载PubMed文献数据"
    echo "=========================================="
    echo "提示: 首次运行需要下载数据，这可能需要几分钟..."
    echo ""
    
    read -p "请输入您的邮箱地址 (NCBI API要求): " email
    if [ -z "$email" ]; then
        email="2843579506@qq.com"
        echo "使用默认邮箱: $email"
    fi
    
    python -m src.data_loader_cli \
        --output_json data/raw/pubmed_articles.json \
        --start_date 2023/11/01 \
        --end_date 2023/11/30 \
        --num_articles 500 \
        --email "$email"
    
    if [ $? -ne 0 ]; then
        echo "错误: 数据下载失败"
        exit 1
    fi
else
    echo "数据文件已存在，跳过下载步骤"
fi

# 运行主程序
echo ""
echo "=========================================="
echo "步骤2: 构建向量库并启动问答系统"
echo "=========================================="
echo ""

python -m src.main \
    --data_file data/raw/pubmed_articles.json \
    --vector_db_path ./chroma_medical_papers_db \
    --interactive

echo ""
echo "=========================================="
echo "运行完成！"
echo "=========================================="


