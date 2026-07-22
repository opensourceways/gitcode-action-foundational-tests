用例 ID:   COMPAT-SECRET-M-02-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-028
母意图:    SEC-SECRET-MASK-02-005
标题:      secrets 日志脱敏行为对标：验证 *** 遮蔽的覆盖范围与 GitHub 一致性

前置条件:
  - 仓库配置了 secret TOKEN
  - workflow 中通过不同方式输出 secret 值

操作步骤:
  1. 直接 echo ${{ secrets.TOKEN }} → 应显示 ***
  2. 通过 env 变量间接 echo → 应显示 ***
  3. echo "$TOKEN" | base64 → 不应泄密
  4. 测试大小写变体和拼接是否绕过脱敏
  5. 对比 GitHub 的脱敏检测覆盖范围

预期结果:
  - 直接/间接/编码后均不泄密
  - 脱敏强度不弱于 GitHub

验证点:
  - [正向] 直接 echo → ***
  - [正向] 间接 env echo → ***
  - [负向] base64 编码后不泄密
  - [负向] 大小写变体/拼接/多行绕过不泄密

清理:      fixture
