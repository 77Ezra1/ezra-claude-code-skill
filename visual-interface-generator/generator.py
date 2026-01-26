#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visual Interface Generator
自动为 Skill 生成可视化进度界面
"""

import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

# 修复 Windows 控制台编码问题
if sys.platform == "win32":
    try:
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
    except:
        pass


class SkillAnalyzer:
    """分析 Skill 文档和工作流程"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.skill_markdown = ""
        self.workflow_steps = []
        self.skill_info = {}

    def read_skill_markdown(self) -> bool:
        """读取 SKILL.md 文件"""
        skill_md_path = self.skill_path / "SKILL.md"

        if not skill_md_path.exists():
            print(f"[Error] 未找到 SKILL.md: {skill_md_path}")
            return False

        with open(skill_md_path, 'r', encoding='utf-8') as f:
            self.skill_markdown = f.read()

        print(f"[OK] 已读取: {skill_md_path}")
        return True

    def extract_skill_info(self) -> Dict[str, Any]:
        """提取 Skill 基本信息"""
        info = {
            'name': self.skill_name,
            'description': '',
            'purpose': '',
            'input': '',
            'output': ''
        }

        # 提取 name 和 description (YAML frontmatter)
        yaml_match = re.search(r'---\nname:\s*(.+)\ndescription:\s*["\'](.+)["\']', self.skill_markdown)
        if yaml_match:
            info['name'] = yaml_match.group(1).strip()
            info['description'] = yaml_match.group(2).strip()

        # 提取用途/目的
        purpose_patterns = [
            r'## 使用场景\s*\n(.+?)(?=\n##|\n\n|\Z)',
            r'## Overview\s*\n(.+?)(?=\n##|\n\n|\Z)',
            r'## Purpose\s*\n(.+?)(?=\n##|\n\n|\Z)',
        ]
        for pattern in purpose_patterns:
            match = re.search(pattern, self.skill_markdown, re.DOTALL)
            if match:
                info['purpose'] = match.group(1).strip()[:200]
                break

        self.skill_info = info
        return info

    def analyze_workflow(self) -> List[Dict[str, str]]:
        """分析工作流程，提取步骤"""
        steps = []

        # 模式 1: 编号的步骤
        numbered_steps = re.findall(
            r'(?:步骤|Step|阶段|Phase)\s*\d+[：:：]\s*\*?\*?(.+?)(?=\n|$|\*)',
            self.skill_markdown,
            re.IGNORECASE
        )
        if numbered_steps:
            for i, step in enumerate(numbered_steps[:10]):  # 最多10步
                steps.append({
                    'id': f'step{i+1}',
                    'name': step.strip(),
                    'type': 'sequential'
                })

        # 模式 2: ## 标记的步骤
        section_headers = re.findall(
            r'#+\s*(步骤|Step|阶段|Phase|\d+\.?\s*[\u4e00-\u9fa5]+)',
            self.skill_markdown,
            re.IGNORECASE
        )
        if section_headers and len(section_headers) > 1:
            for i, header in enumerate(section_headers[:10]):
                steps.append({
                    'id': f'section{i+1}',
                    'name': f"[List] {header}",
                    'type': 'section'
                })

        # 模式 3: 工作流程关键词
        workflow_patterns = [
            (r'第一(?:步|阶段)[:：]\s*(.+)', '[Doc]'),
            (r'第二(?:步|阶段)[:：]\s*(.+)', '[Convert]'),
            (r'第三(?:步|阶段)[:：]\s*(.+)', '[Info]'),
            (r'然后[:：]\s*(.+)', '[Next]'),
            (r'最后[:：]\s*(.+)', '[OK]'),
        ]
        for pattern, icon in workflow_patterns:
            matches = re.findall(pattern, self.skill_markdown)
            for match in matches:
                steps.append({
                    'id': f'workflow_{len(steps)}',
                    'name': f'{icon} {match.strip()}',
                    'type': 'workflow'
                })

        # 模式 4: 描述中的动作序列
        action_indicators = ['撰写', '生成', '处理', '分析', '提取', '转换', '发布', '下载', '上传']
        for indicator in action_indicators:
            matches = re.findall(f'{indicator}(.+?)(?:[，。;\\n]|$)', self.skill_markdown)
            for match in matches:
                step_text = f"{indicator}{match.strip()}"
                if len(step_text) < 50:  # 避免太长的描述
                    steps.append({
                        'id': f'action_{len(steps)}',
                        'name': f'⚙️ {step_text}',
                        'type': 'action'
                    })

        # 去重
        seen = set()
        unique_steps = []
        for step in steps:
            key = step['name'][:30]
            if key not in seen:
                seen.add(key)
                unique_steps.append(step)

        self.workflow_steps = unique_steps[:8]  # 最多8个步骤
        return self.workflow_steps

    def detect_processing_type(self) -> str:
        """检测处理类型"""
        content_lower = self.skill_markdown.lower()

        if '批' in content_lower or '多个' in content_lower or '所有' in content_lower:
            return 'batch'
        elif 'api' in content_lower or '请求' in content_lower or '调用' in content_lower:
            return 'api'
        elif '文件' in content_lower or '文档' in content_lower:
            return 'file'
        elif '数据' in content_lower or 'dataset' in content_lower:
            return 'data'
        else:
            return 'sequential'

    def suggest_theme(self) -> str:
        """建议合适的主题"""
        content_lower = self.skill_markdown.lower()

        if 'professional' in content_lower or '工作' in content_lower or '商务' in content_lower:
            return 'professional'
        elif 'fun' in content_lower or '游戏' in content_lower or '娱乐' in content_lower:
            return 'colorful'
        elif '快速' in content_lower or '简单' in content_lower or 'minimal' in content_lower:
            return 'minimal'
        else:
            return 'default'

    def generate_summary(self) -> Dict[str, Any]:
        """生成分析摘要"""
        return {
            'skill_name': self.skill_info.get('name', self.skill_name),
            'description': self.skill_info.get('description', ''),
            'purpose': self.skill_info.get('purpose', ''),
            'workflow_type': self.detect_processing_type(),
            'steps_count': len(self.workflow_steps),
            'suggested_theme': self.suggest_theme(),
            'steps': self.workflow_steps
        }


