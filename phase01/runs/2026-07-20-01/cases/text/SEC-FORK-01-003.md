用例 ID:   SEC-FORK-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-003
母意图:    —
标题:      pull_request_target 仅在 base 分支 workflow 定义中运行，不执行 fork 侧 workflow YAML

前置条件:
  - 目标仓库 main 分支存在包含 `pull_request_target` 触发器的 workflow 文件
  - fork 仓库对同名 workflow 文件做了恶意修改（添加了 `curl evil.example.com` 或类似标记命令）
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在 fork 仓库中修改 `.gitcode/workflows/pr-target.yml`，添加一段标记命令（如 `echo "FORK_MODIFIED_WORKFLOW"`）
  2. 从 fork 仓库提交 PR 到目标仓库 main 分支
  3. 触发 pull_request_target 事件（PR 创建）
  4. 观察 job 执行日志中实际运行的命令
  5. 对比 base 分支原始 workflow 与 fork 侧修改版，确认执行的是 base 版本

预期结果:
  - 实际执行的 workflow 定义完全来自目标仓库 main 分支
  - fork 侧对 workflow YAML 的任何修改（包括新增 step、修改 run 命令）不应出现在实际执行的 job 中
  - job 日志中不出现 fork 侧新增的任何命令输出
  - ATOMGIT_TOKEN 拥有 permissions 声明的完整权限
  - Secrets 可被访问

验证点:
  - [正向] pull_request_target 触发的 workflow 日志中出现 base 分支独有的步骤输出
  - [负向] 日志中不出现 fork 侧新增的任意标记命令（如 FORK_MODIFIED_WORKFLOW）
  - [负向] fork 侧 workflow 文件中新增的 shell 命令不应有任何执行痕迹
  - [正向] base 分支的 workflow 正常完成执行

清理:      fixture
