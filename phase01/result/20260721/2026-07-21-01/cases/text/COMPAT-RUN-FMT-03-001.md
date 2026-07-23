用例 ID:   COMPAT-RUN-FMT-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-060
标题:      runs-on 标签格式：三段式数组 [ubuntu-latest, x64, small] vs GitHub 单标签 ubuntu-latest

前置条件:
  - 使用不同 runs-on 格式的 workflow

操作步骤:
  1. 使用 GitCode 三段式数组 runs-on: [ubuntu-latest, x64, small]
  2. 使用 GitHub 单标签 runs-on: ubuntu-latest
  3. 使用 runs-on: [ubuntu-24, x64, small] 精确 OS 版本
  4. 对比三种写法是否都能成功调度

预期结果:
  - 三段式数组应正常调度（GitCode 标准格式）
  - GitHub 单标签可能报错或被视为 default
  - 若单标签被接受：文档应声明兼容性

验证点:
  - [正向] 三段式数组正常执行
  - [正向] 单标签行为明确（报错或被接受）
  - [正向] 报错消息指引用户使用三段式格式

清理:      fixture
