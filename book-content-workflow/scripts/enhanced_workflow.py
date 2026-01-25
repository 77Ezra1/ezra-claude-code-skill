#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Book Content Workflow - 集成实际技能调用的书籍内容生产工作流

整合 zlibrary、epub-to-markdown 的实际调用
book-interpreter 和 volcano-images 需要在 Claude Code 环境中执行
"""

import sys
import os
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List

# Fix Windows encoding issue
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 尝试导入 visual-progress（可选）
_visual_progress_available = False
try:
    _visual_progress_path = Path.home() / '.claude' / 'skills' / 'visual-progress'
    if _visual_progress_path.exists():
        sys.path.insert(0, str(_visual_progress_path))
        from core.visual_progress import VisualProgress
        _visual_progress_available = True
except (ImportError, ModuleNotFoundError):
    _visual_progress_available = False


class BookWorkflowIntegrated:
    """集成实际技能调用的书籍内容生产工作流"""

    def __init__(self, base_path: str = None):
        # 默认路径：Windows 使用 D:/ObsidianWorkflows
        if base_path is None:
            if sys.platform == 'win32':
                base_path = "D:/ObsidianWorkflows"
            else:
                base_path = Path.home() / "ObsidianWorkflows"

        self.base_path = Path(base_path).expanduser()
        self.downloads_dir = self.base_path / "01-Books" / "downloads"
        self.raw_dir = self.base_path / "01-Books" / "raw"
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
            'search_results': [],
            'search_performed': False,
        }

    def stage0_search_only(self, book_title: str) -> dict:
        """仅搜索书籍（不下载）"""
        # 添加 zlibrary skill 路径
        zlibrary_skill = Path.home() / '.claude' / 'skills' / 'zlibrary'
        zlibrary_scripts = zlibrary_skill / 'scripts'
        sys.path.insert(0, str(zlibrary_scripts))

        try:
            # 直接导入 zlibrary_client 模块
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "zlibrary_client",
                zlibrary_scripts / "zlibrary_client.py"
            )
            zlibrary_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(zlibrary_module)
            ZlibraryClient = zlibrary_module.ZlibraryClient

            print(f"\n🔍 正在搜索: {book_title}")

            client = ZlibraryClient()

            # 检查登录状态
            if not client.is_logged_in():
                return {
                    "status": "failed",
                    "error": "Zlibrary 未登录，请先配置凭证",
                    "message": "登录失败"
                }

            # 搜索书籍
            search_result = client.search(book_title, limit=10)

            if not search_result.get("success"):
                return {
                    "status": "failed",
                    "error": search_result.get('error', '搜索失败'),
                    "message": "搜索失败"
                }

            books = search_result.get("books", [])
            self.state['search_results'] = books
            self.state['search_performed'] = True
            self.state['book_title'] = book_title

            if not books:
                return {
                    "status": "failed",
                    "error": "未找到匹配的书籍",
                    "message": "未找到结果",
                    "books": []
                }

            # 检查下载额度
            left = client.get_downloads_left()

            # 格式化搜索结果
            formatted_books = []
            for i, book in enumerate(books, 1):
                formatted_books.append({
                    'index': i,
                    'title': book.get('title', '未知'),
                    'author': book.get('author', '未知'),
                    'publisher': book.get('publisher', 'N/A'),
                    'year': book.get('year', 'N/A'),
                    'filesize': book.get('filesize', 'N/A'),
                    'language': book.get('language', 'N/A'),
                })

            # 不在这里打印，由调用者负责打印表格
            print(f"📊 今日剩余下载次数: {left}\n")

            return {
                "status": "success",
                "message": f"找到 {len(books)} 本书籍",
                "books": formatted_books,
                "downloads_left": left,
                "book_title": book_title
            }

        except ImportError as e:
            return {
                "status": "failed",
                "error": f"无法导入 zlibrary_client: {e}",
                "message": "模块导入失败"
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "message": "搜索失败"
            }

    def _ensure_directories(self):
        """确保工作目录存在"""
        for dir_path in [self.downloads_dir, self.raw_dir, self.converted_dir,
                         self.drafts_dir, self.published_dir, self.images_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def print_all_books(self, books: list) -> None:
        """以表格形式打印所有找到的书籍列表（完整显示）"""
        if not books:
            print("\n❌ 未找到匹配的书籍")
            return

        # 动态计算列宽，确保完整显示所有内容
        max_index_width = max(4, len(str(len(books))))

        # 计算实际最长书名（最多100字符）
        max_title_width = min(100, max(len(str(book.get('title', '未知'))) for book in books))
        if max_title_width < 30:
            max_title_width = 30

        # 计算实际最长作者名（最多35字符）
        max_author_width = min(35, max(len(str(book.get('author', '未知'))) for book in books))
        if max_author_width < 15:
            max_author_width = 15

        max_size_width = 10
        max_year_width = 6

        # 表头
        h_line = "─"
        separator = "┌" + h_line * (max_index_width + 2) + "┬" + h_line * (max_title_width + 2) + "┬" + h_line * (max_author_width + 2) + "┬" + h_line * (max_size_width + 2) + "┬" + h_line * (max_year_width + 2) + "┐"
        header = "│ " + "序号".center(max_index_width) + " │ " + "书名".ljust(max_title_width) + " │ " + "作者".ljust(max_author_width) + " │ " + "大小".rjust(max_size_width) + " │ " + "年份".center(max_year_width) + " │"
        middle_separator = "├" + h_line * (max_index_width + 2) + "┼" + h_line * (max_title_width + 2) + "┼" + h_line * (max_author_width + 2) + "┼" + h_line * (max_size_width + 2) + "┼" + h_line * (max_year_width + 2) + "┤"

        # 计算表格总宽度
        table_width = 2 + (max_index_width + 2) + 3 + (max_title_width + 2) + 3 + (max_author_width + 2) + 3 + (max_size_width + 2) + 3 + (max_year_width + 2) + 2

        print(f"\n{'='*table_width}")
        print(f"📚 找到 {len(books)} 本书籍")
        print(f"{'='*table_width}\n")

        # 打印表格
        print(separator)
        print(header)
        print(middle_separator)

        for i, book in enumerate(books, 1):
            # 完整显示书名和作者
            title = str(book.get('title', '未知'))
            author = str(book.get('author', '未知'))
            year = str(book.get('year', 'N/A'))

            # 格式化文件大小
            filesize_raw = book.get('filesize', 'N/A')
            if isinstance(filesize_raw, int):
                size_mb = filesize_raw / 1024 / 1024
                filesize = f"{size_mb:.1f}MB"
            else:
                filesize = str(filesize_raw)

            # 只在必要时截断（超长内容）
            if len(title) > max_title_width:
                title = title[:max_title_width-3] + "..."
            if len(author) > max_author_width:
                author = author[:max_author_width-3] + "..."

            row = "│ " + str(i).rjust(max_index_width) + " │ " + title.ljust(max_title_width) + " │ " + author.ljust(max_author_width) + " │ " + filesize.rjust(max_size_width) + " │ " + year.center(max_year_width) + " │"
            print(row)

        # 表尾
        footer = "└" + h_line * (max_index_width + 2) + "┴" + h_line * (max_title_width + 2) + "┴" + h_line * (max_author_width + 2) + "┴" + h_line * (max_size_width + 2) + "┴" + h_line * (max_year_width + 2) + "┘"
        print(footer)
        print()

    def download_book_by_index(self, book_index: int) -> dict:
        """根据索引下载指定的书籍

        Args:
            book_index: 书籍索引（1-based）

        Returns:
            下载结果字典
        """
        books = self.state.get('search_results', [])

        if not books:
            return {
                "status": "failed",
                "error": "没有搜索结果，请先执行搜索",
                "message": "无搜索结果"
            }

        if book_index < 1 or book_index > len(books):
            return {
                "status": "failed",
                "error": f"书籍索引超出范围 (1-{len(books)})",
                "message": "索引无效"
            }

        # 添加 zlibrary skill 路径
        zlibrary_skill = Path.home() / '.claude' / 'skills' / 'zlibrary'
        zlibrary_scripts = zlibrary_skill / 'scripts'
        sys.path.insert(0, str(zlibrary_scripts))

        try:
            # 导入 zlibrary_client 模块
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "zlibrary_client",
                zlibrary_scripts / "zlibrary_client.py"
            )
            zlibrary_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(zlibrary_module)
            ZlibraryClient = zlibrary_module.ZlibraryClient

            client = ZlibraryClient()

            # 检查下载额度
            left = client.get_downloads_left()
            if left <= 0:
                return {
                    "status": "failed",
                    "error": "今日下载次数已用完",
                    "message": "下载额度不足"
                }

            # 获取选中的书籍
            selected_book = books[book_index - 1]

            print(f"\n⬇️  正在下载: {selected_book.get('title', '未知')}")

            # 下载书籍
            download_result = client.download_book(selected_book)

            if not download_result:
                return {
                    "status": "failed",
                    "error": "下载失败",
                    "message": "下载失败"
                }

            filename, content = download_result

            # 保存文件
            safe_filename = filename.replace("/", "_").replace("\\", "_").replace("|", "_")
            safe_filename = safe_filename.replace(":", "_").replace("?", "_").replace("*", "_")
            safe_filename = safe_filename.replace("<", "_").replace(">", "_").replace('"', '_')

            epub_path = self.downloads_dir / safe_filename

            with open(epub_path, "wb") as f:
                f.write(content)

            size_mb = len(content) / 1024 / 1024

            self.state['book_title'] = selected_book.get('title', '')
            self.state['epub_path'] = str(epub_path)

            print(f"✅ 下载完成!")
            print(f"📁 位置: {epub_path}")
            print(f"📦 大小: {size_mb:.2f} MB")
            print(f"📊 今日剩余: {left - 1} 次\n")

            return {
                "status": "completed",
                "epub_path": str(epub_path),
                "file_size": f"{size_mb:.2f} MB",
                "message": f"已下载: {safe_filename}",
                "downloads_left": left - 1
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "message": "执行失败"
            }

    def stage1_search_download(self, task_id: str, task_info: dict) -> dict:
        """阶段1: 搜索并下载书籍 (zlibrary)"""
        book_title = self.state.get('book_title', task_info.get('book_title', ''))

        # 添加 zlibrary skill 路径
        zlibrary_skill = Path.home() / '.claude' / 'skills' / 'zlibrary'
        zlibrary_scripts = zlibrary_skill / 'scripts'
        sys.path.insert(0, str(zlibrary_scripts))

        try:
            # 直接导入 zlibrary_client 模块
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "zlibrary_client",
                zlibrary_scripts / "zlibrary_client.py"
            )
            zlibrary_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(zlibrary_module)
            ZlibraryClient = zlibrary_module.ZlibraryClient

            print(f"\n🔍 正在搜索: {book_title}")

            client = ZlibraryClient()

            # 检查登录状态
            if not client.is_logged_in():
                return {
                    "status": "failed",
                    "error": "Zlibrary 未登录，请先配置凭证",
                    "message": "登录失败"
                }

            # 搜索书籍
            search_result = client.search(book_title, limit=10)

            if not search_result.get("success"):
                return {
                    "status": "failed",
                    "error": search_result.get('error', '搜索失败'),
                    "message": "搜索失败"
                }

            books = search_result.get("books", [])
            self.state['search_results'] = books

            if not books:
                return {
                    "status": "failed",
                    "error": "未找到匹配的书籍",
                    "message": "未找到结果"
                }

            # 显示搜索结果，选择第一个
            selected_book = books[0]
            print(f"\n📚 找到: {selected_book.get('title', '未知')}")
            print(f"✍️  作者: {selected_book.get('author', '未知')}")
            print(f"📦 大小: {selected_book.get('filesize', 'N/A')}")

            # 检查下载额度
            left = client.get_downloads_left()
            print(f"📊 今日剩余: {left} 次")

            if left <= 0:
                return {
                    "status": "failed",
                    "error": "今日下载次数已用完",
                    "message": "下载额度不足"
                }

            # 下载书籍
            print(f"\n⬇️  正在下载...")
            download_result = client.download_book(selected_book)

            if not download_result:
                return {
                    "status": "failed",
                    "error": "下载失败",
                    "message": "下载失败"
                }

            filename, content = download_result

            # 保存文件
            safe_filename = filename.replace("/", "_").replace("\\", "_").replace("|", "_")
            safe_filename = safe_filename.replace(":", "_").replace("?", "_").replace("*", "_")
            safe_filename = safe_filename.replace("<", "_").replace(">", "_").replace('"', '_')

            epub_path = self.downloads_dir / safe_filename

            with open(epub_path, "wb") as f:
                f.write(content)

            size_mb = len(content) / 1024 / 1024

            self.state['book_title'] = selected_book.get('title', book_title)
            self.state['epub_path'] = str(epub_path)

            print(f"\n✅ 下载完成!")
            print(f"📁 位置: {epub_path}")
            print(f"📦 大小: {size_mb:.2f} MB")

            return {
                "status": "completed",
                "epub_path": str(epub_path),
                "file_size": f"{size_mb:.2f} MB",
                "message": f"已下载: {safe_filename}"
            }

        except ImportError as e:
            return {
                "status": "failed",
                "error": f"无法导入 zlibrary_client: {e}",
                "message": "模块导入失败"
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "message": "执行失败"
            }

    def stage2_convert_markdown(self, task_id: str, task_info: dict) -> dict:
        """阶段2: 转换 EPUB 为 Markdown (epub-to-markdown)"""
        epub_path = self.state.get('epub_path', '')

        if not epub_path or not Path(epub_path).exists():
            return {
                "status": "failed",
                "error": "EPUB 文件不存在",
                "message": "文件未找到"
            }

        print(f"\n📄 正在转换: {Path(epub_path).name}")

        try:
            # 调用 epub-to-markdown skill 的转换脚本
            convert_script = Path.home() / '.claude' / 'skills' / 'epub-to-markdown' / 'scripts' / 'convert_epub.py'

            if not convert_script.exists():
                return {
                    "status": "failed",
                    "error": "转换脚本不存在",
                    "message": "脚本未找到"
                }

            # 执行转换
            result = subprocess.run(
                [sys.executable, str(convert_script), str(epub_path), '--output', str(self.converted_dir)],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )

            if result.returncode != 0:
                return {
                    "status": "failed",
                    "error": result.stderr or "转换失败",
                    "message": "转换失败"
                }

            # 查找生成的 Markdown 文件
            md_files = list(self.converted_dir.glob("*.md"))
            if not md_files:
                # 可能使用了完整书名
                epub_name = Path(epub_path).stem
                md_path = self.converted_dir / f"{epub_name}.md"
            else:
                md_path = md_files[-1]  # 使用最新的

            if not md_path.exists():
                return {
                    "status": "failed",
                    "error": "未找到生成的 Markdown 文件",
                    "message": "输出未找到"
                }

            # 统计字数
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                word_count = len(content)
                # 统计图片
                images_count = content.count('![')

            self.state['md_path'] = str(md_path)

            print(f"\n✅ 转换完成!")
            print(f"📄 文件: {md_path.name}")
            print(f"📊 字数: 约 {word_count:,} 字")
            print(f"🖼️  图片: {images_count} 张")

            return {
                "status": "completed",
                "md_path": str(md_path),
                "word_count": word_count,
                "images_count": images_count,
                "message": "转换完成"
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "failed",
                "error": "转换超时（超过5分钟）",
                "message": "转换超时"
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "message": "转换失败"
            }

    def stage3_interpret_book(self, task_id: str, task_info: dict) -> dict:
        """阶段3: 生成 Ezra 风格解读

        注意：此阶段需要在 Claude Code 环境中执行 book-interpreter skill
        这里返回 Markdown 文件路径，由 Claude Code 继续处理
        """
        md_path = self.state.get('md_path', '')

        if not md_path or not Path(md_path).exists():
            return {
                "status": "failed",
                "error": "Markdown 文件不存在",
                "message": "文件未找到"
            }

        print(f"\n✍️  准备解读: {Path(md_path).name}")
        print(f"⚠️  此阶段需要 Claude Code 执行 book-interpreter skill")

        # 返回信息，让 Claude Code 继续处理
        article_filename = f"{self.state['book_title']}_解读.md"
        article_path = self.drafts_dir / article_filename

        self.state['article_path'] = str(article_path)

        return {
            "status": "pending_claude",
            "md_path": str(md_path),
            "article_path": str(article_path),
            "message": "等待 Claude Code 生成解读",
            "instruction": f"请使用 book-interpreter skill 解读: {md_path}"
        }

    def stage4_generate_images(self, task_id: str, task_info: dict) -> dict:
        """阶段4: 为文章配图

        注意：此阶段需要在 Claude Code 环境中执行 volcano-images skill
        """
        article_path = self.state.get('article_path', '')

        print(f"\n🎨 准备配图")
        print(f"⚠️  此阶段需要 Claude Code 执行 volcano-images skill")

        # 返回信息，让 Claude Code 继续处理
        published_filename = f"{self.state['book_title']}_解读.md"
        published_path = self.published_dir / published_filename

        self.state['published_path'] = str(published_path)

        return {
            "status": "pending_claude",
            "article_path": str(article_path),
            "published_path": str(published_path),
            "message": "等待 Claude Code 生成配图",
            "instruction": f"请使用 volcano-images skill 为文章配图: {article_path}"
        }

    def _run_simple(self, book_title: str, stop_at: str = None,
                    interactive: bool = False) -> dict:
        """
        简单模式运行（当 visual-progress 不可用时）

        Args:
            book_title: 书名
            stop_at: 在哪个阶段停止
            interactive: 是否交互模式
        """
        print(f"\n{'='*60}")
        print(f"书籍解读: {book_title}")
        print(f"{'='*60}")

        results = {}
        task_handlers = {
            'search_download': lambda tid, info: self.stage1_search_download(tid, info),
            'convert_markdown': lambda tid, info: self.stage2_convert_markdown(tid, info),
            'interpret_book': lambda tid, info: self.stage3_interpret_book(tid, info),
            'generate_images': lambda tid, info: self.stage4_generate_images(tid, info),
        }

        workflow_tasks = [
            ('search_download', '📚 搜索并下载书籍'),
            ('convert_markdown', '📄 转换 EPUB 为 Markdown'),
            ('interpret_book', '✍️ 生成 Ezra 风格解读'),
            ('generate_images', '🎨 为文章配图'),
        ]

        # 根据停止点过滤任务
        if stop_at == 'search':
            workflow_tasks = []
        elif stop_at == 'download':
            workflow_tasks = workflow_tasks[:1]
        elif stop_at == 'convert':
            workflow_tasks = workflow_tasks[:2]
        elif stop_at == 'interpret':
            workflow_tasks = workflow_tasks[:3]

        for task_id, task_name in workflow_tasks:
            print(f"\n>>> {task_name}...")
            result = task_handlers[task_id](task_id, {})
            results[task_id] = result

            if result.get('status') == 'failed':
                print(f"❌ {result.get('message', '失败')}: {result.get('error', '')}")
                break

        return {
            'workflow': 'book-content-workflow',
            'book_title': book_title,
            'results': results,
            'state': self.state,
            'next_action': self._get_next_action(stop_at, results)
        }

    def run(self, book_title: str, theme: str = "colorful", stop_at: str = None,
            interactive: bool = False):
        """
        运行带可视化进度的工作流

        Args:
            book_title: 书名
            theme: 可视化主题 (colorful, minimal)
            stop_at: 在哪个阶段停止 ('search', 'download', 'convert', 'interpret', None=全部)
            interactive: 是否交互模式（每步确认）
        """
        self.state['book_title'] = book_title

        # 检查 visual-progress 是否可用
        if not _visual_progress_available:
            print("⚠️  visual-progress 未安装，使用简单文本模式")
            return self._run_simple(book_title, stop_at, interactive)

        # 初始化进度追踪器
        progress = VisualProgress(
            title=f"书籍解读: {book_title}",
            theme=theme
        )

        # 定义工作流任务
        workflow = [
            {
                'id': 'search_download',
                'name': f'📚 搜索并下载《{book_title}》',
                'total': 100
            },
            {
                'id': 'convert_markdown',
                'name': '📄 转换 EPUB 为 Markdown',
                'total': 100
            },
            {
                'id': 'interpret_book',
                'name': '✍️ 生成 Ezra 风格解读',
                'total': 100
            },
            {
                'id': 'generate_images',
                'name': '🎨 为文章配图',
                'total': 100
            },
        ]

        # 根据停止点调整工作流
        if stop_at == 'search':
            workflow = []  # 仅搜索，不执行任务
        elif stop_at == 'download':
            workflow = workflow[:1]
        elif stop_at == 'convert':
            workflow = workflow[:2]
        elif stop_at == 'interpret':
            workflow = workflow[:3]

        # 定义任务处理函数映射
        task_handlers = {
            'search_download': self.stage1_search_download,
            'convert_markdown': self.stage2_convert_markdown,
            'interpret_book': self.stage3_interpret_book,
            'generate_images': self.stage4_generate_images,
        }

        # 交互模式：每步前暂停
        if interactive and workflow:
            print(f"\n{'='*60}")
            print(f"交互模式：将要执行的步骤")
            print(f"{'='*60}")
            for i, task in enumerate(workflow, 1):
                print(f"  {i}. {task['name']}")
            print(f"\n按回车继续，或 Ctrl+C 取消...")
            try:
                input()
            except KeyboardInterrupt:
                print("\n已取消")
                return None

        # 执行工作流（自动显示可视化进度）
        results = progress.run_tasks(workflow, lambda tid, info: task_handlers[tid](tid, info))

        return {
            'workflow': 'book-content-workflow',
            'book_title': book_title,
            'results': results,
            'state': self.state,
            'next_action': self._get_next_action(stop_at, results)
        }

    def _get_next_action(self, stop_at: str, results: dict) -> dict:
        """获取下一步操作建议"""
        if not results:
            return {'action': 'search', 'message': '已搜索书籍，请选择是否下载'}

        # results 是字典 {task_id: result_dict}，获取最后一个结果
        result_values = list(results.values())
        last_result = result_values[-1] if result_values else {}
        status = last_result.get('status', '') if isinstance(last_result, dict) else ''

        if stop_at == 'search':
            return {'action': 'confirm_download', 'message': '请确认是否下载书籍'}
        elif stop_at == 'download':
            if status == 'completed':
                return {'action': 'confirm_convert', 'message': '请确认是否转换为 Markdown'}
        elif stop_at == 'convert':
            if status == 'completed':
                md_path = self.state.get('md_path', '')
                return {
                    'action': 'confirm_interpret',
                    'message': f'请确认是否生成解读 (Markdown: {md_path})'
                }
        elif stop_at == 'interpret':
            if status == 'completed':
                return {'action': 'confirm_images', 'message': '请确认是否生成配图'}

        return {'action': 'complete', 'message': '工作流完成'}


def run_workflow(book_title: str, base_path: str = None,
                 theme: str = "colorful", stop_at: str = None,
                 interactive: bool = False, book_index: int = None) -> Dict[str, Any]:
    """
    运行书籍内容生产工作流的便捷函数

    Args:
        book_title: 书名
        base_path: 工作流基础路径 (默认: Windows用D:/ObsidianWorkflows)
        theme: 可视化主题
        stop_at: 在哪个阶段停止
        interactive: 是否交互模式
        book_index: 指定下载的书籍索引（1-based），用于直接下载指定书籍

    Returns:
        工作流执行结果
    """
    workflow = BookWorkflowIntegrated(base_path=base_path)

    # 仅搜索模式：显示所有书籍并等待用户选择
    if stop_at == 'search':
        search_result = workflow.stage0_search_only(book_title)

        # 打印所有书籍
        books = workflow.state.get('search_results', [])
        if books:
            workflow.print_all_books(books)

            # 如果指定了书籍索引，直接下载
            if book_index is not None:
                print(f"\n📥 下载指定书籍: #{book_index}")
                download_result = workflow.download_book_by_index(book_index)
                return {
                    'workflow': 'book-content-workflow',
                    'mode': 'search_and_download',
                    'book_title': book_title,
                    'search_result': search_result,
                    'download_result': download_result,
                    'state': workflow.state
                }

        return {
            'workflow': 'book-content-workflow',
            'mode': 'search_only',
            'book_title': book_title,
            'search_result': search_result,
            'state': workflow.state
        }

    # 如果指定了书籍索引，使用下载指定书籍的方法
    if book_index is not None:
        # 先搜索
        search_result = workflow.stage0_search_only(book_title)
        if search_result.get('status') == 'success':
            # 下载指定的书
            download_result = workflow.download_book_by_index(book_index)
            if download_result.get('status') == 'completed':
                # 继续后续流程
                return workflow.run(book_title, theme=theme, stop_at=stop_at, interactive=interactive)
        return {
            'workflow': 'book-content-workflow',
            'mode': 'search_and_download',
            'book_title': book_title,
            'search_result': search_result,
            'state': workflow.state
        }

    return workflow.run(book_title, theme=theme, stop_at=stop_at, interactive=interactive)


# CLI 接口
def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='书籍内容生产工作流 - 集成实际技能调用'
    )
    parser.add_argument(
        'book_title',
        help='书名（如：深度学习）'
    )
    parser.add_argument(
        '--base-path',
        default=None,
        help='工作流基础路径 (默认: ~/ObsidianWorkflows)'
    )
    parser.add_argument(
        '--theme',
        choices=['colorful', 'minimal'],
        default='colorful',
        help='可视化主题 (默认: colorful)'
    )
    parser.add_argument(
        '--stop-at',
        choices=['search', 'download', 'convert', 'interpret'],
        help='在指定阶段停止 (search=仅搜索, download=搜索+下载, convert=搜索+下载+转换, interpret=全部)'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='交互模式：每步执行前询问用户确认'
    )
    parser.add_argument(
        '--book-index',
        type=int,
        help='指定下载的书籍索引（1-based），从搜索结果中选择第几本'
    )

    args = parser.parse_args()

    # 运行工作流
    results = run_workflow(
        book_title=args.book_title,
        base_path=args.base_path,
        theme=args.theme,
        stop_at=args.stop_at,
        interactive=args.interactive,
        book_index=args.book_index
    )

    print(f"\n{'='*60}")
    print(f"工作流完成!")
    print(f"{'='*60}")
    print(f"书名: {results['book_title']}")

    # 显示结果摘要
    results_list = results.get('results', [])
    if isinstance(results_list, dict):
        # 如果返回的是字典，转换为列表
        results_list = [{'id': k, **v} if isinstance(v, dict) else {'id': k, 'status': v}
                        for k, v in results_list.items()]

    for result in results_list:
        if isinstance(result, dict):
            status = result.get("status", "unknown")
            status_icon = "✅" if status in ["completed", "pending_claude"] else "❌"
            message = result.get('message', result.get('error', 'Unknown'))
            print(f"{status_icon} {message}")
        else:
            print(f"  • {result}")

    # 如果有 pending_claude 状态，提示下一步
    pending_steps = [r for r in results_list if isinstance(r, dict) and r.get('status') == 'pending_claude']
    if pending_steps:
        print(f"\n{'='*60}")
        print(f"⚠️  以下步骤需要在 Claude Code 中继续:")
        print(f"{'='*60}")
        for step in pending_steps:
            instruction = step.get('instruction', '')
            if instruction:
                print(f"  • {instruction}")

    return 0


if __name__ == '__main__':
    # 演示模式
    if len(sys.argv) == 1:
        print("=== 书籍内容生产工作流 - 集成模式 ===\n")
        print("提示: 使用 --stop-at 参数可以控制执行阶段")
        print("  --stop-at search     : 仅搜索（显示所有找到的书籍）")
        print("  --stop-at download   : 搜索并下载第1本（或用 --book-index 指定）")
        print("  --stop-at convert    : 搜索、下载并转换")
        print("  --stop-at interpret  : 全部流程（解读和配图需在 Claude Code 中）")
        print("\n书籍选择:")
        print("  --book-index N       : 指定下载第几本书（配合 --stop-at search 使用）")
        print("\n交互模式:")
        print("  --interactive       : 每步执行前询问确认")
        print("\n示例:")
        print("  # 搜索并显示所有书籍")
        print("  python enhanced_workflow.py \"python\" --stop-at search")
        print("")
        print("  # 下载第2本书")
        print("  python enhanced_workflow.py \"python\" --stop-at search --book-index 2")
        print("")
        print("  # 搜索、下载、转换")
        print("  python enhanced_workflow.py \"深度学习\" --stop-at convert --interactive\n")
        sys.exit(0)
    else:
        sys.exit(main())
