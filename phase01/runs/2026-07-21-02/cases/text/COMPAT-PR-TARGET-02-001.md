用例 ID:   COMPAT-PR-TARGET-02-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-008
标题:      pull_request_target 语义对齐：验证 base 上下文运行 + fork PR 拥有完整权限隔离

前置条件:
  - 目标仓库 main 分支有 pull_request_target workflow
  - fork 侧有一个针对 target 仓库的 PR
  - workflow 中声明了 permissions: { repository: write }

操作步骤:
  1. 从 fork 创建 PR 到目标仓库 main 分支
  2. 验证执行的 workflow 定义来自 base 分支（非 fork 侧修改）
  3. 验证 pull_request_target 下 ATOMGIT_TOKEN 保有完整写权限
  4. 验证 pull_request_target 可访问项目级 secrets
  5. fork 侧修改 workflow YAML 中的 run 命令不应被执行

预期结果:
  - workflow 使用 main 分支文件版本执行
  - ATOMGIT_TOKEN 拥有写权限（可推送/评论）
  - fork PR 的 pull_request_target 可访问项目 secrets
  - pull_request_target 的 PR open 事件应可靠触发（否则为已知 bug TC-461/TC-463）

验证点:
  - [正向] pull_request_target 使用 main 分支 workflow 执行
  - [正向] ATOMGIT_TOKEN 拥有写权限
  - [正向] fork PR 的 pull_request_target 可访问项目 secrets
  - [负向] fork 侧 workflow 修改不被执行
  - [负向] pull_request_target 的 PR open 事件应可靠触发

清理:      fixture
