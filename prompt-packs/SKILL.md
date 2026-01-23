---
name: prompt-packs
description: OpenAI Academy 提示词库 - 200+ 企业场景提示词，支持销售、产品、工程、HR等10个团队
version: 1.1.0
triggers:
  keywords:
    # 中文表达
    - "提示词"
    - "prompt"
    - "提示库"
    - "提示词库"
    - "用提示词"
    - "prompt packs"
    - "openai prompt"
    # 英文表达
    - "use prompt"
    - "prompt template"
    - "prompt library"
  patterns:
    - "/prompt-packs*"
    - "/pp*"
    - "用提示词*"
    - "*提示词模板"
    - "prompt*"
  intents:
    - prompt-template
    - prompt-library
    - use-prompt
    - prompt-packs
priority: 85
---

# Prompt Packs: OpenAI Academy 提示词库

OpenAI Academy 官方提示词库，包含 232 个企业场景提示词，覆盖 10 个团队。

## 触发方式

- `/prompt-packs` 或 `/pp` - 命令式触发
- `用提示词写个销售邮件` - 自然语言触发

## 支持的团队

| # | 团队 | 提示词数量 |
|---|------|-----------|
| 1 | 销售团队 (Sales) | 22 |
| 2 | 客户成功 (Customer Success) | 24 |
| 3 | 产品管理 (Product Management) | 24 |
| 4 | 工程团队 (Engineering) | 25 |
| 5 | 人力资源 (HR) | 24 |
| 6 | IT团队 | 24 |
| 7 | 管理团队 (Manager) | 20 |
| 8 | 高管 (Executive) | 25 |
| 9 | 政府IT人员 (Gov IT) | 24 |
| 10 | 政府分析师 (Gov Analyst) | 24 |

## 浏览模式

```
/pp list              # 列出所有团队
/pp list 销售         # 列出销售团队的所有提示词
/pp list sales        # 英文团队名也可以
```

## 执行流程

### 步骤 1: 分析用户需求

从用户输入中提取关键信息：
- 团队/角色 (如：销售、产品、HR)
- 具体任务 (如：冷邮件、账户计划、PRD)
- 上下文信息

### 步骤 2: 匹配提示词

基于关键词和语义匹配，找到最相关的 3 个提示词，展示给用户选择。

```
找到 3 个相关提示词：

1. 个性化冷邮件 - 给特定职位/公司写开发信
   模板: Write a short, compelling cold email to a [job title] at [company name]...

2. 演示后续邮件 - 演示后的跟进邮件
   模板: Rewrite this follow-up email after a demo...

3. 续约提案 - 客户续约提案
   模板: Draft a renewal pitch for [customer name]...

请选择或输入序号 [1-3]，或直接描述你的需求：
```

### 步骤 3: 交互式收集占位符信息

**语言检测**: 根据用户的输入语言，使用对应语言进行交互。

**中文用户示例**:
```
需要填写以下信息：
• 收件人职位 (job title) - [必填]
• 目标公司 (company name) - [必填]
• 背景信息 (background/value props) - [可选]

请依次提供以上信息。
```

**英文用户示例**:
```
Please provide the following information:
• Job title - [required]
• Company name - [required]
• Background/Value props - [optional]
```

使用 `AskUserQuestion` 工具进行交互式收集：
- 必填项使用 `required: true`
- 可选项不标记必填
- 每个字段提供清晰的 `description`

### 步骤 4: 翻译并填充模板

将用户提供的信息翻译成英文，填充到英文模板中：

```
用户输入: 职位是CTO，公司是Acme，我们做AI数据分析
翻译后: job title = "CTO", company name = "Acme", background = "We do AI data analytics"
填充模板: Write a short, compelling cold email to a CTO at Acme introducing our product...
```

### 步骤 5: 输出填充好的模板

**重要**: 不执行提示词，只输出填充好的模板给用户复制使用。

**输出格式**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Prompt Packs - 已填充模板
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<填充后的英文模板内容>

Context:
<用户提供的上下文信息>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
复制以上内容，发送给 ChatGPT/Claude 执行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**用户可以**:
- 复制到 ChatGPT 官方使用
- 复制到其他 AI 工具
- 自己修改后再使用

## 提示词数据结构

每个提示词包含以下字段：