class CodeGenerator:
    """生成带进度显示的代码"""

    def __init__(self, analyzer: SkillAnalyzer):
        self.analyzer = analyzer
        self.summary = analyzer.generate_summary()

    def generate_progress_code(self) -> str:
        """生成带进度显示的完整代码"""

        skill_name = self.summary['skill_name']
        theme = self.summary['suggested_theme']
        steps = self.summary['steps']

        # 生成代码
        code = f'''#!/usr/bin/env python3
"""
{skill_name} - 带可视化进度界面

由 visual-interface-generator 自动生成
"""

import sys
import time
sys.path.insert(0, '/Users/ezra/.claude/skills/visual-progress')
from core.visual_progress import VisualProgress

def {self._to_snake_case(skill_name)}(input_data):
    """
    {skill_name} 主处理函数（带可视化进度）

    工作流程:
'''

        # 添加工作流步骤注释
        for i, step in enumerate(steps, 1):
            code += f"    {i}. {step['name']}\n"

        code += f'''

    初始化进度追踪器
    """
    progress = VisualProgress(
        title="{skill_name}",
        theme="{theme}"
    )

    # 定义每个处理步骤
'''

        # 生成步骤函数
        for i, step in enumerate(steps):
            step_id = step['id']
            step_name = step['name']
            code += f'''    def {step_id}_func(task_id, task_info):
        """{step_name}"""
        # TODO: 实现 {step_name} 的逻辑
        # print(f"执行: {step_name}")
        # time.sleep(0.5)  # 模拟处理
        return {{"status": "completed", "step": "{step_id}"}}

'''

        # 生成工作流定义
        code += '    # 定义工作流任务\n'
        code += '    workflow = [\n'
        for step in steps:
            code += f"        {{'id': '{step['id']}', 'name': '{step['name']}', 'total': 100}},\n"
        code += '    ]\n\n'

        # 生成执行代码
        code += '''    # 执行工作流（自动显示可视化进度）
    results = progress.run_tasks(workflow, lambda tid, info: {
'''

        for step in steps:
            code += f"        '{step['id']}': {step['id']}_func,\n"

        code += f'''    }}[tid](tid, info))

    return results


# 使用示例
if __name__ == '__main__':
    # TODO: 替换为实际的输入数据
    input_data = {{"example": "data"}}

    results = {self._to_snake_case(skill_name)}(input_data)

    print("\\n[OK] 处理完成!")
    print(f"结果: {{results}}")
'''

        return code

    def _to_snake_case(self, name: str) -> str:
        """转换为 snake_case"""
        # 移除特殊字符，转换为小写，用下划线连接
        s = re.sub(r'[^\w\s]', '', name)
        s = re.sub(r'[-\s]+', '_', s)
        return s.lower().strip('_')


