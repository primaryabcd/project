"""
数据抓取命令行入口
"""
import argparse
from .data_loader import get_pubmed_data


def main():
    parser = argparse.ArgumentParser(
        description='Download PubMed articles within a specified date range'
    )
    
    parser.add_argument(
        "--output_json",
        type=str,
        default="data/raw/pubmed_articles.json",
        help="Path to the JSON output file (default: data/raw/pubmed_articles.json)",
    )
    parser.add_argument(
        "--start_date",
        type=str,
        default="2023/11/01",
        help="Start date in YYYY/MM/DD format (default: 2023/11/01)",
    )
    parser.add_argument(
        "--end_date",
        type=str,
        default="2023/11/30",
        help="End date in YYYY/MM/DD format (default: 2023/11/30)",
    )
    parser.add_argument(
        "--num_articles",
        type=int,
        default=500,
        help="Maximum number of articles to download (default: 500)",
    )
    parser.add_argument(
        "--email",
        type=str,
        default="2843579506@qq.com",
        help="Email address for NCBI (required by API)",
    )
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    import os
    os.makedirs(os.path.dirname(args.output_json), exist_ok=True)
    
    success = get_pubmed_data(
        output_json_file=args.output_json,
        start_date=args.start_date,
        end_date=args.end_date,
        max_num_articles=args.num_articles,
        email=args.email
    )
    
    if success:
        print(f"\n数据下载完成！文件保存在: {args.output_json}")
    else:
        print("\n数据下载失败，请检查错误信息。")


if __name__ == "__main__":
    main()