```json
{
  "id": "sales-001",
  "category": "销售团队",
  "subcategory": "外联与沟通",
  "name": "个性化冷邮件",
  "template": "Write a short, compelling cold email to a [job title] at [company name]...",
  "keywords": ["cold email", "outreach", "冷邮件", "外联"],
  "placeholders": [
    {"name": "job title", "label": "Job Title", "required": true},
    {"name": "company name", "label": "Company Name", "required": true},
    {"name": "value props or ICP info", "label": "Background/Value Props", "required": false}
  ]
}
```

## 提示词索引

数据文件位置: `D:/OpenAI_Prompts/OpenAI_Academy_Prompts_Structured.json`

### 销售团队 (Sales)

| ID | 名称 | 关键词 |
|----|------|--------|
| sales-001 | 个性化冷邮件 | cold email, outreach, 冷邮件, 外联 |
| sales-002 | 演示后续邮件 | follow-up, demo, 后续邮件 |
| sales-003 | 续约提案 | renewal, pitch, 续约, 提案 |
| sales-004 | 代表活动摘要 | daily update, rep activities, 活动摘要 |
| sales-005 | 高管更新 | pipeline, executive, 高管更新, 管道 |
| sales-006 | 客户账户计划 | account plan, strategy, 账户计划, 策略 |
| sales-007 | 区域规划框架 | territory, planning, 区域规划 |
| sales-008 | 客户优先级 | prioritize, accounts, 优先级, 客户 |
| sales-009 | 评分模型 | scoring, account model, 评分模型 |
| sales-010 | 市场进入规划 | market entry, go-to-market, 市场进入 |
| sales-011 | 竞争对手战卡 | battlecard, competitor, 竞争, 战卡 |
| sales-012 | 竞争定位分析 | competitive positioning, 定位分析 |
| sales-013 | 销售赋能单页 | one-pager, sales enablement, 赋能 |
| sales-014 | 异议处理 | objection, rebuttal, 异议, 反驳 |
| sales-015 | 管道转化率 | pipeline conversion, 转化率, 漏斗 |
| sales-016 | 代表绩效排名 | rep performance, ranking, 绩效排名 |
| sales-017 | 交易速度可视化 | deal velocity, 交易速度 |
| sales-018 | 营销归因 | attribution, marketing, 归因 |
| sales-019 | 销售漏斗可视化 | sales funnel, 漏斗, 可视化 |
| sales-020 | B2B销售漏斗图 | B2B funnel, 销售漏斗 |
| sales-021 | 买家人物插图 | persona, illustration, 买家, 人物 |
| sales-022 | 区域覆盖地图 | territory map, 区域地图, 覆盖 |

### 客户成功团队 (Customer Success)

| ID | 名称 | 关键词 |
|----|------|--------|
| cs-001 | 入职计划模板 | onboarding plan, 入职计划 |
| cs-002 | 入职反馈摘要 | onboarding feedback, 入职反馈 |
| cs-003 | 高接触式入职最佳实践 | high-touch onboarding, 入职最佳实践 |
| cs-004 | 主动行动手册 | proactive playbook, 主动手册 |
| cs-005 | 留存激励策略 | retention strategy, 留存, 激励 |
| cs-006 | CS组织架构基准 | org structure benchmark, 组织架构 |
| cs-007 | 成功指标基准 | success metrics benchmark, 成功指标 |
| cs-008 | CS工具栈评估 | tech stack evaluation, 工具栈 |
| cs-009 | 竞争对手赋能摘要 | competitor enablement, 竞争赋能 |
| cs-010 | CS项目竞争比较 | CS program comparison, CS项目 |
| cs-011 | 高管邮件更新 | executive email update, 高管邮件 |
| cs-012 | QBR谈话要点 | QBR talking points, QBR要点 |
| cs-013 | 续约通话准备 | renewal call prep, 续约准备 |
| cs-014 | 账户计划摘要 | account plan summary, 账户计划 |
| cs-015 | 续约风险摘要 | renewal risk summary, 续约风险 |
| cs-016 | 成功指标大纲 | success metrics outline, 成功指标 |
| cs-017 | CSAT分数分布评估 | CSAT distribution, CSAT分数 |
| cs-018 | 支持工单趋势分析 | ticket trend analysis, 工单趋势 |
| cs-019 | 流失早期预警 | churn early warning, 流失预警 |
| cs-020 | 客户健康评分标准化 | health scoring rubric, 健康评分 |
| cs-021 | 健康评分仪表板 | health score dashboard, 健康仪表板 |
| cs-022 | 客户旅程地图可视化 | customer journey map, 旅程地图 |
| cs-023 | 升级流程图 | escalation flowchart, 升级流程 |
| cs-024 | 客户成熟度模型 | customer maturity model, 成熟度模型 |

