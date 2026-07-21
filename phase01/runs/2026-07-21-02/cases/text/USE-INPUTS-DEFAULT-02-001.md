用例 ID:   USE-INPUTS-DEFAULT-02-001
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-025
母意图:    —
标题:      inputs 默认值在 shell 中以 ${var} 直接引用是否可用/失败可诊断

前置条件:
  - workflow 定义了 workflow_dispatch inputs 并带有默认值

操作步骤:
  1. 通过手动触发 workflow 且不传参
  2. 在 shell 中使用 ${var} 引用 inputs 默认值
  3. 观察运行结果与报错信息

预期结果:
  - 若 GitCode 支持 ${var} 语法，则默认值应正确注入
  - 若不支持，报错应指明正确引用方式

验证点:
  - [正向] 默认值正确注入 shell
  - [nonfunctional] 错误信息可诊断

清理:      重置 fixture 仓库
