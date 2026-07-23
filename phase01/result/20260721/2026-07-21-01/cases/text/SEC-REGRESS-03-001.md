用例 ID:   SEC-REGRESS-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-050
母意图:    —
标题:      [回归 #51] fork 仓提 PR 应完全隔离主仓密钥

前置条件:
  - 主仓库配置了项目级 Secret DEPLOY_TOKEN（已知值用于断言比对）
  - 主仓库配置了组织级 Secret ORG_TOKEN
  - 存在一个来自 fork 仓库的 PR（含 workflow 文件引用上述 Secret）

操作步骤:
  1. 以外部 fork 贡献者身份，在主仓 `.gitcode/workflows/` 下创建一个 workflow，在 `run:` 中 echo `${{ secrets.DEPLOY_TOKEN }}` 和 `${{ secrets.ORG_TOKEN }}`
  2. 向主仓提交 fork PR 触发 pull_request 事件
  3. 观察 job 日志输出

预期结果:
  - fork PR 触发的 job 日志中不出现 DEPLOY_TOKEN 和 ORG_TOKEN 的原始值
  - secret 引用返回空字符串或被遮蔽为 `***`
  - 基于 secret 值的 API 调用返回 401/403 认证失败

验证点:
  - [负向] job 日志搜索 DEPLOY_TOKEN 已知明文值，命中数 = 0
  - [负向] job 日志搜索 ORG_TOKEN 已知明文值，命中数 = 0
  - [负向] 使用 ${{ secrets.DEPLOY_TOKEN }} 做 HTTP Authorization 头的 API 调用返回 401/403
  - [正向] 同一 workflow 在内部 PR（非 fork）触发时，Secret 应正常可用——确保 secret 本身有效

清理:      fixture
