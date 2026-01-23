---
name: multi-platform-content-fetcher
description: 多平台内容获取器 - 从多个内容平台（微信公众号、小红书、知乎、微博、博客RSS等）获取内容并存储到本地数据库。支持自然语言触发（如"获取最新内容"、"抓取全亮平台内容"、"检查更新"）和定时任务。使用 web_reader MCP 工具抓取网页内容，自动去重并记录时间戳。适用于内容监控、知识库构建、信息聚合等场景。
---

# Multi-Platform Content Fetcher

## Overview

从多个内容平台获取文章并存储到本地 JSON 数据库，支持增量更新和内容去重。

## Quick Start

### 添加单个内容

使用 `mcp__web_reader__webReader` 工具获取内容后，调用脚本存储：

```python
# 1. 获取网页内容
mcp__web_reader__webReader(url="https://example.com/article")

# 2. 存储到数据库
python3 scripts/fetch_content.py add \
  --title "文章标题" \
  --url "https://example.com/article" \
  --content "文章内容摘要或全文" \
  --platform "blog" \
  --author "作者名"
```

### 批量获取内容

当用户请求"获取最新内容"或类似触发词时：

1. 读取配置的内容源列表（如果用户已配置）
2. 对每个源使用 `mcp__web_reader__webReader` 获取内容
3. 解析并提取：标题、正文、作者
4. 调用 `fetch_content.py add` 存储
5. 输出获取摘要（新增数量、平台分布）

### 查看已存储内容

```bash
# 查看所有内容
python3 scripts/fetch_content.py list

# 按平台筛选
python3 scripts/fetch_content.py list --platform wechat

# 限制数量
python3 scripts/fetch_content.py list --limit 10
```

### 统计信息

```bash
python3 scripts/fetch_content.py stats
```

## Supported Platforms

| Platform | 说明 | URL模式 |
|----------|------|---------|
| wechat | 微信公众号 | mp.weixin.qq.com |
| zhihu | 知乎专栏/问答 | zhihu.com, zhuanlan.zhihu.com |
| xiaohongshu | 小红书 | xiaohongshu.com |
| weibo | 微博 | weibo.com |
| blog | 博客/RSS | 任意网站 |

## Content Storage Format

每条存储的内容包含：

```json
{
  "id": "abc123def456",
  "title": "文章标题",
  "url": "https://example.com/article",
  "content": "文章正文或摘要",
  "platform": "blog",
  "author": "作者名",
  "fetched_at": "2025-01-23T10:30:00"
}
```

## Triggers

当用户说以下内容时触发此技能：
- "获取最新内容"
- "抓取全亮平台内容"
- "检查更新"
- "获取 xxx 的文章"
- "监控 xxx 内容"
- "聚合内容"
- 或明确提到需要从某平台抓取内容

## Resources

### scripts/fetch_content.py

核心功能脚本，提供：

1. **内容存储**：`add` 命令添加单条内容
2. **内容源管理**：`add-source` 命令添加内容源配置
3. **内容查询**：`list` 命令查询已存储内容
4. **统计信息**：`stats` 命令查看数据库统计

### scripts/fetch_content_visual.py ✨

可视化增强版脚本，提供：

1. **所有基础功能**：与 fetch_content.py 相同的命令
2. **批量处理进度**：`batch` 命令带实时进度显示
3. **统计仪表板**：`stats --dashboard` 显示可视化统计
4. **平台图标**：各平台带有专属 emoji 图标
5. **进度条显示**：实时显示处理进度和状态

**使用示例**：
```bash
# 批量添加内容（带进度）
python3 scripts/fetch_content_visual.py batch --file assets/batch_add_example.json

# 查看统计仪表板
python3 scripts/fetch_content_visual.py stats --dashboard
```

**平台图标**：
- 🟠 Hacker News
- 🚀 Product Hunt
- 🐙 GitHub
- 🔴 微博
- 💬 微信公众号
- 🔵 知乎
- 📕 小红书
- 📝 博客

