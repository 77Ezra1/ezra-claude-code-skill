#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Hot Fetcher - 优先使用官方API版本
优先使用官方API，降低被封号风险
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# 尝试导入依赖
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


# ==================== 平台 API 配置 ====================

class PlatformAPI:
    """平台 API 基类"""

    def __init__(self, cookies: Dict[str, str] = None):
        self.cookies = cookies or {}
        self.session = requests.Session() if HAS_REQUESTS else None
        if self.session and self.cookies:
            self.session.cookies.update(self.cookies)

    def fetch(self, url: str, headers: Dict = None) -> Optional[str]:
        if not self.session:
            return None
        try:
            default_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            if headers:
                default_headers.update(headers)
            resp = self.session.get(url, headers=default_headers, timeout=15)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            return None

    def fetch_json(self, url: str) -> Optional[dict]:
        if not self.session:
            return None
        try:
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return None


class HackerNewsAPI(PlatformAPI):
    """Hacker News 官方 API (Firebase)"""

    def get_hot(self, limit: int = 10) -> List[Dict]:
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
                        'author': item.get('by', ''),
                        'time': datetime.fromtimestamp(item.get('time', 0)).strftime('%H:%M')
                    })
                time.sleep(0.03)  # API 限流
            return results
        except Exception as e:
            return []


class RedditAPI(PlatformAPI):
    """Reddit 公开 JSON API (无需认证)"""

    def get_hot(self, subreddit: str = "programming", limit: int = 10) -> List[Dict]:
        """获取 Reddit 热门"""
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            resp = self.session.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)

            if resp.status_code != 200:
                # 尝试其他热门 subreddits
                alt_subs = ['technology', 'news', 'worldnews', 'fun']
                for alt in alt_subs:
                    url = f"https://www.reddit.com/r/{alt}/hot.json?limit={limit}"
                    resp = self.session.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                    if resp.status_code == 200:
                        subreddit = alt
                        break

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            for post in data['data']['children'][:limit]:
                results.append({
                    'title': post['data'].get('title', ''),
                    'url': f"https://reddit.com{post['data'].get('permalink', '')}",
                    'score': post['data'].get('score', 0),
                    'comments': post['data'].get('num_comments', 0),
                    'subreddit': subreddit
                })

            return results
        except Exception as e:
            return []


class GitHubAPI(PlatformAPI):
    """GitHub API (部分功能)"""

    def get_trending_repos(self, language: str = "", limit: int = 10) -> List[Dict]:
        """GitHub Trending 需要爬取页面，这里提供替代方案"""
        # 使用 GitHub Search API 获取最近更新的热门仓库
        try:
            # 按最近更新和 stars 排序
            query = f"language:{language}" if language else "stars:>1000"
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"

            resp = self.session.get(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/vnd.github.v3+json'
            }, timeout=15)

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            for item in data.get('items', [])[:limit]:
                results.append({
                    'name': item.get('full_name', ''),
                    'url': item.get('html_url', ''),
                    'description': item.get('description', ''),
                    'stars': item.get('stargazers_count', 0),
                    'language': item.get('language', '')
                })

            return results
        except Exception as e:
            return []


class ZhihuAPI(PlatformAPI):
    """知乎 API (需要 Cookie)"""

    def get_hot(self, limit: int = 10) -> List[Dict]:
        """获取知乎热榜"""
        if not self.cookies:
            return []

        try:
            # 知乎热榜 API
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://www.zhihu.com/hot'
            }

            resp = self.session.get(url, headers=headers, timeout=15)

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            for item in data.get('data', [])[:limit]:
                target = item.get('target', {})
                results.append({
                    'title': target.get('title', ''),
                    'url': f"https://zhihu.com{target.get('url', '')}",
                    'excerpt': target.get('excerpt', '')[:100],
                    'score': item.get('detail_text', '').replace(' 万热', '万热'),
                    'type': target.get('type', '')
                })

            return results
        except Exception as e:
            return []


