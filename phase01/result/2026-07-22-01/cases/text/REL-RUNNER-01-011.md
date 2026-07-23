用例 ID:   REL-RUNNER-01-011
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-058
母意图:    —
标题:      Runner 状态机正确性——空闲/运行/离线转换与时序一致性

前置条件:
  - 仓库已启用 Actions
  - 有至少 1 个 runner 注册到该仓库且当前处于 idle 状态
  - 具备让 runner 离线/恢复的手段

操作步骤:
  1. 查询 runner 状态，记录初始状态（应为 idle）
  2. 触发一个 workflow run，使 runner 被分配执行 job
  3. 在 job 运行期间查询 runner 状态，记录状态（应为 busy）
  4. 等待 job 完成，再次查询 runner 状态（应回到 idle）
  5. 将 runner 置为离线，查询状态（应为 offline）
  6. 恢复 runner 在线，查询状态（应回到 idle）

预期结果:
  - runner 状态转换路径符合：idle → busy → idle → offline → idle
  - 状态转换时序合理：busy 应在 job 开始 running 后出现，idle 应在 job 完成后出现
  - 无非法状态跳跃（如 idle 直接到 offline 不经过 busy）——离线除外

验证点:
  - [正向] 状态序列完整且符合预期
  - [正向] busy 状态与 job running 时间段重叠
  - [负向] 无状态回跳或状态缺失

清理:      重置 full_instance
