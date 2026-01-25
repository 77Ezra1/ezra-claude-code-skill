---
name: book-content-workflow
description: "Obsidian书籍内容生产工作流 - 整合zlibrary、epub-to-markdown、book-interpreter、volcano-images四个技能，实现从搜索书籍到生成解读文章的完整流程。每步完成后使用 AskUserQuestion 询问用户是否继续。当用户说「帮我解读《书名》」、「完成《书名》的完整解读流程」、「生成《书名》的读书笔记」或「书籍解读工作流」时使用此技能。"
---

# 书籍内容生产工作流

## 触发时执行

当用户通过自然语言触发此 skill 时（如"帮我解读《深度学习》"），按以下**交互式步骤**执行：

### 阶段 0：搜索书籍

**执行**：调用搜索脚本
```bash
python "$HOME/.claude/skills/book-content-workflow/enhanced_workflow.py" "{书名}" --stop-at search
```

**显示结果**：展示**所有**找到的书籍列表（完整列表，不限制数量）

**交互式选择**：
由于 AskUserQuestion 最多支持 4 个选项，对于搜索结果的处理方式：
- 方式 1：在 CLI 中直接运行 `--stop-at search`，查看所有书籍后使用 `--book-index N` 指定下载
- 方式 2：在 Claude Code 中使用文本输入让用户输入书籍编号

**下载指定书籍**：
```bash
# 下载第 2 本书
python "$HOME/.claude/skills/book-content-workflow/enhanced_workflow.py" "{书名}" --stop-at search --book-index 2
```

---

### 阶段 1：下载书籍

**用户选择**：选择某本书后

**执行**：下载 EPUB
```bash
python "$HOME/.claude/skills/book-content-workflow/enhanced_workflow.py" "{书名}" --stop-at download
```

**显示结果**：下载完成信息

**使用 AskUserQuestion 询问**：
```python
AskUserQuestion(
    questions=[{
        "question": f"✅ 已下载: {filename} ({size_mb} MB)\n下一步想做什么？",
        "header": "下一步",
        "options": [
            {"label": "转换为 Markdown", "description": "将 EPUB 转换为 Markdown 格式"},
            {"label": "先放着，我自己读", "description": "保持 EPUB 格式"}
        ],
        "multiSelect": False
    }])
```

---

### 阶段 2：转换为 Markdown

**用户选择**：选择"转换为 Markdown"

**执行**：转换 EPUB
```bash
python "$HOME/.claude/skills/book-content-workflow/enhanced_workflow.py" "{书名}" --stop-at convert
```

**显示结果**：转换完成信息（字数、图片数等）

**使用 AskUserQuestion 询问**：
```python
AskUserQuestion(
    questions=[{
        "question": f"✅ 已转换: {md_filename}\n📊 约 {word_count} 字，{images_count} 张图片\n\n下一步想做什么？",
        "header": "下一步",
        "options": [
            {"label": "生成 Ezra 风格解读", "description": "将书籍内容转化为通俗易懂的解读文章"},
            {"label": "我自己总结", "description": "我自己阅读 Markdown 文件"},
            {"label": "仅保存 Markdown", "description": "保存转换结果，结束流程"}
        ],
        "multiSelect": False
    }])
```

---

### 阶段 3：生成解读

**用户选择**：选择"生成 Ezra 风格解读"

**执行**：调用 book-interpreter skill
```bash
# 在 Claude Code 中执行，使用 /book-interpreter 或自然语言
"请使用 book-interpreter 解读: {md_path}"
```

**显示结果**：解读完成信息

**使用 AskUserQuestion 询问**：
```python
AskUserQuestion(
    questions=[{
        "question": f"✅ 解读完成: {article_filename}\n📊 约 {word_count} 字，{terms_count} 处术语解释\n\n下一步想做什么？",
        "header": "下一步",
        "options": [
            {"label": "为文章配图", "description": "使用火山引擎生成配图"},
            {"label": "直接发布草稿", "description": "不配图，直接保存到 published/"},
            {"label": "仅保存解读", "description": "保存解读草稿，结束流程"}
        ],
        "multiSelect": False
    }])
```