自动去重：基于 URL + title 生成唯一 ID，避免重复存储。

### assets/sources_config.example.json

内容源配置示例，用户可复制为 `sources_config.json` 并配置自己的内容源列表。

## Workflow

### 手动获取内容

1. 用户指定 URL 或内容源
2. 使用 `mcp__web_reader__webReader` 获取内容
3. 解析提取标题、正文、作者
4. 调用脚本存储到数据库
5. 返回操作结果

### 定时任务模式

如果用户需要定时获取：

1. 用户配置内容源列表（可选）
2. 定期遍历内容源
3. 对每个源获取最新内容
4. 去重后存储
5. 生成变更报告

## Content Production Workflow Integration

此技能是内容制作工作流的第一步 —— **内容获取与存储**。

### 完整工作流

```
┌─────────────────────────────────────────────────────────────────────┐
│                        内容制作工作流                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1️⃣ 内容获取           │
│     ├─ multi-platform-content-fetcher (本技能)                       │
│     ├─ daily-topic-selector (每日选题助手)                            │
│     └─ 输出: 本地内容库 (content_db.json)                            │
│                                                                     │
│  2️⃣ 选题分析           │
│     ├─ 分析热门内容趋势                                               │
│     ├─ 生成科技选题建议                                               │
│     └─ 输出: 选题列表                                                │
│                                                                     │
│  3️⃣ 内容创作           │
│     ├─ 根据选题撰写内容                                               │
│     └─ 输出: Markdown 文章初稿                                        │
│                                                                     │
│  4️⃣ 内容优化 ✨       │
│     ├─ humanizer-zh (去除 AI 味)                                     │
│     ├─ 让内容更自然、有人味                                          │
│     └─ 输出: 优化后的文章                                            │
│                                                                     │
│  5️⃣ 多平台发布          │
│     ├─ auto-redbook-skills → 小红书笔记                               │
│     ├─ qiaomu-x-article-publisher → X Articles                      │
│     └─ 其他平台...                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 配合其他技能使用

**与 daily-topic-selector 配合**:
- 本技能获取全网热门内容
- daily-topic-selector 提供精选的深度选题
- 两者互补：广度 vs 深度

**与 humanizer-zh 配合** (内容优化):
1. 使用本技能收集素材并生成内容初稿
2. humanizer-zh 去除 AI 生成痕迹
3. 让内容更自然、更有人味

**与 auto-redbook-skills 配合**:
1. 使用本技能抓取小红书热门笔记
2. 分析热门话题和内容风格
3. 使用 auto-redbook-skills 创作同类笔记

**与 qiaomu-x-article-publisher 配合**:
1. 使用本技能收集科技资讯
2. 撰写 Markdown 文章
3. 使用 humanizer-zh 优化文章
4. 使用 qiaomu-x-article-publisher 发布到 X Articles

### 典型使用场景

**场景 1：科技内容创作 (完整流程)**
```
用户: "抓取今天热门的科技内容，生成选题并发布"

步骤:
1. 本技能: 抓取 HN、PH、GitHub Trending 热门
2. 分析: 生成 3-5 个科技选题建议
3. 创作: 撰写文章初稿
4. 优化: humanizer-zh 去除 AI 味
5. 发布: 选择平台发布
```

**场景 2：热点追踪 + 深度学习**
```
用户: "监控 AI 领域的最新动态"

步骤:
1. 本技能: 定期抓取 AI 相关内容
2. daily-topic-selector: 过滤并推荐深度内容
3. 持续学习: 构建个人知识库
```

**场景 3：快速生成高质量内容**
```
用户: "基于热门话题写一篇自然、有人味的文章"

步骤:
1. 本技能: 获取热门内容
2. Claude: 撰写初稿
3. humanizer-zh: 去除 AI 痕迹
4. 发布到各平台
```

## Notes

- 数据库默认存储在技能目录下的 `content_db.json`
- 内容去重基于 URL 和标题的 MD5 哈希
- 所有内容按获取时间倒序排列
- 支持跨平台内容聚合查询
