用例 ID:   COMP-RUNNER-01-003
维度标签:   [completeness, compatibility]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-010
母意图:    —
标题:      不存在的标签组合导致 job 排队或失败

前置条件:
  - 平台不存在该标签组合对应的 Runner

操作步骤:
  1. 配置不存在的 runs-on 标签
  2. 触发 workflow

预期结果:
  - job 无法被调度，最终排队超时或失败

验证点:
  - [负向] job 不应成功执行
  - [非功能] 系统应给出标签无匹配的提示

清理:      none
