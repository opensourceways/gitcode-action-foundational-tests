用例 ID:   SEC-FORK-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-001
母意图:    —
标题:      fork PR 触发 pull_request 时 ATOMGIT_TOKEN 应为只读

前置条件:
  - 仓库配置了项目级 Secret（DEPLOY_TOKEN）
  - 存在一个来自外部 fork 的 PR
  - fork 侧的 workflow 声明了 permissions: write-all
  - 目标仓库配置了默认 permissions（含 write）

操作步骤:
  1. 以外部 fork 贡献者身份，提交 PR 到目标仓库
  2. PR 触发 `pull_request` 事件，执行 fork 侧的 workflow（若 base 分支有 workflow 定义则执行 base 侧）
  3. 在 job 中尝试：(a) git clone 代码，(b) git push 到目标仓库，(c) 通过 API 创建 PR 评论，(d) 读取项目级 Secret

预期结果:
  - fork PR 触发的 job 可正常 clone 代码（repository:read 最低权限）
  - fork PR 触发的 job 不应能推送代码到目标仓库（repository:write 被拒绝）
  - fork PR 触发的 job 不应能通过 API 创建/修改 PR 评论（pr:write 被拒绝）
  - fork PR 触发的 job 不应能读取项目级 Secret（${{ secrets.DEPLOY_TOKEN }} 为空）
  - 无论 workflow 中 permissions 声明为何，fork PR 下 Token 强制降级为只读

验证点:
  - [正向] fork PR job 可正常 clone 代码
  - [负向] fork PR job 的 git push 应被拒绝（返回 403 或 Permission denied）
  - [负向] fork PR job 通过 API 创建 PR 评论应被拒绝（返回 403）
  - [负向] fork PR job 中 ${{ secrets.DEPLOY_TOKEN }} 值为空字符串
  - [负向] 日志中不出现 DEPLOY_TOKEN 明文

清理:      fixture
