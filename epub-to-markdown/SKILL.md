---
name: epub-to-markdown
description: EPUB to Markdown converter - Extract content from EPUB files and convert to Markdown format. Use when user mentions "epub", "convert epub", "epub to markdown", or after downloading books from zlibrary. Supports batch conversion, chapter splitting, and metadata preservation.
---

# EPUB to Markdown Converter

将 EPUB 电子书转换为 Markdown 格式，便于 Claude Code 全篇阅读和进一步处理。

## 适用场景

- 用户下载了 EPUB 格式电子书后需要转换
- 用户说「转换 epub」「epub 转 markdown」「提取 epub 内容」
- 配合 zlibrary skill 使用：下载 → 转换 → 阅读

## 执行流程

### 模式 A：单个文件转换

**触发词**：「转换这个 epub」「把 epub 转成 markdown」

**执行步骤**：

1. **确认文件路径**：获取 EPUB 文件路径
2. **执行转换**：
   ```bash
   python ~/.claude/skills/epub-to-markdown/scripts/convert_epub.py <epub_file> --output <output_dir>
   ```
3. **输出结果**：单个 Markdown 文件或分章节 Markdown 文件

### 模式 B：批量转换

**触发词**：「批量转换 epub」「转换所有 epub」

**执行步骤**：

1. **扫描目录**：查找指定目录下的所有 EPUB 文件
2. **批量执行**：
   ```bash
   python ~/.claude/skills/epub-to-markdown/scripts/convert_epub.py --batch <input_dir> --output <output_dir>
   ```

### 模式 C：分章节转换

**触发词**：「按章节转换」「分章节提取」

**执行步骤**：

```bash
python ~/.claude/skills/epub-to-markdown/scripts/convert_epub.py <epub_file> --split-chapters --output <output_dir>
```

**输出结构**：
```
output_dir/
├── book_metadata.json      # 书籍元数据
├── full_book.md            # 完整内容
└── chapters/
    ├── chapter_01.md
    ├── chapter_02.md
    └── ...
```

## 输出格式

### 完整 Markdown 格式

转换后的 Markdown 包含：

- **元数据区**：书名、作者、出版信息
- **目录结构**：根据 EPUB 中的章节结构生成
- **正文内容**：保留段落、列表、引用等格式
- **图片引用**：提取图片并生成相对路径引用

### 元数据 JSON 格式

```json
{
  "title": "书籍标题",
  "author": "作者",
  "language": "zh",
  "publisher": "出版社",
  "published_date": "2023-01-01",
  "isbn": "978-7-xxx-xxxx-x",
  "source_file": "original.epub",
  "chapters": [
    {"id": "ch1", "title": "第一章", "file": "chapters/chapter_01.md"}
  ]
}
```

## 使用示例

### 示例 1：基本转换

```
用户：我下载了一本 Python 书籍，帮我转换成 markdown

Claude：
正在转换 EPUB 文件...

✅ 转换完成
📄 输出文件: Python编程从入门到实践.md
📊 字数: 约 150,000 字
🖼️ 图片: 已提取 23 张
📁 保存位置: ~/Books/converted/
```

### 示例 2：分章节转换

```
用户：把这本书按章节分开转换

Claude：
正在按章节转换 EPUB 文件...

✅ 转换完成
📚 书名: 深度学习
📖 章节数: 15 章
📁 输出目录: ~/Books/深度学习/
   ├── full_book.md (完整版)
   ├── book_metadata.json (元数据)
   └── chapters/ (分章节)
       ├── chapter_01_引言.md
       ├── chapter_02_神经网络基础.md
       └── ...
```

## 依赖项

### 可选依赖

安装后可获得更好的转换效果：

```bash
# 使用 ebooklib 进行更精确的 EPUB 解析
pip install --break-system-packages ebooklib

# 或使用 pandoc 进行格式转换
brew install pandoc
```

### 纯 Python 模式

脚本支持无依赖纯 Python 模式，使用 `zipfile` 直接提取 EPUB 内容：

- EPUB 本质是 ZIP 格式
- 直接解压读取 HTML/XML 内容
- 提取文本和图片资源

## 文件结构

```
~/.claude/skills/epub-to-markdown/
├── SKILL.md              # 本文件
├── scripts/
│   ├── convert_epub.py   # 主转换脚本
│   └── epub_parser.py    # EPUB 解析器
└── assets/
    └── template.md       # Markdown 输出模板
```

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 转换后乱码 | 检查 EPUB 编码，尝试指定 `--encoding utf-8` |
| 图片丢失 | 使用 `--extract-images` 参数提取图片 |
| 章节混乱 | 使用 `--auto-chapters` 自动检测章节 |
| 格式丢失 | 尝试安装 `ebooklib` 或 `pandoc` 获得更好效果 |

## 与其他 Skills 配合

1. **zlibrary** → 下载 EPUB 书籍
2. **epub-to-markdown** → 转换为 Markdown
3. **book-interpreter** → 按 Ezra 风格解读
4. **volcano-images** → 为文章配图
