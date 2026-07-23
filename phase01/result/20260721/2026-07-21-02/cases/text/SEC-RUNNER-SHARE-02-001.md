用例 ID:   SEC-RUNNER-SHARE-02-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-028
母意图:    —
标题:      多项目共享 Runner 的 Secret 与资源隔离（项目 A secret 不达项目 B）

前置条件:
  - 同一 runner 组被多个项目共享
  - 项目 A 配置了 SECRET_A，项目 B 未配置同名 secret

操作步骤:
  1. 在项目 A 的 workflow 中输出 secrets.SECRET_A
  2. 在项目 B 的 workflow 中尝试读取 secrets.SECRET_A
  3. 观察两项目的运行结果

预期结果:
  - 项目 B 的 workflow 不应读取到项目 A 的 SECRET_A
  - runner 上的 secret 注入应严格按项目隔离

验证点:
  - [负向] 项目 B 日志不含 SECRET_A 明文
  - [正向] 项目 B 中 secrets.SECRET_A 为空或报错

清理:      重置 fixture 仓库
