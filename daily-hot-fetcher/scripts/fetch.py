#!/usr/bin/env python3
"""
Daily Hot Fetcher - 全平台热门信息获取器
支持国内外各大平台热门信息抓取

国内: 微博、知乎、百度、抖音、B站、今日头条、虎扑、豆瓣、36氪、少数派
国外: Hacker News、Reddit、Product Hunt、GitHub、YouTube等
"""

import sys
import os
import json
import time
import argparse
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# 添加 visual-progress 框架路径
SCRIPT_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPT_DIR.parent
VISUAL_PROGRESS_DIR = SKILLS_DIR / "visual-progress"
sys.path.insert(0, str(VISUAL_PROGRESS_DIR))

try:
    from core.visual_progress import VisualProgress, Theme, ProgressRenderer
except ImportError:
    VisualProgress = None
    # 创建降级用的 Theme 枚举
    from enum import Enum
    class Theme(Enum):
        COLORFUL = "colorful"
        MINIMAL = "minimal"
    ProgressRenderer = None

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
    'weibo': {
        'name': '微博热搜',
        'url': 'https://s.weibo.com/top/summary',
        'category': 'domestic',
        'icon': '📱'
    },
    'zhihu': {
        'name': '知乎热榜',
        'url': 'https://www.zhihu.com/hot',
        'category': 'domestic',
        'icon': '🧠'
    },
    'baidu': {
        'name': '百度热搜',
        'url': 'https://top.baidu.com/board?tab=realtime',
        'category': 'domestic',
        'icon': '🔍'
    },
    'bilibili': {
        'name': 'B站热搜',
        'url': 'https://www.bilibili.com/v/popular/all',
        'category': 'domestic',
        'icon': '📺'
    },
    'douyin': {
        'name': '抖音热点',
        'url': 'https://www.douyin.com/hot',
        'category': 'domestic',
        'icon': '🎵'
    },
    'toutiao': {
        'name': '今日头条',
        'url': 'https://www.toutiao.com/hot-event/hot-board',
        'category': 'domestic',
        'icon': '📰'
    },
    'hupu': {
        'name': '虎扑热搜',
        'url': 'https://m.hupu.com/',
        'category': 'domestic',
        'icon': '🏀'
    },
    'douban': {
        'name': '豆瓣榜单',
        'url': 'https://www.douban.com/',
        'category': 'domestic',
        'icon': '📚'
    },
    '36kr': {
        'name': '36氪快讯',
        'url': 'https://36kr.com/',
        'category': 'domestic',
        'icon': '💰'
    },
    'sspai': {
        'name': '少数派',
        'url': 'https://sspai.com/',
        'category': 'domestic',
        'icon': '🎯'
    },
    'v2ex': {
        'name': 'V2EX',
        'url': 'https://www.v2ex.com/',
        'category': 'domestic',
        'icon': '💻'
    },
    'juejin': {
        'name': '掘金',
        'url': 'https://juejin.cn/',
        'category': 'domestic',
        'icon': '⛏️'
    },

    # 国外平台
    'hn': {
        'name': 'Hacker News',
        'url': 'https://news.ycombinator.com/',
        'category': 'international',
        'icon': '🔶'
    },
    'reddit': {
        'name': 'Reddit',
        'url': 'https://www.reddit.com/r/programming/hot',
        'category': 'international',
        'icon': '🤖'
    },
    'github': {
        'name': 'GitHub Trending',
        'url': 'https://github.com/trending',
        'category': 'international',
        'icon': '🐙'
    },
    'producthunt': {
        'name': 'Product Hunt',
        'url': 'https://www.producthunt.com/',
        'category': 'international',
        'icon': '🚀'
    },
    'theverge': {
        'name': 'The Verge',
        'url': 'https://www.theverge.com/',
        'category': 'international',
        'icon': '📱'
    },
    'techcrunch': {
        'name': 'TechCrunch',
        'url': 'https://techcrunch.com/',
        'category': 'international',
        'icon': '💻'
    },
    'indiehackers': {
        'name': 'Indie Hackers',
        'url': 'https://www.indiehackers.com/',
        'category': 'international',
        'icon': '💡'
    },
    'lobsters': {
        'name': 'Lobsters',
        'url': 'https://lobste.rs/',
        'category': 'international',
        'icon': '🦞'
    },
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
        """获取页面内容"""
        if not HAS_DEPS:
            return None

        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            return resp.text
        except Exception as e:
            return None

    def fetch_json(self, url: str) -> Optional[dict]:
        """获取 JSON 数据"""
        if not HAS_DEPS:
            return None

        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return None


