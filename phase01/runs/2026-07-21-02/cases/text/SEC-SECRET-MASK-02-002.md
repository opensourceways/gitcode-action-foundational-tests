用例 ID:   SEC-SECRET-MASK-02-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-006
标题:      Secret 经过 base64 编码后 echo 到日志仍应被脱敏

前置条件:
  - 仓库配置了 Secret（TEST_SECRET）
  - workflow 中将 Secret base64 编码后 echo

操作步骤:
  1. `run: echo "${{ secrets.TEST_SECRET }}" | base64`
  2. 搜索原始 Secret 值和 base64 编码后的值

预期结果:
  - 理想：base64 编码输出也被遮蔽
  - 底线：原始 Secret 值不泄露

验证点:
  - [负向] 日志中不出现 Secret 原始明文
  - [非功能] 若平台支持 base64 遮蔽，编码后的值也被遮蔽

清理:      fixture
