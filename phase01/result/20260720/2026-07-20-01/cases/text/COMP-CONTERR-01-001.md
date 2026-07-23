用例 ID:   COMP-CONTERR-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-023
标题:      验证 continue-on-error 对 job DAG 失败传播的影响

前置条件:
  - 仓库有多 job workflow
  - job A 声明 continue-on-error: true 且必然失败
  - job B 依赖 job A（默认条件），job C 依赖 job A（if: always()）

操作步骤:
  1. 配置 job A（continue-on-error: true, exit 1）
  2. job B 依赖 A，使用默认 if 条件
  3. job C 依赖 A，使用 if: always()
  4. 触发 workflow，观察各 job 状态
  5. 检查 needs.<A>.result 在 C 中的值

预期结果:
  - job A 失败后 workflow 继续执行（不中止）
  - job B（默认 if）→ skipped
  - job C（if: always()）→ 正常执行
  - needs.<A>.result = failure
  - ${{ success }} = false, ${{ always }} = true

验证点:
  - [正向] continue-on-error job 失败不中止 workflow
  - [正向] 默认 if 的下游 job 被 skipped
  - [正向] if: always() 的下游 job 正常执行
  - [正向] needs result 反映真实状态

清理:      fixture
