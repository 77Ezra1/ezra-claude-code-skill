#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 自动登录获取 Cookie
支持知乎、抖音等平台的自动登录和 Cookie 管理
"""

import os
import json
import time
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

try:
    from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    print("错误: 需要安装 playwright")
    print("请运行: pip install playwright && python -m playwright install chromium")


# ==================== Session 存储 ====================

class SessionManager:
    """Session 管理器 - 保存和加载登录状态"""

    def __init__(self, session_dir: str = None):
        if session_dir is None:
            session_dir = os.path.expanduser('~/.claude/skills/daily-hot-fetcher/sessions')
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def get_session_path(self, platform: str) -> Path:
        """获取平台 session 文件路径"""
        return self.session_dir / f"{platform}_session.json"

    def get_cookie_path(self, platform: str) -> Path:
        """获取平台 cookie 文件路径"""
        return self.session_dir / f"{platform}_cookies.json"

    def save_session(self, platform: str, context: BrowserContext):
        """保存完整的 session (包含 cookies, localStorage, sessionStorage)"""
        session_path = self.get_session_path(platform)
        context.storage_state(path=str(session_path))

        # 单独保存 cookies 为方便使用的格式
        cookies = context.cookies()
        cookie_path = self.get_cookie_path(platform)
        cookie_dict = {c['name']: c['value'] for c in cookies}
        with open(cookie_path, 'w', encoding='utf-8') as f:
            json.dump({
                'cookies': cookie_dict,
                'timestamp': datetime.now().isoformat(),
                'expires': (datetime.now() + timedelta(days=7)).isoformat()
            }, f, indent=2, ensure_ascii=False)

        return True

    def load_session(self, platform: str) -> Optional[Dict]:
        """加载 session 信息"""
        cookie_path = self.get_cookie_path(platform)
        if not cookie_path.exists():
            return None

        try:
            with open(cookie_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 检查是否过期
            expires = datetime.fromisoformat(data.get('expires', ''))
            if datetime.now() > expires:
                print(f"[{platform}] Session 已过期")
                return None

            return data
        except Exception as e:
            print(f"[{platform}] 加载 session 失败: {e}")
            return None

    def is_session_valid(self, platform: str) -> bool:
        """检查 session 是否有效"""
        session_path = self.get_session_path(platform)
        if not session_path.exists():
            return False

        data = self.load_session(platform)
        return data is not None

    def get_cookies(self, platform: str) -> Dict[str, str]:
        """获取 cookies 字典"""
        data = self.load_session(platform)
        if data:
            return data.get('cookies', {})
        return {}


# ==================== 平台登录器 ====================

class PlatformLogin:
    """平台登录器基类"""

    def __init__(self, session_manager: SessionManager = None):
        self.session_manager = session_manager or SessionManager()
        self.user_data_dir = None

    def get_user_data_dir(self, platform: str) -> str:
        """获取浏览器用户数据目录（持久化登录状态）"""
        user_data_dir = self.session_manager.session_dir / f"browser_{platform}"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        return str(user_data_dir)

    def check_login_status(self, page: Page) -> bool:
        """检查是否已登录（子类实现）"""
        return False

    def wait_for_login(self, page: Page) -> bool:
        """等待用户完成登录（子类实现）"""
        return False

    def login(self, platform: str) -> Dict[str, str]:
        """执行登录流程"""
        raise NotImplementedError


class ZhiHuLogin(PlatformLogin):
    """知乎登录器"""

    def check_login_status(self, page: Page) -> bool:
        """检查知乎登录状态"""
        try:
            page.goto('https://www.zhihu.com', timeout=15000)
            time.sleep(2)

            # 检查是否存在登录按钮
            if page.locator('.SignButton', timeout=5000).count() > 0:
                return False

            # 检查是否能获取用户信息
            if page.locator('.AppHeader-profile', timeout=5000).count() > 0:
                return True

            return False
        except:
            return False

    def wait_for_login(self, page: Page) -> bool:
        """等待用户扫码登录"""
        print("\n[知乎] 等待扫码登录...")
        print("[知乎] 请使用手机知乎 APP 扫描二维码登录\n")

        try:
            # 新版知乎可能不显示二维码，等待页面加载
            time.sleep(3)

            # 尝试查找二维码（多种可能的选择器）
            qrcode_selectors = ['.QRCode', 'img[src*="qr"]', 'img[alt*="二维码"]', 'canvas']
            qrcode_found = False
            for selector in qrcode_selectors:
                try:
                    if page.wait_for_selector(selector, timeout=5000).count() > 0:
                        print("[知乎] 二维码已显示，请扫码...")
                        qrcode_found = True
                        break
                except:
                    continue

            if not qrcode_found:
                print("[知乎] 未检测到二维码，可能已进入其他登录方式")
                print("[知乎] 请在页面完成登录...")

            # 等待登录成功（检测多种可能的登录成功标志）
            success_selectors = [
                '.AppHeader-profile',
                '.ProfileHeader-name',
                '[class*="avatar"]',
                '[class*="user"]',
                'a[href*="/people/"]',
                'img[class*="Avatar"]'
            ]

            # 使用 race 方式等待任意一个登录成功标志出现
            for selector in success_selectors:
                try:
                    page.wait_for_selector(selector, timeout=120000)
                    print("[知乎] 登录成功!")
                    return True
                except:
                    continue

            print("[知乎] 登录超时，未能检测到登录成功标志")
            return False
        except Exception as e:
            print(f"[知乎] 登录超时或失败: {e}")
            return False

    def login(self, platform: str = "zhihu") -> Dict[str, str]:
        """执行知乎登录"""
        cookies = {}
        user_data_dir = self.get_user_data_dir(platform)

        with sync_playwright() as p:
            # 启动浏览器，使用持久化用户数据
            browser = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                viewport={'width': 1280, 'height': 800}
            )

            try:
                # 检查是否已登录
                if self.check_login_status(browser):
                    print("[知乎] 已处于登录状态")
                else:
                    # 需要登录
                    page = browser.new_page()
                    page.goto('https://www.zhihu.com/signin')

                    # 等待用户扫码登录
                    if self.wait_for_login(page):
                        time.sleep(2)  # 等待页面稳定
                    else:
                        return {}

                # 保存 session
                self.session_manager.save_session(platform, browser)

                # 获取 cookies
                cookies_list = browser.cookies()
                cookies = {c['name']: c['value'] for c in cookies_list}

                print(f"[知乎] Cookie 已保存 ({len(cookies)} 个)")

            finally:
                browser.close()

        return cookies


class DouyinLogin(PlatformLogin):
    """抖音登录器"""

    def check_login_status(self, page: Page) -> bool:
        """检查抖音登录状态"""
        try:
            page.goto('https://www.douyin.com/', timeout=15000)
            time.sleep(2)

            # 未登录会有登录按钮
            if page.locator('[class*="login"]').count() > 0:
                return False

            # 已登录会有用户头像
            if page.locator('[class*="avatar"], [class*="user"]').count() > 0:
                return True

            return False
        except:
            return False

    def wait_for_login(self, page: Page) -> bool:
        """等待用户扫码登录"""
        print("\n[抖音] 等待扫码登录...")
        print("[抖音] 请使用抖音 APP 扫码登录\n")

        try:
            # 等待登录成功（检测用户头像出现）
            page.wait_for_selector('[class*="avatar"], [class*="user"]', timeout=120000)
            print("[抖音] 登录成功!")
            return True
        except Exception as e:
            print(f"[抖音] 登录超时或失败: {e}")
            return False

    def login(self, platform: str = "douyin") -> Dict[str, str]:
        """执行抖音登录"""
        cookies = {}
        user_data_dir = self.get_user_data_dir(platform)

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                viewport={'width': 1280, 'height': 800}
            )

            try:
                page = browser.new_page()

                # 检查是否已登录
                if self.check_login_status(page):
                    print("[抖音] 已处于登录状态")
                else:
                    page.goto('https://www.douyin.com/')
                    time.sleep(2)

                    # 尝试点击登录按钮
                    login_btn = page.locator('text=登录, [class*="login"]').first
                    if login_btn.count() > 0:
                        login_btn.click()
                        time.sleep(1)

                    # 等待扫码登录
                    if self.wait_for_login(page):
                        time.sleep(2)
                    else:
                        return {}

                # 保存 session
                self.session_manager.save_session(platform, browser)

                # 获取 cookies
                cookies_list = browser.cookies()
                cookies = {c['name']: c['value'] for c in cookies_list}

                print(f"[抖音] Cookie 已保存 ({len(cookies)} 个)")

            finally:
                browser.close()

        return cookies


class WeiboLogin(PlatformLogin):
    """微博登录器"""

    def check_login_status(self, page: Page) -> bool:
        """检查微博登录状态"""
        try:
            page.goto('https://weibo.com', timeout=15000)
            time.sleep(2)

            # 未登录会有登录按钮
            if page.locator('.W_login, [node-type="loginBtn"]').count() > 0:
                return False

            # 已登录有用户名
            if page.locator('[class*="name"], [class*="user"]').count() > 0:
                return True

            return False
        except:
            return False

    def wait_for_login(self, page: Page) -> bool:
        """等待用户扫码登录"""
        print("\n[微博] 等待扫码登录...")
        print("[微博] 请使用微博 APP 扫码登录\n")

        try:
            # 等待登录成功
            page.wait_for_selector('[class*="name"], [class*="user"]', timeout=120000)
            print("[微博] 登录成功!")
            return True
        except Exception as e:
            print(f"[微博] 登录超时或失败: {e}")
            return False

    def login(self, platform: str = "weibo") -> Dict[str, str]:
        """执行微博登录"""
        cookies = {}
        user_data_dir = self.get_user_data_dir(platform)

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                viewport={'width': 1280, 'height': 800}
            )

            try:
                page = browser.new_page()

                if self.check_login_status(page):
                    print("[微博] 已处于登录状态")
                else:
                    page.goto('https://weibo.com/login.php')
                    time.sleep(2)

                    if self.wait_for_login(page):
                        time.sleep(2)
                    else:
                        return {}

                # 保存 session
                self.session_manager.save_session(platform, browser)

                cookies_list = browser.cookies()
                cookies = {c['name']: c['value'] for c in cookies_list}

                print(f"[微博] Cookie 已保存 ({len(cookies)} 个)")

            finally:
                browser.close()

        return cookies


class TwitterLogin(PlatformLogin):
    """Twitter/X 登录器"""

    def check_login_status(self, page: Page) -> bool:
        """检查 Twitter/X 登录状态"""
        try:
            page.goto('https://x.com/', timeout=15000)
            time.sleep(3)

            # 未登录会有登录按钮
            login_selectors = [
                'a[data-testid="login"]',
                'a[href="/login"]',
                '[data-testid="loginPage"]'
            ]

            for selector in login_selectors:
                if page.locator(selector).count() > 0:
                    return False

            # 已登录会有用户信息
            logged_in_selectors = [
                '[data-testid="SideNav_AccountSwitcher_Button"]',
                '[data-testid="userActions"]',
                '[aria-label="Profile"]'
            ]

            for selector in logged_in_selectors:
                if page.locator(selector).count() > 0:
                    return True

            return False
        except:
            return False

    def wait_for_login(self, page: Page) -> bool:
        """等待用户登录"""
        print("\n[X] 等待登录...")
        print("[X] 请在页面完成登录（用户名/密码或扫码）\n")

        try:
            # 等待登录成功
            success_selectors = [
                '[data-testid="SideNav_AccountSwitcher_Button"]',
                '[data-testid="userActions"]',
                '[aria-label="Profile"]',
                '[data-testid="AppTabBar_Profile_Link"]'
            ]

            for selector in success_selectors:
                try:
                    page.wait_for_selector(selector, timeout=120000)
                    print("[X] 登录成功!")
                    return True
                except:
                    continue

            print("[X] 登录超时")
            return False
        except Exception as e:
            print(f"[X] 登录超时或失败: {e}")
            return False

    def login(self, platform: str = "twitter") -> Dict[str, str]:
        """执行 Twitter/X 登录"""
        cookies = {}
        user_data_dir = self.get_user_data_dir(platform)

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                viewport={'width': 1280, 'height': 800}
            )

            try:
                page = browser.new_page()

                if self.check_login_status(page):
                    print("[X] 已处于登录状态")
                else:
                    page.goto('https://x.com/i/flow/login')
                    time.sleep(2)

                    if self.wait_for_login(page):
                        time.sleep(2)
                    else:
                        return {}

                # 保存 session
                self.session_manager.save_session(platform, browser)

                cookies_list = browser.cookies()
                cookies = {c['name']: c['value'] for c in cookies_list}

                print(f"[X] Cookie 已保存 ({len(cookies)} 个)")

            finally:
                browser.close()

        return cookies


# ==================== 登录管理器 ====================

class AutoLoginManager:
    """自动登录管理器"""

    def __init__(self):
        self.session_manager = SessionManager()
        self.platforms = {
            'zhihu': ZhiHuLogin(self.session_manager),
            'douyin': DouyinLogin(self.session_manager),
            'weibo': WeiboLogin(self.session_manager),
            'twitter': TwitterLogin(self.session_manager),
            'x': TwitterLogin(self.session_manager)
        }

    def login_platform(self, platform: str, force: bool = False) -> Dict[str, str]:
        """登录指定平台"""
        if platform not in self.platforms:
            print(f"错误: 不支持的平台 '{platform}'")
            return {}

        # 检查是否已有有效 session
        if not force and self.session_manager.is_session_valid(platform):
            print(f"[{platform}] 使用已保存的 session")
            return self.session_manager.get_cookies(platform)

        # 执行登录
        platform_login = self.platforms[platform]
        return platform_login.login(platform)

    def login_all(self, platforms: List[str] = None, force: bool = False) -> Dict[str, Dict[str, str]]:
        """登录多个平台"""
        if platforms is None:
            platforms = ['zhihu', 'douyin', 'weibo', 'twitter']

        results = {}
        for platform in platforms:
            print(f"\n{'='*50}")
            print(f"正在处理: {platform.upper()}")
            print('='*50)

            cookies = self.login_platform(platform, force)
            if cookies:
                results[platform] = cookies
                print(f"[{platform}] 成功获取 {len(cookies)} 个 Cookie")
            else:
                print(f"[{platform}] 登录失败")

        return results

    def refresh_cookie(self, platform: str) -> Dict[str, str]:
        """刷新指定平台的 Cookie"""
        return self.login_platform(platform, force=True)

    def check_cookies(self) -> Dict[str, bool]:
        """检查各平台 Cookie 状态"""
        status = {}
        for platform in self.platforms.keys():
            status[platform] = self.session_manager.is_session_valid(platform)
        return status


# ==================== 命令行工具 ====================

def main():
    import argparse

    parser = argparse.ArgumentParser(description='自动登录获取 Cookie')
    parser.add_argument('platform', nargs='?',
                       choices=['zhihu', 'douyin', 'weibo', 'twitter', 'x', 'all'],
                       default='all',
                       help='要登录的平台')
    parser.add_argument('--force', '-f', action='store_true',
                       help='强制重新登录，忽略已保存的 session')
    parser.add_argument('--check', '-c', action='store_true',
                       help='检查各平台 Cookie 状态')

    args = parser.parse_args()

    if not HAS_PLAYWRIGHT:
        print("错误: 请先安装 playwright")
        print("运行: pip install playwright && python -m playwright install chromium")
        return

    manager = AutoLoginManager()

    if args.check:
        # 检查状态
        print("\nCookie 状态检查:")
        print("-" * 40)
        status = manager.check_cookies()
        for platform, valid in status.items():
            state = "[OK] 有效" if valid else "[X] 无效/过期"
            print(f"  {platform:10s} {state}")
        return

    # 执行登录
    platforms = [args.platform] if args.platform != 'all' else None
    results = manager.login_all(platforms, force=args.force)

    # 显示结果
    print(f"\n{'='*50}")
    print("登录结果汇总")
    print('='*50)

    for platform, cookies in results.items():
        if cookies:
            print(f"[{platform}] ✓ 成功 ({len(cookies)} 个 Cookie)")
        else:
            print(f"[{platform}] ✗ 失败")


if __name__ == "__main__":
    main()