def generate_visual_interface(skill_path: str, output_path: str = None) -> str:
    """
    为 Skill 生成可视化界面

    Args:
        skill_path: Skill 路径 (如: ~/.claude/skills/auto-redbook-skills)
        output_path: 输出文件路径 (可选)

    Returns:
        生成的代码
    """

    print(f"\\n{'='*60}")
    print(f"[Gen] 为 Skill 生成可视化界面")
    print(f"{'='*60}")

    # 1. 分析 Skill
    print(f"\\n[Folder] 分析 Skill: {skill_path}")
    analyzer = SkillAnalyzer(skill_path)

    if not analyzer.read_skill_markdown():
        return None

    print(f"[Book] 提取基本信息...")
    info = analyzer.extract_skill_info()
    print(f"   名称: {info.get('name', 'Unknown')}")
    print(f"   描述: {info.get('description', 'No description')[:80]}...")

    print(f"\\n[Search] 分析工作流程...")
    workflow = analyzer.analyze_workflow()
    print(f"   识别到 {len(workflow)} 个步骤:")

    for i, step in enumerate(workflow, 1):
        print(f"   {i}. {step['name']}")

    processing_type = analyzer.detect_processing_type()
    print(f"\\n[Info] 处理类型: {processing_type}")

    theme = analyzer.suggest_theme()
    print(f"   建议主题: {theme}")

    # 2. 生成代码
    print(f"\\n[Magic] 生成可视化代码...")
    generator = CodeGenerator(analyzer)
    code = generator.generate_progress_code()

    # 3. 保存或输出
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)

        print(f"\\n[OK] 代码已保存到: {output_path}")
    else:
        print(f"\\n{'='*60}")
        print(f"[Doc] 生成的代码:")
        print(f"{'='*60}\\n")
        print(code)

    # 4. 生成总结
    summary = analyzer.generate_summary()
    print(f"\\n{'='*60}")
    print(f"[List] 分析总结")
    print(f"{'='*60}")
    print(f"Skill 名称: {summary['skill_name']}")
    print(f"工作流类型: {summary['workflow_type']}")
    print(f"识别步骤数: {summary['steps_count']}")
    print(f"建议主题: {summary['suggested_theme']}")

    return code


# CLI 接口
def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='为 Skill 自动生成可视化进度界面'
    )
    parser.add_argument(
        'skill_path',
        help='Skill 路径 (如: ~/.claude/skills/auto-redbook-skills)'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径 (如: enhanced_skill.py)'
    )
    parser.add_argument(
        '--theme',
        choices=['default', 'minimal', 'colorful', 'professional', 'detailed'],
        help='覆盖建议的主题'
    )

    args = parser.parse_args()

    # 生成可视化界面
    code = generate_visual_interface(args.skill_path, args.output)

    if code:
        print(f"\\n[Success] 成功! 现在可以使用生成的带进度显示的代码了")
        return 0
    else:
        print(f"\\n[Error] 失败! 请检查 Skill 路径是否正确")
        return 1


if __name__ == '__main__':
    sys.exit(main())
