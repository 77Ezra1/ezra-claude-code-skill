#!/usr/bin/env python3
"""
Zlibrary Client - Zlibrary API 封装
基于 bipinkrish/Zlibrary-API 的简化客户端
"""

import json
import sys
from pathlib import Path


class ZlibraryClient:
    """Zlibrary API 客户端封装"""

    def __init__(self, email=None, password=None, remix_userid=None, remix_userkey=None, domain=None, verify_ssl=True, proxies=None):
        """
        初始化客户端

        参数:
            email: 邮箱（可选，优先级低于配置文件）
            password: 密码（可选）
            remix_userid: Remix 用户 ID（推荐）
            remix_userkey: Remix 用户密钥（推荐）
            domain: Z-library 域名（可选，默认 1lib.sk）
            verify_ssl: 是否验证 SSL 证书（默认 True）
            proxies: 代理设置字典，如 {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
        """
        # 尝试从配置文件加载凭证
        config_path = Path(__file__).parent.parent / "config" / "credentials.json"

        if config_path.exists():
            with open(config_path, "r") as f:
                config = json.load(f)
                if not remix_userid and config.get("remix_userid"):
                    remix_userid = config.get("remix_userid")
                if not remix_userkey and config.get("remix_userkey"):
                    remix_userkey = config.get("remix_userkey")
                if not email and config.get("email"):
                    email = config.get("email")
                if not password and config.get("password"):
                    password = config.get("password")
                if not domain and config.get("domain"):
                    domain = config.get("domain")
                if config.get("verify_ssl") is not None:
                    verify_ssl = config.get("verify_ssl")
                if not proxies and config.get("proxies"):
                    proxies = config.get("proxies")

        self._verify_ssl = verify_ssl
        self._timeout = 30  # 默认超时 30 秒
        self._proxies = proxies

        # 将技能根目录添加到 Python 路径
        skill_root = Path(__file__).parent.parent
        sys.path.insert(0, str(skill_root))

        # 导入并初始化 API
        try:
            from Zlibrary import Zlibrary
            self._api = Zlibrary(
                email=email,
                password=password,
                remix_userid=remix_userid,
                remix_userkey=remix_userkey,
                domain=domain,
                verify_ssl=verify_ssl,
                timeout=self._timeout,
                proxies=proxies
            )
        except Exception as e:
            print(f"初始化失败: {e}")
            self._api = None

    def is_logged_in(self):
        """检查是否已登录"""
        return self._api and self._api.isLoggedIn()

    def search(self, message, **kwargs):
        """
        搜索图书

        参数:
            message: 搜索关键词
            yearFrom: 起始年份
            yearTo: 结束年份
            languages: 语言，如 "Chinese,English"
            extensions: 格式，如 "pdf,epub"
            order: 排序方式 "popular", "year", "newest"
            page: 页码
            limit: 每页数量
        """
        if not self.is_logged_in():
            return {"success": False, "error": "未登录"}
        return self._api.search(message, **kwargs)

    def get_book_info(self, bookid, hashid, switch_language=None):
        """获取图书详情"""
        if not self.is_logged_in():
            return {"success": False, "error": "未登录"}
        return self._api.getBookInfo(bookid, hashid, switch_language)

    def download_book(self, book):
        """
        下载图书

        参数:
            book: 图书对象（包含 id 和 hash 字段）

        返回:
            (filename, content) 元组
        """
        if not self.is_logged_in():
            return None
        return self._api.downloadBook(book)

    def get_image(self, book):
        """获取图书封面"""
        if not self.is_logged_in():
            return None
        return self._api.getImage(book)

    def get_most_popular(self, switch_language=None, limit=10):
        """获取热门图书"""
        if not self.is_logged_in():
            return {"success": False, "error": "未登录"}
        result = self._api.getMostPopular(switch_language)
        if result.get("success") and "books" in result:
            result["books"] = result["books"][:limit]
        return result

    def get_recently(self, limit=10):
        """获取最近添加的图书"""
        if not self.is_logged_in():
            return {"success": False, "error": "未登录"}
        result = self._api.getRecently()
        if result.get("success") and "books" in result:
            result["books"] = result["books"][:limit]
        return result

    def save_book(self, bookid):
        """收藏图书"""
        if not self.is_logged_in():
            return {"success": False, "error": "未登录"}
        return self._api.saveBook(bookid)

    def get_user_saved(self, limit=10):
        """获取用户收藏的图书"""
        if not self.is_logged_in():
            return {"success": False, "error": "未登录"}
        result = self._api.getUserSaved(limit=limit)
        return result

    def get_downloads_left(self):
        """获取剩余下载次数"""
        if not self.is_logged_in():
            return 0
        return self._api.getDownloadsLeft()

    def get_profile(self):
        """获取用户资料"""
        if not self.is_logged_in():
            return {"success": False, "error": "未登录"}
        return self._api.getProfile()

    def get_similar(self, bookid, hashid):
        """获取相似图书推荐"""
        if not self.is_logged_in():
            return {"success": False, "error": "未登录"}
        return self._api.getSimilar(bookid, hashid)


def format_book(book):
    """格式化图书信息用于显示"""
    title = book.get("title", "未知标题")
    author = book.get("author", "未知作者")
    year = book.get("year", "")
    extension = book.get("extension", "")
    size = book.get("filesize", "")
    language = book.get("language", "")

    parts = [f"{title} ({author})"]
    if year:
        parts.append(f"{year}年")
    if language:
        parts.append(f"{language}")
    parts.append(f"{extension.upper()}")
    if size:
        parts.append(f"{size}")

    return " | ".join(parts)


# CLI 工具
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Zlibrary 电子书搜索工具")
    parser.add_argument("search", nargs="?", help="搜索关键词")
    parser.add_argument("--popular", action="store_true", help="显示热门图书")
    parser.add_argument("--recent", action="store_true", help="显示最新图书")
    parser.add_argument("--limit", type=int, default=10, help="结果数量")

    args = parser.parse_args()

    client = ZlibraryClient()

    if not client.is_logged_in():
        print("登录失败，请检查 config/credentials.json 配置")
        exit(1)

    if args.search:
        print(f"正在搜索: {args.search}")
        results = client.search(args.search, limit=args.limit)

        if results.get("success"):
            books = results.get("books", [])
            print(f"\n找到 {len(books)} 本图书:\n")
            for i, book in enumerate(books, 1):
                print(f"{i}. {format_book(book)}")
        else:
            print(f"搜索失败: {results.get('error', '未知错误')}")

    elif args.popular:
        print("获取热门图书...")
        results = client.get_most_popular(limit=args.limit)

        if results.get("success"):
            books = results.get("books", [])
            print(f"\n热门图书 TOP {len(books)}:\n")
            for i, book in enumerate(books, 1):
                print(f"{i}. {format_book(book)}")
        else:
            print(f"获取失败: {results.get('error', '未知错误')}")

    elif args.recent:
        print("获取最新图书...")
        results = client.get_recently(limit=args.limit)

        if results.get("success"):
            books = results.get("books", [])
            print(f"\n最新添加 {len(books)} 本:\n")
            for i, book in enumerate(books, 1):
                print(f"{i}. {format_book(book)}")
        else:
            print(f"获取失败: {results.get('error', '未知错误')}")

    else:
        # 显示下载额度
        left = client.get_downloads_left()
        print(f"今日剩余下载次数: {left}")
        print(f"\n使用示例:")
        print(f"  python3 {__file__} 搜索关键词")
        print(f"  python3 {__file__} --popular")
        print(f"  python3 {__file__} --recent")
