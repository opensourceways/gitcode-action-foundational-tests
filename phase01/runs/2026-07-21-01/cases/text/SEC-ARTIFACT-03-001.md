用例 ID:   SEC-ARTIFACT-03-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-026
母意图:    —
标题:      跨 job artifact 在 fork PR 场景下不应被后续高权限 job 无条件信任

前置条件:
  - 存在 fork PR 可触发 pull_request workflow
  - 后续内部 push workflow 尝试下载 artifact

操作步骤:
  1. fork PR workflow 上传 artifact
  2. 内部 push workflow 尝试下载相同 artifact
  3. 观察是否可自动下载

预期结果:
  - fork PR artifact 不被内部 push workflow 自动下载
  - artifact 作用域应与触发事件和权限上下文绑定

验证点:
  - [负向] fork PR workflow 上传 artifact，后续内部 push workflow 不应能自动下载
  - [负向] 若支持跨 workflow artifact 下载，应提供来源标识

清理:      fixture
