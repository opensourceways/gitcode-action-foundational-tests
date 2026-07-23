用例 ID:   SEC-FORKART-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-019
母意图:    —
标题:      fork PR 上传的 artifact 不可被主仓 workflow 下载或执行

前置条件:
  - 主仓配置了 workflow 可上传 artifact
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在 fork PR 的 workflow 中上传一个 artifact
  2. 在主仓 workflow 中尝试通过 download-artifact 下载该 fork PR 产生的 artifact
  3. 观察主仓 workflow 执行结果

预期结果:
  - 主仓 workflow 无法下载或访问 fork PR 上传的 artifact
  - 系统返回权限不足或 artifact 不存在的错误
  - 主仓 workflow 不会因下载到不可信 artifact 而执行其中内容

验证点:
  - [负向] 主仓 workflow 未成功下载 fork PR 的 artifact
  - [负向] 主仓 workflow 未执行 fork PR artifact 中的内容
  - [正向] 系统返回明确的隔离或权限错误

清理:      重置 fixture 仓库
