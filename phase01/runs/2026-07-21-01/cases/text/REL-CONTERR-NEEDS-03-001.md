用例 ID:   REL-CONTERR-NEEDS-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-051
标题:      continue-on-error=true job 失败后下游 job 的 needs 依赖行为

前置条件:
  - job-flaky (continue-on-error=true, exit 1)
  - job-A needs: job-flaky（默认 if）
  - job-B needs: job-flaky + if: ${{ always() }}

操作步骤:
  1. job-flaky 执行 exit 1 但 continue-on-error=true
  2. 观察 job-A（默认 if）是否执行
  3. 观察 job-B（if: always()）是否执行

预期结果:
  - job-A status = skipped（默认 if: success() 不满足）
  - job-B 正常执行（if: always() 满足）
  - 验证 continue-on-error 对失败传播的影响

验证点:
  - [正向] job-A status = skipped
  - [正向] job-B status = success

清理:      none
