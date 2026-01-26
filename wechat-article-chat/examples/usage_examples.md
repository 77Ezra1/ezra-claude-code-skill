# 微信公众号文章助手 - 使用示例

## 命令行使用

### 1. 基础使用 - 直接保存文章

```bash
# 使用可视化进度版本（推荐）
python scripts/save_article_visual.py "https://mp.weixin.qq.com/s/dn5RhWaLPwP3e70PHBqzxw"

# 输出示例：
# +------------------------------------------------------------+
# |                   WeChat Article Saver                     |
# +------------------------------------------------------------+
#
# [OK] 1. Validating URL (0.30s)
# [OK] 2. Fetching content (0.96s)
# [OK] 3. Parsing article (0.20s)
# [OK] 4. Creating directory (0.20s)
# [OK] 5. Saving original (0.31s)
# [OK] 6. Generating analysis (0.30s)
#
# Elapsed: 2.27s
# Progress: [########################################] 6/6 (100%)
```

### 2. 使用简单主题（兼容所有终端）

```bash
python scripts/save_article_visual.py "https://mp.weixin.qq.com/s/xxxxx" --theme simple
```

### 3. 访问需要登录的文章

```bash
python scripts/save_article_visual.py "https://mp.weixin.qq.com/s/xxxxx" --cookie assets/cookie_config.json
```

### 4. 使用原始版本（无进度显示）

```bash
python scripts/save_article.py "https://mp.weixin.qq.com/s/xxxxx"
```

### 5. 仅获取文章内容（不保存）

```bash
python scripts/fetch_article.py "https://mp.weixin.qq.com/s/xxxxx"
python scripts/fetch_article.py "https://mp.weixin.qq.com/s/xxxxx" --output article.md
```

## 交互式菜单使用

### 启动交互式界面

```bash
python scripts/wechat_cli.py
```

### 菜单操作流程

```
1. 选择 [1] 保存公众号文章
2. 输入文章链接
3. 选择是否使用Cookie (y/N)
4. 选择进度主题 (1=default, 2=simple)
5. 查看保存进度
6. 按回车返回主菜单
```

## Python代码调用

### 在Python脚本中使用

```python
from scripts.save_article_visual import save_article_with_progress

# 保存文章（自动显示进度）
result = save_article_with_progress(
    url="https://mp.weixin.qq.com/s/xxxxx",
    cookie_file=None,  # 或指定Cookie文件路径
    theme="default"    # 或 "simple"
)

if result:
    print("保存成功!")
else:
    print("保存失败!")
```

### 使用原始保存函数

```python
from scripts.save_article import save_article

result = save_article("https://mp.weixin.qq.com/s/xxxxx")
```

### 仅获取文章内容

```python
from scripts.fetch_article import fetch_article

result = fetch_article("https://mp.weixin.qq.com/s/xxxxx")

if 'error' not in result:
    print(f"标题: {result['title']}")
    print(f"作者: {result['author']}")
    print(f"内容: {result['content'][:200]}...")
else:
    print(f"错误: {result['error']}")
```

## 常见使用场景

### 场景1：批量保存文章

```python
urls = [
    "https://mp.weixin.qq.com/s/xxxxx1",
    "https://mp.weixin.qq.com/s/xxxxx2",
    "https://mp.weixin.qq.com/s/xxxxx3",
]

from scripts.save_article_visual import save_article_with_progress

for url in urls:
    print(f"\n处理: {url}")
    save_article_with_progress(url)
```

### 场景2：保存后立即分析

```bash
# 保存文章
python scripts/save_article_visual.py "文章链接"

# 然后把保存的文章发送给Claude进行分析
```

### 场景3：定期备份

创建批处理文件 `backup_articles.bat`:

```batch
@echo off
set ARTICLES=(
    https://mp.weixin.qq.com/s/xxxxx1
    https://mp.weixin.qq.com/s/xxxxx2
)

for %%a in %ARTICLES% do (
    python scripts/save_article_visual.py %%a
)
```

## 故障排查示例

### 问题1：文章获取失败

```bash
# 检查Cookie是否有效
python scripts/check_cookie.py --cookie assets/cookie_config.json

# 输出：[OK] Cookie有效 或 [ERROR] Cookie已失效
```

### 问题2：终端显示异常

```bash
# 切换到简单主题
python scripts/save_article_visual.py "链接" --theme simple
```

### 问题3：保存路径不存在

```python
# 编辑 save_article_visual.py
# 修改 DEFAULT_PATH 为已存在的路径
DEFAULT_PATH = "C:/MyArticles"
```

## 与Claude Code集成

### 方式1：发送链接给Claude

```
用户: 帮我保存这篇文章 https://mp.weixin.qq.com/s/xxxxx

Claude会自动：
1. 调用save_article_visual.py
2. 显示保存进度
3. 返回保存位置
```

### 方式2：请求分析

```
用户: 分析我刚保存的这篇文章

Claude会：
1. 读取 D:/WeChatArticles/最新的文章
2. 生成深度分析
3. 填充到 02_总结分析.md
```

## 高级用法

### 自定义保存路径

```python
import sys
sys.path.insert(0, 'scripts')
from save_article_visual import save_article_with_progress, ARTICLES_DIR

# 修改保存路径
ARTICLES_DIR = "E:/MyWeChatArticles"

save_article_with_progress("文章链接")
```

### 批处理并生成报告

```python
import json
from datetime import datetime
from scripts.save_article_visual import save_article_with_progress

urls = ["url1", "url2", "url3"]
report = {
    "date": datetime.now().isoformat(),
    "total": len(urls),
    "success": 0,
    "failed": 0,
    "articles": []
}

for url in urls:
    result = save_article_with_progress(url)
    if result:
        report["success"] += 1
    else:
        report["failed"] += 1

# 保存报告
with open("save_report.json", "w") as f:
    json.dump(report, f, indent=2)
```
