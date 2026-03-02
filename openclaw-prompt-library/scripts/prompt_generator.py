#!/usr/bin/env python3
"""
OpenClaw Prompt Generator - 提示词生成器
根据模板自动生成定制化提示词
"""

import json
import os
from datetime import datetime

# ============ 模板库 ============

TEMPLATES = {
    "code_generation": {
        "name": "代码生成",
        "template": """创建一个 {language} 函数，实现 {function_description}
要求：
- 输入：{input_params}
- 输出：{output_description}
- 时间复杂度：{complexity}
- 包含错误处理
- 包含类型注解""",
        "params": ["language", "function_description", "input_params", "output_description", "complexity"]
    },
    
    "code_review": {
        "name": "代码审查",
        "template": """审查以下 {language} 代码：

```{language}
{code}
```

请指出：
1. 潜在 bug
2. 性能问题
3. 安全漏洞
4. 代码风格建议
5. 改进建议（按优先级排序）""",
        "params": ["language", "code"]
    },
    
    "article": {
        "name": "文章撰写",
        "template": """写一篇关于 {topic} 的文章：
- 字数：{word_count}
- 风格：{style}
- 受众：{audience}
- 要点：
  1. {point_1}
  2. {point_2}
  3. {point_3}
- 包含 {case_count} 个案例
- 结尾要有行动号召""",
        "params": ["topic", "word_count", "style", "audience", "point_1", "point_2", "point_3", "case_count"]
    },
    
    "social_media": {
        "name": "社交媒体",
        "template": """生成 {count} 条 {platform} 推文：
- 主题：{topic}
- 风格：{tone}
- 每条不超过 {max_chars} 字符
- 包含相关 hashtag
- 包含行动号召

格式：
```
标题：[推文内容]
```""",
        "params": ["count", "platform", "topic", "tone", "max_chars"]
    },
    
    "email": {
        "name": "邮件模板",
        "template": """写一封 {email_type} 邮件：
- 收件人：{recipient}
- 目的：{purpose}
- 语气：{tone}
- 关键信息：
  - {info_1}
  - {info_2}
- 期望行动：{cta}

格式要求：
- 主题行：{subject}
- 开头称呼：{salutation}
- 结尾签名：{signature}""",
        "params": ["email_type", "recipient", "purpose", "tone", "info_1", "info_2", "cta", "subject", "salutation", "signature"]
    },
    
    "workflow": {
        "name": "工作流设计",
        "template": """设计 OpenClaw 自动化工作流：

**触发条件**：{trigger}

**执行步骤**：
1. {step_1}
2. {step_2}
3. {step_3}

**条件分支**：
- 如果 {condition_a} → 执行 {action_a}
- 如果 {condition_b} → 执行 {action_b}

**完成后**：
- 通知方式：{notification}
- 日志记录：{logging}""",
        "params": ["trigger", "step_1", "step_2", "step_3", "condition_a", "action_a", "condition_b", "action_b", "notification", "logging"]
    },
    
    "data_analysis": {
        "name": "数据分析",
        "template": """分析数据集：
- 数据来源：{data_source}
- 数据量：{data_size}
- 时间范围：{time_range}

**分析目标**：
1. {goal_1}
2. {goal_2}

**输出要求**：
- 图表类型：{chart_types}
- 报告格式：{format}
- 关键指标：{metrics}

**预期发现**：
- {finding_1}
- {finding_2}""",
        "params": ["data_source", "data_size", "time_range", "goal_1", "goal_2", "chart_types", "format", "metrics", "finding_1", "finding_2"]
    },
    
    "seo_content": {
        "name": "SEO 内容",
        "template": """写一篇 SEO 优化的文章：

**目标关键词**：{primary_keyword}
**长尾关键词**：{long_tail_keywords}

**文章结构**：
- H1：{h1_title}
- H2（4-6个）：{h2_outline}
- H3：{h3_details}

**要求**：
- 字数：{word_count}
- 关键词密度：1-2%
- 包含内部链接建议
- Meta 描述（<160字符）：{meta_description}

**SEO 最佳实践**：
- 使用小标题
- 列表和表格
- 图片 alt 文本""",
        "params": ["primary_keyword", "long_tail_keywords", "h1_title", "h2_outline", "h3_details", "word_count", "meta_description"]
    }
}


def generate_prompt(template_name: str, params: dict) -> str:
    """根据模板生成提示词"""
    if template_name not in TEMPLATES:
        raise ValueError(f"未知模板: {template_name}")
    
    template = TEMPLATES[template_name]
    prompt = template["template"]
    
    for key, value in params.items():
        prompt = prompt.replace(f"{{{key}}}", str(value))
    
    return prompt


def list_templates():
    """列出所有可用模板"""
    print("\n📚 可用模板：")
    print("-" * 40)
    for key, info in TEMPLATES.items():
        print(f"  {key:20} - {info['name']}")
    print()


def interactive_mode():
    """交互式生成"""
    print("\n🚀 OpenClaw 提示词生成器")
    print("=" * 40)
    
    list_templates()
    
    template_name = input("选择模板 (输入名称): ").strip()
    
    if template_name not in TEMPLATES:
        print("❌ 无效模板")
        return
    
    template = TEMPLATES[template_name]
    print(f"\n📝 填写参数 ({template['name']})")
    print("-" * 40)
    
    params = {}
    for param in template["params"]:
        value = input(f"  {param}: ").strip()
        params[param] = value or f"[{param}]"
    
    print("\n" + "=" * 40)
    print("✨ 生成的提示词：")
    print("=" * 40)
    print(generate_prompt(template_name, params))
    print("=" * 40)


def generate_from_args(template_name: str, **kwargs) -> str:
    """从命令行参数生成"""
    return generate_prompt(template_name, kwargs)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            list_templates()
        elif sys.argv[1] == "--interactive":
            interactive_mode()
        else:
            # 从文件读取参数
            if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
                with open(sys.argv[2], 'r') as f:
                    params = json.load(f)
                template_name = sys.argv[1]
                print(generate_from_args(template_name, **params))
            else:
                print("用法:")
                print("  python prompt_generator.py --list")
                print("  python prompt_generator.py --interactive")
                print("  python prompt_generator.py <模板名> <参数文件.json>")
    else:
        interactive_mode()
