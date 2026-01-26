---
name: book-interpreter
description: Ezra style book interpreter - Transform books into conversational Chinese articles following Ezra's writing style. Use when user mentions "read book", "interpret book", "book summary", "Ezra style", or after converting epub to markdown. Features conversational language, term explanations with quotes, life analogies, and cognitive extensions.
user-invocable: true
---


# 书籍解读 (Ezra 风格)

将书籍内容转化为 Ezra 风格的通俗易懂解读文章。

## 概述

**核心特点**：
- 对话式语言，像和朋友聊天
- 每个术语都有引用块解释
- 生活化类比帮助理解
- 从技术延伸到认知层面

**输出**：
- 5000-10000字深度解读文章
- 术语解释丰富（≥15处）
- 生活化类比（≥3处）
- 结尾有认知升华

## 执行流程

### 步骤 1：创建进度追踪

```python
TodoWrite([
    {"content": "阅读书籍 Markdown 内容", "status": "in_progress", "activeForm": "阅读书籍 Markdown 内容"},
    {"content": "提取核心观点和章节结构", "status": "pending", "activeForm": "提取核心观点和章节结构"},
    {"content": "生成 Ezra 风格解读文章", "status": "pending", "activeForm": "生成 Ezra 风格解读文章"},
    {"content": "质量检查和优化", "status": "pending", "activeForm": "质量检查和优化"},
    {"content": "保存最终文件", "status": "pending", "activeForm": "保存最终文件"}
])
```

### 步骤 2：阅读书籍内容

**目标**：理解书籍的核心论点、结构和关键概念

**执行**：
1. 读取书籍 Markdown 文件
2. 识别章节结构
3. 提取核心概念和论点
4. 记录关键案例和数据

### 步骤 3：生成解读文章

#### 内容结构（必须包含）

1. **引入**：用故事/场景引入，不直接讲主题
2. **核心概念**：术语解释（引用块）+ 生活化类比
3. **主要论点**：是什么 → 为什么 → 怎么做
4. **案例支撑**：书中的关键案例和故事
5. **深度洞察**：方法论启发、现实意义
6. **结尾升华**：延伸到认知层面

#### 术语解释格式（强制）

```markdown
> **概念名称（英文）**：通俗解释。类比说明。
```

示例：
```markdown
> **元认知（Metacognition）**：对思考的思考。就像你在做数学题时，脑子里有另一个"你"在观察你解题的过程，提醒你哪里算错了、哪里可以换个方法。
```

#### 风格要求（严格遵守）

详见 [references/style-guide.md](references/style-guide.md)，核心：
- ✅ 短段落，多留白
- ✅ "就像""比如""试想一下"
- ✅ 中文标点（，。：！？）
- ✅ 重要观点加粗
- ❌ 绝对不用破折号
- ❌ 不用"首先""其次""值得注意的是"

### 步骤 4：质量检查（静默执行）

生成后自检：
- 核心论点覆盖？
- 术语解释完整？（≥15处）
- 生活化类比？（≥3处）
- 案例引用？（≥2个）
- 破折号？（=0个）
- 中文标点？（100%）
- 结尾有升华？

发现问题 → 静默修复 → 继续

### 步骤 5：保存文件

```bash
# 保存到指定目录
python ~/.claude/skills/book-interpreter/scripts/save_article.py \
  --input <book_md> \
  --output <output_dir>
```

## 使用示例

### 示例 1：解读技术书籍

```
用户：解读一下《思考，快与慢》

Claude：
📖 正在阅读书籍内容...
📋 提取核心论点和结构...
✍️ 生成 Ezra 风格解读...

✅ 解读完成！
📄 文件: 快与慢_解读.md
📊 字数: 约 8,500 字
💡 术语解释: 18 处
🎨 类比说明: 5 处
```

### 示例 2：解读商业书籍

```
用户：用 Ezra 风格解读《从0到1》

Claude：
正在生成解读...

核心内容：
- 引入：从 PayPal 创始故事引入
- 概念：垂直进步 vs 水平进步
- 类比：就像从1到n是复制，从0到1是创新
- 升华：创新的认知框架

✅ 已保存到: ~/Books/解读/从0到1_解读.md
```

## 文件结构

```
~/.claude/skills/book-interpreter/
├── SKILL.md              # 本文件
├── references/
│   └── style-guide.md    # Ezra 风格指南
└── scripts/
    └── save_article.py   # 保存文章脚本
```

## 质量检查清单

生成的文档必须通过：

- [x] 所有术语有引用块解释（≥15处）
- [x] 生活化类比（≥3处）
- [x] 语言口语化
- [x] 破折号（=0个）
- [x] 中文标点（100%）
- [x] 重要观点加粗
- [x] 案例引用（≥2个）
- [x] 结尾有升华

## 与其他 Skills 配合

1. **zlibrary** → 下载 EPUB 书籍
2. **epub-to-markdown** → 转换为 Markdown
3. **book-interpreter** → 按 Ezra 风格解读
4. **volcano-images** → 为文章配图
