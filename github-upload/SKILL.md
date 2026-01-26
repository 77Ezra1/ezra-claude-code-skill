---
name: github-upload
description: 上传项目到 GitHub - 自动创建仓库、处理提交和冲突。提交后自动更新说明文档。
user-invocable: true
---


# GitHub Upload: 项目上传到 GitHub

自动化将项目上传到 GitHub，智能处理仓库创建、代码提交和冲突解决。

## 适用场景

以下情况应该触发此 skill：

- 用户说「上传到 GitHub」「推送到 GitHub」「提交到 GitHub」
- 用户说「帮我提交 skill 到 GitHub 上」
- 用户说「同步代码到远程仓库」「推送代码」
- 用户说「创建 GitHub 仓库并上传」

## 执行流程

### 阶段 1: 环境检查

1. **检查 Git 初始化状态**
   ```bash
   git rev-parse --is-inside-work-tree
   ```
   - 如果不是 git 仓库，询问用户是否初始化

2. **检查 GitHub CLI 认证**
   ```bash
   gh auth status
   ```
   - 如果未认证，提示用户先运行 `gh auth login`

3. **获取当前目录信息**
   - 确定项目名称（从目录名或 package.json）
   - 检查是否有远程仓库配置

### 阶段 2: 仓库状态判断

使用以下命令检查远程仓库：

```bash
git remote -v
```

**场景 A: 无远程仓库** → 进入「创建仓库流程」
**场景 B: 有远程仓库** → 进入「同步提交流程」

---

## 场景 A: 创建仓库流程

### 步骤 1: 确认仓库信息

使用 `AskUserQuestion` 询问用户：

1. **仓库名称**: 默认使用当前目录名
2. **仓库可见性**:
   - Public（公开）
   - Private（私有，推荐）
3. **仓库描述**: 可选

### 步骤 2: 创建 GitHub 仓库

```bash
gh repo create <repo-name> --private --source=. --remote=origin --description="<description>"
```

或者分步执行：

```bash
# 创建远程仓库
gh repo create <repo-name> --private --description="<description>"

# 添加远程地址
git remote add origin https://github.com/<username>/<repo-name>.git
```

### 步骤 3: 初始提交并推送

```bash
# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit"

# 推送到远程
git push -u origin main
```

### 步骤 4: 确认结果

```bash
# 显示仓库 URL
gh repo view --web
```

---

## 场景 B: 同步提交流程

### 步骤 1: 检查本地状态

```bash
# 查看未提交的更改
git status

# 查看具体更改内容
git diff --stat
```

如果没有更改，告知用户「没有需要提交的更改」并结束。

### 步骤 2: 拉取远程更新

```bash
# 获取远程更新
git fetch origin

# 检查是否有远程更新
git status
```

### 步骤 3: 处理冲突情况

**情况 1: 本地领先远程（无冲突）**
- 直接进入提交流程

**情况 2: 远程领先本地**
- 先拉取并合并
  ```bash
  git pull origin main
  ```

**情况 3: 存在冲突**
- **必须使用 `AskUserQuestion` 询问用户**：

  ```
  检测到代码冲突，请选择处理方式：

  1. 查看冲突文件详情
  2. 使用本地版本覆盖（强制推送）
  3. 使用远程版本覆盖（放弃本地更改）
  4. 手动解决冲突（我来处理）
  5. 暂时取消操作
  ```

### 步骤 4: 提交更改

```bash
# 查看要提交的更改
git diff --cached
git diff

# 添加更改
git add .

# 生成有意义的提交信息
git commit -m "<根据更改内容生成的提交信息>"
```

**提交信息规范**：
- feat: 新功能
- fix: 修复 bug
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- chore: 杂项更新

### 步骤 5: 推送到远程

```bash
git push origin main
```

---

## 冲突解决流程（详细）

当检测到冲突时，**必须**执行以下流程：

### 1. 显示冲突信息

```bash
# 列出冲突文件
git diff --name-only --diff-filter=U

# 显示冲突详情
git diff
```

### 2. 询问用户处理方式

使用 `AskUserQuestion` 工具，提供以下选项：

**选项说明**：

| 选项 | 说明 | 风险 |
|------|------|------|
| 查看详情 | 显示每个冲突文件的具体差异 | 无 |
| 使用本地版本 | 强制推送本地版本，覆盖远程 | 会丢失远程更改 |
| 使用远程版本 | 放弃本地更改，使用远程版本 | 会丢失本地更改 |
| 手动解决 | 让用户自己编辑冲突文件 | 无 |
| 取消操作 | 暂时不处理，保持当前状态 | 无 |

### 3. 根据用户选择执行

**使用本地版本**：
```bash
git push --force-with-lease origin main
```

**使用远程版本**：
```bash
git checkout --theirs .
git add .
git commit -m "Resolve conflicts using remote version"
git push origin main
```

