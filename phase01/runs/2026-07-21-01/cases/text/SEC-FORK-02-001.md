用例 ID:   SEC-FORK-02-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-001
母意图:    —
标题:      fork PR 触发 pull_request 时 ATOMGIT_TOKEN 应为只读
incorporates: TC-345 (fork 触发事件), TC-100 (secrets.atomgit_token 引用)

前置条件:
  - 仓库配置了项目级 Secret（DEPLOY_TOKEN）
  - 存在一个来自外部 fork 的 PR
  - fork 侧的 workflow 声明了 permissions: write-all
  - 目标仓库配置了含 write 的默认 permissions

操作步骤:
  1. 以外部 fork 贡献者身份，提交 PR 到目标仓库
  2. PR 触发 pull_request 事件
  3. 在 job 中验证：(a) git clone 代码成功，(b) git push 被拒绝，(c) 项目级 Secret 不可读，(d) API 写操作被拒

预期结果:
  - fork PR 的 ATOMGIT_TOKEN 仅具 repository:read
  - git push 返回 Permission denied 或 403
  - ${{ secrets.DEPLOY_TOKEN }} 为空字符串
  - 无论 permissions 声明为何，Token 强制降级为只读

验证点:
  - [正向] fork PR job 可正常 clone 代码
  - [负向] fork PR job 的 git push 应被拒绝
  - [负向] fork PR job 中 ${{ secrets.DEPLOY_TOKEN }} 值为空
  - [负向] 日志中不出现 DEPLOY_TOKEN 明文

清理:      fixture
