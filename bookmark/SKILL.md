---
name: bookmark
description: 收藏夹管理 - 管理书签和收藏链接，支持添加、查看、搜索和组织收藏内容。
user-invocable: true
---


# Bookmark: 收藏夹管理

管理你的书签和收藏链接，支持添加、查看、搜索和组织收藏内容。

## 适用场景

- 用户说「收藏这个链接」「添加到书签」
- 用户说「查看我的收藏」「打开收藏夹」
- 用户说「管理书签」「整理收藏」
- 用户说「搜索收藏」「找一下之前收藏的」

## 文档位置

```
~/.claude/
└── bookmarks.json    # 收藏数据存储
```

## 数据格式

```json
{
  "bookmarks": [
    {
      "id": "uuid",
      "title": "链接标题",
      "url": "https://example.com",
      "description": "可选描述",
      "tags": ["tag1", "tag2"],
      "createdAt": "2025-01-01T00:00:00Z",
      "folder": "默认"
    }
  ],
  "folders": ["默认", "工作", "学习", "工具"]
}
```

## 执行流程

### 添加收藏

1. 获取链接 URL
2. 自动获取页面标题（如果可能）
3. 询问用户是否添加标签或描述
4. 保存到 bookmarks.json

### 查看收藏

1. 读取 bookmarks.json
2. 按文件夹或标签分类展示
3. 显示最近添加的收藏

### 搜索收藏

1. 接收搜索关键词
2. 在标题、描述、标签中搜索
3. 返回匹配结果

### 管理收藏

1. 支持删除、编辑、移动
2. 支持创建/删除文件夹
3. 支持批量操作

## 命令示例

```
用户：收藏 https://example.com
助手：已收藏「Example Domain」。需要添加标签吗？

用户：查看我的收藏
助手：
📁 默认 (3)
  - Example Domain
  - Another Site
  - Tool Documentation

📁 工作 (2)
  - Project Docs
  - API Reference

用户：搜索 API
助手：找到 2 个匹配的收藏：
1. API Reference (工作)
2. REST API Guide (学习)
```

## 快捷命令

- `/bookmark add <url>` - 添加收藏
- `/bookmark list` - 查看所有收藏
- `/bookmark search <keyword>` - 搜索收藏
- `/bookmark delete <id>` - 删除收藏