**手动解决**：
```bash
# 列出需要手动解决的文件
git diff --name-only --diff-filter=U
```
告知用户需要手动编辑这些文件，解决后运行：
```bash
git add .
git commit -m "Resolve merge conflicts"
git push origin main
```

---

## 特殊处理

### .gitignore 检查

提交前检查是否存在 .gitignore，如果不存在，建议创建：

```bash
# 检查 .gitignore
if [ ! -f .gitignore ]; then
    echo "建议创建 .gitignore 文件"
fi
```

常见需要忽略的内容：
- node_modules/
- .env
- .env.local
- dist/
- build/
- *.log

### 敏感文件检查

提交前检查是否包含敏感文件：
- .env 文件
- 私钥文件
- credentials.json
- *.pem

如果检测到，**警告用户**并建议添加到 .gitignore。

---

## 输出格式

### 成功创建仓库

```
✓ GitHub 仓库创建成功！

仓库地址: https://github.com/<username>/<repo-name>
可见性: Private
初始提交: xxxxxxx

下一步:
- 访问仓库: gh repo view --web
- 查看状态: git status
```

### 成功推送

```
✓ 代码已推送到 GitHub！

提交: abc1234 - feat: add new feature
推送: main → origin/main
更改: 3 files changed, 42 insertions(+), 10 deletions(-)

仓库地址: https://github.com/<username>/<repo-name>
```

### 冲突提示

```
⚠ 检测到代码冲突

冲突文件:
- src/index.ts
- package.json

请选择处理方式...
```

---

## 安全原则

1. **永远不要强制推送**，除非用户明确同意
2. **发现冲突必须询问用户**，不能自动覆盖
3. **检查敏感文件**，防止泄露密钥
4. **使用 --force-with-lease** 而非 --force，更安全

---

## 提交后自动更新说明文档

当仓库包含说明文档（如 README.md、SKILLS-INDEX.md）且项目结构发生变化时，提交后应自动更新这些文档。

### 检测项目类型

在提交后，检查项目是否为以下类型：

**1. Claude Code Skills 仓库**

检测特征：
- 存在 `SKILLS-INDEX.md` 文件
- 存在多个 `*/SKILL.md` 文件

**2. 普通项目仓库**

检测特征：
- 存在 `README.md` 文件
- 可能存在其他文档文件

### Skills 仓库文档更新流程

**步骤 1: 扫描 skill 目录**

```bash
# 查找所有 skill 目录
find . -name "SKILL.md" -type f | grep -v ".git" | sort
```

**步骤 2: 提取 skill 信息**

从每个 `SKILL.md` 提取：
- `name`: skill 名称
- `description`: 描述
- `priority`: 优先级（如果有）
- `triggers`: 触发词（如果有）

**步骤 3: 更新 SKILLS-INDEX.md**

根据扫描结果，生成/更新：
- 按分类组织的触发词表
- 优先级规则
- 意图分类

**步骤 4: 更新 README.md**

更新内容：
- Skills 总数统计
- 按分类的 skills 列表
- 典型工作流示例

**步骤 5: 提交文档更新**

```bash
# 如果文档有变化，自动提交
git add SKILLS-INDEX.md README.md
git commit -m "docs: auto-update skills documentation"
git push origin main
```

### 普通项目文档更新流程

**步骤 1: 分析项目结构**

```bash
# 检查项目类型
if [ -f "package.json" ]; then
    # Node.js 项目
    echo "Node.js 项目"
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    # Python 项目
    echo "Python 项目"
elif [ -f "go.mod" ]; then
    # Go 项目
    echo "Go 项目"
fi
```

**步骤 2: 更新 README.md**

根据项目变化更新：
- 安装/使用说明
- 功能列表
- 项目结构图
- 依赖项列表

**步骤 3: 检查文档完整性**

确保以下内容是最新的：
- 项目描述
- 安装步骤
- 配置说明
- 使用示例
- API 文档（如果有）

### 自动更新触发条件

当满足以下条件时，自动触发文档更新：

| 条件 | 说明 |
|------|------|
| 新增 skill | 检测到新的 `*/SKILL.md` 文件 |
| 删除 skill | 之前存在的 skill 目录消失 |
| 修改 skill | `SKILL.md` 内容有变化 |
| 新增文件 | 项目根目录新增了文件 |
| 结构变化 | 目录结构发生变化 |

### 实现示例

```bash
# 伪代码：文档自动更新逻辑
if project_is_skills_repo; then
    scan_skills()
    update_skills_index()
    update_readme()

    if git diff --quiet; then
        echo "文档已是最新，无需更新"
    else
        git add SKILLS-INDEX.md README.md
        git commit -m "docs: auto-update skills documentation"
        git push origin main
        echo "✓ 文档已自动更新"
    fi
fi
```

---

## 快捷命令

用户可以直接说：
- 「上传到 GitHub」- 执行完整流程
- 「推送代码」- 仅推送（需要已有远程仓库）
- 「创建仓库」- 仅创建远程仓库
