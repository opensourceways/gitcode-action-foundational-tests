用例 ID:   REL-CONTERR-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-028
标题:      continue-on-error: true 后 job 失败不阻断 workflow 但下游 if: success() 不满足

前置条件:
  - jobA continue-on-error: true 且必然失败
  - jobB needs: [A]（默认 if）
  - jobC needs: [A], if: always()

操作步骤:
  1. jobA 失败 → workflow 继续（不中止）
  2. jobB 被 skipped
  3. jobC（if: always()）→ success

预期结果:
  - continue-on-error 不影响 downstream if: success()
  - always() 强制执行

验证点:
  - [正向] A 失败但不中止 workflow
  - [正向] B 状态为 skipped
  - [正向] C 状态为 success

清理:      fixture
