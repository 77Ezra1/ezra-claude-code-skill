# DocPilot 代码风格规范

> 本文件定义了 DocPilot 项目的代码风格规范，所有代码修改和样式调整都必须遵守这些原则。

---

## 前端风格规范 (frontend/)

### 1. 代码格式化

**Prettier 配置：**
```json
{
  "semi": false,           // 不使用分号
  "singleQuote": true,     // 使用单引号
  "tabWidth": 2,           // 2 空格缩进
  "trailingComma": "es5",  // ES5 尾随逗号
  "printWidth": 100,       // 每行最大 100 字符
  "arrowParens": "avoid",  // 箭头函数单参数时省略括号
  "endOfLine": "lf"        // LF 换行符
}
```

**必须遵守：**
- 无分号结尾
- 使用单引号
- 2 空格缩进
- 行宽不超过 100 字符

### 2. TypeScript 规范

**严格模式启用，关键规则：**
```typescript
// 正确
import type { Message } from '@/types/chat'

const isLoading = false
const hasPermission = true

// 事件处理函数使用 handle 前缀
const handleClick = useCallback(() => {}, [])

// 禁止 any 类型，使用具体类型或 unknown
const data: unknown = response.data
```

### 3. 组件规范

**页面组件 (pages/)：**
```typescript
// 使用 default export
export default function ChatPage() {
  return <div>...</div>
}
```

**通用组件 (components/)：**
```typescript
// 使用 named export
export function AppLayout({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

**组件文件结构：**
```
ComponentName/
├── ComponentName.tsx
├── ComponentName.module.scss
└── index.ts (可选，用于统一导出)
```

### 4. 样式规范 (CSS Modules + SCSS)

**必须使用 `.module.scss` 文件**

**命名规范：**
```scss
// 类名使用 camelCase
.messageBubble { }
.userAvatar { }
.chatContainer { }

// 使用 CSS 自定义属性
background: var(--color-bg-secondary);
padding: var(--spacing-md);
border-radius: var(--radius-lg);
transition: all var(--transition-normal);
```

**SCSS 嵌套规范：**
```scss
.messageBubble {
  margin-bottom: 24px;

  .messageWrapper {
    display: flex;
    gap: 12px;
  }

  &:last-child {
    margin-bottom: 0;
  }

  &.user { }

  &.assistant { }
}
```

**禁止使用：**
- 内联样式 (除了动态计算值)
- 全局 CSS (使用 :global 包裹必要的全局样式)
- CSS-in-JS 库

### 5. 导入顺序

```typescript
/**
 * 组件描述
 */
// 1. React 相关
import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'

// 2. 第三方库
import { useQuery } from '@tanstack/react-query'

// 3. 内部组件 (使用 @/ 别名)
import { Button } from '@/components/ui/Button'
import { useAuthStore } from '@/stores/authStore'

// 4. 类型导入
import type { Message, ChatSession } from '@/types'

// 5. 样式文件
import styles from './ChatPage.module.scss'

// 6. 相对路径导入 (避免，优先使用 @/)
import { LocalComponent } from './components/LocalComponent'
```

### 6. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件 | PascalCase | `ChatPage`, `MessageBubble`, `AppLayout` |
| 函数 | camelCase | `handleSend`, `formatTime`, `fetchData` |
| 变量 | camelCase | `isLoading`, `hasPermission`, `userName` |
| 布尔值 | is/has 前缀 | `isUser`, `isAdmin`, `hasPermission` |
| 接口/类型 | PascalCase | `ChatSession`, `Message`, `ApiResponse` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| 文件 | PascalCase | `ChatPage.tsx`, `useAuth.ts` |

### 7. Hooks 规范

```typescript
// 自定义 Hook 使用 use 前缀
export function useWebSocket() { }
export function useAuth() { }

// 事件处理函数使用 useCallback 包装
const handleClick = useCallback(() => {
  navigate('/chat')
}, [navigate])
```

### 8. 类型定义规范

```typescript
// 使用 interface 定义对象结构
interface User {
  id: string
  name: string
  email: string
}

// 使用 type 定义联合类型、交叉类型
type Status = 'online' | 'offline' | 'away'
type MessageWithUser = Message & { user: User }

// 导出类型使用
export type { Message, ChatSession }
```

---

## 后端风格规范 (backend/)

### 1. 代码格式化

**Ruff 配置：**
```toml
line-length = 100
quote-style = "double"
indent-style = "space"
```

**必须遵守：**
- 100 字符行宽
- 使用双引号
- 4 空格缩进

### 2. 导入顺序

```python
"""
模块文档字符串
"""
# 1. 标准库导入
from datetime import datetime, timedelta
from typing import Annotated, Optional

