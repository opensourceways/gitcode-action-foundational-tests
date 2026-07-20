用例 ID:   SEC-FORKPR-03-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-002
母意图:    —
标题:      fork PR 触发 pull_request 时不可访问项目级和组织级 Secret

前置条件:
  - 主仓库配置了项目级 Secret DEPLOY_TOKEN 和组织级 Secret ORG_KEY
  - 来自 fork 的 PR

操作步骤:
  1. fork PR 触发 workflow，在 run 中 echo ${{ secrets.DEPLOY_TOKEN }}
  2. 同样 echo ${{ secrets.ORG_KEY }}
  3. 用 Secret 值做 HTTP Bearer 认证
  4. 对比：内部 PR 下同样 workflow 应正常读取 Secret

预期结果: fork PR 下 Secret 引用返回空字符串；日志不出现明文；API 认证失败

验证点:
  - [负向] 日志搜索已知 secret 明文命中数 = 0
  - [负向] Secret 在 fork PR 下应为空值
  - [正向] 内部 PR 下同一 Secret 可正常引用（确保 secret 本身有效）
  - [回归] 复现 history #51 场景

清理: fixture