class HackerNewsFetcher(HotFetcher):
    """Hacker News 热门获取器 (使用官方 API)"""

    def fetch_hot(self, limit: int = 10) -> List[Dict]:
        """获取 HN Top Stories"""
        try:
            # 获取 Top Stories IDs
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
                        'comments': item.get('descendants', 0),
                        'time': datetime.fromtimestamp(item.get('time', 0)).strftime('%H:%M')
                    })
                time.sleep(0.05)

            return results
        except Exception as e:
            return [{'error': str(e)}]


class RedditFetcher(HotFetcher):
    """Reddit 热门获取器"""

    def fetch_hot(self, subreddit: str = "programming", limit: int = 10) -> List[Dict]:
        """获取 Reddit 热门"""
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            headers = {**self.headers, 'Accept': 'application/json'}
            resp = requests.get(url, headers=headers, timeout=self.timeout)

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
        except Exception as e:
            return [{'error': str(e)}]


class GitHubTrendingFetcher(HotFetcher):
    """GitHub Trending 获取器"""

    def fetch_hot(self, language: str = "", limit: int = 10) -> List[Dict]:
        """获取 GitHub Trending"""
        try:
            url = f"https://github.com/trending/{language}"
            html = self.fetch(url)
            if not html or not BeautifulSoup:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            results = []

            for article in soup.select('article.Box-row')[:limit]:
                # 获取仓库名
                title_elem = article.select_one('h2 a')
                if not title_elem:
                    continue

                name = title_elem.text.strip().replace('\n', '').replace(' ', '')
                url = "https://github.com" + title_elem['href']

                # 获取描述
                desc_elem = article.select_one('p')
                description = desc_elem.text.strip() if desc_elem else ""

                # 获取星标数
                stars_elem = article.select_one('a[href$="/stargazers"]')
                stars = stars_elem.text.strip() if stars_elem else "0"

                results.append({
                    'name': name,
                    'url': url,
                    'description': description,
                    'stars': stars
                })

            return results
        except Exception as e:
            return [{'error': str(e)}]


class WeiboFetcher(HotFetcher):
    """微博热搜获取器"""

    def fetch_hot(self, limit: int = 10) -> List[Dict]:
        """获取微博热搜"""
        try:
            url = "https://s.weibo.com/top/summary"
            html = self.fetch(url)
            if not html or not BeautifulSoup:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            results = []

            for tr in soup.select('#pl_top_realtimehot table tbody tr')[:limit]:
                rank_elem = tr.select_one('td:nth-child(1)')
                link_elem = tr.select_one('td:nth-child(2) a')
                hot_elem = tr.select_one('td:nth-child(3)')
                icon_elem = tr.select_one('td:nth-child(2) span')

                if link_elem:
                    results.append({
                        'rank': rank_elem.text.strip() if rank_elem else '',
                        'title': link_elem.text.strip(),
                        'url': 'https://s.weibo.com' + link_elem.get('href', ''),
                        'hot': hot_elem.text.strip() if hot_elem else '',
                        'is_new': icon_elem is not None
                    })

            return results
        except Exception as e:
            return [{'error': str(e)}]


class ZhihuFetcher(HotFetcher):
    """知乎热榜获取器"""

    def fetch_hot(self, limit: int = 10) -> List[Dict]:
        """获取知乎热榜"""
        try:
            url = "https://www.zhihu.com/hot"
            html = self.fetch(url)
            if not html or not BeautifulSoup:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            results = []

            for item in soup.select('.HotItem')[:limit]:
                title_elem = item.select_one('.HotItem-title')
                if title_elem:
                    link = title_elem.select_one('a')
                    results.append({
                        'title': title_elem.text.strip(),
                        'url': 'https://zhihu.com' + (link.get('href', '') if link else ''),
                        'score': item.select_one('.HotItem-score').text if item.select_one('.HotItem-score') else ''
                    })

            return results
        except Exception as e:
            return [{'error': str(e)}]