### 产品管理团队 (Product Management)

| ID | 名称 | 关键词 |
|----|------|--------|
| pm-001 | 竞争对手入职UX比较 | competitor onboarding UX, 竞争UX |
| pm-002 | 竞争对手定价策略基准 | competitor pricing benchmark, 定价策略 |
| pm-003 | 技术栈选项比较 | tech stack comparison, 技术栈 |
| pm-004 | 新功能监管风险识别 | regulatory risk, 监管风险 |
| pm-005 | 产品驱动增长战术研究 | PLG tactics, 产品驱动增长 |
| pm-006 | 基于影响力优先级 | impact prioritization, 影响优先级 |
| pm-007 | 货币化模式探索 | monetization strategy, 货币化 |
| pm-008 | 产品愿景声明 | product vision statement, 愿景声明 |
| pm-009 | 从客户反馈头脑风暴功能 | feature brainstorming, 功能头脑风暴 |
| pm-010 | A/B测试计划 | A/B test plan, A/B测试 |
| pm-011 | PRD草案 | PRD draft, 产品需求文档 |
| pm-012 | 更新日志和发布说明 | changelog release notes, 更新日志 |
| pm-013 | 上市FAQ | launch FAQ, 上市FAQ |
| pm-014 | 一句话价值主张 | value proposition, 价值主张 |
| pm-015 | 产品演示文稿大纲 | product deck outline, 演示大纲 |
| pm-016 | 用户旅程地图可视化 | user journey map, 用户旅程 |
| pm-017 | 入职流程线框图 | onboarding wireframe, 入职线框图 |
| pm-018 | 产品比较视觉图 | product comparison visual, 产品比较 |
| pm-019 | 用户旅程信息图 | user journey infographic, 旅程信息图 |
| pm-020 | 产品反馈主题分析 | feedback theme analysis, 反馈分析 |
| pm-021 | 使用数据综合洞察 | usage data insights, 使用数据 |
| pm-022 | 产品采用风险识别 | adoption risk, 采用风险 |
| pm-023 | A/B测试结果分析 | A/B test analysis, A/B分析 |
| pm-024 | 客户细分功能采用比较 | segment feature adoption, 细分采用 |

### 工程团队 (Engineering)

| ID | 名称 | 关键词 |
|----|------|--------|
| eng-001 | 云提供商评估 | cloud provider evaluation, 云评估 |
| eng-002 | 实时应用框架研究 | real-time framework, 实时框架 |
| eng-003 | 可观测性工具基准 | observability benchmark, 可观测性 |
| eng-004 | 物流领域AI/ML趋势 | AI/ML trends, AI趋势 |
| eng-005 | 合规最佳实践调查 | compliance best practices, 合规实践 |
| eng-006 | 系统设计文档审查 | design doc review, 设计文档 |
| eng-007 | 内部API行为文档化 | API documentation, API文档 |
| eng-008 | 值班工程师运行手册草案 | on-call runbook, 运行手册 |
| eng-009 | 新员工入职指南草案 | new hire onboarding, 新人入职 |
| eng-010 | 根据规范编写JIRA工单 | JIRA ticket, JIRA工单 |
| eng-011 | 生产系统故障调试 | production debugging, 生产故障 |
| eng-012 | 性能瓶颈分析 | performance bottleneck, 性能瓶颈 |
| eng-013 | 数据管道故障分析 | data pipeline failure, 管道故障 |
| eng-014 | 可观测性改进建议 | observability improvement, 可观测改进 |
| eng-015 | 测试边缘案例头脑风暴 | edge cases, 边缘案例 |
| eng-016 | 产品使用日志趋势识别 | usage log trends, 使用日志 |
| eng-017 | 系统错误率随时间可视化 | error rate visualization, 错误率 |
| eng-018 | 性能测试结果分析 | performance test analysis, 性能测试 |
| eng-019 | 基于影响力优先处理Bug | bug prioritization, Bug优先级 |
| eng-020 | 用户调查反馈摘要 | survey feedback summary, 调查反馈 |
| eng-021 | 组件图创建 | component diagram, 组件图 |
| eng-022 | 系统架构可视化 | system architecture visualization, 架构图 |
| eng-023 | 向利益相关者解释CI/CD管道 | CI/CD explanation, CI/CD说明 |
| eng-024 | ML管道数据流建模 | ML pipeline data flow, ML管道 |
| eng-025 | 应用程序客户旅程图 | app customer journey, 应用旅程 |

