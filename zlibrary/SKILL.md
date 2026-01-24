---
name: zlibrary
description: Zlibrary 电子书搜索与下载 - 封装 Zlibrary API，支持搜索图书、获取详情、下载图书、收藏管理等功能。
version: 1.0.0
triggers:
  keywords:
    # 核心关键词
    - "zlibrary"
    - "电子书"
    - "图书"
    - "书籍"
    - "小说"
    # 搜索相关
    - "搜书"
    - "搜索书"
    - "找书"
    - "找本书"
    - "搜一本"
    - "搜索一本"
    - "查书"
    # 下载相关
    - "下载电子书"
    - "下载图书"
    - "下载书"
    - "下载小说"
    # 其他
    - "z-lib"
    - "zlib"
    - "kindle"
    - "图书馆"
  patterns:
    # 高优先级模式
    - "搜索*书"
    - "找*书"
    - "*电子书"
    - "下载*书"
    - "zlibrary*"
    - "*kindle"
    - "有没有*书"
    - "推荐*书"
    - "我要*书"
    - "想要*书"
    - "有没有*电子书"
    - "找本*"
    - "搜本*"
  intents:
    - book-search
    - book-download
    - library-query
    - ebook-search
priority: 90
conflicts: []
---

# Zlibrary: 电子书搜索与下载

封装 [bipinkrish/Zlibrary-API](https://github.com/bipinkrish/Zlibrary-API)，提供电子书搜索、详情获取、下载等功能。

## 适用场景

- 用户说「搜索 Python 相关的书籍」「找机器学习电子书」
- 用户说「下载这本书」「获取图书详情」
- 用户说「查看热门图书」「最近添加的书籍」
- 用户说「zlibrary 搜索」等

## 执行流程

### 模式 A：搜索图书

**触发词**：「搜索」「找书」「搜书」「*电子书」

**执行步骤**：

1. **解析用户意图**：提取搜索关键词
2. **初始化客户端**：
   ```python
   import sys
   sys.path.insert(0, '/Users/ezra/.claude/skills/zlibrary')
   from scripts.zlibrary_client import ZlibraryClient, format_book

   client = ZlibraryClient()
   ```
3. **执行搜索**：
   ```python
   results = client.search(message="搜索关键词", limit=10)
   ```
4. **格式化输出**：
   ```python
   if results.get("success"):
       books = results.get("books", [])
       for i, book in enumerate(books[:10], 1):
           print(f"{i}. {format_book(book)}")
   ```

### 模式 B：下载图书

**触发词**：「下载*书」「获取图书文件」

**执行步骤**：

1. **确认下载目标**：从搜索结果中获取 book 对象
2. **检查下载额度**：
   ```python
   left = client.get_downloads_left()
   if left == 0:
       print("今日下载次数已用完")
       return
   ```
3. **执行下载**：
   ```python
   filename, content = client.download_book(book)
   ```
4. **保存文件**：
   ```python
   import os
   save_dir = os.path.expanduser("~/Downloads")
   save_path = os.path.join(save_dir, filename)
   with open(save_path, "wb") as f:
       f.write(content)
   print(f"已保存到: {save_path}")
   ```

### 模式 C：热门/最新图书

**触发词**：「热门图书」「最新书籍」「推荐图书」「今天有什么书」

**执行步骤**：

```python
# 热门图书
results = client.get_most_popular(limit=10)

# 最新图书
results = client.get_recently(limit=10)

# 格式化输出
if results.get("success"):
    books = results.get("books", [])
    for i, book in enumerate(books, 1):
        print(f"{i}. {format_book(book)}")
```

### 模式 D：图书详情

**触发词**：「图书详情」「书籍信息」「*详情」

**执行步骤**：

```python
info = client.get_book_info(bookid, hashid)

# 显示详细信息
title = info.get("title", "")
description = info.get("description", "")
year = info.get("year", "")
publisher = info.get("publisher", "")
isbn = info.get("identifier", "")

print(f"书名: {title}")
print(f"作者: {info.get('author', '')}")
print(f"年份: {year}")
print(f"出版社: {publisher}")
print(f"ISBN: {isbn}")
print(f"\n简介:\n{description}")
```

## 响应模板

### 搜索结果模板

```
找到 X 本相关图书：

1. 书名 (作者) | 年份 | 语言 | 格式 | 大小
2. ...

输入序号下载图书，或继续搜索其他关键词。
```

### 下载确认模板

```
正在下载: 书名

✅ 下载完成 (XX MB)
已保存到: ~/Downloads/文件名.epub

今日剩余下载次数: X
```

### 错误处理模板

```
❌ 操作失败: [错误信息]

请检查：
1. 是否已登录 (运行一次客户端测试)
2. 今日下载次数是否用完
3. 网络连接是否正常
```

## 使用示例

### 示例 1：搜索图书

```
用户：搜索 Python 编程相关的电子书

Claude：
正在搜索 "Python 编程"...

找到 10 本相关图书：

1. 趣学Python算法100例 (刘河飞 & 闫凯峰) | 2020年 | Chinese | EPUB | 17.2 MB
2. Python编程三剑客 (埃里克·马瑟斯) | 2020年 | Chinese | EPUB | 16.4 MB
3. ...

需要下载哪一本？输入序号即可。
```

### 示例 2：下载图书

```
用户：下载第 1 本

Claude：
正在下载: 趣学Python算法100例...

✅ 下载完成 (17.2 MB)
已保存到: ~/Downloads/趣学Python算法100例.epub

今日剩余下载次数: 9
```

### 示例 3：热门图书

```
用户：今天有什么热门图书？

Claude：
获取热门图书中...

热门榜单 TOP 10：
1. [人工智能] 人工智能：一种现代方法 | 2022年 | English | PDF | 25.3 MB
2. [小说] 三体全集 | 2008年 | Chinese | EPUB | 5.8 MB
3. ...
```

## API 限制

| 限制项 | 说明 |
|--------|------|
| 每日下载 | 免费账户约 5-10 次 |
| 搜索频率 | 建议间隔 > 1 秒 |
| 并发请求 | 不建议 |

## 文件结构

```
~/.claude/skills/zlibrary/
├── SKILL.md              # 本文件
├── Zlibrary.py           # 原始 API
├── scripts/
│   └── zlibrary_client.py   # Python 客户端封装
├── config/
│   └── credentials.json     # 登录凭证（已配置）
```

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 登录失败 | 检查 remix_userid 和 remix_userkey 是否正确 |
| 搜索无结果 | 尝试更换关键词或移除语言/格式过滤 |
| 下载失败 | 检查今日下载次数是否用完 |
| 网络超时 | 检查网络连接，稍后重试 |
