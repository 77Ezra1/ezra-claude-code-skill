#!/usr/bin/env python3
"""
Visual Progress Framework
为 Claude Code Skills 提供可视化进度显示
"""

import sys
import time
import threading
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Theme(Enum):
    """可视化主题"""
    COLORFUL = "colorful"      # 彩色主题
    MINIMAL = "minimal"        # 极简主题
    DARK = "dark"              # 深色主题
    FOREST = "forest"          # 森林主题
    OCEAN = "ocean"            # 海洋主题


@dataclass
class Task:
    """任务定义"""
    id: str
    name: str
    total: int = 100
    completed: int = 0
    status: str = "pending"


class ProgressRenderer:
    """进度渲染器"""

    # 主题配色
    THEMES = {
        Theme.COLORFUL: {
            "header": "\033[95m",     # 紫色
            "success": "\033[92m",    # 绿色
            "warning": "\033[93m",    # 黄色
            "info": "\033[94m",       # 蓝色
            "reset": "\033[0m",
            "bar_fill": "█",
            "bar_empty": "░",
        },
        Theme.MINIMAL: {
            "header": "",
            "success": "",
            "warning": "",
            "info": "",
            "reset": "",
            "bar_fill": "=",
            "bar_empty": "-",
        },
        Theme.DARK: {
            "header": "\033[36m",     # 青色
            "success": "\033[32m",    # 绿色
            "warning": "\033[33m",    # 黄色
            "info": "\033[37m",       # 白色
            "reset": "\033[0m",
            "bar_fill": "▓",
            "bar_empty": "░",
        },
        Theme.FOREST: {
            "header": "\033[38;5;22m",    # 深绿
            "success": "\033[38;5;34m",   # 绿色
            "warning": "\033[38;5;214m",  # 橙色
            "info": "\033[38;5;28m",      # 蓝绿
            "reset": "\033[0m",
            "bar_fill": "🌲",
            "bar_empty": "·",
        },
        Theme.OCEAN: {
            "header": "\033[38;5;27m",    # 深蓝
            "success": "\033[38;5;39m",   # 浅蓝
            "warning": "\033[38;5;222m",  # 金色
            "info": "\033[38;5;45m",      # 天蓝
            "reset": "\033[0m",
            "bar_fill": "🌊",
            "bar_empty": "·",
        },
    }

    def __init__(self, theme: Theme = Theme.COLORFUL):
        self.theme = Theme(theme)
        self.colors = self.THEMES[self.theme]

    def colorize(self, text: str, color_type: str) -> str:
        """给文本添加颜色"""
        colors = self.colors
        return f"{colors.get(color_type, '')}{text}{colors['reset']}"

    def render_header(self, title: str):
        """渲染标题"""
        width = 60
        border = self.colors["header"] + "═" * width + self.colors["reset"]
        padding = (width - len(title) - 2) // 2
        line = self.colors["header"] + "═" + " " * padding + title + " " * (width - padding - len(title) - 2) + "═" + self.colors["reset"]
        print(f"\n{border}")
        print(f"{line}")
        print(f"{border}\n")

    def render_progress_bar(self, current: int, total: int, width: int = 40, prefix: str = ""):
        """渲染进度条"""
        if total == 0:
            progress = 1.0
        else:
            progress = min(current / total, 1.0)

        filled = int(width * progress)
        bar = self.colors["bar_fill"] * filled + self.colors["bar_empty"] * (width - filled)
        percentage = int(progress * 100)

        info = f"{prefix} [{bar}] {percentage}%"
        print(f"\r{info}", end="", flush=True)

        if progress >= 1.0:
            print()  # 换行

    def render_task_list(self, tasks: List[Task], current_index: int):
        """渲染任务列表"""
        for i, task in enumerate(tasks):
            if i < current_index:
                # 已完成
                icon = self.colorize("✓", "success")
                status = self.colorize("完成", "success")
            elif i == current_index:
                # 进行中
                icon = self.colorize("⟳", "warning")
                status = self.colorize("进行中", "warning")
            else:
                # 待处理
                icon = "○"
                status = "等待中"

            print(f"  {icon} {task.name} [{status}]")

    def render_summary(self, results: Dict[str, Any]):
        """渲染完成摘要"""
        width = 60
        border = self.colors["success"] + "═" * width + self.colors["reset"]
        print(f"\n{border}")
        print(self.colorize("           🎉 所有任务完成！", "success"))
        print(f"{border}\n")

        # 显示结果摘要
        for key, value in results.items():
            if isinstance(value, dict):
                print(f"  • {key}:")
                for k, v in value.items():
                    print(f"    - {k}: {v}")
            else:
                print(f"  • {key}: {value}")


