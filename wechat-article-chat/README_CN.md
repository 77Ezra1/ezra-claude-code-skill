# 微信公众号文章助手 - 中文可视化界面

## 概述

为 wechat-article-chat skill 创建了完整的中文可视化界面，支持中文进度显示和交互式菜单操作。

## 新增文件

| 文件 | 说明 |
|------|------|
| `scripts/save_article_visual_cn.py` | 带中文进度显示的保存脚本 |
| `scripts/wechat_cli_cn.py` | 中文交互式菜单界面 |
| `启动中文版.bat` | Windows快捷启动（交互式菜单） |
| `保存文章.bat` | Windows快捷启动（直接保存） |

## 使用方法

### 方式一：双击批处理文件（最简单）

1. **启动交互式菜单**
   - 双击 `启动中文版.bat`
   - 按照菜单提示操作

2. **快速保存文章**
   - 双击 `保存文章.bat`
   - 输入文章链接
   - 自动保存

### 方式二：命令行运行

```bash
# 带中文进度的保存脚本
python scripts/save_article_visual_cn.py "文章链接"

# 使用简单主题（英文界面，兼容性更好）
python scripts/save_article_visual_cn.py "文章链接" --theme simple

# 使用Cookie
python scripts/save_article_visual_cn.py "文章链接" --cookie assets/cookie_config.json
```

### 方式三：交互式菜单

```bash
python scripts/wechat_cli_cn.py
```

## 中文界面效果

### 进度显示效果（默认主题）

```
┌────────────────────────────────────────────────────────────┐
│                  微信公众号文章保存                          │
└────────────────────────────────────────────────────────────┘

[完成] 1. 验证文章链接 (0.30秒)
[完成] 2. 获取文章内容 (1.30秒)
[完成] 3. 解析文章数据 (0.20秒)
[完成] 4. 创建保存目录 (0.20秒)
[进行中] 5. 保存原文Markdown
[等待] 6. 生成分析模板

已用时间: 2.00秒
进度: [■■■■■■■■■■■■■■■□□□□□□□□□□□□□] 4/6 (67%)
```

### 交互式菜单效果

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║              微信公众号文章阅读室                            ║
║            WeChat Article Reading Room                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 保存公众号文章
  [2] 查看已保存的文章
  [3] 配置Cookie
  [4] 使用帮助

────────────────────────────────────────────────────────────
  保存路径: D:/WeChatArticles
────────────────────────────────────────────────────────────

请选择操作 [q=退出]:
```

## 特点

### 1. 完整中文支持

- ✓ 进度步骤全部中文化
- ✓ 菜单界面中英文双语
- ✓ 成功/失败提示中文
- ✓ 错误信息中文说明

### 2. UTF-8编码优化

```python
# 自动设置UTF-8编码输出
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
```

### 3. 两种主题选择

| 主题 | 语言 | 特点 |
|------|------|------|
| default | 中文 | 完整中文界面，支持UTF-8终端 |
| simple | 英文 | 纯ASCII字符，兼容所有终端 |

## 常见问题

### Q1: 中文显示乱码怎么办？

**A**: 使用简单主题：
```bash
python scripts/save_article_visual_cn.py "链接" --theme simple
```

### Q2: Windows CMD显示中文不正常？

**A**: 使用批处理文件启动（已设置UTF-8编码）：
- 双击 `启动中文版.bat`
- 双击 `保存文章.bat`

### Q3: PowerShell中中文显示正常吗？

**A**: 是的，PowerShell原生支持UTF-8，中文显示正常：
```powershell
python scripts/save_article_visual_cn.py "链接"
```

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│              微信公众号文章保存工作流（中文）                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [1/6] 验证文章链接       ✓ 验证URL有效性                     │
│  [2/6] 获取文章内容       ✓ 发送HTTP请求                     │
│  [3/6] 解析文章数据       ✓ 提取标题、作者、内容             │
│  [4/6] 创建保存目录       ✓ 生成文件夹并创建                 │
│  [5/6] 保存原文Markdown   ✓ 转换并保存原文                   │
│  [6/6] 生成分析模板       ✓ 创建AI分析模板                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 对比英文版

| 特性 | 英文版 | 中文版 |
|------|--------|--------|
| 进度显示 | 英文 | 中文 |
| 状态提示 | 英文 | 中文 |
| 错误信息 | 英文 | 中文 |
| 菜单界面 | 英文 | 中英双语 |
| UTF-8支持 | 需手动配置 | 自动配置 |
| Windows兼容 | 默认英文 | 批处理优化 |

## 代码示例

### 在Python中使用中文版

```python
from scripts.save_article_visual_cn import save_article_with_progress

# 保存文章（自动显示中文进度）
result = save_article_with_progress(
    url="https://mp.weixin.qq.com/s/xxxxx",
    cookie_file=None,
    theme="default"  # 中文界面
)
```

### 批量保存文章

```python
urls = [
    "https://mp.weixin.qq.com/s/xxxxx1",
    "https://mp.weixin.qq.com/s/xxxxx2",
    "https://mp.weixin.qq.com/s/xxxxx3",
]

from scripts.save_article_visual_cn import save_article_with_progress

for url in urls:
    print(f"\n正在处理: {url}")
    save_article_with_progress(url)
```

## 技术实现

### UTF-8输出配置

```python
# Windows下设置UTF-8编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
```

### 中文进度条字符

```python
# 使用Unicode字符绘制进度条
bar = "■" * filled + "□" * (bar_length - filled)
```

### 框线绘制

```python
# 使用Unicode框线字符
corner_tl = "┌"  # 左上角
corner_tr = "┐"  # 右上角
border = "│"    # 边框
header = "─"    # 横线
```

## 文件说明

### save_article_visual_cn.py

- 完整的中文进度显示
- 支持两种主题切换
- 自动UTF-8编码配置
- 实时进度更新

### wechat_cli_cn.py

- 中文交互式菜单
- 四大功能模块
- 友好的用户提示
- 错误处理和帮助

### 批处理文件

- `启动中文版.bat` - 启动交互式菜单
- `保存文章.bat` - 快速保存单篇文章
- 自动设置UTF-8编码（chcp 65001）

## 快速开始

### 第一次使用

1. 双击 `启动中文版.bat`
2. 选择 `[1] 保存公众号文章`
3. 输入文章链接
4. 查看保存进度
5. 保存完成！

### 后续使用

- **偶尔保存**：双击 `保存文章.bat`，输入链接即可
- **频繁使用**：运行 `python scripts/wechat_cli_cn.py` 使用菜单
- **批量保存**：编写Python脚本调用 `save_article_with_progress()`

## 总结

中文版提供了：

- ✅ 完整的中文界面
- ✅ 直观的进度显示
- ✅ 友好的交互菜单
- ✅ 便捷的批处理启动
- ✅ UTF-8编码自动配置

让保存公众号文章变得更加简单直观！
