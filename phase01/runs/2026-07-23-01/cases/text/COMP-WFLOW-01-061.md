用例 ID:   COMP-WFLOW-01-061
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-366~401
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      workflow name 与 on 字段必填与类型验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 name 和 on 的 workflow
  2. 验证 name 为可选但 on 为必填，on 必须为 map

预期结果:
  - workflow 可正常提交并触发，name 缺省时使用文件名，on 为 map 格式

验证点:
  - [正向] 含 name 的 workflow 被正确显示
  - [正向] on 为 map 时 workflow 可被触发
  - [负向] on 为数组时平台拒绝

清理:      重置 fixture 仓库
