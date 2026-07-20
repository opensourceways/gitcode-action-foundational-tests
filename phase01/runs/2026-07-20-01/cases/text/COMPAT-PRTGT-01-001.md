用例 ID:   COMPAT-PRTGT-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-008
母意图:    —
标题:      pull_request_target 语义对齐：base 上下文运行 + fork PR 完整权限隔离

前置条件:
  - 目标仓库 main 分支存在包含 pull_request_target 触发器的 workflow 文件
  - 存在一个来自 fork 的 PR
  - fork 侧对该 workflow 文件做了修改（添加了不同的 run 命令）
  - 仓库配置了项目级 Secret（如 DEPLOY_TOKEN）

操作步骤:
  1. 从 fork 仓库提交 PR 到目标仓库 main 分支
  2. fork 侧的 workflow 文件在 pull_request_target 下添加了 echo "FORK_CODE" 的步骤
  3. 触发 pull_request_target 事件，观察实际执行的 workflow 内容
  4. 对比实际执行日志中是否出现 "FORK_CODE"
  5. 验证 ATOMGIT_TOKEN 在 pull_request_target 下是否拥有写权限

预期结果:
  - 实际执行的 workflow 定义来自目标仓库 main 分支，而非 fork 侧的修改版本
  - fork 侧新增的 echo "FORK_CODE" 不出现于 job 日志中
  - pull_request_target 下的 ATOMGIT_TOKEN 拥有 permissions 声明的完整权限（可写）
  - fork PR 的 pull_request_target 可访问项目级 secrets

验证点:
  - [正向] pull_request_target 使用 main 分支 workflow 文件版本执行
  - [负向] fork 侧对 workflow YAML 的任何修改不应影响实际执行的逻辑
  - [负向] fork 侧的 workflow 文件中新增的 shell 命令不应在 runner 上执行
  - [正向] pull_request_target 下的 ATOMGIT_TOKEN 拥有写权限（可推送/评论）
  - [正向] fork PR 的 pull_request_target 可访问项目级 secrets
  - [负向] pull_request_target 的 PR open 事件应可靠触发（已有 TC-461/TC-463 FAIL 线索）

清理:      fixture
