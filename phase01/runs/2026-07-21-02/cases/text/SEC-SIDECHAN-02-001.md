用例 ID:   SEC-SIDECHAN-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-032
母意图:    —
标题:      Secret 不经 output / artifact / step summary 侧信道绕过脱敏外泄

前置条件:
  - 仓库配置了 SIDECHAN_SECRET
  - workflow 将 secret 写入 output、artifact 与 step summary

操作步骤:
  1. 在 step 中将 secret 写入 $ATOMGIT_OUTPUT
  2. 在 step 中将 secret 写入 $ATOMGIT_STEP_SUMMARY
  3. 上传包含 secret 的文件作为 artifact

预期结果:
  - output 与 step summary 中的 secret 值应被脱敏为 ***
  - artifact 中的 secret 明文不应被保留（或被平台拒绝）

验证点:
  - [负向] output 中不含 secret 明文
  - [负向] step summary 中不含 secret 明文
  - [负向] artifact 下载内容不含 secret 明文

清理:      重置 fixture 仓库
