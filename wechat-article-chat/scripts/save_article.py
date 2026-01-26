#!/usr/bin/env python3
"""
保存公众号文章（原文+总结）到D盘
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(__file__))
from fetch_article import fetch_article, WeChatArticleFetcher

# 文章保存目录
ARTICLES_DIR = "D:/WeChatArticles"


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        name = name.replace(char, '_')
    return name.strip()


def generate_summary(article_data):
    """生成文章总结分析"""
    title = article_data.get('title', '')
    author = article_data.get('author', '')
    content = article_data.get('content', '')

    return f"""# 文章分析

## 📄 基本信息

- **标题**: {title}
- **来源**: {author}
- **链接**: {article_data.get('url', '')}
- **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📝 核心摘要

> 此部分需要AI根据文章内容生成200-300字的核心摘要

---

## 🎯 关键观点

1. **观点一**
   - 内容: [待AI分析]

2. **观点二**
   - 内容: [待AI分析]

3. **观点三**
   - 内容: [待AI分析]

---

## 🧠 逻辑结构

[待AI梳理文章的论证框架]

---

## 💡 延伸思考

- **值得探讨的问题**: [待AI补充]
- **相关话题**: [待AI补充]
- **补充视角**: [待AI补充]

---

## 📊 文章链接

- 原文链接: {article_data.get('url', '')}
- 原文Markdown: ./01_原文.md
"""


def save_article(url, cookie_file=None):
    """保存文章（原文+总结）"""
    print(f"Fetching article: {url}")

    # 获取文章内容
    fetcher = WeChatArticleFetcher(cookie_file)
    result = fetcher.fetch_article(url)

    if 'error' in result:
        print(f"[ERROR] Failed to fetch: {result['error']}")
        if 'cookie_help' in result:
            print(f"[TIP] {result['cookie_help']}")
        return False

    # 清理文件名
    title = sanitize_filename(result['title'])
    author = sanitize_filename(result['author'])
    date_str = datetime.now().strftime('%Y%m%d')

    # 创建文章文件夹
    folder_name = f"{date_str}_{author}_{title[:50]}"  # 限制长度
    article_dir = Path(ARTICLES_DIR) / folder_name
    article_dir.mkdir(parents=True, exist_ok=True)

    print(f"Folder created: {article_dir}")

    # 保存原文
    original_file = article_dir / "01_原文.md"
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(fetcher.to_markdown(result))
    print(f"[OK] Original saved: {original_file}")

    # 保存总结模板
    summary_file = article_dir / "02_总结分析.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(generate_summary(result))
    print(f"[OK] Summary saved: {summary_file}")

    print(f"\n[DONE] Article saved successfully!")
    print(f"[DIR] {article_dir}")

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description='保存公众号文章（原文+总结）')
    parser.add_argument('url', help='公众号文章链接')
    parser.add_argument('--cookie', help='Cookie配置文件路径')

    args = parser.parse_args()

    save_article(args.url, args.cookie)


if __name__ == '__main__':
    main()
