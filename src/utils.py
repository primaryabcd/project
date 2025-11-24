"""
工具函数模块
"""
import re
import http.client


def setup_http_protocol():
    """解决HTTP协议版本问题"""
    http.client.HTTPConnection._http_vsn = 10
    http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'


def validate_date(date_str):
    """验证日期格式 YYYY/MM/DD"""
    if not re.match(r'\d{4}/\d{2}/\d{2}', date_str):
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY/MM/DD")
    return date_str


def extract_publication_date(article):
    """提取出版日期"""
    date_fields = ['ArticleDate', 'JournalIssue', 'PubDate']
    for field in date_fields:
        if field in article:
            date_info = article[field]
            if isinstance(date_info, list) and len(date_info) > 0:
                date_info = date_info[0]
            if 'Year' in date_info:
                return {
                    "year": date_info.get('Year', ''),
                    "month": date_info.get('Month', ''),
                    "day": date_info.get('Day', '')
                }
    return {"year": "", "month": "", "day": ""}


def extract_authors(article):
    """提取作者信息"""
    authors = []
    if 'AuthorList' in article:
        for author in article['AuthorList']:
            author_name = f"{author.get('LastName', '')} {author.get('ForeName', '')}".strip()
            if author_name:
                authors.append(author_name)
    return authors


def extract_journal_info(article):
    """提取期刊信息"""
    journal = article.get('Journal', {})
    return {
        "title": journal.get('Title', ''),
        "volume": journal.get('JournalIssue', {}).get('Volume', ''),
        "issue": journal.get('JournalIssue', {}).get('Issue', '')
    }

