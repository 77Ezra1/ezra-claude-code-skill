---
name: commit
description: '创建格式良好的 Git 提交 - 使用 Conventional Commit 规范生成提交信息。


  使用场景：当用户提到 「提交代码」、「提交更改」、「提交一下」、「帮我提交」、「写提交信息」、「生成提交信息」、「保存更改」、「保存代码」、「记录更改」、「做个提交」
  等关键词时触发此技能。'
user-invocable: true
---

# Commit: Git 提交助手

创建格式良好的 Git 提交，使用 Conventional Commit 规范自动生成提交信息。

## 适用场景

- 用户说「提交代码」「帮我 commit」
- 用户说「提交这些更改」「写个提交信息」
- 用户完成功能开发后需要提交
- 需要规范化的提交信息

## 与 github-upload 的区别

| 场景 | 使用 Skill |
|------|------------|
| 只需本地提交 | `/commit` |
| 需要推送到远程 | `/github-upload` |
| 创建远程仓库 | `/github-upload` |

## Conventional Commit 规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat: add user login |
| fix | Bug 修复 | fix: resolve memory leak |
| docs | 文档更新 | docs: update README |
| style | 代码格式 | style: format code |
| refactor | 重构 | refactor: simplify logic |
| perf | 性能优化 | perf: optimize query |
| test | 测试相关 | test: add unit tests |
| chore | 杂项 | chore: update deps |
| ci | CI/CD | ci: fix build script |

### Scope（可选）

表示影响范围，如：
- `feat(auth)`: 认证相关功能
- `fix(ui)`: UI 相关修复
- `docs(api)`: API 文档

## 执行流程

### 步骤 1: 检查状态

```bash
git status
git diff --stat
```

如果没有更改，告知用户并结束。

### 步骤 2: 分析更改

1. 查看 staged 和 unstaged 的更改
2. 分析更改类型（新增/修改/删除）
3. 识别主要改动的模块

### 步骤 3: 生成提交信息

根据更改内容自动生成符合规范的提交信息：

```bash
git diff --cached  # 查看 staged 更改
git diff           # 查看 unstaged 更改
```

### 步骤 4: 执行提交

```bash
git add .  # 如果需要
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>
EOF
)"
```

### 步骤 5: 确认结果

```bash
git log -1 --oneline
git status
```

## 命令示例

```
用户：提交代码
助手：检测到以下更改：
- 新增 src/auth/login.ts
- 修改 src/components/Button.tsx
- 删除 src/utils/deprecated.ts

建议提交信息：
feat(auth): add user login functionality

- Add login form component
- Implement authentication logic
- Remove deprecated utilities

是否使用此提交信息？

用户：好的
助手：✅ 提交成功
commit abc1234: feat(auth): add user login functionality
```

## 安全检查

提交前自动检查：

1. **敏感文件**: .env, credentials, private keys
2. **大文件**: 超过 10MB 的文件
3. **调试代码**: console.log, debugger 等

如发现问题，警告用户并建议处理方式。

## 快捷命令

- `/commit` - 自动分析并提交
- `/commit -m "message"` - 使用指定信息提交
- `/commit --amend` - 修改上次提交（谨慎使用）
