# Visual Interface Generator

自动为 Skill 生成可视化进度界面的元技能。

## 快速使用

### 在 Claude Code 中使用

```
# 为现有 Skill 添加可视化
为 auto-redbook-skills 创建可视化界面

# 为文档分析 Skill 添加进度
为 document-analyzer-workflow 生成可视化版本

# 从描述生成新 Skill
创建一个批量下载图片的 Skill，带可视化界面
```

### 命令行使用

```bash
# 基本用法
python3 ~/.claude/skills/visual-interface-generator/generator.py ~/.claude/skills/auto-redbook-skills

# 保存到文件
python3 ~/.claude/skills/visual-interface-generator/generator.py ~/.claude/skills/auto-redbook-skills -o enhanced_skill.py

# 指定主题
python3 ~/.claude/skills/visual-interface-generator/generator.py ~/.claude/skills/auto-redbook-skills --theme colorful
```

## 工作原理

```
1️⃣ 读取目标 Skill 的 SKILL.md
   ↓
2️⃣ 分析工作流程
   - 识别处理步骤
   - 检测处理类型
   - 建议合适的主题
   ↓
3️⃣ 生成代码
   - 创建 VisualProgress 实例
   - 定义处理步骤函数
   - 设置工作流任务
   ↓
4️⃣ 输出结果
   - 完整的可执行代码
   - 集成了 visual-progress
```

## 自动识别的工作流类型

| 类型 | 触发关键词 | 生成的进度样式 |
|------|-----------|---------------|
| **批处理** | 批量、多个、所有、这些 | 文件列表进度 |
| **API 请求** | API、请求、调用 | 请求进度 |
| **文件处理** | 文件、文档、转换 | 文件操作进度 |
| **数据处理** | 数据、分析、清洗 | 管道阶段进度 |
| **顺序流程** | 步骤1→2→3 | 顺序进度条 |

## 示例

### 输入
```
为 auto-redbook-skills 创建可视化界面
```

### 分析结果
```
✅ 已读取: auto-redbook-skills/SKILL.md
📖 提取基本信息...
   名称: xhs-note-creator
   描述: 小红书笔记素材创作技能

🔍 分析工作流程...
   识别到 3 个步骤:
   1. 📝 撰写小红书笔记内容
   2. 🎨 生成图片卡片
   3. 📤 发布小红书笔记

📊 处理类型: file
   建议主题: default
```

### 生成代码（片段）
```python
def xhs_note_creator(input_data):
    """xhs-note-creator 主处理函数（带可视化进度）

    工作流程:
    1. 📝 撰写小红书笔记内容
    2. 🎨 生成图片卡片
    3. 📤 发布小红书笔记
    """

    progress = VisualProgress(
        title="xhs-note-creator",
        theme="default"
    )

    # 定义处理步骤
    def step1_func(task_id, task_info):
        """📝 撰写小红书笔记内容"""
        # TODO: 实现撰写逻辑
        return {"status": "completed"}

    def step2_func(task_id, task_info):
        """🎨 生成图片卡片"""
        # TODO: 实现生成逻辑
        return {"status": "completed"}

    def step3_func(task_id, task_info):
        """📤 发布小红书笔记"""
        # TODO: 实现发布逻辑
        return {"status": "completed"}

    workflow = [
        {'id': 'step1', 'name': '📝 撰写小红书笔记内容', 'total': 100},
        {'id': 'step2', 'name': '🎨 生成图片卡片', 'total': 100},
        {'id': 'step3', 'name': '📤 发布小红书笔记', 'total': 100},
    ]

    results = progress.run_tasks(workflow, lambda tid, info: {
        'step1': step1_func,
        'step2': step2_func,
        'step3': step3_func,
    }[tid](tid, info))

    return results
```

## 自然语言触发

在 Claude Code 中说这些话会自动触发：

| 用户说 | 操作 |
|--------|------|
| "为 xxx 创建可视化界面" | 分析并生成代码 |
| "为 xxx 添加进度显示" | 分析并生成代码 |
| "生成 xxx 的可视化版本" | 分析并生成代码 |
| "为 Skill 创建进度条" | 分析并生成代码 |

## 集成步骤

1. **生成代码**
   ```bash
   python3 generator.py ~/.claude/skills/your-skill -o enhanced.py
   ```

2. **实现逻辑**
   - 在生成的 TODO 处添加实际处理逻辑
   - 替换模拟代码为真实代码

3. **测试**
   ```bash
   python3 enhanced.py
   ```

4. **替换原 Skill**
   - 将增强版代码替换到原 Skill 目录
   - 或作为新版本保存

## 高级用法

### 自定义主题
```bash
python3 generator.py ~/.claude/skills/your-skill --theme colorful
```

### 批量处理多个 Skills
```bash
for skill in ~/.claude/skills/*/; do
    python3 generator.py "$skill" -o "enhanced_$(basename $skill).py"
done
```

### 与现有代码集成
生成代码后，将你的实际处理逻辑复制到对应的步骤函数中。

## 限制

- 需要目标 Skill 有 SKILL.md 文件
- 生成的代码包含 TODO，需要手动实现
- 复杂的工作流可能需要手动调整

## 依赖

```bash
pip install rich
```

## License

与父技能相同
