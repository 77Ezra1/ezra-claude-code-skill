#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real-time Search Module
实时搜索模块 - 获取国内外最新资讯
支持多种搜索源，无需 API Key
"""

import sys
import os
import time
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

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


# ==================== 搜索源配置 ====================

class SearchSource:
    """搜索源基类"""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session() if HAS_REQUESTS else None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """执行搜索"""
        raise NotImplementedError


class HackerNewsSearch(SearchSource):
    """Hacker News Algolia 搜索 (官方搜索 API)"""

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索 Hacker News"""
        if not HAS_REQUESTS:
            return []

        try:
            # HN Algolia 搜索 API (官方，无需认证)
            url = "http://hn.algolia.com/api/v1/search"
            params = {
                'query': query,
                'tags': 'story',
                'restrictSearchableAttributes': 'title',
                'hitsPerPage': limit
            }

            # 如果没有查询词，获取最新的热门
            if not query:
                params['numericFilters'] = 'created_at_i>' + str(int(time.time()) - 7 * 24 * 3600)

            resp = self.session.get(url, params=params, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            for item in data.get('hits', [])[:limit]:
                created_at = item.get('created_at_i', 0)
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', '') or f"https://news.ycombinator.com/item?id={item.get('objectID')}",
                    'points': item.get('points', 0),
                    'author': item.get('author', ''),
                    'created_at': datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M'),
                    'num_comments': item.get('num_comments', 0),
                    'source': 'Hacker News'
                })

            return results
        except Exception as e:
            return []


