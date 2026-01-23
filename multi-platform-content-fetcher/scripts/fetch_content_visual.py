#!/usr/bin/env python3
"""
多平台内容获取器 - 可视化增强版
带实时进度显示的多平台内容获取工具
"""

import json
import hashlib
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import sys

# 添加 visual-progress 框架路径
visual_progress_path = Path(__file__).parent.parent.parent / "visual-progress"
if visual_progress_path.exists():
    sys.path.insert(0, str(visual_progress_path))
    from core.visual_progress import VisualProgress
    VISUAL_PROGRESS_AVAILABLE = True
else:
    VISUAL_PROGRESS_AVAILABLE = False
    print("⚠️  visual-progress 框架未找到，将使用基础进度显示")


class ContentFetcherVisual:
    """内容获取器主类 - 可视化增强版"""

    def __init__(self, db_path: str = None, enable_visual: bool = True):
        """初始化内容获取器

        Args:
            db_path: 数据库文件路径
            enable_visual: 是否启用可视化进度
        """
        if db_path is None:
            skill_dir = Path(__file__).parent.parent
            db_path = skill_dir / "content_db.json"

        self.db_path = Path(db_path)
        self.db = self._load_database()
        self.enable_visual = enable_visual and VISUAL_PROGRESS_AVAILABLE

        # 平台图标映射
        self.platform_icons = {
            "hackernews": "🟠",
            "producthunt": "🚀",
            "github": "🐙",
            "weibo": "🔴",
            "wechat": "💬",
            "zhihu": "🔵",
            "xiaohongshu": "📕",
            "blog": "📝",
        }

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
        """检查内容是否已存在"""
        content_id = self._generate_content_id(url, title)
        return any(c["id"] == content_id for c in self.db["contents"])

    def add_content(self, title: str, url: str, content: str,
                    platform: str, author: str = "", silent: bool = False) -> Optional[Dict]:
        """添加内容到数据库

        Args:
            title: 内容标题
            url: 内容URL
            content: 内容正文/摘要
            platform: 平台来源
            author: 作者/发布者
            silent: 静默模式（不打印输出）

        Returns:
            添加的内容条目，如果重复则返回 None
        """
        # 检查是否重复
        if self.is_duplicate(url, title):
            if not silent:
                icon = self.platform_icons.get(platform, "📄")
                print(f"⚠️  {icon} 内容已存在，跳过: {title[:50]}...")
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

        if not silent:
            icon = self.platform_icons.get(platform, "📄")
            print(f"✅ {icon} 已添加: {title[:50]}... ({platform})")

        return content_entry

    def add_source(self, name: str, url: str, platform: str, source_type: str = "web"):
        """添加内容源配置"""
        source_entry = {
            "name": name,
            "url": url,
            "platform": platform,
            "type": source_type,
            "added_at": datetime.now().isoformat()
        }

        if not any(s["url"] == url and s["platform"] == platform for s in self.db["sources"]):
            self.db["sources"].append(source_entry)
            self._save_database()
            print(f"✅ 已添加内容源: {name} ({platform})")

    def get_sources(self, platform: str = None) -> List[Dict]:
        """获取内容源列表"""
        if platform:
            return [s for s in self.db["sources"] if s["platform"] == platform]
        return self.db["sources"]

    def get_contents(self, platform: str = None, limit: int = None) -> List[Dict]:
        """获取内容列表"""
        contents = self.db["contents"]
        if platform:
            contents = [c for c in contents if c["platform"] == platform]

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

    def batch_add_contents(self, items: List[Dict]) -> Dict:
        """批量添加内容（带可视化进度）

        Args:
            items: 内容列表，每个元素包含 title, url, content, platform, author

        Returns:
            处理结果统计
        """
        if not items:
            return {"total": 0, "added": 0, "skipped": 0, "platforms": {}}

        if self.enable_visual:
            return self._batch_add_with_visual(items)
        else:
            return self._batch_add_basic(items)

    def _batch_add_with_visual(self, items: List[Dict]) -> Dict:
        """使用可视化进度批量添加"""
        progress = VisualProgress(
            title="🌐 多平台内容获取",
            theme="colorful"
        )

        # 按平台分组统计
        platform_stats = {}
        for item in items:
            platform = item.get("platform", "unknown")
            platform_stats[platform] = platform_stats.get(platform, 0) + 1

        # 定义工作流
        workflow = []
        for platform, count in platform_stats.items():
            icon = self.platform_icons.get(platform, "📄")
            workflow.append({
                'id': f'fetch_{platform}',
                'name': f'{icon} 获取 {platform} 内容 ({count} 条)...',
                'total': count
            })

        # 任务执行函数
        def fetch_platform(task_id, info):
            platform = task_id.replace('fetch_', '')
            platform_items = [i for i in items if i.get('platform') == platform]

            added = 0
            skipped = 0

            for idx, item in enumerate(platform_items):
                # 更新进度
                current = idx + 1
                yield {'current': current, 'total': len(platform_items)}

                # 添加内容
                result = self.add_content(
                    title=item.get('title', ''),
                    url=item.get('url', ''),
                    content=item.get('content', ''),
                    platform=item.get('platform', ''),
                    author=item.get('author', ''),
                    silent=True
                )

                if result:
                    added += 1
                else:
                    skipped += 1

            return {'added': added, 'skipped': skipped, 'total': len(platform_items)}

        # 执行工作流
        results = progress.run_tasks(workflow, fetch_platform)

        # 汇总统计 - 处理不同的返回格式
        total_added = 0
        total_skipped = 0
        platform_details = {}

        for task_id, result in results.items():
            if isinstance(result, dict):
                added = result.get('added', 0)
                skipped = result.get('skipped', 0)
                total_added += added
                total_skipped += skipped
                platform_details[task_id] = result
            elif isinstance(result, int):
                # 如果返回的是整数，视为新增数量
                total_added += result
                platform_details[task_id] = {'added': result, 'skipped': 0}

        total_items = len(items)

        return {
            "total": total_items,
            "added": total_added,
            "skipped": total_skipped,
            "platforms": platform_details
        }

    def _batch_add_basic(self, items: List[Dict]) -> Dict:
        """基础模式批量添加（无可视化）"""
        print(f"\n📥 开始批量添加 {len(items)} 条内容...")
        print("=" * 50)

        platform_stats = {}
        added = 0
        skipped = 0

        for idx, item in enumerate(items):
            platform = item.get('platform', 'unknown')
            if platform not in platform_stats:
                platform_stats[platform] = {'added': 0, 'skipped': 0}

            print(f"\n[{idx + 1}/{len(items)}] 处理: {item.get('title', 'N/A')[:50]}...")

            result = self.add_content(
                title=item.get('title', ''),
                url=item.get('url', ''),
                content=item.get('content', ''),
                platform=platform,
                author=item.get('author', ''),
                silent=False
            )

            if result:
                added += 1
                platform_stats[platform]['added'] += 1
            else:
                skipped += 1
                platform_stats[platform]['skipped'] += 1

        print("\n" + "=" * 50)
        print(f"✅ 处理完成: {added} 条新增, {skipped} 条跳过")

        return {
            "total": len(items),
            "added": added,
            "skipped": skipped,
            "platforms": platform_stats
        }

    def display_stats_dashboard(self):
        """显示统计信息仪表板"""
        stats = self.get_stats()

        if not self.enable_visual:
            print("\n📊 数据库统计")
            print("=" * 50)
            print(f"总内容数: {stats['total_contents']}")
            print(f"内容源数: {stats['total_sources']}")
            print(f"最后更新: {stats.get('last_updated', 'N/A')}")

            if stats['platforms']:
                print("\n各平台内容分布:")
                for platform, count in sorted(stats['platforms'].items(), key=lambda x: x[1], reverse=True):
                    icon = self.platform_icons.get(platform, "📄")
                    print(f"  {icon} {platform}: {count} 条")
            return

        # 可视化仪表板
        print("\n" + "=" * 60)
        print("📊 多平台内容库 - 数据统计")
        print("=" * 60)

        print(f"\n📈 总览:")
        print(f"  • 总内容数: {stats['total_contents']} 条")
        print(f"  • 内容源数: {stats['total_sources']} 个")
        print(f"  • 最后更新: {stats.get('last_updated', 'N/A')}")

        if stats['platforms']:
            print(f"\n🏷️  平台分布:")

            # 绘制简单条形图
            max_count = max(stats['platforms'].values())
            for platform, count in sorted(stats['platforms'].items(), key=lambda x: x[1], reverse=True):
                icon = self.platform_icons.get(platform, "📄")
                bar_length = int(count / max_count * 30)
                bar = "█" * bar_length
                print(f"  {icon} {platform:15} {count:4d} 条 {bar}")

        print("\n" + "=" * 60)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="多平台内容获取器 - 可视化版")
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
    stats_parser = subparsers.add_parser("stats", help="统计信息")
    stats_parser.add_argument("--dashboard", action="store_true", help="显示仪表板")

    # 批量添加命令（新增）
    batch_parser = subparsers.add_parser("batch", help="批量添加内容（带进度）")
    batch_parser.add_argument("--file", required=True, help="包含内容列表的 JSON 文件")

    args = parser.parse_args()

    # 创建获取器实例
    fetcher = ContentFetcherVisual(enable_visual=True)

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
        if args.dashboard:
            fetcher.display_stats_dashboard()
        else:
            stats = fetcher.get_stats()
            print(json.dumps(stats, ensure_ascii=False, indent=2))

    elif args.command == "batch":
        # 从文件读取内容列表
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 支持两种格式：直接数组或带 items 字段的对象
            items = data if isinstance(data, list) else data.get('items', [])

        if not items:
            print("❌ 未找到可添加的内容")
            return

        # 批量添加
        result = fetcher.batch_add_contents(items)

        # 显示结果
        print("\n✅ 批量添加完成:")
        print(f"  总计: {result['total']} 条")
        print(f"  新增: {result['added']} 条")
        print(f"  跳过: {result['skipped']} 条")

        # 统计各平台数据
        platform_counts = {}
        for item in items:
            platform = item.get('platform', 'unknown')
            platform_counts[platform] = platform_counts.get(platform, 0) + 1

        if platform_counts:
            print("\n各平台详情:")
            for platform, total in platform_counts.items():
                icon = fetcher.platform_icons.get(platform, "📄")
                print(f"  {icon} {platform}: {total} 条")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
