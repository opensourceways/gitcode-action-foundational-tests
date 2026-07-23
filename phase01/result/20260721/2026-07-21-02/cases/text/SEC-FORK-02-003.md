用例 ID:   SEC-FORK-02-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-003
标题:      pull_request_target 仅执行 base 分支 workflow 定义，不执行 fork 侧 YAML

前置条件:
  - 目标仓库 base 分支有 pull_request_target workflow
  - fork 侧修改了同名 workflow 文件，注入了额外的 shell 命令
  - 存在 fork PR 到目标仓库

操作步骤:
  1. fork 侧在 pull_request_target workflow 中添加 `run: echo "FORK_CODE_EXECUTED"`
  2. 目标仓库 base 分支的同名 workflow 保持原始定义（无上述命令）
  3. fork PR 触发 pull_request_target

预期结果:
  - 实际执行的 workflow 来自 base 分支
  - fork 侧注入的命令不出现在 job 日志中
  - ATOMGIT_TOKEN 拥有 permissions 声明的完整权限

验证点:
  - [负向] fork 侧注入的命令不在日志中出现
  - [正向] base 分支 workflow 正常执行完成
  - [负向] 日志中不应出现 FORK_CODE_EXECUTED

清理:      fixture