---

### 阶段 4：生成配图

**用户选择**：选择"为文章配图"

**执行**：调用 volcano-images skill
```bash
# 在 Claude Code 中执行
"请使用 volcano-images 为文章配图: {article_path}"
```

**完成提示**：
```
✅ 配图完成
📁 文章已发布到: published/
🖼️ 生成配图: {count} 张
```

---

**交互式流程总结**：
- ✅ 每个阶段完成后**必须**使用 `AskUserQuestion` 询问用户
- ✅ 根据用户选择决定是否继续下一阶段
- ✅ 用户可以随时选择跳过、停止或切换操作

**自动化场景**：
- 如果用户明确说"完整流程"或"全部执行"，可以跳过询问直接执行
- 如果用户说"交互式执行"，则每步都询问

---

## 概述

这是一个**交互式**书籍内容生产工作流，整合 4 个 Claude Code Skills：

```
zlibrary (搜索下载) → epub-to-markdown (转换) → book-interpreter (解读) → volcano-images (配图)
```

**核心特点**：每个阶段完成后会使用 `AskUserQuestion` 工具询问用户是否继续下一步。

---

## 适用场景

- 用户说「帮我完成《深度学习》的完整解读流程」
- 用户说「生成《原子习惯》的读书笔记」
- 用户说「书籍解读工作流」
- 用户有书籍想解读，但不确定需要哪些步骤

---

## 工作流目录

默认工作目录：`D:/ObsidianWorkflows/`

```
├── 01-Books/              # 书籍相关
│   ├── downloads/         # 从 zlibrary 下载的原始文件
│   ├── raw/               # 用户自己的原始 EPUB/PDF 文件
│   └── converted/         # 转换后的 Markdown
├── 02-Articles/           # 文章相关
│   ├── drafts/            # 草稿
│   └── published/         # 已发布
├── 03-Assets/             # 资源文件
│   └── images/            # 配图
├── 04-Templates/          # 模板文件
└── 05-Workflow/           # 工作文档
```

---

## 执行模式

本工作流支持两种执行模式：

### 模式 1：CLI 直接调用（推荐用于搜索和下载）

使用独立脚本进行搜索、下载、转换操作。

```bash
# 仅搜索（显示所有找到的书籍）
python "$HOME/.claude/skills/book-content-workflow/scripts/enhanced_workflow.py" "python" --stop-at search

# 搜索并下载指定的第2本书
python "$HOME/.claude/skills/book-content-workflow/scripts/enhanced_workflow.py" "python" --stop-at search --book-index 2

# 搜索、下载并转换
python "$HOME/.claude/skills/book-content-workflow/scripts/enhanced_workflow.py" "深度学习" --stop-at convert

# 自定义工作目录
python "$HOME/.claude/skills/book-content-workflow/scripts/enhanced_workflow.py" "书名" --base-path "C:/MyWorkflows"
```

**特点**：
- 实时显示彩色进度面板
- 自动完成所有步骤（无需手动确认）
- 适合 CLI 直接调用

### 模式 2：交互式 Claude Code 模式

通过 Claude Code 对话执行，每步询问用户是否继续。

```python
import sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/book-content-workflow'))
from scripts.workflow import BookWorkflow

# 创建工作流实例
workflow = BookWorkflow(base_path="D:/ObsidianWorkflows")
```

**特点**：
- 每步完成后使用 AskUserQuestion 询问
- 可以灵活跳过某些步骤
- 适合在 Claude Code 对话中使用

---

## 工作流步骤

### 步骤 1：搜索并下载 (zlibrary)

调用 `zlibrary` skill 搜索书籍，让用户选择，下载 EPUB 到 `01-Books/downloads/`。

完成后使用 `AskUserQuestion` 询问：
- 转换为 Markdown
- 先放着，我自己读

### 步骤 2：转换为 Markdown (epub-to-markdown)

调用 `epub-to-markdown` skill 将 EPUB 转换为 Markdown，保存到 `01-Books/converted/`。

