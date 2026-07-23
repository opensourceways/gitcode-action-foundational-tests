用例 ID:   COMPAT-ISOLATE-01-002
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-028
母意图:    COMPAT-ISOLATE-01-001
标题:      Runner 环境隔离——跨 job 环境变量隔离

前置条件:
  - 平台提供多 job 工作流执行能力

操作步骤:
  1. 在 job A 中通过 `echo "KEY=VALUE_A" >> "$ATOMGIT_ENV"` 设置环境变量
  2. 在 job B 中读取同名环境变量 KEY
  3. 验证 job B 读取不到 job A 设置的值

预期结果:
  - job B 中环境变量 KEY 为空或不同于 VALUE_A
  - $ATOMGIT_ENV 的作用域仅限于当前 job，不泄漏到后续 job
  - 环境变量隔离行为与 GitHub Actions 的 job 级隔离语义一致

验证点:
  - [负向] job B 中不应读取到 job A 通过 ATOMGIT_ENV 设置的值
  - [正向] job 内部步骤可正常读取本 job 设置的 ATOMGIT_ENV 变量
  - [正向] 环境变量隔离机制与预期语义一致

清理:      fixture
