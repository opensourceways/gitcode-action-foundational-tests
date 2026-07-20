用例 ID:   SEC-FORK-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-002
母意图:    —
标题:      fork PR 触发 pull_request 时不可访问项目/组织级 Secret

前置条件:
  - 仓库配置了项目级 Secret（DEPLOY_TOKEN）和组织级 Secret（ORG_SECRET）
  - 存在一个来自外部 fork 的 PR
  - 内部 PR（同仓库分支）场景也需准备作为对照组

操作步骤:
  1. 从 fork 仓库提交 PR，触发 `pull_request` 事件
  2. 在 fork PR 的 job 中使用 `${{ secrets.DEPLOY_TOKEN }}` 做 echo 输出
  3. 在 fork PR 的 job 中尝试用 DEPLOY_TOKEN 做 HTTP 认证调用
  4. 以内部 PR（同仓库不同分支）触发同一 workflow，验证 Secret 正常可用
  5. 对比 fork PR 和内部 PR 中 Secret 的可用性差异

预期结果:
  - fork PR 下 `${{ secrets.DEPLOY_TOKEN }}` 和 `${{ secrets.ORG_SECRET }}` 求值为空字符串
  - fork PR 下基于 Secret 的 API 调用返回认证失败（401/403）
  - 内部 PR 下同一 workflow 中 Secret 正常可用（正确注入）
  - 日志中不出现任何 Secret 明文

验证点:
  - [负向] fork PR 下 echo Secret 到日志，输出为空白（或 `***`）
  - [负向] fork PR 下用 Secret 做 HTTP 认证，请求失败（401/403）
  - [正向] 内部 PR 下同一 workflow 中 Secret 正常可用
  - [负向] 日志全文搜索 Secret 明文命中数为 0

清理:      fixture
