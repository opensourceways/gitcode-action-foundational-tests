用例 ID:   COMPAT-STAGES-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-017
标题:      stages 阶段机制：阶段间串行 + fail_fast

前置条件: 仓库 workflow 配置 stages
操作步骤:
  1. 3 stage（build→test→deploy）→ 验证顺序执行
  2. stage 内多 job → 验证并行执行
  3. fail_fast:true 下 build 失败 → 验证后续阶段跳过
  4. fail_fast:false 下 build 失败 → 验证后续阶段继续

预期结果: stages 按声明顺序串行；阶段内 job 并行；fail_fast 正确传播
验证点:
  - [正向] 阶段顺序执行
  - [正向] 阶段内 job 并行
  - [正向] fail_fast 正确跳过后续阶段
清理:      fixture
