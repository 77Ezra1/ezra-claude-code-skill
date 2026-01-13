---
name: github-upload
description: 上传项目到 GitHub - 自动创建仓库、处理提交和冲突
version: 1.0.0
triggers:
  keywords:
    # 中文表达
    - "上传到 GitHub"
    - "推送到 GitHub"
    - "提交到 GitHub"
    - "同步到远程"
    - "推送代码"
    - "创建仓库"
    - "创建 GitHub 仓库"
    - "传到远程"
    - "发布到 GitHub"
    - "同步代码"
    # 英文/混合表达
    - "push"
    - "git push"
    - "push to github"
    - "upload to github"
    # 口语化表达
    - "传上去"
    - "推上去"
    - "发到 GitHub"
    - "放到 GitHub"
  patterns:
    - "*到 GitHub"
    - "推送*"
    - "上传*到*"
    - "同步*远程*"
    - "*传到*"
    - "push*"
  intents:
    - code-upload
    - git-push
    - repo-create
priority: 80
conflicts:
  - commit
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

## 快捷命令

用户可以直接说：
- 「上传到 GitHub」- 执行完整流程
- 「推送代码」- 仅推送（需要已有远程仓库）
- 「创建仓库」- 仅创建远程仓库
