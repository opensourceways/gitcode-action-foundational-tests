```
用例 ID:   COMPAT-IF-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-003
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      continue-on-error 标记后失败 step 不阻断后续执行

前置条件:
  - 仓库已启用 GitCode Action

操作步骤:
  1. 提交一个包含两个 step 的 workflow
  2. 第一个 step 显式返回非零退出码，但设置 continue-on-error 为 true
  3. 第二个 step 输出一条消息
  4. 手动触发该 workflow

预期结果:
  - 第一个 step 虽失败，但因 continue-on-error 标记，后续 step 仍继续执行
  - job 整体状态可能为成功或特殊标记，但不因该失败而中断

验证点:
  - [正向] 第二个 step 成功执行并输出消息
  - [正向] 第一个 step 的失败后，后续 step 未被跳过
  - [正向] job 未在第一个 step 处中断

清理:      重置 fixture 仓库
```