### 人力资源 (HR)

| ID | 名称 | 关键词 |
|----|------|--------|
| hr-001 | 员工调查问题起草 | employee survey questions, 员工调查 |
| hr-002 | 绩效评估提示生成 | performance review questions, 绩效评估 |
| hr-003 | 离职调查主题分析 | exit survey analysis, 离职调查 |
| hr-004 | 员工流失趋势分析 | attrition analysis, 流失分析 |
| hr-005 | 薪酬基准报告生成 | salary benchmark, 薪酬基准 |
| hr-006 | 全球HR合规更新研究 | HR compliance update, HR合规 |
| hr-007 | DEI预算基准 | DEI budget benchmark, DEI预算 |
| hr-008 | 2025年HR技术趋势探索 | HR tech trends 2025, HR技术 |
| hr-009 | 跨行业员工留存策略比较 | retention strategies, 留存策略 |
| hr-010 | 招聘工具研究 | recruiting tools, 招聘工具 |
| hr-011 | 面试问题创建 | interview questions, 面试问题 |
| hr-012 | 职位描述草案 | job description draft, 职位描述 |
| hr-013 | 参与计划头脑风暴 | engagement ideas, 参与计划 |
| hr-014 | 内部表彰简介撰写 | recognition message, 表彰信息 |
| hr-015 | DEI研讨会大纲创建 | DEI workshop outline, DEI研讨会 |
| hr-016 | 内部政策摘要草案 | policy summary, 政策摘要 |
| hr-017 | 返办公室FAQ草案 | return-to-office FAQ, 返办公室FAQ |
| hr-018 | 入职周计划 | onboarding schedule, 入职计划 |
| hr-019 | 健康计划头脑风暴 | wellbeing programs, 健康计划 |
| hr-020 | 合规培训推广计划 | compliance training rollout, 合规培训 |
| hr-021 | 入职欢迎横幅创建 | onboarding banner, 欢迎横幅 |
| hr-022 | 内部DEI海报设计 | DEI poster design, DEI海报 |
| hr-023 | 混合办公政策插图 | hybrid work illustration, 混合办公 |
| hr-024 | 员工生命周期可视化 | employee lifecycle, 员工生命周期 |

### IT团队

| ID | 名称 | 关键词 |
|----|------|--------|
| it-001 | 云提供商比较 | cloud provider comparison, 云比较 |
| it-002 | 供应商比较图表生成 | vendor comparison chart, 供应商比较 |
| it-003 | AI可观测性工具比较 | AI observability tools, AI可观测 |
| it-004 | 零信任框架调查 | zero trust framework, 零信任 |
| it-005 | 全球数据驻留法律评估 | data residency laws, 数据驻留 |
| it-006 | 远程访问工具分析 | remote access tools, 远程访问 |
| it-007 | 合规检查清单生成 | compliance checklist, 合规清单 |
| it-008 | 访问控制验证 | access control review, 访问控制 |
| it-009 | API安全态势审查 | API security review, API安全 |
| it-010 | IT入职检查清单草案 | IT onboarding checklist, IT入职 |
| it-011 | 硬件生命周期政策生成 | hardware lifecycle policy, 硬件政策 |
| it-012 | 资产库存政策草案 | asset inventory policy, 资产政策 |
| it-013 | IT工单优先级帮助 | ticket prioritization, 工单优先级 |
| it-014 | 硬件生命周期风险跟踪 | hardware lifecycle risk, 硬件风险 |
| it-015 | 事件事后报告草案 | incident postmortem, 事后报告 |
| it-016 | DR演练手册草案创建 | DR playbook draft, DR手册 |
| it-017 | 停机时间内部沟通撰写 | downtime communication, 停机沟通 |
| it-018 | 错误日志翻译成通俗语言 | log translation, 日志翻译 |
| it-019 | SaaS工具冗余评估 | SaaS redundancy, SaaS冗余 |
| it-020 | 系统健康趋势摘要 | system health trends, 系统健康 |
| it-021 | 系统监控改进建议 | monitoring improvements, 监控改进 |
| it-022 | 服务正常运行时间和事件频率分析 | uptime incident analysis, 运行时间分析 |
| it-023 | 用户访问日志异常审计 | access log audit, 访问日志审计 |
| it-024 | IT支持工单量预测 | ticket volume forecasting, 工单预测 |

