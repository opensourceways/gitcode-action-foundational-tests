用例 ID:   COMP-MATRIX-02-005
维度标签:   [completeness, compatibility]
维度:      完备性
优先级:    P1
溯源意图:  INTENT-COMP-010
标题:      验证 matrix include 向已有组合追加额外变量及新增组合的正确展开

前置条件:
  - 工作流中定义了基础矩阵（如 os × version）
  - include 中声明了向现有组合追加额外变量以及完全不在基础矩阵中的新组合

操作步骤:
  1. 触发含基础矩阵 + include 的工作流
  2. 观测生成的 job 实例数与各实例变量集
  3. 检查 include 追加的额外变量是否仅出现在目标组合中
  4. 检查 include 引入的全新组合是否生成额外 job 实例且变量完整

预期结果:
  - include 中匹配基础矩阵维度的项为对应组合追加额外变量
  - include 中定义全新维度值的项生成新的 job 实例
  - 追加后的变量在 job 步骤内可访问且值正确
  - 总实例数 = 基础矩阵笛卡尔积实例数 + 新增组合数 - 被排除数

验证点:
  - [正向] 基础矩阵生成预期实例数，include 为其中 1 个现有组合追加 experimental=true，该实例可读取此变量
  - [正向] include 引入的全新组合生成额外 job 实例且变量完整
  - [负向] include 追加的变量不应泄漏到不匹配的基础矩阵实例中
  - [非功能] 矩阵展开后的各实例 job 名/日志应能区分，便于用户识别 include 追加的实例

清理:      fixture
