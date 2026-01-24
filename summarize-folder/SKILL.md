---
name: summarize-folder
description: "目录文件遍历和内容总结。当用户需要分析整个目录/文件夹中的所有文件时触发：遍历目录、识别文件类型、提取多种格式文件内容（docx/pdf/xlsx/txt/md/csv等）、生成结构化总结。触发词：总结这个目录、分析这个文件夹、看看这个目录有什么、遍历文件夹、帮我看看这个文件夹"
priority: 85
---

# 目录文件遍历和内容总结

## 触发条件

当用户说以下内容时自动触发：
- "帮我总结这个目录" / "总结这个文件夹"
- "分析这个目录" / "看看这个文件夹有什么"
- "遍历文件夹" / "查看目录内容"
- "这个目录里有什么文件" / "帮我看看这个文件夹"

## 工作流程

### 第一步：确认目标目录

首先确认用户要分析的目录路径：
- 如果用户提供了路径，直接使用
- 如果没有提供，询问用户具体目录路径
- 支持相对路径和绝对路径

### 第二步：遍历目录结构

使用 `find` 命令遍历目录，获取所有文件列表：

```bash
# 遍历目录，按类型分类显示文件
find "<目录路径>" -type f | head -100
```

统计文件类型分布：
```bash
find "<目录路径>" -type f -name "*.docx" | wc -l  # Word 文档
find "<目录路径>" -type f -name "*.pdf" | wc -l   # PDF 文档
find "<目录路径>" -type f -name "*.xlsx" -o -name "*.xls" -o -name "*.csv" | wc -l  # Excel/表格
find "<目录路径>" -type f -name "*.txt" -o -name "*.md" | wc -l  # 文本文件
find "<目录路径>" -type f -name "*.pptx" | wc -l  # PowerPoint
```

### 第三步：按文件类型提取内容

#### DOCX (Word 文档) - 使用 pandoc

```bash
# 提取单个文档内容
pandoc "<文件路径>.docx" -t markdown -o temp_output.md

# 批量提取
find "<目录路径>" -type f -name "*.docx" -exec sh -c 'pandoc "$1" -t markdown --output="$1.md"' _ {} \;
```

#### PDF - 使用 pdfplumber 或 pdftotext

```python
# Python 脚本提取 PDF 内容
import pdfplumber
import sys

def extract_pdf_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    print(extract_pdf_text(sys.argv[1]))
```

或使用命令行：
```bash
pdftotext "<文件路径>.pdf" -  # 输出到标准输出
pdftotext "<文件路径>.pdf" output.txt  # 输出到文件
```

#### XLSX/XLS/CSV (Excel 和表格) - 使用 pandas

```python
# Python 脚本读取表格内容
import pandas as pd
import sys

def extract_spreadsheet(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            # 读取所有 sheet
            excel_file = pd.ExcelFile(file_path)
            result = f"文件: {file_path}\nSheet 列表: {excel_file.sheet_names}\n\n"
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                result += f"--- Sheet: {sheet_name} ---\n"
                result += f"形状: {df.shape}\n"
                result += f"列名: {list(df.columns)}\n"
                result += f"预览:\n{df.head(10).to_string()}\n\n"
            return result
    except Exception as e:
        return f"错误: {str(e)}"

if __name__ == "__main__":
    print(extract_spreadsheet(sys.argv[1]))
```

或使用命令行快速查看：
```bash
# CSV 文件
cat "<文件路径>.csv" | head -50

# XLSX 文件（需要 python）
python -c "import pandas as pd; df = pd.read_excel('<文件路径>.xlsx'); print(df.to_string())"
```

#### TXT/MD (文本文件)

```bash
# 直接读取
cat "<文件路径>.txt"

# Markdown 文件
cat "<文件路径>.md"
```

#### PPTX (PowerPoint)

```bash
# 使用 pandoc 提取
pandoc "<文件路径>.pptx" -t markdown -o output.md
```

### 第四步：生成结构化总结

将所有提取的内容整理成以下结构：