### 管理团队 (Manager)

| ID | 名称 | 关键词 |
|----|------|--------|
| mgr-001 | 季度目标起草 | quarterly goals, 季度目标 |
| mgr-002 | 高管更新谈话要点 | exec update talking points, 高管要点 |
| mgr-003 | 技能差距分析 | skills gap analysis, 技能差距 |
| mgr-004 | 招聘路线图计划 | hiring roadmap, 招聘路线图 |
| mgr-005 | 转型后目标重新定位 | goals reframing, 目标重新定位 |
| mgr-006 | 1:1模板创建 | 1:1 meeting template, 1:1模板 |
| mgr-007 | 反馈交付改进 | feedback delivery, 反馈交付 |
| mgr-008 | 困难对话准备 | difficult conversation prep, 困难对话 |
| mgr-009 | 跨团队冲突解决 | cross-team conflict, 跨团队冲突 |
| mgr-010 | 从工时识别职业倦怠风险 | burnout risk detection, 倦怠风险 |
| mgr-011 | 工作负载分布分析 | workload distribution, 工作负载 |
| mgr-012 | 团队健康问题诊断 | team health diagnosis, 团队健康 |
| mgr-013 | 混合参与最佳实践 | hybrid engagement best practices, 混合参与 |
| mgr-014 | 经理与IC比率基准 | manager IC ratio, 经理IC比率 |
| mgr-015 | 有效技能提升计划研究 | upskilling program research, 技能提升 |
| mgr-016 | DEI策略示例比较 | DEI strategy comparison, DEI策略 |
| mgr-017 | 职业倦怠风险与缓解理解 | burnout mitigation, 倦怠缓解 |
| mgr-018 | 团队成长历程描绘 | team growth journey, 团队成长 |
| mgr-019 | 团队文化视觉摘要 | team culture visual, 团队文化 |
| mgr-020 | 季度重点领域展示 | quarterly priorities, 季度重点 |

### 高管 (Executive)

| ID | 名称 | 关键词 |
|----|------|--------|
| exec-001 | 投资者趋势摘要 | investor trends, 投资者趋势 |
| exec-002 | 投资者情绪调查 | investor sentiment, 投资者情绪 |
| exec-003 | 高管薪酬基准 | executive compensation benchmark, 薪酬基准 |
| exec-004 | 并购机会评估 | M&A opportunity assessment, 并购评估 |
| exec-005 | 行业未来趋势评估 | industry future trends, 行业趋势 |
| exec-006 | 愿景声明起草 | vision statement draft, 愿景声明 |
| exec-007 | 全员大会谈话要点生成 | town hall talking points, 全员大会 |
| exec-008 | 内部沟通策略更新 | internal comms strategy, 内部沟通 |
| exec-009 | 重组沟通顺序计划 | reorganization comms plan, 重组沟通 |
| exec-010 | 继任计划备忘录起草 | succession planning memo, 继任计划 |
| exec-011 | 定价策略简报创建 | pricing strategy brief, 定价策略 |
| exec-012 | 增长杠杆优先级 | growth levers, 增长杠杆 |
| exec-013 | 市场进入风险分析 | market entry risk analysis, 市场进入风险 |
| exec-014 | 战略权衡重新定位 | strategic tradeoffs, 战略权衡 |
| exec-015 | 3年战略大纲设计 | 3-year strategy outline, 三年战略 |
| exec-016 | 顶级和底层表现细分识别 | top bottom performer segments, 表现细分 |
| exec-017 | 季度业务指标分析 | quarterly business metrics, 季度指标 |
| exec-018 | 客户旅程流失分析 | customer journey churn analysis, 旅程流失 |
| exec-019 | 基于历史趋势预测下一季度 | forecast next quarter, 预测下一季 |
| exec-020 | 战略投资优先级 | strategic investment priorities, 战略投资 |
| exec-021 | 竞争格局网格构建 | competitive landscape grid, 竞争网格 |
| exec-022 | 2x2市场定位矩阵设计 | 2x2 positioning matrix, 定位矩阵 |
| exec-023 | 转型时间线展示 | transformation timeline, 转型时间线 |
| exec-024 | 战略愿景或飞轮可视化 | strategic flywheel vision, 战略飞轮 |
| exec-025 | 未来产品愿景插图 | future product vision, 产品愿景 |

