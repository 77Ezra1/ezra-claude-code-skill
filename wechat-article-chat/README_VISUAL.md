# 微信公众号文章助手 - 可视化界面

## 功能介绍

为 wechat-article-chat skill 添加了命令行可视化进度界面，让文章保存过程更加直观。

## 包含的脚本

### 1. save_article_visual.py - 可视化进度版本

带实时进度显示的文章保存脚本。

```bash
# 使用默认主题（带颜色和Unicode字符）
python scripts/save_article_visual.py "文章链接"

# 使用简单主题（纯ASCII字符，适合所有终端）
python scripts/save_article_visual.py "文章链接" --theme simple

# 使用Cookie
python scripts/save_article_visual.py "文章链接" --cookie assets/cookie_config.json
```

**进度显示效果：**
```
+------------------------------------------------------------+
|                   WeChat Article Saver                     |
+------------------------------------------------------------+

[OK] 1. Validating URL (0.30s)
[OK] 2. Fetching content (0.96s)
[OK] 3. Parsing article (0.20s)
[OK] 4. Creating directory (0.20s)
[OK] 5. Saving original (0.31s)
[..] 6. Generating analysis

Elapsed: 1.97s
Progress: [#################################-------] 5/6 (83%)
```

### 2. wechat_cli.py - 交互式菜单界面

完整的交互式CLI程序，提供友好的菜单导航。

```bash
python scripts/wechat_cli.py
```

**菜单界面：**
```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          微信公众号文章阅读室 WeChat Article Room           ║
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

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│           微信公众号文章保存工作流                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [1/6] Validating URL       验证链接有效性                   │
│  [2/6] Fetching content      获取文章内容                     │
│  [3/6] Parsing article       解析文章数据                     │
│  [4/6] Creating directory    创建保存目录                     │
│  [5/6] Saving original       保存原文Markdown                │
│  [6/6] Generating analysis   生成AI分析模板                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 主题选择

### Default Theme (默认)
- 使用Unicode框线字符
- 彩色输出（绿色=完成，黄色=进行中，红色=失败）
- 适合支持Unicode的现代终端

### Simple Theme (简单)
- 纯ASCII字符
- 无颜色
- 兼容所有终端环境

## 快速开始

### 方式一：直接命令行

```bash
# 保存文章（自动显示进度）
python scripts/save_article_visual.py "https://mp.weixin.qq.com/s/xxxxx"

# 使用简单主题
python scripts/save_article_visual.py "https://mp.weixin.qq.com/s/xxxxx" --theme simple
```

### 方式二：交互式菜单

```bash
# 启动交互式界面
python scripts/wechat_cli.py

# 然后按照菜单提示操作
```

## 输出示例

```
+------------------------------------------------------------+
|                   WeChat Article Saver                     |
+------------------------------------------------------------+

[OK] 1. Validating URL (0.30s)
[OK] 2. Fetching content (0.96s)
[OK] 3. Parsing article (0.20s)
[OK] 4. Creating directory (0.20s)
[OK] 5. Saving original (0.31s)
[OK] 6. Generating analysis (0.30s)

Elapsed: 2.27s
Progress: [########################################] 6/6 (100%)

[SUCCESS] 文章已保存到: D:\WeChatArticles\20260126_公众号名称_文章标题\

保存的文件:
  - D:\WeChatArticles\...\01_原文.md
  - D:\WeChatArticles\...\02_总结分析.md
```

## 优势

| 特性 | 说明 |
|------|------|
| **实时进度** | 每个步骤的执行状态和时间 |
| **可视反馈** | 进度条和完成百分比 |
| **错误提示** | 失败步骤会显示具体错误信息 |
| **主题切换** | 支持不同终端环境 |
| **交互友好** | 菜单界面简化操作流程 |

## 对比原版本

| 功能 | 原版本 | 可视化版本 |
|------|--------|-----------|
| 保存文章 | ✓ | ✓ |
| 进度显示 | 简单文本 | 实时进度条 |
| 错误处理 | 文本提示 | 高亮显示 |
| 用户体验 | 命令行参数 | 菜单导航 |
| 主题支持 | 无 | 2种主题 |

## 注意事项

1. **终端兼容性**：如果显示异常，使用 `--theme simple` 切换到简单主题
2. **编码问题**：Windows CMD可能显示中文乱码，但不影响功能
3. **清屏效果**：进度界面会清屏，如需保留日志请重定向输出

## 技术实现

- 使用ANSI转义序列实现动态更新
- 框线字符使用Unicode绘制
- 支持彩色输出（可选）
- 时间统计精确到毫秒

## 未来增强

- [ ] 支持批量保存文章
- [ ] 添加进度条动画效果
- [ ] 支持自定义主题颜色
- [ ] 添加保存历史记录
- [ ] 支持导出统计报告