class DouyinAPI(PlatformAPI):
    """抖音 API (需要 Cookie)"""

    def get_hot(self, limit: int = 10) -> List[Dict]:
        """获取抖音热点"""
        if not self.cookies:
            return []

        try:
            # 抖音热点榜 API
            url = "https://www.douyin.com/aweme/v1/hot/search/list/"
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://www.douyin.com/'
            }

            resp = self.session.get(url, headers=headers, timeout=15)

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            for item in data.get('data', [])[:limit]:
                word_list = item.get('word_list', [])
                for word in word_list[:limit]:
                    results.append({
                        'title': word.get('word', ''),
                        'hot_value': word.get('hot_value', ''),
                        'url': f"https://www.douyin.com/search/{word.get('word', '')}"
                    })

            return results[:limit]
        except Exception as e:
            return []


class WeiboAPI(PlatformAPI):
    """微博 API (需要 Cookie)"""

    def get_hot(self, limit: int = 10) -> List[Dict]:
        """获取微博热搜"""
        if not self.cookies:
            return []

        try:
            # 微博热搜 API
            url = "https://weibo.com/ajax/side/hotSearch"
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://weibo.com',
                'X-Requested-With': 'XMLHttpRequest'
            }

            resp = self.session.get(url, headers=headers, timeout=15)

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            if 'data' in data and 'realtime' in data['data']:
                for item in data['data']['realtime'][:limit]:
                    results.append({
                        'title': item.get('word', '').replace('#', ''),
                        'rank': item.get('rank', 0),
                        'hot': item.get('num', 0),
                        'category': item.get('category', ''),
                        'url': f"https://s.weibo.com/weibo?q={item.get('word', '')}"
                    })

            return results
        except Exception as e:
            return []


class BilibiliAPI(PlatformAPI):
    """B站 API"""

    def get_hot(self, limit: int = 10) -> List[Dict]:
        """获取B站热门"""
        try:
            # B站热门 API (部分公开)
            url = "https://api.bilibili.com/x/web-interface/popular"
            headers = {'User-Agent': 'Mozilla/5.0'}

            resp = self.session.get(url, headers=headers, timeout=15)

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            for item in data.get('data', {}).get('list', [])[:limit]:
                results.append({
                    'title': item.get('title', ''),
                    'url': f"https://www.bilibili.com/video/{item.get('bvid', '')}",
                    'view': item.get('stat', {}).get('view', 0),
                    'danmaku': item.get('stat', {}).get('danmaku', 0),
                    'author': item.get('owner', {}).get('name', '')
                })

            return results
        except Exception as e:
            return []


class StackOverflowAPI(PlatformAPI):
    """Stack Overflow API"""

    def get_hot_questions(self, limit: int = 10) -> List[Dict]:
        """获取 Stack Overflow 热门问题"""
        try:
            # 使用 Stack Exchange API
            url = "https://api.stackexchange.com/2.3/questions"
            params = {
                'order': 'desc',
                'sort': 'hot',
                'site': 'stackoverflow',
                'pagesize': limit,
                'filter': 'withbody'
            }

            resp = self.session.get(url, params=params, timeout=15)

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            for item in data.get('items', [])[:limit]:
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'score': item.get('score', 0),
                    'answers': item.get('answer_count', 0),
                    'tags': ', '.join(item.get('tags', [])[:3])
                })

            return results
        except Exception as e:
            return []


# ==================== Cookie 管理器 ====================