### 政府IT人员 (Gov IT)

| ID | 名称 | 关键词 |
|----|------|--------|
| gov-it-001 | 漏洞扫描分析 | vulnerability scan analysis, 漏洞扫描 |
| gov-it-002 | 安全例外摘要 | security exception summary, 安全例外 |
| gov-it-003 | 攻击向量提取与可视化 | attack vector visualization, 攻击向量 |
| gov-it-004 | 代码覆盖率报告合并 | code coverage merge, 代码覆盖率 |
| gov-it-005 | 性能测试数据摘要 | performance test summary, 性能测试 |
| gov-it-006 | 变更管理请求模板创建 | change management template, 变更管理 |
| gov-it-007 | 基础设施即代码合规检查 | IaC compliance check, IaC合规 |
| gov-it-008 | 服务器配置审查 | server config review, 服务器配置 |
| gov-it-009 | 虚拟机容量报告生成 | VM capacity report, 虚拟机容量 |
| gov-it-010 | 数据去重 | data deduplication, 数据去重 |
| gov-it-011 | 响应时间分布仪表板 | response time dashboard, 响应时间 |
| gov-it-012 | 多文件合并与转换 | multi-file merge, 多文件合并 |
| gov-it-013 | 知识库文章生成 | knowledge base article, 知识库 |
| gov-it-014 | 工单日志分析 | ticket log analysis, 工单日志 |
| gov-it-015 | 决策树生成 | decision tree generation, 决策树 |
| gov-it-016 | SLA比较 | SLA comparison, SLA比较 |
| gov-it-017 | RFP模板生成 | RFP template generation, RFP模板 |
| gov-it-018 | 供应商绩效指标摘要 | vendor performance summary, 供应商绩效 |
| gov-it-019 | 事件沟通草案 | incident communication draft, 事件沟通 |
| gov-it-020 | 事后报告大纲 | postmortem report outline, 事后报告 |
| gov-it-021 | 连续性运营检查清单 | continuity checklist, 连续性检查 |
| gov-it-022 | 培训要求映射 | training requirements mapping, 培训要求 |
| gov-it-023 | 技术标准比较 | technical standards comparison, 技术标准 |
| gov-it-024 | 架构概述创建 | architecture overview, 架构概述 |

### 政府分析师 (Gov Analyst)

| ID | 名称 | 关键词 |
|----|------|--------|
| gov-ana-001 | 季度绩效仪表板摘要 | quarterly performance summary, 季度绩效 |
| gov-ana-002 | 可视化比较 | visualization comparison, 可视化比较 |
| gov-ana-003 | 数据缺口识别 | data gap identification, 数据缺口 |
| gov-ana-004 | 逻辑模型起草 | logic model draft, 逻辑模型 |
| gov-ana-005 | 数据质量问题识别 | data quality issues, 数据质量 |
| gov-ana-006 | 统计发现摘要 | statistical findings summary, 统计发现 |
| gov-ana-007 | SQL查询编写 | SQL query writing, SQL查询 |
| gov-ana-008 | 聚类技术建议 | clustering techniques, 聚类技术 |
| gov-ana-009 | Python代码转换 | Python code conversion, Python代码 |
| gov-ana-010 | 预算偏差突出显示 | budget variance highlighting, 预算偏差 |
| gov-ana-011 | 财务投影可视化 | financial projection visualization, 财务投影 |
| gov-ana-012 | 收入下降情景分析 | revenue drop scenario, 收入情景 |
| gov-ana-013 | KPI趋势分析 | KPI trend analysis, KPI趋势 |
| gov-ana-014 | 投标比较表 | bid comparison table, 投标比较 |
| gov-ana-015 | 甘特图时间线 | Gantt timeline, 甘特图 |
| gov-ana-016 | 风险登记册生成 | risk register generation, 风险登记册 |
| gov-ana-017 | 协议差距分析 | agreement gap analysis, 协议差距 |
| gov-ana-018 | 合规清单审查 | compliance checklist review, 合规清单 |
| gov-ana-019 | 行动标准化摘要 | action summary standardization, 行动摘要 |
| gov-ana-020 | 响应指标可视化 | response metrics visualization, 响应指标 |
| gov-ana-021 | 协调问题识别 | coordination issues identification, 协调问题 |
| gov-ana-022 | 共同目标识别 | common goals identification, 共同目标 |
| gov-ana-023 | 视觉摘要创建 | visual summary creation, 视觉摘要 |
| gov-ana-024 | 数据共享原则 | data sharing principles, 数据共享 |

