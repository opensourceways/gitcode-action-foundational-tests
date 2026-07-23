用例 ID:   USE-ERR-MSG-02-004
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-002
标题:      字段类型错误时的错误信息可诊断性

前置条件:
  - 在 YAML 中将期望的类型写错：runs-on 写成 string（非 list）、env 写成 string（非 map）

操作步骤:
  1. 配置 `runs-on: ubuntu-latest`（string 而非三段式 list）→ 验证错误消息
  2. 配置 `env: "foo"`（string 而非 map）→ 验证错误消息
  3. 验证错误消息是否指出字段路径、期望类型、实际类型、行号

预期结果:
  - 类型错误消息含：字段路径 + 期望类型 + 实际类型 + 文件行号
  - 非泛化的 "type mismatch"

验证点:
  - [正向] runs-on 类型错误被点名
  - [正向] env 类型错误被点名
  - [非功能] 错误消息含字段路径 + 期望类型 + 实际类型 + 行号

可理解性判据: eval: llm_assisted
清理:      fixture
