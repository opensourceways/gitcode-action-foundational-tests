用例 ID:   USE-STEP-STATUS-03-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-040
标题:      Step 级别执行结果状态回写准确性——exit code 与展示状态一致性（防「假绿」）

前置条件:
  - step 执行 exit 1（故意失败）

操作步骤:
  1. 创建 step 执行 exit 1
  2. 创建 step 执行 exit 0
  3. 观察 Actions 列表和详情页中各 step 的状态标记

预期结果:
  - exit 1 的 step 必须标记为 failure（红色/失败图标）
  - exit 0 的 step 标记为 success
  - 不应出现「exit code != 0 但 step 显示 success」的假绿

验证点:
  - [正向] exit 1 step → 状态 failure
  - [正向] exit 0 step → 状态 success
  - [负向] 不应出现 exit code 与 status 不一致

清理:      none
