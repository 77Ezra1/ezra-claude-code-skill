#!/usr/bin/env python3
"""
微信公众号文章获取脚本
支持Cookie自动检测和失效提示
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    import html2text
except ImportError:
    print("请安装依赖: pip install requests beautifulsoup4 html2text")
    sys.exit(1)


class WeChatArticleFetcher:
    """微信公众号文章获取器"""

    def __init__(self, cookie_file=None):
        self.cookie_file = cookie_file
        self.cookies = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://mp.weixin.qq.com/',
        })

        if cookie_file:
            self.load_cookies(cookie_file)

    def load_cookies(self, cookie_file):
        """加载Cookie配置"""
        try:
            with open(cookie_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                cookies = config.get('cookies', [])
                self.cookies = {c['name']: c['value'] for c in cookies}
                self.session.cookies.update(self.cookies)
                print(f"[OK] Cookie loaded (last updated: {config.get('last_updated', 'unknown')})")
        except FileNotFoundError:
            print(f"[WARN] Cookie file not found: {cookie_file}")
            print("Some articles may require Cookie access, configure Cookie for full functionality")
        except json.JSONDecodeError:
            print(f"[WARN] Cookie file format error: {cookie_file}")

    def check_cookie_validity(self):
        """检查Cookie是否有效"""
        if not self.cookies:
            return False

        try:
            # 测试请求一个简单的接口
            response = self.session.get(
                'https://mp.weixin.qq.com/',
                allow_redirects=False,
                timeout=10
            )
            # 如果返回302跳转到登录页，说明Cookie失效
            if response.status_code == 302 and 'login' in response.headers.get('Location', ''):
                return False
            return response.status_code == 200
        except Exception:
            return False

    def fetch_article(self, url):
        """获取公众号文章内容"""
        if not self._is_valid_wechat_url(url):
            return {"error": "无效的公众号文章链接，请确认链接格式为 mp.weixin.qq.com"}

        # 检查Cookie状态（如果配置了Cookie）
        if self.cookies and not self.check_cookie_validity():
            return {
                "error": "Cookie已失效，请重新获取Cookie并更新配置文件",
                "cookie_help": "在浏览器登录 mp.weixin.qq.com → F12 → Application → Cookies → 复制所有Cookie到配置文件"
            }

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # 检查是否需要登录
            if self._need_login(response.text):
                return {
                    "error": "该文章需要登录才能查看，请配置Cookie",
                    "cookie_help": "编辑 assets/cookie_config.json 添加Cookie信息"
                }

            return self._parse_article(response.text, url)

        except requests.RequestException as e:
            return {"error": f"网络请求失败: {str(e)}"}

    def _is_valid_wechat_url(self, url):
        """验证是否为有效的公众号文章链接"""
        parsed = urlparse(url)
        return 'mp.weixin.qq.com' in parsed.netloc and '/s/' in parsed.path

    def _need_login(self, html):
        """检查是否需要登录"""
        # 检查是否有登录相关的关键词
        login_keywords = ['请先登录', '账号登录', '验证码']
        return any(keyword in html for keyword in login_keywords)

    def _parse_article(self, html, url):
        """解析文章内容"""
        soup = BeautifulSoup(html, 'html.parser')

        # 提取标题
        title_elem = soup.find('meta', property='og:title')
        title = title_elem.get('content', '') if title_elem else soup.find('h1')
        title = title if isinstance(title, str) else (title.get_text() if title else "未获取到标题")

        # 提取公众号名称
        author_elem = soup.find('meta', property='og:site_name')
        author = author_elem.get('content', '') if author_elem else "未知公众号"

        # 提取正文
        content_div = soup.find('div', {'class': re.compile(r'rich_media_content')})
        if not content_div:
            content_div = soup.find('div', {'id': 'js_content'})

        if not content_div:
            return {"error": "无法解析文章内容，可能是文章被删除或链接已失效"}

        # 转换为Markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0
        content = h.handle(str(content_div))

        return {
            "title": title.strip(),
            "author": author.strip(),
            "content": content.strip(),
            "url": url,
            "fetched_at": datetime.now().isoformat()
        }

    def to_markdown(self, article_data):
        """转换为Markdown格式"""
        if 'error' in article_data:
            return f"# 获取失败\n\n{article_data['error']}"

        return f"""# {article_data['title']}

**来源**: {article_data['author']}
**链接**: {article_data['url']}
**获取时间**: {article_data['fetched_at']}

---

{article_data['content']}
"""


def fetch_article(url, cookie_file=None):
    """便捷函数：获取公众号文章"""
    fetcher = WeChatArticleFetcher(cookie_file)
    return fetcher.fetch_article(url)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='获取微信公众号文章')
    parser.add_argument('url', help='公众号文章链接')
    parser.add_argument('--cookie', help='Cookie配置文件路径')
    parser.add_argument('--output', '-o', help='输出Markdown文件路径')

    args = parser.parse_args()

    fetcher = WeChatArticleFetcher(args.cookie)
    result = fetcher.fetch_article(args.url)

    if 'error' in result:
        print(f"[ERROR] {result['error']}")
        if 'cookie_help' in result:
            print(f"\n[TIP] {result['cookie_help']}")
        sys.exit(1)

    # 输出结果
    md_content = fetcher.to_markdown(result)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Article saved to: {args.output}")
    else:
        print(md_content)


if __name__ == '__main__':
    main()
