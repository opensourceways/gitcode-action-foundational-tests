用例 ID:   REL-MATRIX-02-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-006
标题:      matrix include/exclude 总数正确：基础组合 + include - exclude = 最终实例数

前置条件:
  - 基础矩阵 os=[ubuntu, windows] × node=[18, 20] = 4 实例
  - include 追加 3 个组合（含额外变量 experimental）
  - exclude 排除 1 个组合

操作步骤:
  1. 生成全部实例后统计总数 = 4 + 3 - 1 = 6
  2. 验证 include 中额外变量 experimental 仅对其所属实例可见
  3. 验证被 exclude 的组合无对应 job 生成

预期结果:
  - 总 job 数 = 6
  - experimental 变量仅 include 实例可读
  - exclude 的组合被正确排除

验证点:
  - [正向] 总 job 数 = 6
  - [正向] include 追加的 experimental 变量仅在其所属实例中可读
  - [负向] 被 exclude 的组合无对应 job

清理:      fixture
