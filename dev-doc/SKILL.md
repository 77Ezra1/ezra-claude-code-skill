---
name: dev-doc
description: 开发文档生成器 - 当用户有项目规划文档（如 PROJECT.md）并希望生成可落地的开发文档时使用。将产品规划转化为技术架构、API 设计、数据库 schema、组件设计、任务拆分等开发文档。
version: 1.0.0
triggers:
  keywords:
    # 标准表达
    - "生成开发文档"
    - "写技术文档"
    - "转成开发方案"
    - "怎么开始开发"
    - "技术架构"
    - "API 设计"
    - "数据库设计"
    - "组件设计"
    - "任务拆分"
    # 口语化表达
    - "落地方案"
    - "出个方案"
    - "怎么落地"
    - "拆分任务"
    - "拆成任务"
    - "开发方案"
    - "技术方案"
    - "设计文档"
  patterns:
    - "生成*文档"
    - "写*文档"
    - "*转成*方案"
    - "设计*架构"
    - "出个*方案"
    - "*怎么落地"
    - "拆分*"
    - "*拆成任务"
  intents:
    - doc-generation
    - architecture-design
    - planning-to-dev
priority: 70
conflicts: []
preconditions:
  - "存在 PROJECT.md 或类似的项目规划文档"
---

# Dev-Doc: 开发文档生成器

将项目规划文档转化为可落地的技术开发文档，让开发工作有章可循。

## 适用场景

以下情况应该触发此 skill：

- 用户说「生成开发文档」「写技术文档」「转成开发方案」
- 用户有 PROJECT.md 或类似的项目规划文档
- 用户说「帮我把这个规划落地」「怎么开始开发」
- 用户需要技术架构、API 设计、数据库设计等文档

## 执行流程

### 阶段 1: 定位项目规划

1. 确认项目规划文档的位置
2. 读取并理解项目规划文档
3. 提取关键信息：
   - 技术栈选型
   - 功能列表
   - 数据模型
   - 页面规划
   - 设计要求

### 阶段 2: 确认文档范围

询问用户需要生成哪些开发文档：

1. **技术架构文档** - 整体架构、目录结构、技术决策
2. **数据库设计** - Prisma Schema、表关系、索引设计
3. **API 设计** - 接口列表、请求/响应格式、错误码
4. **组件设计** - UI 组件拆分、组件树、Props 定义
5. **开发任务清单** - 具体可执行的开发任务
6. **全部生成** - 一次性生成所有文档

### 阶段 3: 逐个生成文档

根据用户选择，按以下模板生成对应文档。

---

## 文档模板

### 1. 技术架构文档 (ARCHITECTURE.md)

```markdown
# 技术架构文档

## 技术栈

| 层面 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 框架 | Next.js | 14.x | App Router |
| ... | ... | ... | ... |

## 目录结构

\`\`\`
项目名/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── (site)/          # 前台路由组
│   │   ├── admin/           # 后台路由
│   │   └── api/             # API 路由
│   ├── components/          # 组件
│   │   ├── ui/              # 基础 UI 组件
│   │   ├── features/        # 功能组件
│   │   └── layouts/         # 布局组件
│   ├── lib/                 # 工具库
│   ├── hooks/               # 自定义 Hooks
│   ├── types/               # TypeScript 类型
│   └── styles/              # 全局样式
├── prisma/                  # 数据库
├── public/                  # 静态资源
└── ...
\`\`\`

## 架构决策记录 (ADR)

### ADR-001: [决策标题]
- **状态**: 已采纳
- **背景**: ...
- **决策**: ...
- **后果**: ...

## 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| DATABASE_URL | 数据库连接 | postgresql://... |
| ... | ... | ... |
```

### 2. 数据库设计文档 (DATABASE.md + schema.prisma)

```markdown
# 数据库设计文档

## ER 图

[描述实体关系]

## 表设计

### User 表
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| ... | ... | ... | ... |

## 索引设计

| 表 | 索引名 | 字段 | 类型 |
|----|--------|------|------|
| Post | idx_post_slug | slug | UNIQUE |
| ... | ... | ... | ... |

## Prisma Schema

见 prisma/schema.prisma
```

同时生成完整的 `schema.prisma` 文件。

### 3. API 设计文档 (API.md)

```markdown
# API 设计文档

## 基础信息

- Base URL: `/api`
- 认证方式: JWT / Session
- 响应格式: JSON

## 通用响应结构

\`\`\`typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
  }
}
\`\`\`

## 接口列表

### 文章模块

#### GET /api/posts
获取文章列表

**Query 参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | number | 否 | 页码，默认 1 |
| ... | ... | ... | ... |

**响应示例**
\`\`\`json
{
  "success": true,
  "data": {
    "posts": [...],
    "total": 100
  }
}
\`\`\`

#### POST /api/posts
创建文章

**请求体**
\`\`\`typescript
interface CreatePostRequest {
  title: string
  content: string
  categoryId?: string
  tags?: string[]
}
\`\`\`

...
```

### 4. 组件设计文档 (COMPONENTS.md)

```markdown
# 组件设计文档

## 组件分类

### UI 基础组件 (ui/)
通用的、无业务逻辑的基础组件

| 组件 | 说明 | Props |
|------|------|-------|
| Button | 按钮 | variant, size, disabled |
| ... | ... | ... |

### 功能组件 (features/)
带有业务逻辑的功能组件

| 组件 | 说明 | 依赖 |
|------|------|------|
| PostCard | 文章卡片 | ui/Card, ui/Tag |
| ... | ... | ... |

### 布局组件 (layouts/)

| 组件 | 说明 | 使用场景 |
|------|------|----------|
| SiteLayout | 前台布局 | 所有前台页面 |
| ... | ... | ... |

## 组件详细设计

### PostCard

**Props**
\`\`\`typescript
interface PostCardProps {
  post: Post
  variant?: 'default' | 'compact'
  showExcerpt?: boolean
}
\`\`\`

**使用示例**
\`\`\`tsx
<PostCard post={post} variant="compact" />
\`\`\`
```

### 5. 开发任务清单 (TASKS.md)

```markdown
# 开发任务清单

## 阶段 1: xxx

### 1.1 任务名称
- [ ] 子任务 1
- [ ] 子任务 2
- **产出**: 描述完成后的产出物
- **验收**: 如何验证任务完成

### 1.2 任务名称
...

## 阶段 2: xxx
...
```

---

## 输出规范

1. **文档位置**: 所有文档放在项目根目录的 `docs/` 文件夹下
2. **命名规范**: 使用大写字母 + 下划线命名，如 `API.md`、`DATABASE.md`
3. **Prisma Schema**: 放在 `prisma/schema.prisma`
4. **代码示例**: 使用 TypeScript，包含类型定义

## 生成原则

1. **可执行性**: 每个文档都应该能直接指导开发，不是空泛的描述
2. **一致性**: 命名、格式、风格保持一致
3. **完整性**: 覆盖所有规划中的功能点
4. **渐进性**: 按开发阶段组织，优先级清晰
5. **类型安全**: 所有接口、组件都有 TypeScript 类型定义

## 交互方式

使用 `AskUserQuestion` 工具询问用户：
1. 项目规划文档的位置
2. 需要生成哪些文档
3. 是否有特殊要求或约定

生成完成后：
1. 列出生成的所有文件
2. 简要说明每个文件的作用
3. 建议下一步行动
