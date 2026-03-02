# 🔄 自我修复 Prompt 逻辑

> 包含 Plan-Act-Verify 循环的错误处理模板

---

## 核心理念

```
Agent 遇到错误时的处理流程：

1. 感知 (Perceive) - 识别错误类型
2. 分析 (Analyze) - 定位原因
3. 计划 (Plan) - 制定修复方案
4. 验证 (Verify) - 确认修复有效
5. 报告 (Report) - 通知用户
```

---

## 通用错误处理模板

### Shell 命令错误

```
【执行命令】
[原始命令]

【遇到错误】
[错误输出]

【分析阶段】
1. 错误类型：
   - [x] 命令不存在 (command not found)
   - [ ] 权限不足 (permission denied)
   - [ ] 路径错误 (No such file or directory)
   - [ ] 参数错误 (invalid argument)
   - [ ] 超时 (timeout)
   - [ ] 其他：________

2. 原因分析：
   [分析结果]

【修复方案】
- 方案 A：[描述] - 适用于 [场景]
- 方案 B：[描述] - 适用于 [场景]

【行动计划】
1. [第一步]
2. [第二步]
3. [第三步]

【等待确认】
请选择修复方案或输入新的指令：
- A: 执行方案 A
- B: 执行方案 B  
- C: 手动输入修复命令
- S: 停止并报告问题
```

### 文件操作错误

```
【操作】
[操作描述: read/write/delete]

【目标】
[文件路径]

【遇到错误】
[错误信息]

【分析】
1. 错误类型：
   - [ ] 文件不存在
   - [ ] 权限不足
   - [ ] 目录不存在
   - [ ] 磁盘空间不足
   - [ ] 文件被占用

2. 可能原因：
   - [ ] 路径拼写错误
   - [ ] 文件未创建
   - [ ] 需要先创建父目录
   - [ ] 需要先创建文件

【修复步骤】
1. 检查当前状态：
   ```bash
   ls -la [父目录]
   ```
2. [根据结果选择操作]

【验证】
修复后，确认：
- 文件存在：✅/❌
- 权限正确：✅/❌
- 内容正确：✅/❌
```

### API/网络错误

```
【请求】
[API 端点/请求描述]

【错误响应】
[HTTP 状态码]
[错误信息]

【错误分类】
1. 4xx 客户端错误：
   - 401: 认证失败 → 检查 API Key
   - 403: 权限不足 → 检查权限
   - 404: 资源不存在 → 检查 URL
   - 429: 请求过多 → 添加重试/延迟

2. 5xx 服务器错误：
   - 暂时性错误 → 重试策略
   - 持久性错误 → 报告用户

【重试策略】
- 重试次数：3
- 延迟策略：指数退避 (1s, 2s, 4s)
- 超时时间：30s

【代码示例】
```python
import time

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt
            print(f"Retry in {wait}s...")
            time.sleep(wait)
```
```

---

## 浏览器自动化错误处理

### 页面加载失败

```
【操作】
打开 [URL]

【错误】
[Selenium/WebDriver 错误]

【分析】
1. 可能原因：
   - [ ] 网络问题
   - [ ] 页面不存在
   - [ ] JS 渲染问题
   - [ ] 元素选择器失效

2. 诊断步骤：
   ```bash
   # 检查网络
   curl -I [URL]
   
   # 检查页面源码
   curl [URL] | head -100
   ```

【修复方案】
- 方案 A: 等待 JS 渲染 (添加 explicit wait)
- 方案 B: 使用备用选择器
- 方案 C: 截图诊断

【验证】
- 页面标题正确：✅/❌
- 关键元素存在：✅/❌
- 无 JavaScript 错误：✅/❌
```

### 元素定位失败

```
【操作】
点击 [元素描述]

【错误】
NoSuchElementException / ElementNotVisible

【分析】
1. 元素定位方式：
   - ID: [id]
   - CSS: [selector]
   - XPath: [xpath]

2. 可能原因：
   - [ ] 元素还未加载
   - [ ] 元素在 iframe 中
   - [ ] 元素被遮挡
   - [ ] 页面动态变化

【修复方案】
1. 添加等待：
   ```python
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.element_to_be_clickable((By.ID, "id")))
   ```

2. 使用 JavaScript 点击：
   ```python
   driver.execute_script("arguments[0].click();", element)
   ```

【备选方案】
如果多次失败：
1. 截图当前状态
2. 记录 HTML
3. 询问用户下一步
```

---

## OpenClaw 特定错误

### 心跳任务失败

```
【任务】
[heartbeat/定时任务名称]

【错误】
[错误输出]

【分析】
1. 失败阶段：
   - [ ] 任务触发
   - [ ] 上下文加载
   - [ ] 执行
   - [ ] 结果报告

2. 原因：
   - [ ] Token 超限
   - [ ] 工具不可用
   - [ ] 外部依赖失败

【恢复策略】
1. 检查系统状态：
   - [ ] Gateway 运行中
   - [ ] 内存充足
   - [ ] 工具可用

2. 简化任务：
   - 减少上下文
   - 使用更快模型
   - 拆分任务

3. 回退方案：
   - 记录失败
   - 下次重试
   - 通知用户
```

### 记忆检索失败

```
【操作】
memory_recall([查询])

【错误】
[错误信息]

【分析】
1. 问题类型：
   - [ ] 数据库不可用
   - [ ] 向量服务未运行
   - [ ] 查询语法错误
   - [ ] 结果为空

2. 备用方案：
   - 搜索 memory/ 目录
   - 使用 grep
   - 询问用户
```
