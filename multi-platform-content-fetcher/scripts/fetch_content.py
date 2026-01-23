#!/usr/bin/env python3
"""
多平台内容获取器 - 核心脚本
支持从多个平台获取内容并存储到本地 JSON 数据库
"""

import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import sys


class ContentFetcher:
    """内容获取器主类"""

    def __init__(self, db_path: str = None):
        """初始化内容获取器

        Args:
            db_path: 数据库文件路径，默认为 ~/.claude/skills/multi-platform-content-fetcher/content_db.json
        """
        if db_path is None:
            skill_dir = Path(__file__).parent.parent
            db_path = skill_dir / "content_db.json"

        self.db_path = Path(db_path)
        self.db = self._load_database()

    def _load_database(self) -> Dict:
        """加载数据库"""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "contents": [],
            "sources": [],
            "last_updated": None
        }

    def _save_database(self):
        """保存数据库"""
        self.db["last_updated"] = datetime.now().isoformat()
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)

    def _generate_content_id(self, url: str, title: str) -> str:
        """生成内容唯一ID"""
        content = f"{url}|{title}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def is_duplicate(self, url: str, title: str) -> bool:
        """检查内容是否已存在

        Args:
            url: 内容URL
            title: 内容标题

        Returns:
            True if duplicate, False otherwise
        """
        content_id = self._generate_content_id(url, title)
        return any(c["id"] == content_id for c in self.db["contents"])

    def add_content(self, title: str, url: str, content: str,
                    platform: str, author: str = "") -> Dict:
        """添加内容到数据库

        Args:
            title: 内容标题
            url: 内容URL
            content: 内容正文/摘要
            platform: 平台来源
            author: 作者/发布者（可选）

        Returns:
            添加的内容条目
        """
        # 检查是否重复
        if self.is_duplicate(url, title):
            print(f"⚠️  内容已存在，跳过: {title}")
            return None

        content_entry = {
            "id": self._generate_content_id(url, title),
            "title": title,
            "url": url,
            "content": content,
            "platform": platform,
            "author": author,
            "fetched_at": datetime.now().isoformat()
        }

        self.db["contents"].append(content_entry)
        self._save_database()
        print(f"✅ 已添加: {title} ({platform})")
        return content_entry

    def add_source(self, name: str, url: str, platform: str,
                   source_type: str = "web"):
        """添加内容源配置

        Args:
            name: 来源名称
            url: 来源URL
            platform: 平台名称
            source_type: 来源类型 (web, rss, api)
        """
        source_entry = {
            "name": name,
            "url": url,
            "platform": platform,
            "type": source_type,
            "added_at": datetime.now().isoformat()
        }

        # 避免重复添加源
        if not any(s["url"] == url and s["platform"] == platform for s in self.db["sources"]):
            self.db["sources"].append(source_entry)
            self._save_database()
            print(f"✅ 已添加内容源: {name} ({platform})")

    def get_sources(self, platform: str = None) -> List[Dict]:
        """获取内容源列表

        Args:
            platform: 筛选平台，None 表示获取全部

        Returns:
            内容源列表
        """
        if platform:
            return [s for s in self.db["sources"] if s["platform"] == platform]
        return self.db["sources"]

    def get_contents(self, platform: str = None, limit: int = None) -> List[Dict]:
        """获取内容列表

        Args:
            platform: 筛选平台，None 表示获取全部
            limit: 限制返回数量

        Returns:
            内容列表（按获取时间倒序）
        """
        contents = self.db["contents"]
        if platform:
            contents = [c for c in contents if c["platform"] == platform]

        # 按获取时间倒序排序
        contents = sorted(contents, key=lambda x: x["fetched_at"], reverse=True)

        if limit:
            contents = contents[:limit]

        return contents

    def get_stats(self) -> Dict:
        """获取数据库统计信息"""
        stats = {
            "total_contents": len(self.db["contents"]),
            "total_sources": len(self.db["sources"]),
            "platforms": {},
            "last_updated": self.db["last_updated"]
        }

        for content in self.db["contents"]:
            platform = content["platform"]
            stats["platforms"][platform] = stats["platforms"].get(platform, 0) + 1

        return stats


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="多平台内容获取器")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 添加内容命令
    add_parser = subparsers.add_parser("add", help="添加内容")
    add_parser.add_argument("--title", required=True, help="内容标题")
    add_parser.add_argument("--url", required=True, help="内容URL")
    add_parser.add_argument("--content", required=True, help="内容正文")
    add_parser.add_argument("--platform", required=True, help="平台名称")
    add_parser.add_argument("--author", default="", help="作者")

    # 添加源命令
    source_parser = subparsers.add_parser("add-source", help="添加内容源")
    source_parser.add_argument("--name", required=True, help="来源名称")
    source_parser.add_argument("--url", required=True, help="来源URL")
    source_parser.add_argument("--platform", required=True, help="平台名称")
    source_parser.add_argument("--type", default="web", help="来源类型")

    # 列出内容命令
    list_parser = subparsers.add_parser("list", help="列出内容")
    list_parser.add_argument("--platform", help="筛选平台")
    list_parser.add_argument("--limit", type=int, help="限制数量")

    # 统计命令
    subparsers.add_parser("stats", help="统计信息")

    args = parser.parse_args()
    fetcher = ContentFetcher()

    if args.command == "add":
        fetcher.add_content(
            title=args.title,
            url=args.url,
            content=args.content,
            platform=args.platform,
            author=args.author
        )
    elif args.command == "add-source":
        fetcher.add_source(
            name=args.name,
            url=args.url,
            platform=args.platform,
            source_type=args.type
        )
    elif args.command == "list":
        contents = fetcher.get_contents(platform=args.platform, limit=args.limit)
        print(json.dumps(contents, ensure_ascii=False, indent=2))
    elif args.command == "stats":
        stats = fetcher.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
