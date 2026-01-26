---
name: visual-interface-generator
description: 为 Skill 自动生成可视化进度界面。自然语言触发：'为这个Skill创建可视化界面' '为xxx添加进度显示' '生成可视化工作流' '为Skill添加进度条'。自动分析目标Skill的工作流程，生成专属的可视化界面代码并集成visual-progress框架。
user-invocable: false
---


# Visual Interface Generator

## Overview

这是一个**元技能**（Meta-Skill），用于为其他 Skill 自动生成可视化进度界面。

它能：
1. 📖 分析目标 Skill 的 SKILL.md 文件
2. 🔍 理解工作流程和处理步骤
3. 📊 生成专属的可视化进度代码
4. 🔧 自动集成 visual-progress 框架
5. ✅ 输出可直接使用的增强版 Skill

## 自然语言触发

当用户说以下内容时自动触发：

**中文触发词：**
- "为这个 Skill 创建可视化界面"
- "为 xxx 添加进度显示"
- "为 Skill 生成可视化工作流"
- "为这个 Skill 添加进度条"
- "为 xxx 创建可视化版本"
- "生成带进度的 Skill 代码"

**英文触发词：**
- "Create visual interface for this skill"
- "Add progress display to xxx"
- "Generate visual workflow for this skill"
- "Add progress bar to this skill"

## 使用方式

### 方式 1: 分析现有 Skill

```
用户: 为 auto-redbook-skills 创建可视化界面

系统会:
1. 读取 auto-redbook-skills/SKILL.md
2. 分析工作流程（撰写→生成图片→发布）
3. 生成带进度显示的代码
4. 输出增强版代码
```

### 方式 2: 为新 Skill 添加可视化

```
用户: 为 my-new-skill 添加进度显示

系统会:
1. 检查是否存在 SKILL.md
2. 分析处理步骤
3. 生成可视化代码模板
4. 提供集成说明
```

### 方式 3: 从描述生成

```
用户: 我想创建一个数据处理 Skill，帮我生成带可视化界面的代码

系统会:
1. 根据描述生成 Skill 结构
2. 设计工作流步骤
3. 生成完整的可视化代码
```

## 自动分析能力

### 能识别的工作流程模式

| 模式 | 识别方式 | 生成的进度显示 |
|------|---------|---------------|
| **多步骤流程** | "第一步...第二步..." | 📥→🔄→📤 进度条 |
| **批处理** | "处理多个/所有/这些文件" | 文件列表进度 |
| **数据管道** | "加载→清洗→转换→输出" | 管道阶段进度 |
| **API 请求** | "请求/调用/获取" | 请求进度 |
| **文件操作** | "读取/写入/转换" | 操作进度 |

### 能提取的信息

- ✅ Skill 名称和描述
- ✅ 工作流程步骤
- ✅ 输入/输出格式
- ✅ 处理逻辑
- ✅ 可以显示进度的节点

## 输出内容

生成的代码包含：

1. **带进度的主处理函数**
   - 自动集成 visual-progress
   - 匹配原始 Skill 的逻辑

2. **进度显示配置**
   - 主题选择
   - 任务名称
   - 进度描述

3. **集成说明**
   - 如何替换原始代码
   - 如何测试
   - 如何自定义

## 示例输出

### 输入
```
用户: 为 auto-redbook-skills 创建可视化界面
```

### 输出
```python
#!/usr/bin/env python3
"""Auto-Redbook-Skills with Visual Progress"""

import sys
sys.path.insert(0, '/Users/ezra/.claude/skills/visual-progress')
from core.visual_progress import VisualProgress

def create_xiaohongshu_note(topic, materials):
    """
    创建小红书笔记（带可视化进度）

    工作流程:
    1. 📝 撰写笔记内容
    2. 🎨 生成图片卡片
    3. 📤 发布笔记
    """

    progress = VisualProgress(
        title="小红书笔记创作",
        theme="colorful"
    )

    # 步骤 1: 撰写内容
    def write_content(task_id, info):
        # 原始的撰写逻辑
        title = generate_title(topic)
        content = generate_content(topic, materials)
        return {'title': title, 'content': content}

    # 步骤 2: 生成图片
    def generate_images(task_id, info):
        # 原始的图片生成逻辑
        cover = create_cover(info['title'])
        cards = create_content_cards(info['content'])
        return {'cover': cover, 'cards': cards}

    # 步骤 3: 发布
    def publish_note(task_id, info):
        # 原始的发布逻辑
        result = upload_to_xiaohongshu(info)
        return {'published': True, 'url': result.url}

    # 定义工作流
    workflow = [
        {'id': 'write', 'name': '📝 撰写笔记内容...', 'total': 100},
        {'id': 'image', 'name': '🎨 生成图片卡片...', 'total': 100},
        {'id': 'publish', 'name': '📤 发布到小红书...', 'total': 100},
    ]

    # 执行工作流（自动显示进度）
    results = progress.run_tasks(workflow, lambda tid, info: {
        'write': write_content,
        'image': generate_images,
        'publish': publish_note,
    }[tid](tid, info))

    return results

# 使用示例
if __name__ == '__main__':
    create_xiaohongshu_note(
        topic="推荐5个提升效率的工具",
        materials={"tools": [...]}
    )
```

