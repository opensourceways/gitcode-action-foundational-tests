用例 ID:   REL-NEEDS-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-022
标题:      needs 链 (A→B→C) 中 job A 失败时 B/C 被跳过，if: always() 仍可执行
前置条件:  仓库无特殊设置；4-job 链 A→B→C→D
操作步骤:
  1. 配置 A→B→C→D 链，A 必然失败（exit 1）
  2. B 和 C 默认 if 条件（success）
  3. D 设 if: ${{ always }}
预期结果: A failure → B skipped → C skipped → D 执行（always）
验证点:
  - [正向] A failure → B skipped
  - [正向] C（无 always）skipped
  - [正向] D（if: always）正常执行
  - [负向] B 不为 success；C 不为 success
清理:      fixture