class VisualProgress:
    """可视化进度管理器"""

    def __init__(self, title: str = "任务处理", theme: Theme = Theme.COLORFUL,
                 show_details: bool = True):
        """
        初始化可视化进度

        Args:
            title: 任务标题
            theme: 可视化主题
            show_details: 是否显示详细信息
        """
        self.title = title
        self.renderer = ProgressRenderer(theme)
        self.show_details = show_details
        self.tasks: List[Task] = []
        self.results: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def add_task(self, task_id: str, name: str, total: int = 100):
        """添加任务"""
        with self._lock:
            self.tasks.append(Task(id=task_id, name=name, total=total))

    def update_task(self, task_id: str, completed: int):
        """更新任务进度"""
        with self._lock:
            for task in self.tasks:
                if task.id == task_id:
                    task.completed = min(completed, task.total)
                    break

    def run_task(self, task_id: str, name: str, total: int,
                 func: Callable, **kwargs) -> Any:
        """运行单个任务并显示进度"""
        self.add_task(task_id, name, total)

        def wrapper():
            result = func(**kwargs)
            self.update_task(task_id, total)
            return result

        return wrapper()

    def run_tasks(self, workflow: List[Dict[str, Any]],
                  task_func: Callable[[str, Dict], Any]) -> Dict[str, Any]:
        """
        运行工作流

        Args:
            workflow: 工作流定义，格式: [{'id': 'task1', 'name': '任务1', 'total': 100}, ...]
            task_func: 任务执行函数，接收 (task_id, info) 参数

        Returns:
            所有任务的执行结果
        """
        # 初始化任务
        self.tasks = [Task(**task) for task in workflow]
        self.results = {}

        # 显示标题
        self.renderer.render_header(self.title)

        # 显示任务列表
        if self.show_details:
            print(self.colorize("任务列表:", "info"))
            self.renderer.render_task_list(self.tasks, -1)
            print()

        # 执行任务
        for i, task_def in enumerate(workflow):
            task_id = task_def['id']
            task = self.tasks[i]

            # 更新任务状态
            task.status = "running"

            # 显示当前任务
            if self.show_details:
                print(self.colorize(f"\n▶ 执行: {task.name}", "warning"))

            # 执行任务（带进度模拟）
            result = self._execute_with_progress(task, task_func)
            self.results[task_id] = result

            task.status = "completed"
            task.completed = task.total

            # 更新任务列表显示
            if self.show_details:
                print(f"\r{self.renderer.colors['success']}✓{self.renderer.colors['reset']} {task.name} 完成")

        # 显示完成摘要
        if self.show_details:
            self.renderer.render_summary(self.results)

        return self.results

    def _execute_with_progress(self, task: Task,
                               task_func: Callable[[str, Dict], Any]) -> Any:
        """执行任务并显示进度"""
        try:
            result = task_func(task.id, {'total': task.total})
            return result
        except Exception as e:
            task.status = "failed"
            return {"error": str(e)}

    def colorize(self, text: str, color_type: str) -> str:
        """给文本添加颜色"""
        return self.renderer.colorize(text, color_type)

    def show_spinner(self, message: str = "处理中..."):
        """显示旋转加载动画"""
        import itertools
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        try:
            while True:
                print(f"\r{next(spinner)} {message}", end="", flush=True)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print()


class BatchProgress(VisualProgress):
    """批处理进度管理器"""

    def __init__(self, title: str = "批处理", items: List[str] = None,
                 theme: Theme = Theme.COLORFUL):
        super().__init__(title, theme)
        self.items = items or []
        self.processed = 0

    def run_batch(self, process_func: Callable[[str], Any],
                  show_progress: bool = True) -> List[Any]:
        """
        批量处理项目

        Args:
            process_func: 处理单个项目的函数
            show_progress: 是否显示进度

        Returns:
            处理结果列表
        """
        results = []
        total = len(self.items)

        self.renderer.render_header(f"{self.title} (共 {total} 项)")

        for i, item in enumerate(self.items):
            if show_progress:
                self.renderer.render_progress_bar(
                    i + 1, total,
                    prefix=f"处理: {item[:30]}"
                )

            try:
                result = process_func(item)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e), "item": item})

        if show_progress:
            print(f"\n{self.renderer.colorize('✓ 批处理完成', 'success')}")

        return results


class FileProgress(BatchProgress):
    """文件处理进度管理器"""

    def __init__(self, files: List[str], title: str = "文件处理"):
        super().__init__(title, files)
        self.files_by_type = self._group_by_type(files)

    def _group_by_type(self, files: List[str]) -> Dict[str, List[str]]:
        """按文件类型分组"""
        groups = {}
        for file in files:
            import os
            ext = os.path.splitext(file)[1].lower()
            if ext:
                groups.setdefault(ext, []).append(file)
            else:
                groups.setdefault("unknown", []).append(file)
        return groups

    def get_summary(self) -> Dict[str, int]:
        """获取文件类型统计"""
        return {k: len(v) for k, v in self.files_by_type.items()}


# 便捷函数
def create_progress(title: str, theme: Theme = Theme.COLORFUL) -> VisualProgress:
    """创建进度管理器"""
    return VisualProgress(title, theme)


def create_batch_progress(items: List[str], title: str = "批处理",
                         theme: Theme = Theme.COLORFUL) -> BatchProgress:
    """创建批处理进度管理器"""
    return BatchProgress(title, items, theme)


def create_file_progress(files: List[str], title: str = "文件处理") -> FileProgress:
    """创建文件处理进度管理器"""
    return FileProgress(files, title)


if __name__ == "__main__":
    # 测试示例
    progress = VisualProgress("测试任务", Theme.COLORFUL)

    def test_task(task_id: str, info: Dict) -> Dict:
        time.sleep(0.5)
        return {"status": "success", "data": f"Task {task_id} completed"}

    workflow = [
        {'id': 'task1', 'name': '📁 扫描目录文件...', 'total': 100},
        {'id': 'task2', 'name': '📄 提取文件内容...', 'total': 100},
        {'id': 'task3', 'name': '📊 生成分析报告...', 'total': 100},
    ]

    results = progress.run_tasks(workflow, test_task)
    print("\n最终结果:", results)