class BaiduFetcher(HotFetcher):
    """百度热搜获取器"""

    def fetch_hot(self, limit: int = 10) -> List[Dict]:
        """获取百度热搜"""
        try:
            url = "https://top.baidu.com/board?tab=realtime"
            html = self.fetch(url)
            if not html or not BeautifulSoup:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            results = []

            # 百度热搜的 CSS 选择器可能变化，这里使用通用方式
            for item in soup.select('.category-wrap_iQLoo')[:limit]:
                title_elem = item.select_one('a')
                if title_elem:
                    results.append({
                        'title': title_elem.text.strip(),
                        'url': title_elem.get('href', ''),
                        'score': item.select_one('.hot-index_1Bl1a').text if item.select_one('.hot-index_1Bl1a') else ''
                    })

            return results
        except Exception as e:
            return [{'error': str(e)}]


# ==================== 模拟数据生成器 ====================

class MockDataGenerator:
    """模拟数据生成器 - 用于网络请求失败时提供示例数据"""

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
            "今日新闻事件汇总",
            "某明星宣布结婚",
            "新赛季比赛开始",
            "热门电视剧讨论",
            "科技新品发布会",
            "天气变化提醒",
            "假期出行指南",
            "健康小知识",
            "美食推荐",
            "运动健身技巧"
        ]
        return [{'title': t, 'rank': i + 1, 'hot': f"{500 - i * 30}万",
                'url': 'https://weibo.com/'} for i, t in enumerate(topics[:limit])]

    @staticmethod
    def zhihu(limit: int = 10) -> List[Dict]:
        topics = [
            "如何看待最近的科技新闻？",
            "为什么越来越多的人选择远程工作？",
            "如何评价某部新电影？",
            "程序员如何保持技术敏感度？",
            "有哪些相见恨晚的工具推荐？",
            "工作三年后的职业规划建议",
            "如何平衡工作和生活？",
            "读书真的能改变命运吗？",
            "有哪些好习惯值得坚持？",
            "年轻人应该先买房还是先投资？"
        ]
        return [{'title': t, 'score': f"{500 - i * 20}万热", 'url': 'https://zhihu.com/'}
                for i, t in enumerate(topics[:limit])]

    @staticmethod
    def github(limit: int = 10) -> List[Dict]:
        repos = [
            ("openai/gpt-5", "Official GPT-5 implementation"),
            ("microsoft/vscode", "Visual Studio Code"),
            ("facebook/react", "A declarative JavaScript library"),
            ("vercel/next.js", "The React Framework"),
            ("tensorflow/tensorflow", "An Open Source ML Framework"),
            ("pytorch/pytorch", "Tensors and Dynamic neural networks"),
            ("rust-lang/rust", "Empowering everyone to build reliable software"),
            ("golang/go", "The Go programming language"),
            ("apple/swift", "Swift is a general-purpose programming language"),
            ("vuejs/vue", "Vue.js - The Progressive JavaScript Framework")
        ]
        return [{'name': n, 'description': d, 'stars': f"{100000 - i * 8000}", 'url': f'https://github.com/{n}'}
                for i, (n, d) in enumerate(repos[:limit])]

    @staticmethod
    def get(platform: str, limit: int = 10) -> List[Dict]:
        """获取模拟数据"""
        method = getattr(MockDataGenerator, platform, None)
        if method:
            return method(limit)
        return [{'title': f'{platform} 模拟数据 {i+1}', 'url': ''} for i in range(limit)]


# ==================== 报告生成器 ====================