class RedditSearch(SearchSource):
    """Reddit 搜索"""

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索 Reddit"""
        if not HAS_REQUESTS:
            return []

        try:
            # Reddit JSON 搜索 API
            url = f"https://www.reddit.com/search.json"
            params = {
                'q': query,
                'sort': 'relevance',
                't': 'week',  # 最近一周
                'limit': limit
            }

            resp = self.session.get(url, params=params, headers=self.headers, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            for post in data.get('data', {}).get('children', [])[:limit]:
                post_data = post.get('data', {})
                results.append({
                    'title': post_data.get('title', ''),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'subreddit': post_data.get('subreddit', ''),
                    'score': post_data.get('score', 0),
                    'num_comments': post_data.get('num_comments', 0),
                    'created_at': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d %H:%M'),
                    'source': f"r/{post_data.get('subreddit', '')}"
                })

            return results
        except Exception as e:
            return []


class DuckDuckGoSearch(SearchSource):
    """DuckDuckGo 搜索 (无需 API Key)"""

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """使用 DuckDuckGo 搜索"""
        if not HAS_REQUESTS or not HAS_BS4:
            return []

        try:
            # DuckDuckGo HTML 版本
            url = "https://html.duckduckgo.com/html/"
            params = {'q': query}

            resp = self.session.post(url, data=params, headers=self.headers, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []

            # 解析搜索结果
            for result in soup.select('.result')[:limit]:
                title_elem = result.select_one('.result__title')
                link_elem = result.select_one('.result__a')
                snippet_elem = result.select_one('.result__snippet')

                if title_elem and link_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'url': link_elem.get('href', ''),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else '',
                        'source': 'DuckDuckGo'
                    })

            return results
        except Exception as e:
            return []


class BaiduSearch(SearchSource):
    """百度搜索 (中文内容)"""

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """使用百度搜索"""
        if not HAS_REQUESTS or not HAS_BS4:
            return []

        try:
            url = "https://www.baidu.com/s"
            params = {
                'wd': query,
                'rn': limit
            }

            resp = self.session.get(url, params=params, headers=self.headers, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []

            # 解析搜索结果
            for result in soup.select('.result')[:limit]:
                title_elem = result.select_one('h3 a')
                snippet_elem = result.select_one('.c-abstract')

                if title_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else '',
                        'source': '百度'
                    })

            return results
        except Exception as e:
            return []


class GoogleNewsSearch(SearchSource):
    """Google News 搜索 (无需 API Key)"""

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """使用 Google News 搜索"""
        if not HAS_REQUESTS or not HAS_BS4:
            return []

        try:
            # Google News RSS
            url = f"https://news.google.com/rss/search?q={query}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"

            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, 'xml')
            results = []

            for item in soup.find_all('item')[:limit]:
                title = item.find('title')
                link = item.find('link')
                description = item.find('description')
                pub_date = item.find('pubDate')

                if title:
                    results.append({
                        'title': title.get_text() if title else '',
                        'url': link.get_text() if link else '',
                        'snippet': BeautifulSoup(description.get_text(), 'html.parser').get_text(strip=True) if description else '',
                        'published_at': pub_date.get_text() if pub_date else '',
                        'source': 'Google News'
                    })

            return results
        except Exception as e:
            return []


class TechCrunchSearch(SearchSource):
    """TechCrunch 搜索"""

    def search(self, query: str = "", limit: int = 10) -> List[Dict]:
        """获取 TechCrunch 最新文章"""
        if not HAS_REQUESTS or not HAS_BS4:
            return []

        try:
            url = "https://techcrunch.com/"
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []

            # 尝试多种选择器
            selectors = [
                'article a[href*="/2024/"]',
                'article a[href*="/2025/"]',
                '.post-block__title__link',
                'h2 a', 'h3 a',
                '.wp-block-post-title a'
            ]

            seen_urls = set()
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    for item in items[:limit * 2]:
                        title = item.get_text(strip=True)[:80]
                        href = item.get('href', '')
                        if href and href not in seen_urls:
                            seen_urls.add(href)
                            results.append({
                                'title': title,
                                'url': href,
                                'source': 'TechCrunch'
                            })
                            if len(results) >= limit:
                                break
                    if results:
                        break

            return results[:limit]
        except Exception as e:
            return []


class TheVergeSearch(SearchSource):
    """The Verge 搜索"""

    def search(self, query: str = "", limit: int = 10) -> List[Dict]:
        """获取 The Verge 最新文章"""
        if not HAS_REQUESTS or not HAS_BS4:
            return []

        try:
            url = "https://www.theverge.com/"
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []

            # 尝试多种选择器
            selectors = [
                'a[href*="/2024/"]',
                'a[href*="/2025/"]',
                'article h2 a',
                'article h3 a',
                '.duet--recirculation--item a'
            ]

            seen_urls = set()
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    for item in items[:limit * 2]:
                        title = item.get_text(strip=True)[:80]
                        href = item.get('href', '')
                        if href and href not in seen_urls:
                            seen_urls.add(href)
                            results.append({
                                'title': title,
                                'url': href,
                                'source': 'The Verge'
                            })
                            if len(results) >= limit:
                                break
                    if results:
                        break

            return results[:limit]
        except Exception as e:
            return []


class _36KrSearch(SearchSource):
    """36氪搜索 (中文科技资讯)"""

    def search(self, query: str = "", limit: int = 10) -> List[Dict]:
        """获取 36氪最新快讯"""
        if not HAS_REQUESTS or not HAS_BS4:
            return []

        try:
            # 36氪热点列表页面
            url = "https://36kr.com/hot-list"
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []

            # 尝试多种选择器
            selectors = [
                '.hot-list-item',
                '.item-title a',
                'article h3 a',
                'article h2 a',
                '.title a'
            ]

            for selector in selectors:
                items = soup.select(selector)
                if items:
                    for item in items[:limit]:
                        title = item.get_text(strip=True)[:80]
                        href = item.get('href', '')
                        if href and not href.startswith('http'):
                            href = 'https://36kr.com' + href
                        results.append({
                            'title': title,
                            'url': href,
                            'source': '36氪'
                        })
                    if results:
                        break

            return results[:limit]
        except Exception as e:
            return []


class SspaiSearch(SearchSource):
    """少数派搜索 (中文科技)"""

    def search(self, query: str = "", limit: int = 10) -> List[Dict]:
        """获取少数派最新文章"""
        if not HAS_REQUESTS or not HAS_BS4:
            return []

        try:
            # 少数派最新文章页面
            url = "https://sspai.com/"
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []

            # 尝试多种选择器
            selectors = [
                '.post-item a',
                'article h3 a',
                'article h2 a',
                '.title a',
                'a[href*="/post/"]'
            ]

            seen_urls = set()
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    for item in items[:limit * 2]:  # 获取更多以便去重
                        title = item.get_text(strip=True)[:80]
                        href = item.get('href', '')
                        if href and not href.startswith('http'):
                            href = 'https://sspai.com' + href
                        if href and '/post/' in href and href not in seen_urls:
                            seen_urls.add(href)
                            results.append({
                                'title': title,
                                'url': href,
                                'source': '少数派'
                            })
                            if len(results) >= limit:
                                break
                    if results:
                        break

            return results[:limit]
        except Exception as e:
            return []


class GitHubTrending(SearchSource):
    """GitHub Trending (热门仓库)"""

    def search(self, query: str = "", limit: int = 10) -> List[Dict]:
        """获取 GitHub Trending"""
        if not HAS_REQUESTS or not HAS_BS4:
            return []

        try:
            url = "https://github.com/trending"
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)

            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []

            # 解析仓库列表
            for repo in soup.select('article.Box-row')[:limit]:
                title_elem = repo.select_one('h2 a')
                desc_elem = repo.select_one('p')
                stars_elem = repo.select_one('[href*="/stargazers"]')

                if title_elem:
                    full_name = title_elem.get_text(strip=True).replace('\n', '').replace(' ', '')
                    results.append({
                        'title': full_name,
                        'url': 'https://github.com' + title_elem.get('href', ''),
                        'description': desc_elem.get_text(strip=True) if desc_elem else '',
                        'stars': stars_elem.get_text(strip=True) if stars_elem else '',
                        'source': 'GitHub Trending'
                    })

            return results
        except Exception as e:
            return []


# ==================== 实时搜索管理器 ====================

class RealtimeSearchManager:
    """实时搜索管理器"""

    def __init__(self):
        self.sources = {
            'hn': HackerNewsSearch(),
            'reddit': RedditSearch(),
            'ddg': DuckDuckGoSearch(),
            'baidu': BaiduSearch(),
            'gnews': GoogleNewsSearch(),
            'techcrunch': TechCrunchSearch(),
            'verge': TheVergeSearch(),
            '36kr': _36KrSearch(),
            'sspai': SspaiSearch(),
            'github': GitHubTrending()
        }

    def search_all(self, query: str = "", sources: List[str] = None, limit: int = 10) -> Dict[str, List[Dict]]:
        """搜索所有源"""
        if sources is None:
            sources = ['hn', 'reddit', 'gnews', '36kr', 'sspai', 'github']

        results = {}

        for source_name in sources:
            if source_name not in self.sources:
                continue

            source = self.sources[source_name]

            try:
                if source_name in ['github', 'techcrunch', 'verge', '36kr', 'sspai']:
                    # 这些是直接获取最新内容，不需要查询
                    items = source.search("", limit)
                else:
                    items = source.search(query, limit)

                if items:
                    results[source_name] = items
                    time.sleep(0.5)  # 避免请求过快
            except Exception as e:
                continue

        return results

    def get_trending_topics(self, hot_keywords: List[str] = None) -> Dict[str, List[Dict]]:
        """根据热门关键词搜索相关内容"""
        if hot_keywords is None:
            # 默认热门关键词
            hot_keywords = [
                'AI', '人工智能', 'GPT', 'LLM',
                '科技', '技术', '编程',
                '创业', '商业',
                '区块链', 'Web3',
                '新能源', '电动车'
            ]

        # 只搜索前几个关键词
        results = {}
        for keyword in hot_keywords[:5]:
            keyword_results = self.search_all(
                query=keyword,
                sources=['hn', 'reddit', 'gnews'],
                limit=5
            )
            results[keyword] = keyword_results
            time.sleep(1)

        return results


# ==================== 报告生成器 ====================

class SearchReportGenerator:
    """搜索报告生成器"""

    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def generate_markdown(self, results: Dict[str, List[Dict]]) -> str:
        """生成 Markdown 报告"""
        lines = []

        lines.append(f"# 实时搜索结果\n\n")
        lines.append(f"**时间**: {self.timestamp}\n")
        lines.append(f"**来源**: 共 {len(results)} 个搜索源\n\n")
        lines.append("---\n\n")

        # 按类别分组
        tech_sources = ['hn', 'reddit', 'github', 'techcrunch', 'verge']
        cn_sources = ['36kr', 'sspai', 'baidu']
        news_sources = ['gnews', 'ddg']

        # 科技类
        tech_results = {k: v for k, v in results.items() if k in tech_sources}
        if tech_results:
            lines.append("## 科技资讯\n\n")
            for source, items in tech_results.items():
                if items:
                    lines.append(self._format_source(source, items))
            lines.append("\n---\n\n")

        # 中文资讯
        cn_results = {k: v for k, v in results.items() if k in cn_sources}
        if cn_results:
            lines.append("## 中文资讯\n\n")
            for source, items in cn_results.items():
                if items:
                    lines.append(self._format_source(source, items))
            lines.append("\n---\n\n")

        # 综合新闻
        news_results = {k: v for k, v in results.items() if k in news_sources}
        if news_results:
            lines.append("## 综合新闻\n\n")
            for source, items in news_results.items():
                if items:
                    lines.append(self._format_source(source, items))
            lines.append("\n---\n\n")

        lines.append("*数据由 realtime_search.py 生成*\n")

        return ''.join(lines)

    def _format_source(self, source: str, items: List[Dict]) -> str:
        """格式化单个搜索源的结果"""
        source_names = {
            'hn': 'Hacker News',
            'reddit': 'Reddit',
            'ddg': 'DuckDuckGo',
            'baidu': '百度搜索',
            'gnews': 'Google News',
            'techcrunch': 'TechCrunch',
            'verge': 'The Verge',
            '36kr': '36氪',
            'sspai': '少数派',
            'github': 'GitHub Trending'
        }

        lines = []
        lines.append(f"### {source_names.get(source, source)}\n\n")

        if not items:
            lines.append("暂无结果\n\n")
            return ''.join(lines)

        for i, item in enumerate(items[:10], 1):
            title = item.get('title', '')[:80]
            url = item.get('url', '')

            # 添加额外信息
            extra = []
            if item.get('points'):
                extra.append(f"{item['points']} pts")
            if item.get('num_comments'):
                extra.append(f"{item['num_comments']} 评论")
            if item.get('stars'):
                extra.append(item['stars'])
            if item.get('author'):
                extra.append(f"by {item['author']}")

            extra_str = f" ({', '.join(extra)})" if extra else ""

            lines.append(f"{i}. [{title}]({url}){extra_str}\n")

        lines.append("\n")
        return ''.join(lines)


# ==================== 命令行工具 ====================

def main():
    import argparse

    parser = argparse.ArgumentParser(description='实时搜索工具')
    parser.add_argument('--query', '-q', default='', help='搜索关键词')
    parser.add_argument('--sources', '-s', default='hn,reddit,gnews,36kr,sspai,github',
                       help='搜索源 (逗号分隔)')
    parser.add_argument('--limit', '-l', type=int, default=10, help='每源结果数')
    parser.add_argument('--output', '-o', help='输出文件路径')

    args = parser.parse_args()

    if not HAS_REQUESTS:
        print("错误: 需要安装 requests 库")
        print("请运行: pip install requests beautifulsoup4")
        return

    print("\n" + "=" * 50)
    print("      实时搜索")
    print("=" * 50 + "\n")

    manager = RealtimeSearchManager()
    sources = args.sources.split(',')

    print(f"搜索源: {', '.join(sources)}")
    print(f"查询: {args.query or '获取最新内容'}\n")

    results = manager.search_all(query=args.query, sources=sources, limit=args.limit)

    # 生成报告
    generator = SearchReportGenerator()
    report = generator.generate_markdown(results)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存: {args.output}\n")

    total_items = sum(len(items) for items in results.values())
    print(f"完成! 共 {total_items} 条结果\n")

    if not args.output:
        print("\n" + report)


if __name__ == "__main__":
    main()
