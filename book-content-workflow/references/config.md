# Book Content Workflow - 配置说明

## 工作流配置

### 默认路径

| 路径类型 | 默认值 | 说明 |
|---------|--------|------|
| 基础路径 | `~/ObsidianWorkflows/` | 工作流根目录（跨平台） |
| 原始书籍 | `01-Books/raw/` | EPUB 原始文件 |
| 转换后 | `01-Books/converted/` | Markdown 格式 |
| 草稿 | `02-Articles/drafts/` | 解读文章草稿 |
| 已发布 | `02-Articles/published/` | 配图后的文章 |
| 配图 | `03-Assets/images/` | 生成的图片 |

**示例**：
- Windows: `C:\Users\YourName\ObsidianWorkflows\`
- Linux/Mac: `/home/yourname/ObsidianWorkflows/`

### 自定义路径

```python
from scripts.workflow import BookWorkflow

# 使用自定义路径
workflow = BookWorkflow(base_path="/path/to/your/vault")
```

---

## 依赖技能配置

### 1. zlibrary

确保 `~/.claude/skills/zlibrary/` 目录存在并包含：
- `SKILL.md`
- `scripts/zlibrary_client.py`
- `config/credentials.json`

### 2. epub-to-markdown

确保 `~/.claude/skills/epub-to-markdown/` 目录存在并包含：
- `SKILL.md`
- `scripts/convert_epub.py`

### 3. book-interpreter

确保 `~/.claude/skills/book-interpreter/` 目录存在并包含：
- `SKILL.md`
- `references/style-guide.md`

### 4. volcano-images

确保 `~/.claude/skills/volcano-images/` 目录存在并包含：
- `SKILL.md`
- `scripts/generate_images.py`

环境变量配置（可选）：
```bash
# 即梦 API 配置
export JIMENG_API_URL=http://localhost:8000/v1/images/generations
export JIMENG_API_KEY=your_api_key_here
export JIMENG_MODEL=jimeng-image-4.5
```

---

## AskUserQuestion 集成

在 Claude Code 中，工作流会使用内置的 `AskUserQuestion` 工具：

```python
# 阶段完成后的询问示例
AskUserQuestion(
    questions=[{
        "question": "下载完成！下一步你想做什么？",
        "header": "下一步",
        "options": [
            {
                "label": "转换为 Markdown",
                "description": "将EPUB转换为Markdown格式，便于AI阅读"
            },
            {
                "label": "先放着，我自己读",
                "description": "保存EPUB文件，稍后继续"
            }
        ],
        "multiSelect": False
    }])
```

---

## 文件命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| EPUB | `{书名}.epub` | `深度学习.epub` |
| Markdown | `{书名}.md` | `深度学习.md` |
| 解读文章 | `{书名}_解读.md` | `深度学习_解读.md` |
| 配图 | `{章节名}_序号.png` | `引言_01.png` |

---

## 文章状态标记

在生成的解读文章开头添加 YAML frontmatter：

```yaml
---
status: draft      # draft | reviewing | published
source: 深度学习.epub
date: 2025-01-25
images: false      # 是否已配图
book_title: 深度学习
author: Ian Goodfellow
---
```

---

## 质量标准

### Ezra 风格解读文章

- 字数: 5000-10000 字
- 术语解释: ≥15 处（引用块格式）
- 生活化类比: ≥3 处
- 案例引用: ≥2 个
- 破折号: =0 个
- 中文标点: 100%
- 结尾升华: 必需

### 配图标准

- 每个 H2 标题有配图
- 图片描述具体清晰
- 底部有中文标题
- 图片质量清晰

---

## 故障排查

### 问题：工作目录不存在

**解决方案**：工作流会自动创建目录，或手动创建：
```bash
# Linux/Mac
mkdir -p ~/ObsidianWorkflows/01-Books/{raw,converted}
mkdir -p ~/ObsidianWorkflows/02-Articles/{drafts,published}
mkdir -p ~/ObsidianWorkflows/03-Assets/images

# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\ObsidianWorkflows\01-Books\raw"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\ObsidianWorkflows\01-Books\converted"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\ObsidianWorkflows\02-Articles\drafts"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\ObsidianWorkflows\02-Articles\published"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\ObsidianWorkflows\03-Assets\images"
```

### 问题：依赖 skill 未找到

**解决方案**：检查技能是否安装：
```bash
ls ~/.claude/skills/zlibrary
ls ~/.claude/skills/epub-to-markdown
ls ~/.claude/skills/book-interpreter
ls ~/.claude/skills/volcano-images
```

### 问题：zlibrary 下载失败

**解决方案**：
- 检查今日下载次数是否用完
- 检查网络连接
- 手动下载 EPUB 放入 `01-Books/raw/`

### 问题：转换后乱码

**解决方案**：
- 检查 EPUB 编码
- 尝试指定 `--encoding utf-8` 参数

---

## 集成到 Claude Code

触发示例：

```
用户：帮我完成《深度学习》的完整解读流程

Claude：
[自动触发 book-content-workflow skill]

运行工作流...
[1/4] 搜索并下载书籍...
[2/4] 转换为 Markdown...
[3/4] 生成 Ezra 风格解读...
[4/4] 为文章配图...

完成！
```
