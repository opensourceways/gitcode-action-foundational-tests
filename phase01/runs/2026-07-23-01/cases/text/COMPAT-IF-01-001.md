```
用例 ID:   COMPAT-IF-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-003
母意图:    —
标题:      step 失败后后续 step 默认跳过行为

前置条件:
  - 仓库已启用 GitCode Action

操作步骤:
  1. 提交一个包含两个 step 的 workflow
  2. 第一个 step 显式返回非零退出码以模拟失败
  3. 第二个 step 输出一条消息
  4. 手动触发该 workflow

预期结果:
  - 第一个 step 失败后，第二个 step 被系统默认跳过
  - 整个 job 标记为失败状态

验证点:
  - [正向] 第二个 step 未执行，日志中无其输出
  - [正向] job 整体状态为失败
  - [负向] 第二个 step 不应在第一个 step 失败后仍运行

清理:      重置 fixture 仓库
```
