用例 ID:   COMP-STAGES-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-009
标题:      验证 stages 阶段机制串行推进、fail_fast 与 job 并行

前置条件:
  - 配置 3 个 stage，各含多个 job
  - stage1.fail_fast=true

操作步骤:
  1. 验证 Stage 1 所有 job 完成后 Stage 2 才开始
  2. 同一 Stage 内无 needs job 并行执行
  3. fail_fast: true → 某 job 失败 → 同级剩余 job 被取消 + 跳过后续 stage
  4. fail_fast: false → 同级其他 job 继续，后续 stage 跳过
  5. 同一 stage 内 job 通过 needs 串行化

预期结果:
  - 阶段按声明顺序串行
  - 阶段内并行（除非 needs 约束）
  - fail_fast 正确传播

验证点:
  - [正向] 3 个 stage 串行执行
  - [正向] 同 stage 内 job 并行
  - [正向] fail_fast=true 取消同级+跳过后续
  - [正向] fail_fast=false 同级继续

清理:      fixture
