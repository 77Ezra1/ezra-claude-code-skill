---
name: wechat-article-chat
description: 微信公众号文章AI对话助手 - 获取公众号文章内容并与AI进行智能问答和深度分析。当用户提供微信公众号文章链接（mp.weixin.qq.com）时触发此技能，用于：1) 抓取文章完整内容，2) 保存文章到本地（原文+分析），3) 基于文章内容进行智能问答，4) 提供文章深度分析（总结、观点提炼、延伸思考）。
user-invocable: true
---


# 微信公众号文章AI对话助手

当用户发送微信公众号文章链接时，使用此技能获取文章内容、保存到本地，并进行AI对话。

## 快速开始

### 工作流程

```
用户发送链接 → 获取文章内容 → 保存到本地 → AI对话分析
```

### 步骤1: 保存文章

使用 `scripts/save_article.py` 脚本保存文章：

```python
from scripts.save_article import save_article

# 保存文章（自动创建文件夹并保存原文+分析模板）
save_article("https://mp.weixin.qq.com/s/xxx")
```

**保存结构**：
```
D:/WeChatArticles/
└── YYYYMMDD_公众号名称_文章标题（前50字）/
    ├── 01_原文.md          ← 公众号文章完整内容（Markdown格式）
    └── 02_总结分析.md       ← AI生成的深度分析
```

**文件夹命名规则**：
- 格式：`日期_公众号名称_文章标题`
- 日期：YYYYMMDD格式
- 文章标题限制50字，超出部分截断
- 自动清理文件名中的非法字符

### 步骤2: Cookie配置（访问受限文章时需要）

部分公众号文章需要登录才能查看。配置Cookie：

1. **编辑配置文件**：`assets/cookie_config.json`
2. **获取Cookie方法**：
   - 浏览器登录 mp.weixin.qq.com
   - F12 → Application → Cookies → 复制所有Cookie
   - 粘贴到配置文件

3. **使用Cookie**：
```python
save_article("https://mp.weixin.qq.com/s/xxx", cookie_file="assets/cookie_config.json")
```

### 步骤3: 与文章对话

保存文章后，可以：

**智能问答模式**：
- "这篇文章的核心观点是什么？"
- "作者提到的XXX具体是什么意思？"

**深度分析模式**：
- 自动生成文章摘要、关键观点、逻辑结构
- 提供延伸思考、相关话题

**自由讨论模式**：
- 结合问答和分析，自由探讨文章话题

## 脚本使用

### save_article.py（推荐）

保存文章到本地（原文+分析）。

```bash
# 基础用法
python scripts/save_article.py "https://mp.weixin.qq.com/s/xxx"

# 使用Cookie
python scripts/save_article.py "https://mp.weixin.qq.com/s/xxx" --cookie assets/cookie_config.json
```

**输出**：
- 自动创建文件夹
- 保存原文到 `01_原文.md`
- 创建分析模板到 `02_总结分析.md`

### fetch_article.py

仅获取文章内容（不保存）。

```bash
python scripts/fetch_article.py "https://mp.weixin.qq.com/s/xxx"
python scripts/fetch_article.py "https://mp.weixin.qq.com/s/xxx" --output article.md
```

### check_cookie.py

检查Cookie配置的有效性。

```bash
python scripts/check_cookie.py --cookie assets/cookie_config.json
```

## 保存路径配置

**默认路径**：`D:/WeChatArticles/`

**修改路径**：编辑 `scripts/save_article.py` 中的 `ARTICLES_DIR` 变量：

```python
# 修改为自定义路径
ARTICLES_DIR = "D:/MyArticles"
```

## 对话模式

根据用户需求选择对话模式：

| 模式 | 触发方式 | 输出内容 |
|------|---------|---------|
| **智能问答** | 用户提出具体问题 | 基于文章内容的精准回答 |
| **深度分析** | 用户说"分析一下"或"总结" | 结构化分析报告 |
| **自由讨论** | 开放式对话 | 结合问答和分析的交互式讨论 |

## 分析模板格式

`02_总结分析.md` 包含以下结构：

```markdown
# 文章分析

## 基本信息
- 标题、来源、链接、分析时间

## 核心摘要
200-300字的文章核心内容概括

## 关键观点
1. 观点一 - 支撑论据
2. 观点二 - 支撑论据
3. 观点三 - 支撑论据

## 逻辑结构
梳理文章的论证框架

## 延伸思考
- 值得探讨的问题
- 相关话题
- 补充视角
```

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| "文章链接已过期" | 使用Cookie方案重新获取 |
| "需要登录才能查看" | 配置Cookie到 `assets/cookie_config.json` |
| "Cookie已失效" | 按照Cookie配置方法重新获取 |
| "请求过于频繁" | 等待一段时间后重试 |
| "编码显示异常" | 文件已正确保存为UTF-8编码 |

## 参考文档

- **Cookie详细配置**: [references/cookie_guide.md](references/cookie_guide.md)
- **接口技术细节**: [references/api_reference.md](references/api_reference.md)
- **对话最佳实践**: [references/dialogue_patterns.md](references/dialogue_patterns.md)