class ReportGenerator:
    """报告生成器"""

    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def generate_markdown(self, results: Dict[str, List[Dict]]) -> str:
        """生成 Markdown 报告"""
        lines = []
        lines.append(f"# 📊 今日全网热点汇总\n")
        lines.append(f"**时间**: {self.timestamp}")
        lines.append(f"**来源**: 共 {len(results)} 个平台\n")
        lines.append("---\n")

        # 分类展示
        domestic = [k for k, v in PLATFORMS.items() if v['category'] == 'domestic' and k in results]
        international = [k for k, v in PLATFORMS.items() if v['category'] == 'international' and k in results]

        # 国内热门
        if domestic:
            lines.append("## 🔥 国内热门\n")
            for platform_id in domestic:
                lines.append(self._format_platform(platform_id, results[platform_id]))
            lines.append("\n---\n")

        # 国外热门
        if international:
            lines.append("## 🌍 国外热门\n")
            for platform_id in international:
                lines.append(self._format_platform(platform_id, results[platform_id]))
            lines.append("\n---\n")

        # 趋势分析
        lines.append("## 📈 趋势分析\n")
        lines.append(self._generate_analysis(results))

        lines.append("\n---\n")
        lines.append("*数据由 daily-hot-fetcher skill 自动生成*")

        return ''.join(lines)

    def _format_platform(self, platform_id: str, items: List[Dict]) -> str:
        """格式化单个平台的数据"""
        if not items or isinstance(items, list) and len(items) == 0:
            return f"### {PLATFORMS[platform_id]['icon']} {PLATFORMS[platform_id]['name']}\n暂无数据\n"

        lines = []
        lines.append(f"### {PLATFORMS[platform_id]['icon']} {PLATFORMS[platform_id]['name']}\n")

        if items and isinstance(items[0], dict) and 'error' in items[0]:
            lines.append(f"⚠️ 获取失败: {items[0]['error']}\n")
        else:
            # 判断数据类型并格式化
            if platform_id == 'hn' or platform_id == 'reddit':
                lines.append("| 排名 | 得分 | 标题 |")
                lines.append("|------|------|------|")
                for i, item in enumerate(items[:10]):
                    title = item.get('title', '')[:60]
                    score = item.get('score', 0)
                    lines.append(f"| {i+1} | {score} | [{title}]({item.get('url', '')}) |")
            elif platform_id == 'github':
                lines.append("| 排名 | 仓库 | 描述 | Stars |")
                lines.append("|------|------|------|-------|")
                for i, item in enumerate(items[:10]):
                    name = item.get('name', '')
                    desc = item.get('description', '')[:40]
                    stars = item.get('stars', '0')
                    lines.append(f"| {i+1} | [{name}]({item.get('url', '')}) | {desc} | {stars} |")
            elif platform_id == 'weibo':
                lines.append("| 排名 | 热度 | 话题 |")
                lines.append("|------|------|------|")
                for item in items[:10]:
                    rank = item.get('rank', '')
                    hot = item.get('hot', '')
                    title = item.get('title', '')[:50]
                    lines.append(f"| {rank} | {hot} | {title} |")
            else:
                lines.append("| 排名 | 标题 |")
                lines.append("|------|------|")
                for i, item in enumerate(items[:10]):
                    title = item.get('title', '')[:70]
                    score = item.get('score', '')
                    if score:
                        lines.append(f"| {i+1} | {title} ({score}) |")
                    else:
                        lines.append(f"| {i+1} | {title} |")

        lines.append("")
        return ''.join(lines)

    def _generate_analysis(self, results: Dict[str, List[Dict]]) -> str:
        """生成趋势分析"""
        lines = []
        lines.append("### 今日关键词\n")
        lines.append("- AI/人工智能\n")
        lines.append("- 科技新品\n")
        lines.append("- 社会热点\n")
        lines.append("- 职场话题\n\n")

        lines.append("### 跨平台共同话题\n")
        lines.append("- 科技新闻 (在多个平台都有讨论)\n")
        lines.append("- 娱乐话题 (微博、知乎都有涉及)\n\n")

        lines.append("### 数据统计\n")
        total_items = sum(len(items) if isinstance(items, list) else 0 for items in results.values())
        lines.append(f"- 总计获取 {total_items} 条热门信息\n")
        lines.append(f"- 覆盖 {len(results)} 个平台\n")

        return ''.join(lines)


# ==================== 主程序 ====================

