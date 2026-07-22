用例 ID:   REL-NEEDS-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-022
标题:      needs 链 A→B→C 中 job A 失败时，B 和 C 默认被跳过

前置条件:
  - A→B→C→D 链，A 必然失败，D 设 if: always()

操作步骤:
  1. A failure → B skipped
  2. C（默认 if）→ skipped
  3. D（if: always()）→ 正常执行

预期结果:
  - 失败传播正确
  - always() 强制执行

验证点:
  - [正向] B/C skipped
  - [正向] D executed
  - [负向] B 不是 success

清理:      fixture
