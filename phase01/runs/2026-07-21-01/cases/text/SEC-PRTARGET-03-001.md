用例 ID:   SEC-PRTARGET-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-003
母意图:    —
标题:      pull_request_target 仅在 base 分支 workflow 定义中运行

前置条件:
  - 主仓库默认分支有 pull_request_target workflow
  - fork 侧修改了同路径 workflow YAML，添加恶意命令
  - 从 fork 向主仓提交 PR

操作步骤:
  1. fork 侧修改 .gitcode/workflows/pr-target.yml，添加 `run: echo "FORK_SIDE_CODE_EXECUTED"`
  2. 向主仓提交 fork PR
  3. 对比实际执行的 step 与默认分支和 fork 侧的 workflow YAML

预期结果: 实际执行的 workflow 来自默认分支；fork 侧添加的 step 不出现；ATOMGIT_TOKEN 拥有完整权限

验证点:
  - [正向] 实际执行的 steps 与默认分支 YAML 一致
  - [负向] FORK_SIDE_CODE_EXECUTED 不应出现在日志中
  - [正向] pull_request_target 下 ATOMGIT_TOKEN 具完整 write 权限
  - [回归] 复现 history #66 场景

清理: fixture