class CookieManager:
    """Cookie 管理器"""

    def __init__(self, cookie_file: str = None):
        self.cookie_file = cookie_file or os.path.expanduser('~/.claude/skills/daily-hot-fetcher/cookies.json')
        self.cookies = self.load_cookies()

    def load_cookies(self) -> Dict[str, Dict[str, str]]:
        """从文件加载 Cookie"""
        try:
            if os.path.exists(self.cookie_file):
                with open(self.cookie_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def save_cookies(self, cookies: Dict[str, Dict[str, str]]):
        """保存 Cookie 到文件"""
        try:
            os.makedirs(os.path.dirname(self.cookie_file), exist_ok=True)
            with open(self.cookie_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存 Cookie 失败: {e}")

    def get_cookies(self, platform: str) -> Dict[str, str]:
        """获取指定平台的 Cookie"""
        return self.cookies.get(platform, {})

    def set_cookies(self, platform: str, cookies: Dict[str, str]):
        """设置指定平台的 Cookie"""
        self.cookies[platform] = cookies
        self.save_cookies(self.cookies)

    @staticmethod
    def parse_cookie_string(cookie_string: str) -> Dict[str, str]:
        """解析 Cookie 字符串"""
        cookies = {}
        for item in cookie_string.split(';'):
            item = item.strip()
            if '=' in item:
                key, value = item.split('=', 1)
                cookies[key.strip()] = value.strip()
        return cookies


# ==================== 报告生成器 ====================

class ReportGenerator:
    """报告生成器"""

    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def generate_markdown(self, results: Dict[str, List[Dict]]) -> str:
        lines = []
        lines.append(f"# 今日全网热点汇总\n\n")
        lines.append(f"**时间**: {self.timestamp}\n")
        lines.append(f"**平台**: {len(results)} 个\n\n")
        lines.append("---\n\n")

        # 国内平台
        domestic = ['weibo', 'zhihu', 'bilibili', 'douyin']
        domestic_results = {k: v for k, v in results.items() if k in domestic and v}

        if domestic_results:
            lines.append("## 国内热门\n\n")
            for platform, items in domestic_results.items():
                lines.append(self._format_platform(platform, items))

        # 国外平台
        international = ['hn', 'reddit', 'github', 'stackoverflow']
        international_results = {k: v for k, v in results.items() if k in international and v}

        if international_results:
            lines.append("---\n\n")
            lines.append("## 国外热门\n\n")
            for platform, items in international_results.items():
                lines.append(self._format_platform(platform, items))

        # 数据源说明
        lines.append("---\n\n")
        lines.append("## 数据源说明\n\n")
        lines.append("| 平台 | 数据源 | 状态 |\n")
        lines.append("|------|--------|------|\n")

        for platform in results.keys():
            if platform == 'hn':
                lines.append("| Hacker News | 官方 Firebase API | 实时 |\n")
            elif platform == 'reddit':
                lines.append("| Reddit | 公开 JSON API | 实时 |\n")
            elif platform == 'github':
                lines.append("| GitHub | Search API | 实时 |\n")
            elif platform == 'zhihu':
                lines.append(f"| 知乎 | {'Cookie API' if results.get(platform) else '无 Cookie'} | {'实时' if results.get(platform) else '待配置'} |\n")
            elif platform == 'weibo':
                lines.append(f"| 微博 | {'Cookie API' if results.get(platform) else '无 Cookie'} | {'实时' if results.get(platform) else '待配置'} |\n")
            elif platform == 'douyin':
                lines.append(f"| 抖音 | {'Cookie API' if results.get(platform) else '无 Cookie'} | {'实时' if results.get(platform) else '待配置'} |\n")
            elif platform == 'bilibili':
                lines.append("| B站 | 公开 API | 实时 |\n")

        return ''.join(lines)

    def _format_platform(self, platform: str, items: List[Dict]) -> str:
        platform_names = {
            'hn': 'Hacker News',
            'reddit': 'Reddit',
            'github': 'GitHub Trending',
            'stackoverflow': 'Stack Overflow',
            'weibo': '微博热搜',
            'zhihu': '知乎热榜',
            'bilibili': 'B站热门',
            'douyin': '抖音热点'
        }

        lines = []
        lines.append(f"### {platform_names.get(platform, platform)}\n\n")

        if not items:
            lines.append("暂无数据 (需要配置 Cookie 或 API 不可用)\n\n")
            return ''.join(lines)

        if platform == 'hn':
            lines.append("| 排名 | 得分 | 标题 | 评论 |\n")
            lines.append("|------|------|------|------|\n")
            for i, item in enumerate(items[:10]):
                title = item.get('title', '')[:50]
                url = item.get('url', '')
                score = item.get('score', 0)
                comments = item.get('comments', 0)
                lines.append(f"| {i+1} | {score} | [{title}]({url}) | {comments} |\n")

        elif platform == 'reddit':
            lines.append("| 排名 | 得分 | 标题 | 评论 |\n")
            lines.append("|------|------|------|------|\n")
            for i, item in enumerate(items[:10]):
                title = item.get('title', '')[:45]
                url = item.get('url', '')
                score = item.get('score', 0)
                comments = item.get('comments', 0)
                lines.append(f"| {i+1} | {score} | [{title}]({url}) | {comments} |\n")

        elif platform == 'github':
            lines.append("| 排名 | 仓库 | 描述 | Stars |\n")
            lines.append("|------|------|------|-------|\n")
            for i, item in enumerate(items[:10]):
                name = item.get('name', '')
                desc = item.get('description', '')[:35]
                stars = item.get('stars', 0)
                url = item.get('url', '')
                lines.append(f"| {i+1} | [{name}]({url}) | {desc} | {stars} |\n")

        elif platform == 'weibo':
            lines.append("| 排名 | 热度 | 话题 |\n")
            lines.append("|------|------|------|\n")
            for item in items[:10]:
                rank = item.get('rank', '')
                hot = item.get('hot', '')
                title = item.get('title', '')[:40]
                lines.append(f"| {rank} | {hot} | {title} |\n")

        elif platform == 'zhihu':
            lines.append("| 排名 | 标题 | 热度 |\n")
            lines.append("|------|------|------|\n")
            for i, item in enumerate(items[:10]):
                title = item.get('title', '')[:50]
                score = item.get('score', '')
                url = item.get('url', '')
                if url:
                    lines.append(f"| {i+1} | [{title}]({url}) | {score} |\n")
                else:
                    lines.append(f"| {i+1} | {title} | {score} |\n")

        else:
            lines.append("| 排名 | 标题 |\n")
            lines.append("|------|------|\n")
            for i, item in enumerate(items[:10]):
                title = item.get('title', '')[:70]
                url = item.get('url', '')
                if url:
                    lines.append(f"| {i+1} | [{title}]({url}) |\n")
                else:
                    lines.append(f"| {i+1} | {title} |\n")

        lines.append("\n")
        return ''.join(lines)


# ==================== 主程序 ====================

class DailyHotFetcherAPI:
    """使用官方 API 的热门信息获取器"""

    def __init__(self, cookie_file: str = None):
        self.cookie_manager = CookieManager(cookie_file)
        self.apis = {}
        self._init_apis()

    def _init_apis(self):
        """初始化各平台 API"""
        # 无需 Cookie 的平台
        self.apis['hn'] = HackerNewsAPI()
        self.apis['reddit'] = RedditAPI()
        self.apis['github'] = GitHubAPI()
        self.apis['bilibili'] = BilibiliAPI()
        self.apis['stackoverflow'] = StackOverflowAPI()

        # 需要 Cookie 的平台
        zhihu_cookies = self.cookie_manager.get_cookies('zhihu')
        if zhihu_cookies:
            self.apis['zhihu'] = ZhihuAPI(zhihu_cookies)

        douyin_cookies = self.cookie_manager.get_cookies('douyin')
        if douyin_cookies:
            self.apis['douyin'] = DouyinAPI(douyin_cookies)

        weibo_cookies = self.cookie_manager.get_cookies('weibo')
        if weibo_cookies:
            self.apis['weibo'] = WeiboAPI(weibo_cookies)

    def add_cookie(self, platform: str, cookie_string: str):
        """添加平台 Cookie"""
        cookies = CookieManager.parse_cookie_string(cookie_string)
        self.cookie_manager.set_cookies(platform, cookies)

        # 重新初始化该平台 API
        if platform == 'zhihu':
            self.apis['zhihu'] = ZhihuAPI(cookies)
        elif platform == 'douyin':
            self.apis['douyin'] = DouyinAPI(cookies)
        elif platform == 'weibo':
            self.apis['weibo'] = WeiboAPI(cookies)

    def fetch_all(self, platforms: List[str] = None, limit: int = 10) -> Dict[str, List[Dict]]:
        """获取所有平台热门信息"""
        if platforms is None:
            platforms = ['hn', 'reddit', 'github', 'bilibili', 'stackoverflow']
            # 添加已配置 Cookie 的平台
            if 'zhihu' in self.apis:
                platforms.append('zhihu')
            if 'douyin' in self.apis:
                platforms.append('douyin')
            if 'weibo' in self.apis:
                platforms.append('weibo')

        results = {}

        for platform in platforms:
            api = self.apis.get(platform)
            if not api:
                continue

            try:
                if platform == 'hn':
                    results[platform] = api.get_hot(limit)
                elif platform == 'reddit':
                    results[platform] = api.get_hot('programming', limit)
                elif platform == 'github':
                    results[platform] = api.get_trending_repos('', limit)
                elif platform == 'zhihu':
                    results[platform] = api.get_hot(limit)
                elif platform == 'douyin':
                    results[platform] = api.get_hot(limit)
                elif platform == 'weibo':
                    results[platform] = api.get_hot(limit)
                elif platform == 'bilibili':
                    results[platform] = api.get_hot(limit)
                elif platform == 'stackoverflow':
                    results[platform] = api.get_hot_questions(limit)

                time.sleep(0.5)  # API 限流
            except Exception as e:
                results[platform] = []

        return results

    def run(self, platforms: str = "all", limit: int = 10, output: str = None) -> str:
        """执行热门信息获取"""
        if not HAS_REQUESTS:
            print("错误: 需要安装 requests 库")
            print("请运行: pip install requests")
            return ""

        # 解析平台参数
        if platforms == "all":
            platform_list = None  # 自动选择
        elif platforms == "domestic":
            platform_list = ['weibo', 'zhihu', 'bilibili', 'douyin']
        elif platforms == "international":
            platform_list = ['hn', 'reddit', 'github', 'stackoverflow']
        else:
            platform_list = platforms.split(',')

        print("\n" + "=" * 50)
        print("      全网热门信息获取 (官方API优先)")
        print("=" * 50 + "\n")

        # 显示已配置的平台
        print("[已配置平台]")
        for platform in ['hn', 'reddit', 'github', 'bilibili', 'zhihu', 'douyin', 'weibo']:
            status = "✓" if platform in self.apis else "✗"
            if platform == 'hn':
                name = "Hacker News (官方API)"
            elif platform == 'reddit':
                name = "Reddit (官方API)"
            elif platform == 'github':
                name = "GitHub (Search API)"
            elif platform == 'bilibili':
                name = "B站 (公开API)"
            elif platform == 'zhihu':
                name = "知乎 (需Cookie)" if platform in self.apis else "知乎 (未配置Cookie)"
            elif platform == 'douyin':
                name = "抖音 (需Cookie)" if platform in self.apis else "抖音 (未配置Cookie)"
            elif platform == 'weibo':
                name = "微博 (需Cookie)" if platform in self.apis else "微博 (未配置Cookie)"
            print(f"  {status} {name}")

        print()

        # 获取数据
        results = self.fetch_all(platform_list, limit)

        # 生成报告
        generator = ReportGenerator()
        report = generator.generate_markdown(results)

        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存: {output}\n")

        total_items = sum(len(items) for items in results.values())
        print(f"完成! 共 {total_items} 条热门信息")

        return report


def main():
    parser = argparse.ArgumentParser(description='全网热门信息获取器 (官方API优先)')
    parser.add_argument('--platforms', '-p', default='all', help='平台: all, domestic, international')
    parser.add_argument('--limit', '-l', type=int, default=10, help='每平台条目数')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--add-zhihu-cookie', help='添加知乎 Cookie')
    parser.add_argument('--add-douyin-cookie', help='添加抖音 Cookie')
    parser.add_argument('--add-weibo-cookie', help='添加微博 Cookie')

    args = parser.parse_args()

    fetcher = DailyHotFetcherAPI()

    # 添加 Cookie
    if args.add_zhihu_cookie:
        fetcher.add_cookie('zhihu', args.add_zhihu_cookie)
        print("知乎 Cookie 已添加")

    if args.add_douyin_cookie:
        fetcher.add_cookie('douyin', args.add_douyin_cookie)
        print("抖音 Cookie 已添加")

    if args.add_weibo_cookie:
        fetcher.add_cookie('weibo', args.add_weibo_cookie)
        print("微博 Cookie 已添加")

    # 获取热门
    report = fetcher.run(
        platforms=args.platforms,
        limit=args.limit,
        output=args.output
    )

    if not args.output:
        print("\n" + report)


if __name__ == "__main__":
    main()
