# 🧩 模块化 Prompt 设计

> 针对 Token 优化的分层 Prompt 结构

---

## 核心理念

```
一个优化良好的 Prompt 应该包含以下模块（按重要性排序）：

1. Identity (身份) - 20 tokens
2. Task (任务) - 50-200 tokens  
3. Context (上下文) - 按需，最小化
4. Constraints (约束) - 50-100 tokens
5. Output Format (输出格式) - 30-50 tokens
```

---

## 模块化模板

### 最小化模式 (Simple Task)

```
[Identity]
你是一位 Python 工程师。

[Task]
修复以下函数的 bug：
```python
def divide(a, b):
    return a / b
```

[Constraints]
- 考虑除零情况
- 返回 None 而非抛出异常

[Output]
直接给出修复后的代码。
```

### 标准模式 (Normal Task)

```
[Identity]
你是一位 [角色]，专精 [领域]。

[Task]
[详细任务描述]

[Context - 关键信息]
- 相关文件：[文件路径]
- 历史参考：[memory:关键词]

[Constraints]
1. [约束1]
2. [约束2]

[Output Format]
```json
{
  "result": "...",
  "confidence": 0.95
}
```

[Negative Constraints]
- 不要 [危险操作]
- 避免 [已知问题]
```

### 完整模式 (Complex Task)

```
[Identity]
你是 [角色]，拥有 [年限] 经验。

[Mission]
[高层次目标]

[Task Breakdown]
1. 阶段一：[子任务]
2. 阶段二：[子任务]
3. 阶段三：[子任务]

[Context]
## 相关信息
- 文件：[路径]
- 依赖：[列表]
- 约束：[条件]

## 历史参考
[从 memory 检索的相关信息]

## 当前状态
[已完成的步骤]
[遇到的问题]

[Tools Available]
- [工具1]: [用途]
- [工具2]: [用途]

[Constraints]
### 必须
- [必须遵守的规则]

### 禁止
- [绝对禁止的操作]

### 限制
- Token 预算：[数量]
- 执行时间：[限制]

[Quality Standards]
- [质量标准1]
- [质量标准2]

[Output Format]
## 最终输出
[格式要求]

## 验证清单
- [ ] 检查点1
- [ ] 检查点2

[Self-Correction]
如果遇到错误：
1. 分析错误原因
2. 提出修复方案
3. 等待确认后执行
```

---

## Token 优化技巧

### 1. 使用缩写

```
# 原始 (120 tokens)
You are a senior software engineer with expertise in Python and JavaScript.

# 优化 (15 tokens)
You are a Sr. Python/JS engineer.
```

### 2. 省略显式声明

```
# 原始 (80 tokens)
Please provide a detailed explanation of the code above.

# 优化 (25 tokens)
Explain the code above.
```

### 3. 压缩上下文

```
# 原始 (200 tokens)
Based on our previous conversation about the login flow, and considering the bug report you submitted yesterday about the session timeout issue, please analyze...

# 优化 (50 tokens)
Context: login bug, session timeout, report from yesterday.
Task: analyze the issue.
```

### 4. 条件分支

```
# 使用 JSON 压缩可选参数
{
  "task": "fix bug",
  "context": {"file": "auth.py", "line": 42},
  "constraints": {"strict": true}  // 只有需要时才包含
}
```

---

## Minimal Mode 模板库

### 代码生成 (Minimal)

```
[Role] Python dev
[Task] Create [function description]
[Input] [parameters]
[Output] code only
[Constraint] O(n), type hints, docstring
```

### 代码审查 (Minimal)

```
[Role] Sr. Eng
[Task] Review code for bugs/security
[Input] 
```
[code]
```
[Output] JSON: {critical:[], medium:[], suggestions:[]}
```

### 写作 (Minimal)

```
[Role] Tech writer
[Topic] [subject]
[Style] [tone]
[Length] [words]
[Output] markdown
```
