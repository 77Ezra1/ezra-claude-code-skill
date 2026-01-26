#!/usr/bin/env python3
"""
Cookie有效性检查脚本
"""

import json
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("请安装依赖: pip install requests")
    sys.exit(1)


def check_cookie(cookie_file):
    """检查Cookie配置文件的有效性"""
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        return {"valid": False, "error": "Cookie配置文件不存在"}
    except json.JSONDecodeError:
        return {"valid": False, "error": "Cookie配置文件格式错误"}

    cookies = config.get('cookies', [])
    if not cookies:
        return {"valid": False, "error": "Cookie配置为空"}

    # 构建Cookie字典
    cookie_dict = {c['name']: c['value'] for c in cookies}

    # 检查Cookie是否包含必要字段
    required_keys = ['key', 'pass_ticket', 'wxuin']
    missing_keys = [k for k in required_keys if k not in cookie_dict]
    if missing_keys:
        return {
            "valid": False,
            "error": f"Cookie缺少必要字段: {', '.join(missing_keys)}",
            "warning": "请确保从 mp.weixin.qq.com 复制完整的Cookie"
        }

    # 测试Cookie是否有效
    session = requests.Session()
    session.cookies.update(cookie_dict)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://mp.weixin.qq.com/',
    })

    try:
        response = session.get(
            'https://mp.weixin.qq.com/',
            allow_redirects=False,
            timeout=10
        )

        if response.status_code == 302 and 'login' in response.headers.get('Location', ''):
            return {
                "valid": False,
                "error": "Cookie已失效",
                "solution": "请重新登录 mp.weixin.qq.com 获取最新Cookie"
            }

        if response.status_code == 200:
            last_updated = config.get('last_updated', 'unknown')
            return {
                "valid": True,
                "message": f"Cookie有效 (最后更新: {last_updated})",
                "last_updated": last_updated
            }

        return {"valid": False, "error": f"未知状态码: {response.status_code}"}

    except requests.RequestException as e:
        return {"valid": False, "error": f"网络请求失败: {str(e)}"}


def main():
    import argparse

    parser = argparse.ArgumentParser(description='检查微信公众号Cookie有效性')
    parser.add_argument('--cookie', required=True, help='Cookie配置文件路径')

    args = parser.parse_args()

    result = check_cookie(args.cookie)

    if result['valid']:
        print(f"[OK] {result['message']}")
        sys.exit(0)
    else:
        print(f"[ERROR] {result['error']}")
        if 'warning' in result:
            print(f"[WARN] {result['warning']}")
        if 'solution' in result:
            print(f"[TIP] {result['solution']}")
        sys.exit(1)


if __name__ == '__main__':
    main()