## 技术实现

### 分析器功能

```python
class SkillAnalyzer:
    """分析 Skill 文档"""

    def analyze_workflow(self, skill_markdown: str) -> dict:
        """从 SKILL.md 提取工作流程"""
        # 识别步骤标记
        # 提取处理逻辑
        # 生成进度节点

    def generate_progress_code(self, analysis: dict) -> str:
        """生成带进度的代码"""
        # 创建 VisualProgress 实例
        # 定义任务函数
        # 创建工作流数组

    def integrate_code(self, original_code: str, progress_code: str) -> str:
        """集成到原始代码"""
        # 找到集成点
        # 插入进度代码
        # 保持原始逻辑
```

## 支持的工作流类型

### 1. 顺序工作流
```
步骤1 → 步骤2 → 步骤3
↓
生成顺序进度条
```

### 2. 批处理工作流
```
文件1 → 完成
文件2 → 完成
文件3 → 完成
↓
生成文件列表进度
```

### 3. 并行工作流
```
任务1 ─┐
任务2 ─┼→ 完成
任务3 ─┘
↓
生成并行进度
```

### 4. 条件工作流
```
判断 → 分支A → 完成
    → 分支B → 完成
↓
生成条件进度
```

## 集成模式

### 模式 1: 包装器模式
```python
# 原函数不变，外部添加进度
@add_progress("My Task")
def original_function():
    # 原始逻辑
    pass
```

### 模式 2: 注入模式
```python
# 在原函数中注入进度代码
def enhanced_function():
    progress = VisualProgress(...)
    # 原始逻辑 + 进度更新
```

### 模式 3: 重写模式
```python
# 完全重写，深度集成进度
def new_function():
    progress = VisualProgress(...)
    # 重新组织代码以支持进度
```

## 自定义选项

生成时可以指定：

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `theme` | 可视化主题 | colorful |
| `show_details` | 显示详细信息 | True |
| `batch_size` | 批处理大小 | 自动 |
| `update_interval` | 更新频率 | 0.1秒 |

## 使用示例

### 示例 1: 为现有 Skill 添加可视化
```
用户: 为 auto-redbook-skills 添加可视化界面

生成器:
1. ✅ 读取 ~/.claude/skills/auto-redbook-skills/SKILL.md
2. ✅ 分析工作流: 撰写 → 生成图片 → 发布
3. ✅ 生成带进度的代码
4. ✅ 输出: auto-redbook-skills-with-progress.py
```

### 示例 2: 为文档分析 Skill 添加可视化
```
用户: 为 document-analyzer-workflow 生成可视化版本

生成器:
1. ✅ 分析文档处理流程
2. ✅ 识别: 检测 → 提取 → 分析
3. ✅ 生成进度代码
4. ✅ 输出增强版代码
```

### 示例 3: 从描述生成新 Skill
```
用户: 创建一个批量下载图片的 Skill，带可视化

生成器:
1. ✅ 理解需求
2. ✅ 设计工作流: 获取URLs → 下载 → 保存
3. ✅ 生成完整代码
4. ✅ 包含进度显示
```

## 输出格式

生成的代码文件结构：

```
skill-name-with-progress/
├── enhanced_skill.py      # 带进度的主代码
├── README.md              # 使用说明
├── test_example.py        # 测试示例
└── integration_guide.md   # 集成指南
```

## 限制和注意事项

1. **需要 SKILL.md 文件** - 用于分析工作流
2. **保持原始逻辑** - 只添加进度，不改变功能
3. **可逆集成** - 可以移除进度代码恢复原版
4. **兼容性** - 确保与原 Skill 的依赖兼容

## 最佳实践

1. **明确工作流** - 在 SKILL.md 中清晰描述步骤
2. **合理分步** - 将长任务分解为可显示进度的步骤
3. **选择合适主题** - 根据 Skill 特点选择可视化风格
4. **测试验证** - 生成后测试确保功能正常
