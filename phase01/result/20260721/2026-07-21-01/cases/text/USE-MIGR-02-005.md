用例 ID:   USE-MIGR-02-005
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-018
标题:      workflow_dispatch inputs 使用 GitHub 支持的非 string 类型时的行为与报错

前置条件:
  - workflow_dispatch 或 workflow_call inputs 中使用非 string 类型

操作步骤:
  1. 配置 `type: boolean` → 验证报错且提示仅支持 string
  2. 配置 `type: number` → 同上
  3. 配置 `type: choice` → 同上
  4. 验证错误消息是否明确指出 GitCode 仅支持 string

预期结果:
  - 非 string 类型明确报错
  - 错误信息指明 GitCode 仅支持 string 类型
  - 不静默当 string 处理

验证点:
  - [正向] boolean/number/choice 均被报错
  - [正向] 错误消息提示仅支持 string
  - [负向] 不静默当 string 处理

可理解性判据: eval: llm_assisted
清理:      fixture
