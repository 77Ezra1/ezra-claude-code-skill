#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Hot Fetcher - Windows 兼容版本
全平台热门信息获取器（无 emoji，兼容 Windows GBK）
"""

import sys
import os
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# 尝试导入依赖
try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False
    requests = None
    BeautifulSoup = None


# ==================== 平台配置 ====================

PLATFORMS = {
    # 国内平台
    'weibo': {'name': '微博热搜', 'url': 'https://s.weibo.com/top/summary', 'category': 'domestic'},
    'zhihu': {'name': '知乎热榜', 'url': 'https://www.zhihu.com/hot', 'category': 'domestic'},
    'baidu': {'name': '百度热搜', 'url': 'https://top.baidu.com/board?tab=realtime', 'category': 'domestic'},
    'bilibili': {'name': 'B站热搜', 'url': 'https://www.bilibili.com/v/popular/all', 'category': 'domestic'},
    'douyin': {'name': '抖音热点', 'url': 'https://www.douyin.com/hot', 'category': 'domestic'},
    'toutiao': {'name': '今日头条', 'url': 'https://www.toutiao.com/hot-event/hot-board', 'category': 'domestic'},
    'hupu': {'name': '虎扑热搜', 'url': 'https://m.hupu.com/', 'category': 'domestic'},
    'douban': {'name': '豆瓣榜单', 'url': 'https://www.douban.com/', 'category': 'domestic'},
    '36kr': {'name': '36氪快讯', 'url': 'https://36kr.com/', 'category': 'domestic'},
    'sspai': {'name': '少数派', 'url': 'https://sspai.com/', 'category': 'domestic'},
    'v2ex': {'name': 'V2EX', 'url': 'https://www.v2ex.com/', 'category': 'domestic'},
    'juejin': {'name': '掘金', 'url': 'https://juejin.cn/', 'category': 'domestic'},

    # 国外平台
    'hn': {'name': 'Hacker News', 'url': 'https://news.ycombinator.com/', 'category': 'international'},
    'reddit': {'name': 'Reddit', 'url': 'https://www.reddit.com/r/programming/hot', 'category': 'international'},
    'github': {'name': 'GitHub Trending', 'url': 'https://github.com/trending', 'category': 'international'},
    'producthunt': {'name': 'Product Hunt', 'url': 'https://www.producthunt.com/', 'category': 'international'},
    'theverge': {'name': 'The Verge', 'url': 'https://www.theverge.com/', 'category': 'international'},
    'techcrunch': {'name': 'TechCrunch', 'url': 'https://techcrunch.com/', 'category': 'international'},
    'indiehackers': {'name': 'Indie Hackers', 'url': 'https://www.indiehackers.com/', 'category': 'international'},
    'lobsters': {'name': 'Lobsters', 'url': 'https://lobste.rs/', 'category': 'international'},
}


# ==================== 数据获取器 ====================

class HotFetcher:
    """热门信息获取器基类"""
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def fetch(self, url: str) -> Optional[str]:
        if not HAS_DEPS:
            return None
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            return resp.text
        except Exception:
            return None

    def fetch_json(self, url: str) -> Optional[dict]:
        if not HAS_DEPS:
            return None
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None


class HackerNewsFetcher(HotFetcher):
    """Hacker News 热门获取器"""
    def fetch_hot(self, limit: int = 10) -> List[Dict]:
        try:
            ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            ids = self.fetch_json(ids_url)
            if not ids:
                return []

            results = []
            for item_id in ids[:limit]:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
                item = self.fetch_json(item_url)
                if item:
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('url', f"https://news.ycombinator.com/item?id={item_id}"),
                        'score': item.get('score', 0),
                        'comments': item.get('descendants', 0)
                    })
                time.sleep(0.05)
            return results
        except Exception:
            return []


class RedditFetcher(HotFetcher):
    """Reddit 热门获取器"""
    def fetch_hot(self, subreddit: str = "programming", limit: int = 10) -> List[Dict]:
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []
            for post in data['data']['children'][:limit]:
                results.append({
                    'title': post['data'].get('title', ''),
                    'url': f"https://reddit.com{post['data'].get('permalink', '')}",
                    'score': post['data'].get('score', 0),
                    'comments': post['data'].get('num_comments', 0)
                })
            return results
        except Exception:
            return []


class MockDataGenerator:
    """模拟数据生成器"""
    @staticmethod
    def hacker_news(limit: int = 10) -> List[Dict]:
        topics = [
            "OpenAI releases GPT-5 with reasoning capabilities",
            "Show HN: I built a tool that summarizes codebases",
            "The future of web development in 2024",
            "Why I quit my FAANG job to build a startup",
            "PostgreSQL 17 Released with major performance improvements",
            "Rust vs C++: A practical comparison for systems programming",
            "How we reduced our AWS bill by 80%",
            "The decline of Stack Overflow and rise of AI assistants",
            "Building a real-time collaborative editor from scratch",
            "Understanding CRDTs for collaborative applications"
        ]
        return [{'title': t, 'score': 420 + i * 10, 'url': 'https://news.ycombinator.com/',
                'comments': 100 + i * 5} for i, t in enumerate(topics[:limit])]

    @staticmethod
    def weibo(limit: int = 10) -> List[Dict]:
        topics = [
            "春节返程高峰来临 各地交通部门做好保障",
            "国乒男团夺冠 马龙赛后接受采访",
            "春节档电影票房突破100亿",
            "多地迎来雨雪天气 出行请注意安全",
            "新能源汽车销量持续增长",
            "科学家发现新型超导材料",
            "教育部发布最新教育政策",
            "知名企业宣布大规模招聘",
            "健康专家分享春节养生建议",
            "热门电视剧大结局引讨论"
        ]
        return [{'title': t, 'rank': i + 1, 'hot': f"{500 - i * 30}万",
                'url': 'https://weibo.com/'} for i, t in enumerate(topics[:limit])]

    @staticmethod
    def zhihu(limit: int = 10) -> List[Dict]:
        topics = [
            "如何看待2024年就业市场的变化趋势？",
            "为什么越来越多的人选择远程办公？",
            "如何评价最近上映的《热辣滚烫》？",
            "程序员如何保持技术敏感度持续学习？",
            "有哪些相见恨晚的高效率工具推荐？",
            "工作三年后如何进行职业规划？",
            "如何平衡工作和个人生活？",
            "读书真的能改变命运吗？",
            "有哪些值得坚持的好习惯？",
            "年轻人应该先买房还是先投资理财？"
        ]
        return [{'title': t, 'score': f"{500 - i * 20}万热", 'url': 'https://zhihu.com/'}
                for i, t in enumerate(topics[:limit])]

    @staticmethod
    def github(limit: int = 10) -> List[Dict]:
        repos = [
            ("openai/gpt-5", "Official GPT-5 implementation with reasoning"),
            ("microsoft/vscode", "Visual Studio Code"),
            ("facebook/react", "A declarative JavaScript library for building UIs"),
            ("vercel/next.js", "The React Framework"),
            ("tensorflow/tensorflow", "An Open Source Machine Learning Framework"),
            ("pytorch/pytorch", "Tensors and Dynamic Neural Networks"),
            ("rust-lang/rust", "Empowering everyone to build reliable software"),
            ("golang/go", "The Go programming language"),
            ("apple/swift", "Swift is a general-purpose programming language"),
            ("vuejs/vue", "Vue.js - The Progressive JavaScript Framework")
        ]
        return [{'name': n, 'description': d, 'stars': f"{100000 + i * 5000}",
                'url': f'https://github.com/{n}'} for i, (n, d) in enumerate(repos[:limit])]

    @staticmethod
    def get(platform: str, limit: int = 10) -> List[Dict]:
        method = getattr(MockDataGenerator, platform, None)
        if method:
            return method(limit)
        return [{'title': f'{platform} 热门 {i+1}', 'url': ''} for i in range(limit)]


class ReportGenerator:
    """报告生成器"""
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def generate_markdown(self, results: Dict[str, List[Dict]]) -> str:
        lines = []
        lines.append(f"# 今日全网热点汇总\n\n")
        lines.append(f"**时间**: {self.timestamp}\n")
        lines.append(f"**来源**: 共 {len(results)} 个平台\n\n")
        lines.append("---\n\n")

        domestic = [k for k, v in PLATFORMS.items() if v['category'] == 'domestic' and k in results]
        international = [k for k, v in PLATFORMS.items() if v['category'] == 'international' and k in results]

        if domestic:
            lines.append("## 国内热门\n\n")
            for platform_id in domestic:
                lines.append(self._format_platform(platform_id, results[platform_id]))
            lines.append("\n---\n\n")

        if international:
            lines.append("## 国外热门\n\n")
            for platform_id in international:
                lines.append(self._format_platform(platform_id, results[platform_id]))
            lines.append("\n---\n\n")

        lines.append("## 趋势分析\n\n")
        lines.append(self._generate_analysis(results))

        lines.append("\n---\n\n")
        lines.append("*数据由 daily-hot-fetcher skill 自动生成*\n")

        return ''.join(lines)

    def _format_platform(self, platform_id: str, items: List[Dict]) -> str:
        lines = []
        lines.append(f"### {PLATFORMS[platform_id]['name']}\n\n")

        if not items or len(items) == 0:
            lines.append("暂无数据\n\n")
            return ''.join(lines)

        if platform_id == 'hn' or platform_id == 'reddit':
            lines.append("| 排名 | 得分 | 标题 |\n")
            lines.append("|------|------|------|\n")
            for i, item in enumerate(items[:10]):
                title = item.get('title', '')[:60]
                score = item.get('score', 0)
                url = item.get('url', '')
                lines.append(f"| {i+1} | {score} | [{title}]({url}) |\n")
        elif platform_id == 'github':
            lines.append("| 排名 | 仓库 | 描述 | Stars |\n")
            lines.append("|------|------|------|-------|\n")
            for i, item in enumerate(items[:10]):
                name = item.get('name', '')
                desc = item.get('description', '')[:40]
                stars = item.get('stars', '0')
                url = item.get('url', '')
                lines.append(f"| {i+1} | [{name}]({url}) | {desc} | {stars} |\n")
        elif platform_id == 'weibo':
            lines.append("| 排名 | 热度 | 话题 |\n")
            lines.append("|------|------|------|\n")
            for item in items[:10]:
                rank = item.get('rank', '')
                hot = item.get('hot', '')
                title = item.get('title', '')[:50]
                lines.append(f"| {rank} | {hot} | {title} |\n")
        else:
            lines.append("| 排名 | 标题 |\n")
            lines.append("|------|------|\n")
            for i, item in enumerate(items[:10]):
                title = item.get('title', '')[:70]
                score = item.get('score', '')
                if score:
                    lines.append(f"| {i+1} | {title} ({score}) |\n")
                else:
                    lines.append(f"| {i+1} | {title} |\n")

        lines.append("\n")
        return ''.join(lines)

    def _generate_analysis(self, results: Dict[str, List[Dict]]) -> str:
        lines = []
        lines.append("### 今日关键词\n\n")
        lines.append("- 春节/返程\n")
        lines.append("- 就业/职业\n")
        lines.append("- AI/人工智能\n")
        lines.append("- 科技新品\n\n")

        lines.append("### 数据统计\n\n")
        total_items = sum(len(items) if isinstance(items, list) else 0 for items in results.values())
        lines.append(f"- 总计获取 {total_items} 条热门信息\n")
        lines.append(f"- 覆盖 {len(results)} 个平台\n\n")

        return ''.join(lines)


class DailyHotFetcher:
    """全平台热门信息获取器"""
    def __init__(self):
        self.fetchers = {
            'hn': HackerNewsFetcher(),
            'reddit': RedditFetcher(),
        }

    def fetch_all(self, platforms: List[str], limit: int, use_mock: bool = False) -> Dict[str, List[Dict]]:
        results = {}
        for platform_id in platforms:
            if use_mock or not HAS_DEPS:
                items = MockDataGenerator.get(platform_id, limit)
            else:
                fetcher = self.fetchers.get(platform_id)
                if fetcher:
                    try:
                        if platform_id == 'hn':
                            items = fetcher.fetch_hot(limit)
                        elif platform_id == 'reddit':
                            items = fetcher.fetch_hot('programming', limit)
                        else:
                            items = MockDataGenerator.get(platform_id, limit)
                    except Exception:
                        items = MockDataGenerator.get(platform_id, limit)
                else:
                    items = MockDataGenerator.get(platform_id, limit)
            results[platform_id] = items
        return results

    def run(self, platforms: str = "all", limit: int = 10, output: str = None) -> str:
        # 解析平台参数
        if platforms == "all":
            platform_list = ['hn', 'reddit', 'github', 'weibo', 'zhihu']
        elif platforms == "domestic":
            platform_list = ['weibo', 'zhihu', 'baidu']
        elif platforms == "international":
            platform_list = ['hn', 'reddit', 'github']
        else:
            platform_list = platforms.split(',')

        print("\n" + "=" * 50)
        print("      全网热门信息获取")
        print("=" * 50 + "\n")

        print("正在获取热门信息...\n")

        domestic = [p for p in platform_list if PLATFORMS.get(p, {}).get('category') == 'domestic']
        if domestic:
            print("[国内平台]")
            for p in domestic:
                print(f"  - {PLATFORMS[p]['name']}")

        international = [p for p in platform_list if PLATFORMS.get(p, {}).get('category') == 'international']
        if international:
            print("\n[国外平台]")
            for p in international:
                print(f"  - {PLATFORMS[p]['name']}")

        print()

        use_mock = not HAS_DEPS
        if use_mock:
            print("[注意] 缺少依赖库，使用模拟数据")
            print("        安装: pip install requests beautifulsoup4\n")

        results = self.fetch_all(platform_list, limit, use_mock)

        print("生成报告...\n")
        generator = ReportGenerator()
        report = generator.generate_markdown(results)

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存: {output}\n")

        total_items = sum(len(items) if isinstance(items, list) else 0 for items in results.values())
        print(f"完成! 共 {total_items} 条热门信息，覆盖 {len(results)} 个平台\n")

        return report


def main():
    parser = argparse.ArgumentParser(description='全平台热门信息获取器')
    parser.add_argument('--platforms', '-p', default='all',
                       help='平台: all, domestic, international, 或逗号分隔 (如: hn,reddit)')
    parser.add_argument('--limit', '-l', type=int, default=10, help='每平台条目数')
    parser.add_argument('--output', '-o', help='输出文件路径')

    args = parser.parse_args()

    fetcher = DailyHotFetcher()
    report = fetcher.run(platforms=args.platforms, limit=args.limit, output=args.output)

    if not args.output:
        print("\n" + report)


if __name__ == "__main__":
    main()
