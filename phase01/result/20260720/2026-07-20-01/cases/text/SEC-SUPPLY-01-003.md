用例 ID:   SEC-SUPPLY-01-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-026
标题:      跨 job artifact 在 fork PR 场景下不应被后续高权限 job 无条件信任

前置条件:
  - 仓库有 fork PR workflow（低权限）和 push workflow（高权限）
  - fork PR workflow 上传 artifact
  - push workflow 尝试下载 artifact

操作步骤:
  1. fork PR 触发 workflow 上传 artifact fork-artifact
  2. 内部 push 触发 workflow 尝试下载 fork-artifact
  3. 验证内部 push workflow 是否能无条件获取 fork PR 的 artifact
  4. 若可获取，验证 artifact 来源是否有标识

预期结果:
  - fork PR 上传的 artifact 不被内部 push workflow 自动/隐式继承
  - 跨 workflow artifact 下载需显式引用 run ID
  - 同 workflow 内 artifact 正常传递

验证点:
  - [负向] 内部 push workflow 默认不能下载 fork PR 的 artifact
  - [负向] artifact 不存在跨信任边界隐式传递
  - [正向] 同 workflow 内 artifact 正常传递

清理:      fixture
