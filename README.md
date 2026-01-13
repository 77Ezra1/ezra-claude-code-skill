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

### 1. Commit - Git 提交助手

**命令**: `/commit`
**优先级**: 90（最高）

**功能**:
- 自动分析代码变更
- 生成符合 Conventional Commit 规范的提交信息
- 检查敏感文件，防止泄露

**触发词**: 提交代码、commit、存一下、改完了、搞定了

**示例**:
```
用户: 改完了，帮我提交
Claude: 检测到以下更改...建议提交信息: feat(auth): add user login
```

---

### 2. GitHub Upload - 上传到 GitHub

**命令**: `/github-upload`
**优先级**: 80

**功能**:
- 自动创建 GitHub 仓库（如不存在）
- 处理代码推送和冲突
- 支持选择公开/私有仓库

**触发词**: 上传到 GitHub、推送代码、push、传上去

**示例**:
```
用户: 帮我把代码推到 GitHub
Claude: 检测到无远程仓库，是否创建新仓库？
```

---

### 3. PM - 产品经理助手

**命令**: `/pm`
**优先级**: 60

**功能**:
- 通过结构化追问完善产品想法
- 帮助明确核心功能和技术方案
- 输出可落地的项目规划文档 (PROJECT.md)

**触发词**: 我想做一个、有个想法、帮我规划、想搞个

**示例**:
```
用户: 我想做一个个人博客
Claude: 好的，让我来帮你规划。首先，这个博客的目标用户是谁？
```

---

### 4. Dev-Doc - 开发文档生成器

**命令**: `/dev-doc`
**优先级**: 70

**功能**:
- 将项目规划转化为技术开发文档
- 生成技术架构、API 设计、数据库设计
- 输出可执行的任务清单 (TASKS.md)

**前置条件**: 需要先有 PROJECT.md 项目规划文档

**触发词**: 生成开发文档、技术架构、落地方案、任务拆分

**示例**:
```
用户: 帮我把规划转成开发文档
Claude: 我来读取 PROJECT.md，为你生成技术架构和任务清单...
```

---

### 5. Dev-Track - 项目进度跟踪

**命令**: `/dev-track`
**优先级**: 50

**功能**:
- 基于 TASKS.md 维护项目进度
- 标记任务完成状态
- 展示进度百分比和进度条

**触发词**: 更新进度、查看进度、做到哪了、xxx完成了

**示例**:
```
用户: 登录功能做完了
Claude: 已将「2.1 用户登录」标记为完成。总体进度 25%。
```

---

### 6. Bookmark - 收藏夹管理

**命令**: `/bookmark`
**优先级**: 40

**功能**:
- 保存和管理链接收藏
- 支持标签和文件夹分类
- 搜索收藏内容

**触发词**: 收藏、存个链接、查看收藏、添加书签

**示例**:
```
用户: 收藏 https://example.com
Claude: 已收藏「Example」。需要添加标签吗？
```

---

### 7. Pre-Dev - 开发前指南

**命令**: `/pre-dev`
**优先级**: 30（兜底）

**功能**:
- 在编码前澄清需求
- 确认实现方案
- 避免返工

**触发词**: 开始开发、帮我实现、开干、搞起来

**示例**:
```
用户: 帮我实现用户登录功能
Claude: 在开始之前，让我确认几个问题：1. 使用什么认证方式？
```

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

```
commit (90) > github-upload (80) > dev-doc (70) > pm (60) > dev-track (50) > bookmark (40) > pre-dev (30)
```

**冲突处理示例**:
- 「提交代码」→ 触发 `/commit`（不是 `/github-upload`）
- 「我想做一个登录功能」→ 触发 `/pm`（不是 `/pre-dev`）

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