完成后使用 `AskUserQuestion` 询问：
- 生成 Ezra 风格解读
- 我自己总结
- 仅保存 Markdown

### 步骤 3：生成解读 (book-interpreter)

调用 `book-interpreter` skill 按 Ezra 风格解读书籍，生成对话式文章，保存到 `02-Articles/drafts/`。

完成后使用 `AskUserQuestion` 询问：
- 为文章配图
- 直接发布草稿
- 仅保存解读

### 步骤 4：生成配图 (volcano-images)

调用 `volcano-images` skill 为文章每个 H2 标题生成配图，保存到 `02-Articles/published/`。

---

## 使用示例

### 示例 1：完整流程

```
用户：帮我完成《深度学习》的完整解读流程

Claude：
📚 正在搜索《深度学习》...
✅ 已下载：深度学习.epub (25.3 MB)

下一步？
用户：转换为 Markdown

Claude：
🔄 正在转换为 Markdown...
✅ 已转换：深度学习.md (150,000 字)

下一步？
用户：生成解读

Claude：
✍️ 正在生成 Ezra 风格解读...
✅ 解读完成：深度学习_解读.md (8,500 字)

下一步？
用户：配图

Claude：
🎨 正在生成配图...
✅ 配图完成 (8 张)
📁 已发布到 published/
```

---

### 示例 2：部分流程（无配图）

```
用户：解读《原子习惯》，不需要配图

Claude：
[下载 → 转换 → 解读]

解读完成，已保存到 drafts/
用户选择：直接发布草稿
✅ 完成，无需配图
```

---

### 示例 3：仅下载

```
用户：搜索《思考，快与慢》电子书

Claude：
✅ 已下载：思考，快与慢.epub

下一步？
用户：先放着，我自己读

Claude：
好的，已保存到 ~/Downloads/，随时可以继续转换。
```

---

## 响应模板

### 阶段完成模板

```
✅ {阶段名称}完成
📄 {关键信息1}
📊 {关键信息2}

下一步你想做什么？
```

### 错误处理模板

```
❌ {阶段名称}失败：{错误信息}

请检查：
1. {检查项1}
2. {检查项2}

是否重试？
```

---

## 文件结构

```
~/.claude/skills/book-content-workflow/
├── SKILL.md                   # 本文件
├── metadata.json              # 技能元数据
├── scripts/
│   ├── workflow.py            # 基础工作流（模拟实现）
│   └── enhanced_workflow.py   # 集成实际技能调用的工作流
└── references/
    └── config.md              # 配置说明
```

**使用方式**：
- CLI 直接调用: `python ~/.claude/skills/book-content-workflow/scripts/enhanced_workflow.py "书名"`
- 在 Claude Code 中触发: 说「帮我解读《书名》」
```

---

## 依赖技能

| Skill | 功能 | 触发词 |
|-------|------|--------|
| zlibrary | 搜索下载电子书 | 搜索、电子书、zlibrary |
| epub-to-markdown | EPUB 转 Markdown | 转换、epub、markdown |
| book-interpreter | Ezra 风格解读 | 解读、读书笔记、Ezra |
| volcano-images | 火山引擎配图 | 配图、生成图片、jimeng |

---

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 工作目录不存在 | 自动创建 D:/ObsidianWorkflows/ 及子目录 |
| 依赖 skill 未安装 | 检查 4 个 skills 是否存在于 %USERPROFILE%\.claude\skills\ |
| 用户中断 | 保存当前进度，可随时恢复 |
| AskUserQuestion 失败 | 降级为文本提示，等待用户输入 |

---

## 与其他 Skills 配合

本 skill 是一个**元技能**（Meta-Skill），整合了以下 skills：

1. **zlibrary** → 下载 EPUB 书籍
2. **epub-to-markdown** → 转换为 Markdown
3. **book-interpreter** → 按 Ezra 风格解读
4. **volcano-images** → 为文章配图

---

## 更新日志

- 2025-01-25: v1.0.0 - 创建交互式书籍内容生产工作流
