用例 ID:   SEC-TOKEN-EXPIRE-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-023
母意图:    —
标题:      ATOMGIT_TOKEN 运行后失效且不可通过缓存/残留复活

前置条件:
  - 仓库配置了 TOKEN_TEST_SECRET
  - workflow 在运行中将 token 写入临时文件

操作步骤:
  1. 在 run step 中将 ${{ atomgit.token }} 写入 /tmp/token_dump.txt
  2. 在后续 step 中尝试读取该文件并使用 token 调用 API
  3. 在 run 结束后尝试从外部复用该 token

预期结果:
  - 运行期间临时文件中的 token 不应在运行结束后仍然有效
  - runner 工作区应在 job 结束后清理

验证点:
  - [负向] 运行结束后 token 调用 API 被拒绝
  - [正向] 同一 runner 后续 job 读取不到旧 token 文件

清理:      重置 fixture 仓库