```markdown
# 目录总结报告

## 目录概览
- **路径**: [目录路径]
- **文件总数**: [数量]
- **子目录数**: [数量]

## 文件类型分布
| 类型 | 数量 | 说明 |
|------|------|------|
| Word (.docx) | X | 文档文件 |
| PDF | X | PDF 文档 |
| Excel | X | 表格文件 |
| 文本 (.txt/.md) | X | 文本文件 |
| 其他 | X | 其他格式 |

## 文件列表及内容摘要

### 1. [文件名1].[扩展名]
**路径**: [相对路径]
**类型**: [文件类型]
**大小**: [文件大小]

**内容摘要**:
[提取的关键内容/摘要]

---

### 2. [文件名2].[扩展名]
[同上结构...]

## 整体分析

### 主要主题/内容
[分析所有文件的整体主题和内容关联]

### 关键信息提取
- [关键点1]
- [关键点2]
- [关键点3]

### 建议行动
- [基于内容分析的建议]
```

## 支持的文件格式

| 格式 | 扩展名 | 提取方法 |
|------|--------|----------|
| Word 文档 | .docx | pandoc |
| PDF 文档 | .pdf | pdfplumber / pdftotext |
| Excel 表格 | .xlsx, .xls | pandas / openpyxl |
| CSV 表格 | .csv | pandas |
| 文本文件 | .txt | 直接读取 |
| Markdown | .md | 直接读取 |
| PowerPoint | .pptx | pandoc |
| 图片 (OCR) | .jpg, .png | pytesseract (可选) |

## 错误处理

- 如果文件损坏或无法读取，记录错误但继续处理其他文件
- 对于受密码保护的文件，提示用户提供密码
- 对于无法识别的格式，使用 `file` 命令检测 MIME 类型

## 依赖工具

确保以下工具可用（大部分已内置在官方 skills 中）：

```bash
# 文档转换
pandoc --version  # Word/PowerPoint 转换

# PDF 处理
pdftotext -v      # PDF 文本提取
pip install pdfplumber  # Python PDF 处理

# Excel 处理
pip install pandas openpyxl  # Python Excel 处理

# 图片 OCR (可选)
pip install pytesseract pdf2image
```

## 使用示例

```
用户: 帮我总结这个目录

Claude: 好的，请告诉我你要分析哪个目录的路径？

用户: C:\Users\Administrator\Documents\work

Claude: 开始分析目录...
- 扫描文件...
- 发现 12 个文件（3个Word文档，2个PDF，5个Excel，2个文本文件）
- 正在提取内容...
- 生成总结报告...

[输出结构化总结报告]
```

## 可视化界面

本 skill 集成了 **visual-progress 框架**，提供美观的进度显示。

### 命令行使用

```bash
# 基本用法
python ~/.claude/skills/summarize-folder/scripts/summarize.py <目录路径>

# 递归处理子目录
python ~/.claude/skills/summarize-folder/scripts/summarize.py <目录路径> -r

# 保存报告到文件
python ~/.claude/skills/summarize-folder/scripts/summarize.py <目录路径> -o report.md

# 使用极简主题
python ~/.claude/skills/summarize-folder/scripts/summarize.py <目录路径> -t minimal
```

### 可视化效果

```
══════════════════════════════════════════════════════════════
═══════════════════════ 目录文件分析 ══════════════════════════
══════════════════════════════════════════════════════════════

▶ 📁 扫描目录文件...
  [████████████████████████████████████] 100%
  ✓ 发现 12 个文件

▶ 📄 提取文件内容...
  处理: document1.docx [████████░░░░░░░░░░░░░░░░░░░] 50%
  ...

══════════════════════════════════════════════════════════════
           🎉 所有任务完成！
══════════════════════════════════════════════════════════════

  • 文件总数: 12
  • 总大小: 2.5 MB
  • 报告长度: 15234 字符
```

### 支持的主题

| 主题 | 描述 | 使用方式 |
|------|------|----------|
| colorful | 彩色主题（默认） | `-t colorful` |
| minimal | 极简主题（无颜色） | `-t minimal` |

### Python API 使用

```python
from summarize_folder.scripts.summarize import SummarizeFolderVisual

# 创建分析器
analyzer = SummarizeFolderVisual(theme="colorful")

# 执行分析
report = analyzer.run(
    directory="/path/to/folder",
    recursive=False,
    output_file="report.md"
)

print(report)
```

## 注意事项

1. **大文件处理**: 对于超过 100MB 的文件，先询问是否需要处理
2. **敏感信息**: 提取内容时注意识别和提醒敏感信息
3. **编码问题**: 对于非 UTF-8 编码的文件，使用 `chardet` 检测编码
4. **递归深度**: 默认只处理当前目录，询问用户是否需要递归处理子目录
5. **文件数量限制**: 单次处理建议不超过 50 个文件，超过则建议分批处理
