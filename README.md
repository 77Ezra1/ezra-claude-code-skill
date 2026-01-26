# Ezra's Claude Code Skills

一组自定义的 Claude Code Skills，支持自然语言触发，提升开发效率。

## 快速开始

### 安装

**方式一：直接克隆（推荐）**

```bash
# 进入 Claude 配置目录
cd ~/.claude

# 如果已有 skills 目录，先备份
mv skills skills.bak

# 克隆仓库
git clone https://github.com/77Ezra1/ezra-claude-code-skill.git skills
```

**方式二：手动下载**

1. 下载本仓库的 ZIP 文件
2. 解压到 `~/.claude/skills/` 目录
3. 确保目录结构正确（skills 文件夹下直接是各个 skill 子目录）

**安装位置说明**

| 操作系统 | 安装路径 |
|----------|----------|
| Windows | `C:\Users\<用户名>\.claude\skills\` |
| macOS | `~/.claude/skills/` |
| Linux | `~/.claude/skills/` |

### 验证安装

安装完成后，在 Claude Code 中输入：

```
/commit
```

如果看到 skill 被触发，说明安装成功。

## 使用方式

### 方式一：斜杠命令（精确调用）

直接输入斜杠命令来调用指定的 skill：

```
/commit              # 调用 Git 提交助手
/github-upload       # 调用 GitHub 上传
/pm                  # 调用产品经理助手
/dev-doc             # 调用开发文档生成器
/dev-track           # 调用进度跟踪器
/bookmark            # 调用收藏夹管理
/pre-dev             # 调用开发前指南
```

### 方式二：自然语言（智能触发）

直接用中文描述你的需求，skill 会自动识别并触发：

| 你说的话 | 触发的 Skill |
|----------|--------------|
| 「改完了，帮我提交」 | `/commit` |
| 「推送到 GitHub」 | `/github-upload` |
| 「我想做一个博客系统」 | `/pm` |
| 「帮我生成开发文档」 | `/dev-doc` |
| 「登录功能做完了」 | `/dev-track` |
| 「收藏这个链接」 | `/bookmark` |
| 「开始开发这个功能」 | `/pre-dev` |

## Skills 详细说明

本仓库包含 **39 个 Claude Code Skills**，涵盖开发工作流的各个环节。

### 核心开发工作流 (7个)

#### 1. PM - 产品经理助手

**命令**: `/pm`

**功能**:
- 通过结构化追问完善产品想法
- 帮助明确核心功能和技术方案
- 输出可落地的项目规划文档 (PROJECT.md)

**触发词**: 我想做一个、有个想法、帮我规划、想搞个

---

#### 2. Dev-Doc - 开发文档生成器

**命令**: `/dev-doc`

**功能**:
- 将项目规划转化为技术开发文档
- 生成技术架构、API 设计、数据库设计
- 输出可执行的任务清单 (TASKS.md)

**触发词**: 生成开发文档、技术架构、落地方案、任务拆分

---

#### 3. Pre-Dev - 开发前指南

**命令**: `/pre-dev`

**功能**:
- 在编码前澄清需求
- 确认实现方案
- 避免返工

**触发词**: 开始开发、帮我实现、开干、搞起来

---

#### 4. Dev-Track - 项目进度跟踪

**命令**: `/dev-track`

**功能**:
- 基于 TASKS.md 维护项目进度
- 标记任务完成状态
- 展示进度百分比和进度条

**触发词**: 更新进度、查看进度、做到哪了、xxx完成了

---

#### 5. Commit - Git 提交助手

**命令**: `/commit`

**功能**:
- 自动分析代码变更
- 生成符合 Conventional Commit 规范的提交信息
- 检查敏感文件，防止泄露

**触发词**: 提交代码、commit、存一下、改完了、搞定了

---

#### 6. GitHub Upload - 上传到 GitHub

**命令**: `/github-upload`

**功能**:
- 自动创建 GitHub 仓库（如不存在）
- 处理代码推送和冲突
- 支持选择公开/私有仓库

**触发词**: 上传到 GitHub、推送代码、push、传上去

---

#### 7. Iteration Planner - 项目迭代规划器

**命令**: `/iteration-planner`

**功能**:
- 分析代码库现状
- 提出功能迭代建议
- 生成开发路线图

**触发词**: 迭代规划、功能规划、下一步做什么、版本规划

### 内容处理与文件操作 (10个)

#### 8. PDF - PDF 处理工具

**命令**: `/pdf`

**功能**: PDF 文档的提取、合并、分割、表单填写

#### 9. DOCX - Word 文档处理

**命令**: `/docx`

**功能**: Word 文档的创建、编辑、批注、修订

#### 10. XLSX - Excel 表格处理

**命令**: `/xlsx`

**功能**: Excel 表格的创建、编辑、数据分析

#### 11. PPTX - PowerPoint 演示文稿

**命令**: `/pptx`

**功能**: PPT 演示文稿的创建、编辑、分析

#### 12. Summarize Folder - 目录总结

**命令**: `/summarize-folder`

**功能**: 遍历目录、提取多种格式文件内容、生成结构化总结

**触发词**: 总结这个目录、分析这个文件夹、看看这个目录有什么

#### 13. Bookmark - 收藏夹管理

**命令**: `/bookmark`

**功能**: 保存和管理链接收藏，支持标签分类

**触发词**: 收藏、存个链接、查看收藏

### 信息获取与聚合 (4个)

#### 14. Daily Hot Fetcher - 全平台热门信息

**命令**: `/daily-hot-fetcher`

**功能**:
- 抓取国内外各平台热门信息（微博、知乎、抖音、B站等）
- 抓取国外热门（Hacker News、Reddit、Product Hunt）
- 实时搜索和管理登录状态

**触发词**: 今天有什么热点、看看热搜、热门话题、今天流行什么

#### 15. Multi-Platform Content Fetcher - 多平台内容获取

**命令**: `/multi-platform-content-fetcher`

**功能**: 从微信公众号、小红书、知乎、博客RSS等平台获取内容并存储

#### 16. Prompt Packs - 提示词库

**命令**: `/prompt-packs` 或 `/pp`

**功能**: OpenAI Academy 200+ 企业场景提示词库

**触发词**: 提示词、prompt、提示库

#### 17. Daily Topic Selector - 每日选题助手

**命令**: `/daily-topic-selector`

**功能**: 监控 Import AI、Hacker News 等高质量内容源，推荐选题

#### 18. WeChat Article Chat - 微信公众号文章对话

**命令**: `/wechat-article-chat`

**功能**:
- 获取公众号文章完整内容
- 与 AI 进行智能问答和深度分析
- 提供文章总结、观点提炼、延伸思考

**触发词**: 分析公众号文章、公众号对话、解读这篇文章

### 书籍与阅读 (4个)

#### 19. Zlibrary - 电子书搜索与下载

**命令**: `/zlibrary`

**功能**: 搜索、获取详情、下载电子书、收藏管理

**触发词**: 搜索电子书、找书、下载书、zlibrary

#### 20. EPUB to Markdown - EPUB 转换器

**命令**: `/epub-to-markdown`

**功能**: 提取 EPUB 内容并转换为 Markdown 格式，支持章节分割

#### 21. Book Interpreter - 书籍解读 (Ezra 风格)

**命令**: `/book-interpreter`

**功能**: 将书籍转换为对话式中文文章，使用生活化语言、术语解释、生活类比

#### 22. Book Content Workflow - 书籍内容生产工作流

**命令**: `/book-content-workflow`

**功能**: 整合 zlibrary、epub-to-markdown、book-interpreter、volcano-images，实现从搜索书籍到生成解读文章的完整流程

**触发词**: 解读《书名》、完成《书名》的完整解读流程、生成读书笔记

### 媒体处理 (2个)

#### 23. Video Downloader - 视频下载器

**命令**: `/video-downloader`

**功能**: 使用 yt-dlp 和 ffmpeg 下载视频

#### 24. Volcano Images - 火山引擎图片生成

**命令**: `/volcano-images`

**功能**: 使用火山引擎（即梦/Jimeng）API 生成图片，支持 New Yorker 风格插图

**触发词**: 生成图片、配图、即梦、jimeng

### 前端开发与设计 (9个)

#### 25. Frontend Design - 前端设计

**命令**: `/frontend-design`

**功能**: 创建高质量的前端界面和组件

#### 19. Frontend Test - 前端测试套件

**命令**: `/frontend-test`

**功能**: UI 测试、功能测试、性能分析、代码质量审查

#### 20. UI Optimizer - UI 优化器

**命令**: `/ui-optimizer`

**功能**: DocPilot 项目的 UI 优化专家（Notion 风格设计系统）

#### 21. Canvas Design - 视觉设计

**命令**: `/canvas-design`

**功能**: 创建精美的视觉艺术作品（PNG/PDF 格式）

#### 22. Theme Factory - 主题工厂

**命令**: `/theme-factory`

**功能**: 为文档应用预设主题样式

#### 23. Algorithmic Art - 算法艺术

**命令**: `/algorithmic-art`

**功能**: 使用 p5.js 创建算法生成艺术

#### 24. Brand Guidelines - 品牌规范

**命令**: `/brand-guidelines`

**功能**: 应用 Anthropic 官方品牌颜色和排版

#### 34. Web Artifacts Builder - Web 构件构建器

**命令**: `/web-artifacts-builder`

**功能**: 使用 React、Tailwind CSS、shadcn/ui 创建复杂的 HTML 构件

#### 35. Visual Interface Generator - 可视化界面生成器

**命令**: `/visual-interface-generator`

**功能**: 为 Skill 自动生成可视化进度界面

**触发词**: 为这个Skill创建可视化界面、为xxx添加进度显示

### 后端开发与分析 (4个)

#### 36. Backend Checker - 后端代码分析器

**命令**: `/backend-checker`

**功能**: Python/FastAPI/Flask/Django 项目的安全、性能、代码质量分析

#### 37. MCP Builder - MCP 服务器构建器

**命令**: `/mcp-builder`

**功能**: 创建高质量的 Model Context Protocol 服务器

#### 38. Webapp Testing - Web 应用测试

**命令**: `/webapp-testing`

**功能**: 使用 Playwright 进行本地 Web 应用测试

#### 39. Project Optimizer - 项目优化器

**命令**: `/project-optimizer`

**功能**: 分析项目并提供优化建议

### 工具与实用功能 (7个)

#### 40. Visual Progress - 可视化进度框架

**命令**: `/visual-progress`

**功能**:
- 美观的终端进度条
- 任务列表显示
- 批处理进度跟踪
- 多主题支持（彩色、极简、深色、森林、海洋）

**触发词**: 显示进度、进度条、工作流跟踪、批处理进度

#### 41. Skill Creator - Skill 创建器

**命令**: `/skill-creator`

**功能**: 指导创建新的 Claude Code Skill

#### 42. UI Skills - UI 技能约束

**命令**: `/ui-skills`

**功能**: 构建更好 UI 界面的约束条件

#### 43. Doc Coauthoring - 文档协作

**命令**: `/doc-coauthoring`

**功能**: 结构化文档协作工作流

#### 44. Internal Comms - 内部沟通

**命令**: `/internal-comms`

**功能**: 生成内部沟通文档（状态报告、领导层更新等）

#### 45. Slack Gif Creator - Slack GIF 创建器

**命令**: `/slack-gif-creator`

**功能**: 创建优化的 Slack 动画 GIF

#### 46. Auto Redbook Skills - 小红书笔记创作

**命令**: `/auto-redbook-skills`

**功能**: 小红书笔记素材创作（标题+正文+图片卡片）

### 中文处理与优化 (2个)

#### 47. Humanizer ZH - 中文人性化处理

**命令**: `/humanizer-zh`

**功能**: 去除文本中的 AI 生成痕迹，使文本更自然

#### 48. Docpilot Code Style - DocPilot 代码风格

**命令**: `/docpilot-code-style`

**功能**: DocPilot 项目代码风格检查

### 其他工具

#### GH Analyze - GitHub 分析

**命令**: `/gh-analyze`

**功能**: GitHub 仓库分析

#### Analyze Project Style - 项目风格分析

**命令**: `/analyze-project-style`

**功能**: 分析项目代码风格

---

本仓库现在包含 **46 个 Claude Code Skills**，涵盖开发工作流的各个环节。

## 典型工作流

### 从想法到上线的完整流程

```
1. 我想做一个博客          → /pm 帮你完善想法，输出 PROJECT.md
2. 帮我生成开发文档        → /dev-doc 生成技术架构和 TASKS.md
3. 开始开发首页            → /pre-dev 澄清需求后开始编码
4. 首页做完了              → /dev-track 更新进度
5. 改完了，帮我提交        → /commit 生成规范的提交信息
6. 推送到 GitHub           → /github-upload 推送代码
```

## 优先级规则

当你的话可能匹配多个 skill 时，系统会自动选择优先级最高的：

| 优先级 | Skill | 说明 |
|--------|-------|------|
| 95 | summarize-folder | 目录遍历和文件总结 |
| 90 | commit | 明确的提交意图，最精确 |
| 88 | daily-hot-fetcher | 全平台热门信息获取 |
| 85 | prompt-packs | 提示词库 |
| 80 | visual-progress | 可视化进度显示 |
| 75 | github-upload | 明确的上传/推送意图 |
| 70 | dev-doc | 有明确的文档生成需求 |
| 60 | pm | 产品规划阶段，想法模糊 |
| 50 | dev-track | 进度跟踪 |
| 45 | visual-interface-generator | 进度界面生成 |
| 40 | bookmark | 收藏管理 |
| 35 | backend-checker | 后端代码分析 |
| 30 | pre-dev | 通用开发任务（兜底） |

**冲突处理示例**:
- 「提交代码」→ 触发 `/commit`（不是 `/github-upload`）
- 「我想做一个登录功能」→ 触发 `/pm`（不是 `/pre-dev`）
- 「总结这个目录」→ 触发 `/summarize-folder`（高优先级）

## 文件结构

```
~/.claude/skills/
├── SKILLS-INDEX.md      # 统一触发索引（Claude 参考用）
├── README.md            # 本文件
├── pm/
│   └── SKILL.md         # 产品经理助手
├── dev-doc/
│   └── SKILL.md         # 开发文档生成器
├── pre-dev/
│   └── SKILL.md         # 开发前指南
├── github-upload/
│   └── SKILL.md         # GitHub 上传
├── dev-track/
│   ├── SKILL.md         # 进度跟踪器
│   └── TEMPLATE.md      # 进度文档模板
├── bookmark/
│   └── SKILL.md         # 收藏夹管理
└── commit/
    └── SKILL.md         # Git 提交助手
```

## 自定义 Skill

如果你想创建自己的 skill，只需：

1. 在 `~/.claude/skills/` 下创建新目录
2. 添加 `SKILL.md` 文件，包含：
   - YAML frontmatter（name, description, triggers, priority）
   - 详细的执行流程说明

参考现有 skill 的格式即可。

## 常见问题

**Q: Skill 没有被触发？**
- 检查安装路径是否正确
- 确认 SKILL.md 文件存在
- 尝试使用斜杠命令直接调用

**Q: 如何更新 skills？**
```bash
cd ~/.claude/skills
git pull
```

**Q: 如何卸载？**
```bash
rm -rf ~/.claude/skills
```

## License

MIT
