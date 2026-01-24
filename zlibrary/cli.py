#!/usr/bin/env python3
"""
Zlibrary 电子书搜索与下载
封装 Zlibrary API，支持搜索图书、获取详情、下载图书、收藏管理等功能。
"""

import sys
import os
from pathlib import Path

# 添加技能根目录到 Python 路径
skill_root = Path(__file__).parent
sys.path.insert(0, str(skill_root))

from scripts.zlibrary_client import ZlibraryClient, format_book


def search_books(keyword, limit=10):
    """搜索图书"""
    client = ZlibraryClient()
    if not client.is_logged_in():
        return {"success": False, "error": "未登录，请检查配置"}

    results = client.search(message=keyword, limit=limit)
    if not results.get("success"):
        return results

    books = results.get("books", [])
    return {
        "success": True,
        "books": books,
        "count": len(books),
        "formatted": "\n".join([
            f"{i}. {format_book(book)}"
            for i, book in enumerate(books, 1)
        ])
    }


def download_book(book):
    """下载图书"""
    client = ZlibraryClient()
    if not client.is_logged_in():
        return {"success": False, "error": "未登录，请检查配置"}

    left = client.get_downloads_left()
    if left == 0:
        return {"success": False, "error": "今日下载次数已用完"}

    filename, content = client.download_book(book)

    # 保存到 Downloads
    save_dir = os.path.expanduser("~/Downloads")
    save_path = os.path.join(save_dir, filename)
    with open(save_path, "wb") as f:
        f.write(content)

    size_mb = len(content) / (1024 * 1024)
    return {
        "success": True,
        "filename": filename,
        "path": save_path,
        "size_mb": round(size_mb, 1),
        "remaining": left - 1
    }


def get_popular(limit=10):
    """获取热门图书"""
    client = ZlibraryClient()
    if not client.is_logged_in():
        return {"success": False, "error": "未登录，请检查配置"}

    results = client.get_most_popular(limit=limit)
    if not results.get("success"):
        return results

    books = results.get("books", [])
    return {
        "success": True,
        "books": books,
        "count": len(books),
        "formatted": "\n".join([
            f"{i}. {format_book(book)}"
            for i, book in enumerate(books, 1)
        ])
    }


def get_recent(limit=10):
    """获取最新图书"""
    client = ZlibraryClient()
    if not client.is_logged_in():
        return {"success": False, "error": "未登录，请检查配置"}

    results = client.get_recently(limit=limit)
    if not results.get("success"):
        return results

    books = results.get("books", [])
    return {
        "success": True,
        "books": books,
        "count": len(books),
        "formatted": "\n".join([
            f"{i}. {format_book(book)}"
            for i, book in enumerate(books, 1)
        ])
    }


def get_status():
    """获取账户状态"""
    client = ZlibraryClient()
    if not client.is_logged_in():
        return {"success": False, "error": "未登录，请检查配置"}

    profile = client.get_profile()
    return {
        "success": True,
        "email": profile.get("user", {}).get("email", ""),
        "name": profile.get("user", {}).get("name", ""),
        "downloads_left": client.get_downloads_left(),
        "is_premium": profile.get("user", {}).get("isPremium", False)
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Zlibrary 电子书搜索工具")
    parser.add_argument("action", nargs="?", help="操作: search/download/popular/recent/status")
    parser.add_argument("--query", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=10, help="结果数量")

    args = parser.parse_args()

    if args.action == "search" or not args.action:
        query = args.query or input("搜索关键词: ")
        result = search_books(query, args.limit)
        if result.get("success"):
            print(f"找到 {result['count']} 本相关图书：\n")
            print(result['formatted'])
        else:
            print(f"搜索失败: {result.get('error')}")

    elif args.action == "popular":
        result = get_popular(args.limit)
        if result.get("success"):
            print(f"热门图书 TOP {result['count']}：\n")
            print(result['formatted'])
        else:
            print(f"获取失败: {result.get('error')}")

    elif args.action == "recent":
        result = get_recent(args.limit)
        if result.get("success"):
            print(f"最新图书 {result['count']} 本：\n")
            print(result['formatted'])
        else:
            print(f"获取失败: {result.get('error')}")

    elif args.action == "status":
        result = get_status()
        if result.get("success"):
            print(f"账户: {result['name']} ({result['email']})")
            print(f"类型: {'Premium' if result['is_premium'] else '免费'}")
            print(f"今日剩余下载: {result['downloads_left']} 次")
        else:
            print(f"获取失败: {result.get('error')}")
