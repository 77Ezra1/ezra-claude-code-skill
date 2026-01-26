#!/usr/bin/env python3
"""
微信公众号文章助手 - 交互式CLI界面
"""

import os
import sys
import time
from pathlib import Path

# 添加模块路径
sys.path.insert(0, os.path.dirname(__file__))
from save_article_visual import save_article_with_progress

# 默认保存路径
DEFAULT_PATH = "D:/WeChatArticles"


class Menu:
    """菜单系统"""

    def __init__(self):
        self.options = []

    def add_option(self, key, label, action):
        """添加菜单选项"""
        self.options.append({"key": key, "label": label, "action": action})

    def show(self):
        """显示菜单"""
        self._clear_screen()
        self._show_header()
        self._show_options()
        self._show_footer()

    def _clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _show_header(self):
        """显示标题"""
        print()
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                                                            ║")
        print("║          微信公众号文章阅读室 WeChat Article Room           ║")
        print("║                                                            ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()

    def _show_options(self):
        """显示选项"""
        for opt in self.options:
            print(f"  [{opt['key']}] {opt['label']}")
        print()

    def _show_footer(self):
        """显示底部"""
        print("─" * 60)
        print(f"  保存路径: {DEFAULT_PATH}")
        print("─" * 60)
        print()

    def get_choice(self):
        """获取用户选择"""
        try:
            choice = input("请选择操作 [q=退出]: ").strip().lower()
            if choice == 'q':
                return None
            for opt in self.options:
                if opt['key'] == choice:
                    return opt['action']
            print("无效的选择，请重试")
            time.sleep(1)
            return self.get_choice()
        except KeyboardInterrupt:
            print("\n\n再见!")
            sys.exit(0)


def save_article_interactive():
    """交互式保存文章"""
    print("\n" + "─" * 60)
    print("  保存公众号文章")
    print("─" * 60)

    url = input("\n请输入文章链接: ").strip()

    if not url:
        print("链接不能为空!")
        input("\n按回车继续...")
        return

    # 询问是否使用Cookie
    use_cookie = input("\n是否使用Cookie? [y/N]: ").strip().lower()
    cookie_file = None
    if use_cookie == 'y':
        cookie_path = input("请输入Cookie配置文件路径 [assets/cookie_config.json]: ").strip()
        cookie_file = cookie_path if cookie_path else "assets/cookie_config.json"

    # 询问主题
    theme = input("\n选择进度主题 [1=default, 2=simple] [1]: ").strip()
    theme = "simple" if theme == "2" else "default"

    # 保存文章
    print("\n正在处理...\n")
    result = save_article_with_progress(url, cookie_file, theme)

    if result:
        print("\n[SUCCESS] 保存完成!")
    else:
        print("\n[ERROR] 保存失败!")

    input("\n按回车继续...")


def view_saved_articles():
    """查看已保存的文章"""
    print("\n" + "─" * 60)
    print("  已保存的文章")
    print("─" * 60)

    articles_dir = Path(DEFAULT_PATH)
    if not articles_dir.exists():
        print("\n暂无保存的文章")
        input("\n按回车继续...")
        return

    # 获取所有文章文件夹
    folders = sorted([f for f in articles_dir.iterdir() if f.is_dir()], reverse=True)

    if not folders:
        print("\n暂无保存的文章")
        input("\n按回车继续...")
        return

    print(f"\n共 {len(folders)} 篇文章:\n")

    for i, folder in enumerate(folders[:20], 1):  # 最多显示20篇
        # 从文件夹名解析信息
        name = folder.name
        parts = name.split('_', 2)
        if len(parts) >= 3:
            date_str = parts[0]
            author = parts[1]
            title = parts[2][:40]
            print(f"  {i:2d}. [{date_str}] {author}")
            print(f"      {title}")
        else:
            print(f"  {i:2d}. {name}")

    if len(folders) > 20:
        print(f"\n  ... 还有 {len(folders) - 20} 篇文章")

    print(f"\n保存位置: {articles_dir}")

    input("\n按回车继续...")


def configure_cookie():
    """配置Cookie"""
    print("\n" + "─" * 60)
    print("  Cookie配置向导")
    print("─" * 60)

    print("""
获取Cookie步骤:

  1. 在浏览器中访问 https://mp.weixin.qq.com/ 并登录
  2. 按F12打开开发者工具
  3. 切换到 Application (应用) 标签
  4. 左侧找到 Storage → Cookies → https://mp.weixin.qq.com
  5. 复制关键Cookie (key, pass_ticket, wxuin等)
    """)

    choice = input("\n是否现在配置Cookie? [y/N]: ").strip().lower()

    if choice == 'y':
        cookie_path = input("\n请输入Cookie配置文件路径 [assets/cookie_config.json]: ").strip()
        cookie_path = cookie_path if cookie_path else "assets/cookie_config.json"

        print(f"\n正在创建配置文件: {cookie_path}")

        # 创建配置文件
        config_content = """{
  "cookies": [
    {
      "name": "key",
      "value": "请粘贴从浏览器复制的key值",
      "domain": "mp.weixin.qq.com"
    },
    {
      "name": "pass_ticket",
      "value": "请粘贴从浏览器复制的pass_ticket值",
      "domain": "mp.weixin.qq.com"
    },
    {
      "name": "wxuin",
      "value": "请粘贴从浏览器复制的wxuin值",
      "domain": "mp.weixin.qq.com"
    }
  ],
  "last_updated": "请手动更新此时间为当前时间"
}
"""

        try:
            cookie_file = Path(cookie_path)
            cookie_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cookie_file, 'w', encoding='utf-8') as f:
                f.write(config_content)
            print("\n[SUCCESS] 配置文件已创建")
            print(f"\n请用文本编辑器打开 {cookie_file}")
            print("将浏览器中的Cookie值粘贴到对应字段")
        except Exception as e:
            print(f"\n[ERROR] 创建配置文件失败: {e}")

    input("\n按回车继续...")


def show_help():
    """显示帮助信息"""
    print("\n" + "─" * 60)
    print("  使用帮助")
    print("─" * 60)

    print("""
支持的链接格式:
  - https://mp.weixin.qq.com/s/xxxxxxxx
  - https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx&sn=xxx

工作流程:
  1. 验证链接有效性
  2. 获取文章内容 (可能需要Cookie)
  3. 解析文章数据
  4. 创建保存目录
  5. 保存原文Markdown
  6. 生成AI分析模板

保存结构:
  D:/WeChatArticles/
  └── YYYYMMDD_公众号名称_文章标题/
      ├── 01_原文.md
      └── 02_总结分析.md

Cookie说明:
  - 大部分公开文章不需要Cookie
  - 仅限关注/过期链接需要Cookie
  - Cookie会定期失效，需重新获取

常见问题:
  Q: 为什么有些文章获取失败?
  A: 可能是链接已过期或需要登录，请配置Cookie

  Q: 如何修改保存路径?
  A: 编辑脚本中的 DEFAULT_PATH 变量

  Q: Cookie多久需要更新?
  A: 通常几天到一周，失效时重新获取即可
    """)

    input("\n按回车继续...")


def main():
    """主程序"""
    # 创建菜单
    menu = Menu()
    menu.add_option('1', '保存公众号文章', save_article_interactive)
    menu.add_option('2', '查看已保存的文章', view_saved_articles)
    menu.add_option('3', '配置Cookie', configure_cookie)
    menu.add_option('4', '使用帮助', show_help)

    # 主循环
    while True:
        menu.show()
        action = menu.get_choice()
        if action is None:
            print("\n再见!")
            break
        action()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n再见!")
        sys.exit(0)
