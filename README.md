# Ezra's Claude Code Skills

一组自定义的 Claude Code Skills，支持自然语言触发，提升开发效率。

## Skills 列表

| Skill | 命令 | 优先级 | 描述 |
|-------|------|--------|------|
| **Commit** | `/commit` | 90 | Git 提交助手 - 使用 Conventional Commit 规范自动生成提交信息 |
| **GitHub Upload** | `/github-upload` | 80 | 上传项目到 GitHub - 自动创建仓库、处理提交和冲突 |
| **Dev-Doc** | `/dev-doc` | 70 | 开发文档生成器 - 将项目规划转化为技术架构、API 设计等文档 |
| **PM** | `/pm` | 60 | 产品经理助手 - 通过追问帮助完善想法，输出项目规划文档 |
| **Dev-Track** | `/dev-track` | 50 | 项目进度跟踪器 - 基于 TASKS.md 维护项目进度 |
| **Bookmark** | `/bookmark` | 40 | 收藏夹管理 - 管理书签和收藏链接 |
| **Pre-Dev** | `/pre-dev` | 30 | 开发前指南 - 在编码前进行需求澄清和方案确认 |

## 自然语言触发

每个 skill 都支持自然语言触发，无需记住命令：

### Commit (`/commit`)
| 触发词 | 示例 |
|--------|------|
| 提交代码 | 「帮我提交代码」 |
| commit | 「帮我 commit」 |
| 存一下 | 「代码存一下」 |
| 改完了 | 「改完了，提交吧」 |
| 搞定了 | 「搞定了」 |

### GitHub Upload (`/github-upload`)
| 触发词 | 示例 |
|--------|------|
| 上传到 GitHub | 「把代码上传到 GitHub」 |
| 推送代码 | 「帮我推送代码」 |
| push | 「帮我 push」 |
| 传上去 | 「传上去」 |

### PM (`/pm`)
| 触发词 | 示例 |
|--------|------|
| 我想做一个 | 「我想做一个博客」 |
| 有个想法 | 「我有个想法」 |
| 帮我规划 | 「帮我规划一下」 |
| 想搞个 | 「想搞个小工具」 |

### Dev-Doc (`/dev-doc`)
| 触发词 | 示例 |
|--------|------|
| 生成开发文档 | 「帮我生成开发文档」 |
| 技术架构 | 「设计技术架构」 |
| 落地方案 | 「出个落地方案」 |
| 任务拆分 | 「帮我拆分任务」 |

### Dev-Track (`/dev-track`)
| 触发词 | 示例 |
|--------|------|
| 更新进度 | 「更新项目进度」 |
| 查看进度 | 「进度怎样了」 |
| 做到哪了 | 「做到哪了」 |
| xxx完成了 | 「登录功能完成了」 |

### Bookmark (`/bookmark`)
| 触发词 | 示例 |
|--------|------|
| 收藏 | 「收藏这个链接」 |
| 存个链接 | 「存个链接」 |
| 查看收藏 | 「查看我的收藏」 |

### Pre-Dev (`/pre-dev`)
| 触发词 | 示例 |
|--------|------|
| 开始开发 | 「开始开发这个功能」 |
| 帮我实现 | 「帮我实现这个功能」 |
| 开干 | 「开干」 |
| 搞起来 | 「搞起来」 |

## 优先级规则

当多个 skill 可能匹配时，按优先级自动选择：

```
commit (90) > github-upload (80) > dev-doc (70) > pm (60) > dev-track (50) > bookmark (40) > pre-dev (30)
```

## 安装使用

将 skills 文件夹复制到 `~/.claude/skills/` 目录即可使用。

## 文件结构

```
skills/
├── SKILLS-INDEX.md      # 统一触发索引
├── README.md            # 本文件
├── pm/
│   └── SKILL.md
├── dev-doc/
│   └── SKILL.md
├── pre-dev/
│   └── SKILL.md
├── github-upload/
│   └── SKILL.md
├── dev-track/
│   ├── SKILL.md
│   └── TEMPLATE.md
├── bookmark/
│   └── SKILL.md
└── commit/
    └── SKILL.md
```

## License

MIT
