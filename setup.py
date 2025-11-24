"""
Setup script for Medical RAG QA System
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="medical-rag-qa",
    version="1.0.0",
    author="Xie Xin",
    author_email="2843579506@qq.com",
    description="基于RAG与大模型技术的医疗问答系统",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/medical-rag-qa",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "medical-rag-download=src.data_loader_cli:main",
            "medical-rag-qa=src.main:main",
        ],
    },
)

