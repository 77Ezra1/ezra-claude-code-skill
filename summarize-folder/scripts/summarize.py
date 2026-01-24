#!/usr/bin/env python3
"""
Summarize Folder with Visual Progress
目录文件遍历和内容总结 - 带可视化界面

支持文件格式:
- Word (.docx) - 使用 pandoc
- PDF (.pdf) - 使用 pdfplumber/pdftotext
- Excel (.xlsx, .xls, .csv) - 使用 pandas
- 文本 (.txt, .md) - 直接读取
- PowerPoint (.pptx) - 使用 pandoc
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

# 添加 visual-progress 框架路径
SCRIPT_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPT_DIR.parent
VISUAL_PROGRESS_DIR = SKILLS_DIR / "visual-progress"
sys.path.insert(0, str(VISUAL_PROGRESS_DIR))

try:
    from core.visual_progress import VisualProgress, FileProgress, Theme
except ImportError:
    # 降级到无界面模式
    VisualProgress = None
    FileProgress = None
    Theme = None
    print("⚠️  警告: visual-progress 框架未找到，使用无界面模式")


@dataclass
class FileSummary:
    """文件摘要"""
    path: str
    name: str
    ext: str
    size: int
    content: str = ""
    error: str = ""
    sheets: List[str] = field(default_factory=list)


@dataclass
class DirectorySummary:
    """目录摘要"""
    path: str
    total_files: int = 0
    total_size: int = 0
    files_by_type: Dict[str, List[FileSummary]] = field(default_factory=dict)
    content_summary: str = ""


class FileExtractor:
    """文件内容提取器"""

    @staticmethod
    def get_file_size(size_bytes: int) -> str:
        """获取可读的文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    @staticmethod
    def extract_text(file_path: str) -> str:
        """提取文本文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if len(content) > 5000:
                content = content[:5000] + "\n\n... (内容过长，已截断)"
            return content
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
                if len(content) > 5000:
                    content = content[:5000] + "\n\n... (内容过长，已截断)"
                return content
            except Exception as e:
                return f"[编码错误: {str(e)}]"

    @staticmethod
    def extract_docx(file_path: str) -> str:
        """提取 Word 文档内容"""
        try:
            result = subprocess.run(
                ['pandoc', '-f', 'docx', '-t', 'markdown', file_path],
                capture_output=True, text=True, timeout=30
            )
            content = result.stdout
            if len(content) > 10000:
                content = content[:10000] + "\n\n... (内容过长，已截断)"
            return content
        except FileNotFoundError:
            return "[错误: 需要安装 pandoc]"
        except subprocess.TimeoutExpired:
            return "[错误: 文档处理超时]"
        except Exception as e:
            return f"[错误: {str(e)}]"

    @staticmethod
    def extract_pdf(file_path: str) -> str:
        """提取 PDF 内容"""
        # 先尝试 pdftotext
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', file_path, '-'],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout:
                content = result.stdout
                if len(content) > 10000:
                    content = content[:10000] + "\n\n... (内容过长，已截断)"
                return content
        except FileNotFoundError:
            pass
        except subprocess.TimeoutExpired:
            return "[错误: PDF 处理超时]"

        # 降级到 pdfplumber
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages[:20]:  # 限制页数
                    text += page.extract_text() + "\n"
                if len(text) > 10000:
                    text = text[:10000] + "\n\n... (内容过长，已截断)"
                return text
        except ImportError:
            return "[错误: 需要安装 pdftotext 或 pdfplumber]"
        except Exception as e:
            return f"[错误: {str(e)}]"

    @staticmethod
    def extract_xlsx(file_path: str) -> Dict[str, str]:
        """提取 Excel 表格内容"""
        try:
            import pandas as pd
            result = {"sheets": [], "content": ""}

            excel_file = pd.ExcelFile(file_path)
            result["sheets"] = excel_file.sheet_names

            content = f"文件: {Path(file_path).name}\n"
            content += f"Sheet 列表: {excel_file.sheet_names}\n\n"

            for sheet_name in excel_file.sheet_names[:5]:  # 限制 sheet 数量
                df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=50)
                content += f"--- Sheet: {sheet_name} ---\n"
                content += f"形状: {df.shape}\n"
                content += f"列名: {list(df.columns)}\n\n"
                content += df.head(10).to_string(max_cols=10) + "\n\n"

            if len(content) > 15000:
                content = content[:15000] + "\n\n... (内容过长，已截断)"

            result["content"] = content
            return result
        except ImportError:
            return {"sheets": [], "content": "[错误: 需要安装 pandas 和 openpyxl]"}
        except Exception as e:
            return {"sheets": [], "content": f"[错误: {str(e)}]"}

    @staticmethod
    def extract_csv(file_path: str) -> str:
        """提取 CSV 内容"""
        try:
            import pandas as pd
            df = pd.read_csv(file_path, nrows=100)
            content = f"文件: {Path(file_path).name}\n"
            content += f"形状: {df.shape}\n"
            content += f"列名: {list(df.columns)}\n\n"
            content += df.head(50).to_string(max_cols=20)
            return content
        except ImportError:
            return "[错误: 需要安装 pandas]"
        except Exception as e:
            return f"[错误: {str(e)}]"

    @staticmethod
    def extract_pptx(file_path: str) -> str:
        """提取 PowerPoint 内容"""
        try:
            result = subprocess.run(
                ['pandoc', '-f', 'pptx', '-t', 'markdown', file_path],
                capture_output=True, text=True, timeout=30
            )
            content = result.stdout
            if len(content) > 10000:
                content = content[:10000] + "\n\n... (内容过长，已截断)"
            return content
        except FileNotFoundError:
            return "[错误: 需要安装 pandoc]"
        except Exception as e:
            return f"[错误: {str(e)}]"

    @classmethod
    def extract(cls, file_path: str) -> FileSummary:
        """根据文件类型提取内容"""
        path = Path(file_path)
        ext = path.suffix.lower()
        size = path.stat().st_size

        summary = FileSummary(
            path=str(path),
            name=path.name,
            ext=ext,
            size=size
        )

        try:
            if ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml']:
                summary.content = cls.extract_text(file_path)
            elif ext == '.docx':
                summary.content = cls.extract_docx(file_path)
            elif ext == '.pdf':
                summary.content = cls.extract_pdf(file_path)
            elif ext in ['.xlsx', '.xls']:
                result = cls.extract_xlsx(file_path)
                summary.sheets = result.get('sheets', [])
                summary.content = result.get('content', '')
            elif ext == '.csv':
                summary.content = cls.extract_csv(file_path)
            elif ext == '.pptx':
                summary.content = cls.extract_pptx(file_path)
            else:
                summary.content = f"[不支持的文件类型: {ext}]"
        except Exception as e:
            summary.error = str(e)
            summary.content = f"[提取失败: {str(e)}]"

        return summary


class DirectoryScanner:
    """目录扫描器"""

    SUPPORTED_EXTS = {
        '.docx', '.pdf', '.xlsx', '.xls', '.csv', '.txt',
        '.md', '.pptx', '.py', '.js', '.html', '.css',
        '.json', '.xml', '.yaml', '.yml'
    }

    @classmethod
    def scan(cls, directory: str, recursive: bool = False) -> List[Path]:
        """扫描目录获取所有支持的文件"""
        path = Path(directory)
        if not path.exists():
            raise ValueError(f"目录不存在: {directory}")

        if not path.is_dir():
            raise ValueError(f"路径不是目录: {directory}")

        files = []
        if recursive:
            for ext in cls.SUPPORTED_EXTS:
                files.extend(path.rglob(f'*{ext}'))
        else:
            for ext in cls.SUPPORTED_EXTS:
                files.extend(path.glob(f'*{ext}'))

        return sorted(files, key=lambda p: p.name)

    @classmethod
    def get_stats(cls, files: List[Path]) -> Dict[str, Any]:
        """获取文件统计信息"""
        by_type = defaultdict(list)
        total_size = 0

        for file in files:
            ext = file.suffix.lower()
            by_type[ext].append(file)
            total_size += file.stat().st_size

        return {
            'total_files': len(files),
            'total_size': total_size,
            'by_type': {k: len(v) for k, v in by_type.items()},
            'size_by_type': {
                k: sum(f.stat().st_size for f in v)
                for k, v in by_type.items()
            }
        }


class SummarizeFolderVisual:
    """目录总结 - 带可视化界面"""

    def __init__(self, theme: str = "colorful"):
        self.theme = Theme.COLORFUL if theme == "colorful" else Theme.MINIMAL
        self.title = "目录文件分析"
        self.summary: Optional[DirectorySummary] = None

    def scan_directory(self, directory: str, recursive: bool = False) -> Dict[str, Any]:
        """步骤1: 扫描目录"""
        files = DirectoryScanner.scan(directory, recursive)
        stats = DirectoryScanner.get_stats(files)

        return {
            'files': [str(f) for f in files],
            'stats': stats
        }

    def extract_contents(self, files: List[str]) -> Dict[str, FileSummary]:
        """步骤2: 提取文件内容"""
        results = {}
        for file_path in files:
            summary = FileExtractor.extract(file_path)
            results[file_path] = summary
        return results

    def generate_report(self, scan_result: Dict, contents: Dict[str, FileSummary]) -> str:
        """步骤3: 生成报告"""
        stats = scan_result['stats']

        report = ["# 📁 目录总结报告\n"]
        report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append("---\n")

        # 目录概览
        report.append("## 📊 目录概览\n")
        report.append(f"- **文件总数**: {stats['total_files']} 个\n")
        report.append(f"- **总大小**: {FileExtractor.get_file_size(stats['total_size'])}\n")
        report.append("\n")

        # 文件类型分布
        report.append("## 📋 文件类型分布\n")
        report.append("| 类型 | 数量 | 大小 |\n")
        report.append("|------|------|------|\n")

        for ext, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
            size = FileExtractor.get_file_size(stats['size_by_type'].get(ext, 0))
            ext_name = ext if ext else '无扩展名'
            report.append(f"| {ext_name} | {count} | {size} |\n")
        report.append("\n")

        # 文件列表和内容摘要
        report.append("## 📄 文件列表及内容摘要\n\n")

        for i, file_path in enumerate(scan_result['files'][:50], 1):  # 限制显示数量
            summary = contents.get(file_path)
            if not summary:
                continue

            report.append(f"### {i}. {summary.name}\n")
            report.append(f"**路径**: `{summary.path}`\n")
            report.append(f"**大小**: {FileExtractor.get_file_size(summary.size)}\n")
            report.append(f"**类型**: {summary.ext}\n")

            if summary.error:
                report.append(f"**⚠️ 错误**: {summary.error}\n")
            else:
                report.append("**内容摘要**:\n")
                content_lines = summary.content.strip().split('\n')[:20]  # 限制行数
                for line in content_lines:
                    report.append(f"    {line}\n")
                if len(summary.content.strip().split('\n')) > 20:
                    report.append("    ... (更多内容已省略)\n")

            report.append("\n---\n\n")

        # 整体分析
        report.append("## 🔍 整体分析\n\n")
        report.append("### 主要主题/内容\n")
        report.append("[AI 基于文件内容分析的主题...]\n\n")

        report.append("### 关键信息提取\n")
        report.append("- [关键点1]\n")
        report.append("- [关键点2]\n")
        report.append("- [关键点3]\n\n")

        report.append("---\n")
        report.append("*本报告由 Claude Code summarize-folder skill 自动生成*\n")

        return ''.join(report)

    def run(self, directory: str, recursive: bool = False,
            output_file: str = None) -> str:
        """执行完整的目录分析流程"""
        if VisualProgress is None:
            return self._run_without_progress(directory, recursive, output_file)

        # 创建可视化进度
        progress = VisualProgress(
            title=self.title,
            theme=self.theme
        )

        # 定义工作流
        def scan_step(task_id: str, info: Dict) -> Dict:
            time.sleep(0.3)  # 模拟处理
            return self.scan_directory(directory, recursive)

        def extract_step(task_id: str, info: Dict) -> Dict:
            scan_result = info.get('scan_result', {})
            files = scan_result.get('files', [])[:50]  # 限制处理数量
            return self.extract_contents(files)

        def report_step(task_id: str, info: Dict) -> Dict:
            scan_result = info.get('scan_result', {})
            contents = info.get('contents', {})
            report = self.generate_report(scan_result, contents)
            return {'report': report}

        # 工作流定义
        workflow = [
            {'id': 'scan', 'name': '📁 扫描目录文件...', 'total': 100},
            {'id': 'extract', 'name': '📄 提取文件内容...', 'total': 100},
            {'id': 'report', 'name': '📊 生成分析报告...', 'total': 100},
        ]

        # 执行工作流（手动实现以传递上下文）
        progress.renderer.render_header(progress.title)

        # 步骤 1: 扫描
        print(f"\n▶ {workflow[0]['name']}")
        scan_result = scan_step('scan', {})
        progress.renderer.render_progress_bar(1, 1, prefix="✓ 扫描完成")
        print(f"  发现 {scan_result['stats']['total_files']} 个文件")

        # 步骤 2: 提取
        print(f"\n▶ {workflow[1]['name']}")
        contents = {}
        files = scan_result['files'][:50]
        for i, file_path in enumerate(files):
            contents[file_path] = FileExtractor.extract(file_path)
            progress.renderer.render_progress_bar(
                i + 1, len(files),
                prefix=f"  处理: {Path(file_path).name[:30]}"
            )
        print(f"\n  ✓ 提取完成 {len(contents)} 个文件")

        # 步骤 3: 报告
        print(f"\n▶ {workflow[2]['name']}")
        report = self.generate_report(scan_result, contents)
        progress.renderer.render_progress_bar(1, 1, prefix="✓ 报告生成完成")

        # 保存报告
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n  ✓ 报告已保存: {output_file}")

        # 显示完成摘要
        progress.renderer.render_summary({
            '文件总数': scan_result['stats']['total_files'],
            '总大小': FileExtractor.get_file_size(scan_result['stats']['total_size']),
            '报告长度': f"{len(report)} 字符"
        })

        return report

    def _run_without_progress(self, directory: str, recursive: bool = False,
                             output_file: str = None) -> str:
        """无进度条模式"""
        print(f"正在分析目录: {directory}")

        scan_result = self.scan_directory(directory, recursive)
        print(f"发现 {scan_result['stats']['total_files']} 个文件")

        files = scan_result['files'][:50]
        contents = {}
        for file_path in files:
            contents[file_path] = FileExtractor.extract(file_path)
            print(f"  ✓ {Path(file_path).name}")

        report = self.generate_report(scan_result, contents)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存: {output_file}")

        return report


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='目录文件遍历和内容总结工具'
    )
    parser.add_argument('directory', help='要分析的目录路径')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='递归处理子目录')
    parser.add_argument('-o', '--output', help='输出报告文件路径')
    parser.add_argument('-t', '--theme', choices=['colorful', 'minimal'],
                       default='colorful', help='可视化主题')

    args = parser.parse_args()

    analyzer = SummarizeFolderVisual(theme=args.theme)
    report = analyzer.run(
        directory=args.directory,
        recursive=args.recursive,
        output_file=args.output
    )

    if not args.output:
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)


if __name__ == "__main__":
    main()
