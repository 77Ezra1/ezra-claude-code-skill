#!/usr/bin/env python3
"""
Book Content Workflow - 书籍内容生产工作流执行脚本

整合 zlibrary、epub-to-markdown、book-interpreter、volcano-images 四个技能
实现从搜索书籍到生成解读文章的交互式流程
"""

import sys
import os
from pathlib import Path
import time


class BookWorkflow:
    """书籍内容生产工作流"""

    def __init__(self, base_path: str = None):
        # 默认路径：Windows 使用 D:/ObsidianWorkflows
        if base_path is None:
            if sys.platform == 'win32':
                base_path = "D:/ObsidianWorkflows"
            else:
                base_path = Path.home() / "ObsidianWorkflows"

        self.base_path = Path(base_path).expanduser()
        self.downloads_dir = self.base_path / "01-Books" / "downloads"  # zlibrary 下载的文件
        self.raw_dir = self.base_path / "01-Books" / "raw"              # 用户自己的文件
        self.converted_dir = self.base_path / "01-Books" / "converted"
        self.drafts_dir = self.base_path / "02-Articles" / "drafts"
        self.published_dir = self.base_path / "02-Articles" / "published"
        self.images_dir = self.base_path / "03-Assets" / "images"

        # 确保目录存在
        self._ensure_directories()

        # 工作流状态
        self.state = {
            'book_title': '',
            'epub_path': '',
            'md_path': '',
            'article_path': '',
            'published_path': '',
        }

    def _ensure_directories(self):
        """确保工作目录存在"""
        for dir_path in [self.downloads_dir, self.raw_dir, self.converted_dir, self.drafts_dir,
                         self.published_dir, self.images_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    # ==================== 阶段 1: 搜索下载 ====================

    def stage1_search_download(self, book_title: str) -> dict:
        """阶段1: 搜索并下载书籍"""
        print(f"\n{'='*60}")
        print(f"[1/4] 搜索并下载书籍")
        print(f"{'='*60}")
        print(f"正在搜索: {book_title}")

        # TODO: 集成 zlibrary skill
        # sys.path.insert(0, '~/.claude/skills/zlibrary')
        # from scripts.zlibrary_client import ZlibraryClient
        # client = ZlibraryClient()
        # results = client.search(message=book_title, limit=10)

        # 模拟搜索和下载
        time.sleep(0.5)
        epub_filename = f"{book_title}.epub"
        epub_path = f"~/Downloads/{epub_filename}"

        self.state['book_title'] = book_title
        self.state['epub_path'] = epub_path

        result = {
            "stage": "search_download",
            "epub_path": epub_path,
            "file_size": "25.3 MB",
            "message": f"已下载: {epub_filename}"
        }

        print(f"\n[下载完成]")
        print(f"结果: {result['message']}")
        print(f"位置: {epub_path}")

        return result

    # ==================== 阶段 2: 转换格式 ====================

    def stage2_convert_markdown(self) -> dict:
        """阶段2: 转换 EPUB 为 Markdown"""
        print(f"\n{'='*60}")
        print(f"[2/4] 转换为 Markdown")
        print(f"{'='*60}")
        print(f"正在转换: {self.state['epub_path']}")

        # TODO: 集成 epub-to-markdown skill
        # import subprocess
        # subprocess.run([
        #     'python', '~/.claude/skills/epub-to-markdown/scripts/convert_epub.py',
        #     self.state['epub_path'], '--output', str(self.converted_dir)
        # ])

        # 模拟转换
        time.sleep(0.5)
        md_filename = f"{self.state['book_title']}.md"
        md_path = self.converted_dir / md_filename

        self.state['md_path'] = str(md_path)

        result = {
            "stage": "convert",
            "md_path": str(md_path),
            "word_count": 150000,
            "images_count": 12,
            "message": "转换完成"
        }

        print(f"\n[转换完成]")
        print(f"文件: {md_filename}")
        print(f"字数: 约 {result['word_count']:,} 字")
        print(f"图片: 已提取 {result['images_count']} 张")

        return result

    # ==================== 阶段 3: 生成解读 ====================

    def stage3_interpret_book(self) -> dict:
        """阶段3: 生成 Ezra 风格解读"""
        print(f"\n{'='*60}")
        print(f"[3/4] 生成 Ezra 风格解读")
        print(f"{'='*60}")
        print(f"正在解读: {self.state['md_path']}")

        # TODO: 集成 book-interpreter skill
        # 读取书籍内容
        # 提取核心观点
        # 生成解读文章

        # 模拟解读
        time.sleep(0.5)
        article_filename = f"{self.state['book_title']}_解读.md"
        article_path = self.drafts_dir / article_filename

        self.state['article_path'] = str(article_path)

        result = {
            "stage": "interpret",
            "article_path": str(article_path),
            "word_count": 8500,
            "terms_count": 18,
            "analogies_count": 6,
            "message": "解读完成"
        }

        print(f"\n[解读完成]")
        print(f"文件: {article_filename}")
        print(f"字数: 约 {result['word_count']:,} 字")
        print(f"术语解释: {result['terms_count']} 处")
        print(f"类比说明: {result['analogies_count']} 处")

        return result

    # ==================== 阶段 4: 配图发布 ====================

    def stage4_generate_images(self) -> dict:
        """阶段4: 为文章配图"""
        print(f"\n{'='*60}")
        print(f"[4/4] 为文章配图")
        print(f"{'='*60}")
        print(f"正在配图: {self.state['article_path']}")

        # TODO: 集成 volcano-images skill
        # 分析文章结构
        # 批量生成配图
        # 插入图片

        # 模拟配图
        time.sleep(0.5)
        published_filename = f"{self.state['book_title']}_解读.md"
        published_path = self.published_dir / published_filename

        self.state['published_path'] = str(published_path)

        result = {
            "stage": "images",
            "published_path": str(published_path),
            "images_count": 8,
            "message": "配图完成"
        }

        print(f"\n[配图完成]")
        print(f"已发布到: published/")
        print(f"生成配图: {result['images_count']} 张")

        return result

    # ==================== 工作流执行 ====================

    def run(self, book_title: str, stop_at: str = None):
        """
        运行工作流

        Args:
            book_title: 书名
            stop_at: 在哪个阶段停止 ('download', 'convert', 'interpret', None=全部)
        """
        self.state['book_title'] = book_title

        print(f"\n{'='*60}")
        print(f"书籍内容生产工作流")
        print(f"{'='*60}")

        # 阶段 1: 搜索下载
        result1 = self.stage1_search_download(book_title)
        if stop_at == 'download':
            print(f"\n[流程暂停] 下载完成")
            return result1

        # 询问用户是否继续（在实际 Claude Code 中会调用 AskUserQuestion）
        # 这里简化为等待用户确认
        print(f"\n下一步?")
        print(f"  1. 转换为 Markdown")
        print(f"  2. 先放着，我自己读")

        # 阶段 2: 转换格式
        result2 = self.stage2_convert_markdown()
        if stop_at == 'convert':
            print(f"\n[流程暂停] 转换完成")
            return {**result1, **result2}

        print(f"\n下一步?")
        print(f"  1. 生成 Ezra 风格解读")
        print(f"  2. 我自己总结")
        print(f"  3. 仅保存 Markdown")

        # 阶段 3: 生成解读
        result3 = self.stage3_interpret_book()
        if stop_at == 'interpret':
            print(f"\n[流程暂停] 解读完成")
            return {**result1, **result2, **result3}

        print(f"\n下一步?")
        print(f"  1. 为文章配图")
        print(f"  2. 直接发布草稿")
        print(f"  3. 仅保存解读")

        # 阶段 4: 配图发布
        result4 = self.stage4_generate_images()

        print(f"\n{'='*60}")
        print(f"工作流完成!")
        print(f"{'='*60}")

        return {
            'stage1': result1,
            'stage2': result2,
            'stage3': result3,
            'stage4': result4,
        }

    def run_auto(self, book_title: str):
        """自动运行完整工作流（不询问）"""
        self.state['book_title'] = book_title

        print(f"\n{'='*60}")
        print(f"书籍内容生产工作流 (自动模式)")
        print(f"{'='*60}")

        result1 = self.stage1_search_download(book_title)
        result2 = self.stage2_convert_markdown()
        result3 = self.stage3_interpret_book()
        result4 = self.stage4_generate_images()

        print(f"\n{'='*60}")
        print(f"工作流完成!")
        print(f"{'='*60}")

        return {
            'stage1': result1,
            'stage2': result2,
            'stage3': result3,
            'stage4': result4,
        }


# ==================== CLI 接口 ====================

def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='书籍内容生产工作流'
    )
    parser.add_argument(
        'book_title',
        help='书名（如：深度学习）'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='自动运行，不询问'
    )
    parser.add_argument(
        '--stop-at',
        choices=['download', 'convert', 'interpret'],
        help='在指定阶段停止'
    )
    parser.add_argument(
        '--base-path',
        default=None,
        help='工作流基础路径 (默认: ~/ObsidianWorkflows)'
    )

    args = parser.parse_args()

    # 运行工作流
    workflow = BookWorkflow(base_path=args.base_path)

    if args.auto:
        results = workflow.run_auto(args.book_title)
    else:
        results = workflow.run(args.book_title, stop_at=args.stop_at)

    return 0


if __name__ == '__main__':
    # 演示模式
    if len(sys.argv) == 1:
        print("=== 书籍内容生产工作流 - 演示 ===\n")
        workflow = BookWorkflow()
        workflow.run_auto("演示书籍")
    else:
        sys.exit(main())
