用例 ID:   REL-MATRIX-01-038
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-038
母意图:    —
标题:      大规模 matrix——20 个组合应全部生成并正确调度

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发含 4 维×5 值=20 组合的 matrix workflow

预期结果:
  - 20 个 jobs 全部生成
  - 每个实例获得正确的矩阵变量值
  - 20 个 jobs 全部 completed(success)

验证点:
  - [正向] 20 个 jobs 全部生成
  - [正向] 矩阵变量校验 100% 通过
  - [负向] 不应出现重复组合或遗漏组合

清理:      无需特殊清理
