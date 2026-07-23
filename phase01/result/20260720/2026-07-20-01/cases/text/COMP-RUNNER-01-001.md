用例 ID:   COMP-RUNNER-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-017
标题:      验证 runner 标签匹配: 官方三段式标签、default 等效、自托管全匹配
前置条件:  仓库无特殊设置
操作步骤:
  1. runs-on: [ubuntu-latest, x64, small] 官方三段式
  2. runs-on: default 等效验证
  3. 动态 runs-on（matrix 变量）正确展开
  4. 无匹配 runner → 排队或超时失败
预期结果: 标签全匹配（非子集匹配），无匹配时合理调度或超时
验证点:
  - [正向] default 等价于 [ubuntu-latest, x64, small]
  - [正向] 动态 runs-on matrix 变量正确展开
  - [负向] 无匹配 runner 时不应随机分配到其他 runner
清理:      fixture
