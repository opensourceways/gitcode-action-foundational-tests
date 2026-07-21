用例 ID:   COMP-CONTERR-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-023
标题:      验证 continue-on-error 对 job DAG 失败传播的影响

前置条件:
  - jobA 配置 continue-on-error: true 并故意失败
  - jobB needs: [A]（默认 if 条件）
  - jobC needs: [A], if: always()

操作步骤:
  1. jobA 失败但 continue-on-error: true → workflow 不中止
  2. jobB（默认 if）→ skipped
  3. jobC（if: always()）→ 正常执行
  4. needs.<A>.result 反映真实 outcome

预期结果:
  - continue-on-error 不影响下游 if: success() 判断
  - always() 强制执行
  - needs result 反映真实状态

验证点:
  - [正向] continue-on-error job 失败不阻断 workflow
  - [正向] 默认条件 job 被 skipped
  - [正向] always() job 执行
  - [正向] needs.<id>.result 反映真实值

清理:      fixture
