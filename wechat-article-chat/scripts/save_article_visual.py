#!/usr/bin/env python3
"""
保存公众号文章（原文+总结）到D盘 - 带可视化进度界面
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# 添加 fetch_article 模块路径
sys.path.insert(0, os.path.dirname(__file__))
from fetch_article import fetch_article, WeChatArticleFetcher

# 文章保存目录
ARTICLES_DIR = "D:/WeChatArticles"


class VisualProgress:
    """命令行可视化进度显示"""

    def __init__(self, title, theme="default"):
        self.title = title
        self.theme = theme
        self.steps = []
        self.current_step = 0
        self.start_time = time.time()

        # 主题配置
        self.themes = {
            "default": {
                "border": "┃",
                "corner_tl": "┏",
                "corner_tr": "┓",
                "corner_bl": "┗",
                "corner_br": "┛",
                "header": "━",
                "done": "[DONE]",
                "doing": "[....]",
                "todo": "[    ]",
                "success": "\033[92m",
                "active": "\033[93m",
                "reset": "\033[0m",
            },
            "simple": {
                "border": "|",
                "corner_tl": "+",
                "corner_tr": "+",
                "corner_bl": "+",
                "corner_br": "+",
                "header": "-",
                "done": "[OK]",
                "doing": "[..]",
                "todo": "[  ]",
                "success": "",
                "active": "",
                "reset": "",
            }
        }

        self.t = self.themes.get(theme, self.themes["default"])

    def add_step(self, name):
        """添加步骤"""
        self.steps.append({"name": name, "status": "todo"})

    def start(self, step_index):
        """开始某个步骤"""
        self.current_step = step_index
        self.steps[step_index]["status"] = "doing"
        self.steps[step_index]["start_time"] = time.time()
        self._render()

    def complete(self, step_index):
        """完成某个步骤"""
        self.steps[step_index]["status"] = "done"
        self.steps[step_index]["end_time"] = time.time()
        self._render()

    def fail(self, step_index, error_msg=""):
        """步骤失败"""
        self.steps[step_index]["status"] = "failed"
        self.steps[step_index]["error"] = error_msg
        self._render()

    def _get_status_icon(self, status):
        """获取状态图标"""
        if status == "done":
            return f"{self.t['success']}{self.t['done']}{self.t['reset']}"
        elif status == "doing":
            return f"{self.t['active']}{self.t['doing']}{self.t['reset']}"
        elif status == "failed":
            return f"\033[91m[FAIL]{self.t['reset']}"
        else:
            return self.t['todo']

    def _render(self):
        """渲染进度界面"""
        # 清屏并移动到顶部
        print("\033[H\033[J", end="")

        # 计算总用时
        elapsed = time.time() - self.start_time

        # 绘制标题
        width = 60
        print(f"{self.t['corner_tl']}{self.t['header'] * width}{self.t['corner_tr']}")
        title_padding = (width - len(self.title) - 2) // 2
        print(f"{self.t['border']}{' ' * title_padding}{self.title}{' ' * (width - title_padding - len(self.title))}{self.t['border']}")
        print(f"{self.t['corner_bl']}{self.t['header'] * width}{self.t['corner_tr']}")
        print()

        # 绘制步骤列表
        for i, step in enumerate(self.steps):
            status_icon = self._get_status_icon(step["status"])
            step_num = f"{i + 1}. "
            step_name = step["name"]

            if step["status"] == "doing":
                # 添加闪烁效果
                print(f"{status_icon} {step_num}{step_name}")
            elif step["status"] == "failed":
                print(f"{status_icon} {step_num}{step_name}")
                if "error" in step:
                    print(f"       Error: {step['error']}")
            elif step["status"] == "done":
                duration = step.get("end_time", 0) - step.get("start_time", 0)
                print(f"{status_icon} {step_num}{step_name} ({duration:.2f}s)")
            else:
                print(f"{status_icon} {step_num}{step_name}")

        # 绘制底部信息
        print()
        print(f"Elapsed: {elapsed:.2f}s")

        # 完成进度
        done_count = sum(1 for s in self.steps if s["status"] == "done")
        total_count = len(self.steps)
        if total_count > 0:
            progress = (done_count / total_count) * 100
            bar_length = 40
            filled = int(bar_length * done_count / total_count)
            bar = "#" * filled + "-" * (bar_length - filled)
            print(f"Progress: [{bar}] {done_count}/{total_count} ({progress:.0f}%)")


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        name = name.replace(char, '_')
    return name.strip()


def generate_summary(article_data):
    """生成文章总结分析"""
    title = article_data.get('title', '')
    author = article_data.get('author', '')
    content = article_data.get('content', '')

    return f"""# 文章分析