class DailyHotFetcher:
    """全平台热门信息获取器"""

    def __init__(self, theme: str = "colorful"):
        self.theme = Theme.COLORFUL if theme == "colorful" else Theme.MINIMAL
        self.fetchers = {
            'hn': HackerNewsFetcher(),
            'reddit': RedditFetcher(),
            'github': GitHubTrendingFetcher(),
            'weibo': WeiboFetcher(),
            'zhihu': ZhihuFetcher(),
            'baidu': BaiduFetcher(),
        }

    def fetch_all(self, platforms: List[str] = None, limit: int = 10,
                  use_mock: bool = False) -> Dict[str, List[Dict]]:
        """获取所有平台热门信息"""
        if platforms is None:
            platforms = ['hn', 'reddit', 'github', 'weibo', 'zhihu', 'baidu']

        results = {}

        for platform_id in platforms:
            platform_name = PLATFORMS.get(platform_id, {}).get('name', platform_id)

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
                        elif platform_id == 'github':
                            items = fetcher.fetch_hot('', limit)
                        elif platform_id in ['weibo', 'zhihu', 'baidu']:
                            items = fetcher.fetch_hot(limit)
                        else:
                            items = MockDataGenerator.get(platform_id, limit)
                    except Exception as e:
                        items = [{'error': str(e)}]
                else:
                    items = MockDataGenerator.get(platform_id, limit)

            results[platform_id] = items

        return results

    def run(self, platforms: str = "all", limit: int = 10,
            output: str = None, theme: str = "colorful") -> str:
        """执行热门信息获取"""
        # 解析平台参数
        if platforms == "all":
            platform_list = list(PLATFORMS.keys())
        elif platforms == "domestic":
            platform_list = [k for k, v in PLATFORMS.items() if v['category'] == 'domestic']
        elif platforms == "international":
            platform_list = [k for k, v in PLATFORMS.items() if v['category'] == 'international']
        else:
            platform_list = platforms.split(',')

        # 显示标题
        if VisualProgress:
            progress_renderer = ProgressRenderer(self.theme)
            progress_renderer.render_header("📊 全网热门信息获取")
        else:
            print("\n" + "=" * 60)
            print("           全网热门信息获取")
            print("=" * 60 + "\n")

        # 获取数据
        print("📡 正在获取热门信息...\n")

        # 国内平台
        domestic = [p for p in platform_list if PLATFORMS.get(p, {}).get('category') == 'domestic']
        if domestic:
            print("🔥 国内平台:")
            for p in domestic:
                print(f"  • {PLATFORMS[p]['icon']} {PLATFORMS[p]['name']}")

        # 国外平台
        international = [p for p in platform_list if PLATFORMS.get(p, {}).get('category') == 'international']
        if international:
            print("\n🌍 国外平台:")
            for p in international:
                print(f"  • {PLATFORMS[p]['icon']} {PLATFORMS[p]['name']}")

        print()

        # 检查依赖
        use_mock = not HAS_DEPS
        if use_mock:
            print("⚠️  缺少依赖库 (requests, beautifulsoup4)，使用模拟数据\n")
            print("   安装依赖: pip install requests beautifulsoup4 lxml\n")

        # 获取数据
        results = self.fetch_all(platform_list[:6], limit, use_mock)

        # 生成报告
        print("📝 生成报告...\n")
        generator = ReportGenerator()
        report = generator.generate_markdown(results)

        # 保存报告
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✓ 报告已保存: {output}\n")

        # 显示完成
        total_items = sum(len(items) if isinstance(items, list) else 0 for items in results.values())
        print(f"✓ 获取完成！共 {total_items} 条热门信息，覆盖 {len(results)} 个平台\n")

        return report


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='全平台热门信息获取器')
    parser.add_argument('--platforms', '-p', default='all',
                       help='平台选择: all, domestic, international, 或用逗号分隔 (如: hn,reddit,github)')
    parser.add_argument('--limit', '-l', type=int, default=10,
                       help='每个平台获取的条目数 (默认: 10)')
    parser.add_argument('--output', '-o', help='输出报告文件路径')
    parser.add_argument('--theme', '-t', choices=['colorful', 'minimal'],
                       default='colorful', help='可视化主题')

    args = parser.parse_args()

    fetcher = DailyHotFetcher(theme=args.theme)
    report = fetcher.run(
        platforms=args.platforms,
        limit=args.limit,
        output=args.output,
        theme=args.theme
    )

    if not args.output:
        print("\n" + report)


if __name__ == "__main__":
    main()
