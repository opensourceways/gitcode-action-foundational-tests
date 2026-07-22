用例 ID:   SEC-ACTION-PERM-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-022
母意图:    —
标题:      第三方 action 对 ATOMGIT_TOKEN / secret 的隐式获取受最小权限约束

前置条件:
  - 仓库配置了 TEST_SECRET
  - 使用一个非官方第三方 action

操作步骤:
  1. 在 workflow 中调用第三方 action
  2. 该 action 的代码尝试读取 secrets.TEST_SECRET 或 atomgit.token
  3. 观察运行日志与权限行为

预期结果:
  - 第三方 action 不应默认获得仓库 secrets 访问权
  - 系统应通过 permissions 或 token 范围限制其权限

验证点:
  - [负向] 第三方 action 日志不含 TEST_SECRET 明文
  - [正向] permissions 声明生效

清理:      重置 fixture 仓库
