用例 ID:   SEC-FORK-02-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-002
标题:      fork PR 触发 pull_request 时不可访问项目/组织级 Secret

前置条件:
  - 仓库配置了项目级 Secret（DEPLOY_KEY）和组织级 Secret（ORG_TOKEN）
  - 存在来自外部 fork 的 PR

操作步骤:
  1. fork PR 触发的 workflow 中分别 echo ${{ secrets.DEPLOY_KEY }} 和 ${{ secrets.ORG_TOKEN }}
  2. 尝试用 Secret 值做 HTTP 认证请求（curl -H "Authorization: Bearer ${{ secrets.DEPLOY_KEY }}"）
  3. 同一 workflow 在内部 PR 下触发，验证 Secret 正常可用（对照）

预期结果:
  - fork PR 下 ${{ secrets.DEPLOY_KEY }} 和 ${{ secrets.ORG_TOKEN }} 求值为空字符串
  - 基于空 Secret 的 API 调用返回 401/403
  - 日志中不出现 Secret 明文
  - 内部 PR 下 Secret 正常可用

验证点:
  - [负向] fork PR 日志 echo Secret 输出为空
  - [负向] fork PR 下 HTTP 认证请求失败
  - [正向] 内部 PR 下同一 Secret 正常可用
  - [负向] 日志中不出现 Secret 明文

清理:      fixture