## 基本信息

- **标题**: {title}
- **来源**: {author}
- **链接**: {article_data.get('url', '')}
- **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 核心摘要

> 此部分需要AI根据文章内容生成200-300字的核心摘要

---

## 关键观点

1. **观点一**
   - 内容: [待AI分析]

2. **观点二**
   - 内容: [待AI分析]

3. **观点三**
   - 内容: [待AI分析]

---

## 逻辑结构

[待AI梳理文章的论证框架]

---

## 延伸思考

- **值得探讨的问题**: [待AI补充]
- **相关话题**: [待AI补充]
- **补充视角**: [待AI补充]

---

## 文章链接

- 原文链接: {article_data.get('url', '')}
- 原文Markdown: ./01_原文.md
"""


def save_article_with_progress(url, cookie_file=None, theme="default"):
    """
    保存文章（原文+总结）- 带可视化进度

    工作流程:
    1. 验证链接
    2. 获取内容
    3. 解析文章
    4. 创建目录
    5. 保存原文
    6. 生成分析
    """

    # 创建进度显示器
    progress = VisualProgress("WeChat Article Saver", theme=theme)

    # 定义工作流步骤
    progress.add_step("Validating URL")
    progress.add_step("Fetching content")
    progress.add_step("Parsing article")
    progress.add_step("Creating directory")
    progress.add_step("Saving original")
    progress.add_step("Generating analysis")

    # 步骤1: 验证链接
    progress.start(0)
    time.sleep(0.3)  # 模拟处理时间

    parsed = urlparse(url)
    if 'mp.weixin.qq.com' not in parsed.netloc:
        progress.fail(0, "无效的公众号链接")
        return False
    progress.complete(0)

    # 步骤2: 获取内容
    progress.start(1)
    fetcher = WeChatArticleFetcher(cookie_file)
    result = fetcher.fetch_article(url)

    if 'error' in result:
        progress.fail(1, result['error'])
        print(f"\n[TIP] {result.get('cookie_help', '请检查Cookie配置')}")
        return False
    progress.complete(1)

    # 步骤3: 解析文章
    progress.start(2)
    time.sleep(0.2)

    title = sanitize_filename(result['title'])
    author = sanitize_filename(result['author'])
    date_str = datetime.now().strftime('%Y%m%d')

    folder_name = f"{date_str}_{author}_{title[:50]}"
    article_dir = Path(ARTICLES_DIR) / folder_name
    progress.complete(2)

    # 步骤4: 创建目录
    progress.start(3)
    time.sleep(0.2)

    try:
        article_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        progress.fail(3, str(e))
        return False
    progress.complete(3)

    # 步骤5: 保存原文
    progress.start(4)
    time.sleep(0.3)

    original_file = article_dir / "01_原文.md"
    try:
        with open(original_file, 'w', encoding='utf-8') as f:
            f.write(fetcher.to_markdown(result))
    except Exception as e:
        progress.fail(4, str(e))
        return False
    progress.complete(4)

    # 步骤6: 生成分析
    progress.start(5)
    time.sleep(0.3)

    summary_file = article_dir / "02_总结分析.md"
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(generate_summary(result))
    except Exception as e:
        progress.fail(5, str(e))
        return False
    progress.complete(5)

    # 最终渲染
    progress._render()
    print()
    print(f"[SUCCESS] 文章已保存到: {article_dir}")
    print()
    print("保存的文件:")
    print(f"  - {original_file}")
    print(f"  - {summary_file}")

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='保存公众号文章（原文+总结）- 带可视化进度',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "https://mp.weixin.qq.com/s/xxx"
  %(prog)s "https://mp.weixin.qq.com/s/xxx" --cookie assets/cookie_config.json
  %(prog)s "https://mp.weixin.qq.com/s/xxx" --theme simple
        """
    )
    parser.add_argument('url', help='公众号文章链接')
    parser.add_argument('--cookie', help='Cookie配置文件路径')
    parser.add_argument('--theme', choices=['default', 'simple'], default='default',
                       help='进度主题 (default: 带颜色和Unicode字符, simple: 纯ASCII)')

    args = parser.parse_args()

    save_article_with_progress(args.url, args.cookie, args.theme)


if __name__ == '__main__':
    main()