# 2. 第三方库导入
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from loguru import logger

# 3. 本地应用导入
from app.api.deps import get_current_user
from app.db.prisma import get_prisma
from app.core.config import settings
```

### 3. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块/文件 | snake_case | `user_service.py`, `cache_service.py` |
| 类 | PascalCase | `UserService`, `CacheService` |
| 函数 | snake_case | `get_user()`, `create_tokens()` |
| 变量 | snake_case | `is_active`, `user_id` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY`, `DEFAULT_TTL` |
| 私有成员 | _前缀 | `_redis`, `_get_cache()` |

### 4. 类型注解规范

```python
# 使用 Annotated 进行依赖注入
from typing import Annotated

CurrentUser = Annotated[dict, Depends(get_current_user)]

# Python 3.10+ 联合类型
def create_user(
    email: str,
    department: str | None = None,
) -> User:
    pass

# 类型别名
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')
```

### 5. API 路由结构

```python
"""
路由模块文档字符串
"""
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

router = APIRouter()

# Pydantic 模型
class ChatRequest(BaseModel):
    """Chat request with RAG context"""

    question: str = Field(..., min_length=1, max_length=2000, description="User question")
    temperature: float = Field(0.7, ge=0, le=1, description="Sampling temperature")


@router.post("/endpoint", status_code=201)
async def endpoint_function(
    request: ChatRequest,
    current_user: CurrentUser,
) -> ChatResponse:
    """
    端点描述

    Args:
        request: 请求参数
        current_user: 当前用户

    Returns:
        响应数据
    """
    return {"success": True, "data": ...}
```

### 6. 文档字符串规范

```python
# Google 风格（多行）
async def get(self, key: str) -> Optional[Any]:
    """
    获取缓存

    Args:
        key: 缓存键

    Returns:
        缓存值，如果不存在返回 None
    """
    pass

# 简洁单行
class CacheService:
    """Redis 缓存服务"""
```

### 7. 异常处理规范

```python
# 使用自定义异常
from app.core.exceptions import NotFoundError, AuthenticationError

# 统一错误响应格式
{
    "success": False,
    "error": {
        "code": "NOT_FOUND",
        "message": "Resource not found",
        "details": {}
    }
}
```

---

## Prisma Schema 规范

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模型 | PascalCase | `User`, `Project`, `Document` |
| 字段 | camelCase | `user_id`, `created_at`, `password_hash` |
| 枚举 | PascalCase | `UserRole`, `DocumentStatus` |
| 枚举值 | UPPER_SNAKE_CASE | `ADMIN`, `PROCESSING` |
| 数据库表 | snake_case | `users`, `chat_sessions` |

### Schema 结构

```prisma
// ============================================
// 分区注释
// ============================================

enum UserRole {
  ADMIN
  USER
}

model User {
  id          String    @id @default(dbgenerated("uuid_generate_v4()")) @db.Uuid
  email       String    @unique @map("email") @db.VarChar(255)
  created_at  DateTime  @default(now()) @map("created_at") @db.Timestamptz(6)
  updated_at  DateTime  @default(now()) @updatedAt @map("updated_at")

  // Relations
  projects    Project[] @relation("UserProjects")

  @@index([email], map: "idx_users_email")
  @@map("users")
}
```

---

## 通用规范

### 1. 文件组织

```
feature/
├── index.ts        # 统一导出
├── Feature.tsx     # 主组件
├── feature.module.scss
└── components/     # 子组件
```

### 2. 注释规范

- 优先使用中文注释
- 复杂逻辑必须添加注释说明
- 公共 API 必须添加文档字符串

### 3. Git 提交规范

```
feat: 新功能
fix: 修复
docs: 文档
style: 样式调整
refactor: 重构
perf: 性能优化
test: 测试
chore: 构建/工具
```

---

## 修改样式时的检查清单

- [ ] 确认使用 `.module.scss` 文件
- [ ] 类名使用 camelCase
- [ ] 优先使用 CSS 自定义属性 (`var(--color-*)`)
- [ ] 避免使用内联样式
- [ ] 确认没有使用 `!important`（除非必要）
- [ ] 响应式设计使用相对单位
- [ ] 遵循组件单一职责原则

---

## 配置文件位置

| 配置 | 路径 |
|------|------|
| ESLint | `frontend/.eslintrc.json` |
| Prettier | `frontend/.prettierrc` |
| TypeScript | `frontend/tsconfig.json` |
| Ruff | `backend/pyproject.toml` |
| Prisma | `backend/prisma/schema.prisma` |
