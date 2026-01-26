---
name: visual-progress
description: Visual progress framework for Claude Code Skills. Provides beautiful terminal-based progress bars, task lists, batch processing, and file processing with multiple themes (colorful, minimal, dark, forest, ocean). Use when user requests: (1) Progress display, (2) Visual workflow tracking, (3) Batch processing with progress, (4) File processing with progress, (5) Terminal UI for long-running tasks 当用户提到「显示进度" / "进度显示" / "可视化进度、进度条" / "显示进度条" / "进度条显示、任务进度" / "显示任务进度" / "进度跟踪、show progress" / "display progress" / "progress bar、工作流" / "任务工作流" / "工作流跟踪、任务列表" / "任务列表显示" / "可视化任务、执行进度" / "执行跟踪" / "任务执行、workflow progress" / "task tracking" / "visual workflow、批处理" / "批量处理" / "批处理进度、批量任务" / "批量操作" / "批量执行、批处理显示" / "批量进度、batch processing" / "batch tasks" / "bulk processing、文件处理" / "文件处理进度" / "批量文件、遍历文件" / "文件扫描" / "文件统计、file processing" / "file batch" / "scan files」等关键词时触发。
user-invocable: true
---



# Visual Progress

Visual Progress is a terminal-based progress framework for Claude Code Skills that provides beautiful, themeable progress displays for long-running operations.

## Features

- **Multiple Themes**: Colorful, Minimal, Dark, Forest, Ocean
- **Progress Bars**: Beautiful ASCII progress bars with percentage
- **Task Lists**: Visual task status (pending, in-progress, completed)
- **Batch Processing**: Track progress when processing multiple items
- **File Processing**: Specialized support for file batch operations
- **Thread-Safe**: Safe for concurrent operations

## Installation

The framework is located in `core/visual_progress.py` and can be imported as a Python module.

## Usage

### Basic Progress

```python
from visual_progress.core import VisualProgress, Theme

progress = VisualProgress("My Task", theme=Theme.COLORFUL)
progress.add_task("task1", "Processing files", total=100)
progress.update_task("task1", 50)  # 50% complete
```

### Workflow with Tasks

```python
workflow = [
    {'id': 'scan', 'name': 'Scanning files...', 'total': 100},
    {'id': 'process', 'name': 'Processing...', 'total': 100},
    {'id': 'report', 'name': 'Generating report...', 'total': 100},
]

def execute_task(task_id, info):
    # Task implementation
    return {"status": "success"}

results = progress.run_tasks(workflow, execute_task)
```

### Batch Processing

```python
from visual_progress.core import BatchProgress

items = ["file1.txt", "file2.txt", "file3.txt"]
batch = BatchProgress("Processing Files", items, theme=Theme.OCEAN)

def process_item(item):
    # Process single item
    return f"Processed {item}"

results = batch.run_batch(process_item)
```

### File Processing

```python
from visual_progress.core import FileProgress

files = ["doc1.pdf", "doc2.pdf", "image.png"]
file_progress = FileProgress(files, title="File Processing")

# Get file type summary
summary = file_progress.get_summary()
# Returns: {'.pdf': 2, '.png': 1}
```

## Themes

| Theme | Description | Style |
|-------|-------------|-------|
| COLORFUL | Full color with emoji | Purple headers, green success |
| MINIMAL | No colors, ASCII only | Simple characters |
| DARK | Dark theme colors | Cyan headers, dim colors |
| FOREST | Nature-inspired | Deep green with tree icons |
| OCEAN | Ocean-inspired | Deep blue with wave icons |

## Integration with Skills

To integrate visual progress into a skill:

1. Import the framework: `from visual_progress.core import VisualProgress`
2. Create a progress instance with your task title
3. Define your workflow steps
4. Execute with `run_tasks()`

Example for a skill that processes documents:

```python
from visual_progress.core import VisualProgress, Theme

def process_documents(skill_context):
    progress = VisualProgress(
        "Document Processing",
        theme=Theme.COLORFUL
    )

    workflow = [
        {'id': 'scan', 'name': 'Scanning for documents...', 'total': 100},
        {'id': 'extract', 'name': 'Extracting content...', 'total': 100},
        {'id': 'analyze', 'name': 'Analyzing documents...', 'total': 100},
    ]

    def execute(task_id, info):
        if task_id == 'scan':
            return skill_context.scan_files()
        elif task_id == 'extract':
            return skill_context.extract_content()
        elif task_id == 'analyze':
            return skill_context.analyze_content()

    return progress.run_tasks(workflow, execute)
```

## API Reference

### VisualProgress

Main class for task progress management.

**Parameters:**
- `title` (str): Task title
- `theme` (Theme): Visual theme (default: COLORFUL)
- `show_details` (bool): Show detailed task list (default: True)

**Methods:**
- `add_task(task_id, name, total)`: Add a new task
- `update_task(task_id, completed)`: Update task progress
- `run_tasks(workflow, task_func)`: Execute a workflow
- `colorize(text, color_type)`: Add color to text

### BatchProgress

Extended class for batch processing.

**Parameters:**
- `title` (str): Batch title
- `items` (List[str]): Items to process
- `theme` (Theme): Visual theme

**Methods:**
- `run_batch(process_func, show_progress)`: Process items in batch

### FileProgress

Specialized class for file processing.

**Parameters:**
- `files` (List[str]): File paths to process
- `title` (str): Processing title

**Methods:**
- `get_summary()`: Get file type statistics
- `run_batch(process_func)`: Process files with progress

## Examples

### Example 1: Simple Progress Bar

```python
from visual_progress.core import VisualProgress, Theme

progress = VisualProgress("Download", Theme.OCEAN)

for i in range(101):
    progress.renderer.render_progress_bar(i, 100, prefix="Downloading")
    time.sleep(0.1)
```

### Example 2: Task List

```python
tasks = [
    Task("1", "Initialize", status="completed"),
    Task("2", "Process", status="running"),
    Task("3", "Finalize", status="pending"),
]

renderer = ProgressRenderer(Theme.COLORFUL)
renderer.render_task_list(tasks, current_index=1)
```

### Example 3: Complete Workflow

```python
from visual_progress.core import VisualProgress, Theme

def my_skill_function():
    progress = VisualProgress("My Skill Workflow", Theme.FOREST)

    workflow = [
        {'id': 'step1', 'name': 'Validating input...', 'total': 100},
        {'id': 'step2', 'name': 'Processing data...', 'total': 100},
        {'id': 'step3', 'name': 'Generating output...', 'total': 100},
    ]

    def step_executor(task_id, info):
        # Implement each step
        time.sleep(1)  # Simulate work
        return {"task": task_id, "status": "done"}

    results = progress.run_tasks(workflow, step_executor)
    return results
```

## License

MIT
