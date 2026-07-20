用例 ID:   COMP-STAGES-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-009
标题:      验证 stages 阶段机制: 串行推进、fail_fast 与 job 并行
前置条件:  仓库无特殊设置；配置 3 个 stage 的 workflow
操作步骤:
  1. 配置 3 个 stage：build → test → deploy
  2. 每个 stage 内含 2-3 个并行 job
  3. 验证 fail_fast:true 时 stage 内失败→后续 stage 跳过
  4. 验证 fail_fast:false 时同 stage 其他 job 继续
预期结果:
  - Stage 1 全部完成 → Stage 2 开始
  - 同一 Stage 内无 needs 的 job 并行
  - fail_fast:true 下失败 job 同 stage 其他取消、后续 stage skipped
  - fail_fast:false 下失败不波及其他
验证点:
  - [正向] 3 个 stage 按序串行执行
  - [正向] 同 stage 内 job 并行启动
  - [正向] fail_fast 失败传播正确
清理:      fixture