## 使用示例

### 示例 1: 销售冷邮件（中文用户）

```
你: /pp 写个销售冷邮件

AI: 找到 3 个相关提示词：

1. 个性化冷邮件 - 给特定职位/公司写开发信
2. 演示后续邮件 - 演示后的跟进邮件
3. 续约提案 - 客户续约提案

请选择 [1-3]：

你: 1

AI: 需要填写以下信息：
• 收件人职位 - [必填]
• 目标公司 - [必填]
• 背景信息 - [可选]

请提供以上信息。

你: 职位是CTO，公司是Acme Corp，我们做AI数据分析平台

AI: [使用 AskUserQuestion 收集信息]

[收集完成后，输出填充好的模板]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Prompt Packs - 已填充模板
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Write a short, compelling cold email to a CTO at Acme Corp
introducing our product. Use the background below to
customize it. Background: We do AI data analytics platform.
Format it in email-ready text.

Context:
- Job Title: CTO
- Company: Acme Corp
- Background: AI数据分析平台

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
复制以上内容，发送给 ChatGPT 执行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 示例 2: 产品PRD（英文用户）

```
you: /pp help me write a PRD

AI: Found 3 relevant prompts:

1. PRD草案 - 基于功能想法和客户需求编写PRD
2. 产品愿景声明 - 编写简洁的产品愿景声明
3. 产品演示文稿大纲 - 创建产品演示文稿大纲

Select [1-3]:

you: 1

AI: Please provide the following information:
• Feature idea/concept - [required]
• Customer need/problem - [required]
• Additional context - [optional]

[使用 AskUserQuestion 收集信息，然后输出填充好的模板]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Prompt Packs - 已填充模板
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<填充后的英文 PRD 模板内容>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Copy and send to ChatGPT to execute
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 示例 3: 浏览模式

```
你: /pp list 销售

AI: 销售团队提示词 (22个):

外联与沟通:
  1. 个性化冷邮件
  2. 演示后续邮件
  3. 续约提案
  ...

销售策略与规划:
  6. 客户账户计划
  7. 区域规划框架
  ...

[显示完整列表]
```

## 语言处理规则

1. **语言检测**: 检测用户输入的语言（中文/英文）
2. **交互语言**: 使用检测到的语言进行交互和收集信息
3. **模板保持**: 模板保持英文不变
4. **信息翻译**: 将用户提供的信息翻译成英文后填入模板
5. **输出格式**: 输出填充好的模板，**不执行**提示词
6. **用户使用**: 用户复制模板到 ChatGPT/Claude 等工具执行

## 占位符处理规则

1. **必填/可选**: 根据 `required` 字段判断
2. **多个占位符**: 使用 `AskUserQuestion` 的 `multiSelect: false` 顺序收集
3. **用户跳过**: 如果可选字段用户跳过，使用 `[ omitted ]` 标记
4. **复用信息**: 如果用户之前提供过相关信息（如公司名），自动复用

## 数据源

提示词数据存储在: `D:/OpenAI_Prompts/OpenAI_Academy_Prompts_Structured.json`

每次执行时读取最新数据。

## 快捷命令

| 命令 | 说明 |
|------|------|
| `/pp` | 根据自然语言描述匹配提示词 |
| `/pp list` | 列出所有团队 |
| `/pp list <团队>` | 列出指定团队的提示词 |
| `/pp search <关键词>` | 搜索包含关键词的提示词 |
| `/pp <id>` | 直接使用指定ID的提示词 |
