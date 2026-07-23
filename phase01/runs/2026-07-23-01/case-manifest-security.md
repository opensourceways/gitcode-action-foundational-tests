# Security 维度用例清单 (Run 2026-07-23-01)

生成用例总数: 51
P0: 50 | P1: 1 | P2: 0
Negative 断言数: 56/102
覆盖 intent 数: 36/36

所有 36 条准入 intent 均已覆盖。

| 用例 ID | 溯源意图 | 优先级 | 标题 |
|---|---|---|---|
| SEC-ARTF-01-001 | INTENT-SEC-019 | P0 | fork PR 上传的 artifact 必须不可被主仓 workflow 下载或执行 |
| SEC-ARTF-01-002 | INTENT-SEC-019 | P0 | 跨仓库 artifact 下载返回 403 或 404 |
| SEC-BASE-01-001 | INTENT-SEC-035 | P0 | pull_request_target 使用 base 分支的 workflow 版本 |
| SEC-BASE-01-002 | INTENT-SEC-035 | P0 | fork PR 改 workflow 不被 pull_request_target 采用 |
| SEC-CACHE-01-001 | INTENT-SEC-018 | P0 | fork PR 写入的 cache 必须不可被主仓后续 workflow 读取 |
| SEC-CACHE-01-002 | INTENT-SEC-018 | P0 | 主仓 cache restore 对 fork cache miss |
| SEC-COMM-01-001 | INTENT-SEC-026 | P0 | issue_comment / pull_request_comment 触发关键字过滤必须不可被绕过 |
| SEC-DEFPERM-01-001 | INTENT-SEC-036 | P0 | ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效 |
| SEC-DEFPERM-01-002 | INTENT-SEC-036 | P0 | job 级覆盖后权限正确收窄 |
| SEC-DOS-01-001 | INTENT-SEC-033 | P0 | 大 artifact / 大 cache 必须受配额与边界限制 |
| SEC-ENV-01-001 | INTENT-SEC-027 | P0 | 环境级 secret 必须经审批后才能被 workflow 访问 |
| SEC-ENV-01-002 | INTENT-SEC-027 | P0 | 环境级 secret 审批前 workflow 不可读取 |
| SEC-FORK-01-001 | INTENT-SEC-001 | P0 | fork PR 触发 pull_request 时不可读取项目 secrets |
| SEC-FORK-01-002 | INTENT-SEC-001 | P0 | fork PR 中 secrets 引用返回空值且 job 不崩溃 |
| SEC-INJ-01-001 | INTENT-SEC-009 | P0 | 不可信 PR 标题不可直接插进 run 脚本导致命令注入 |
| SEC-INJ-01-002 | INTENT-SEC-010 | P0 | 不可信分支名不可直接插进 run 脚本导致命令注入 |
| SEC-INJ-01-003 | INTENT-SEC-011 | P0 | 不可信 issue/PR 评论内容不可直接插进 run 脚本导致命令注入 |
| SEC-INJ-01-004 | INTENT-SEC-012 | P0 | 不可信 commit message 不可直接插进 run 脚本导致命令注入 |
| SEC-INJ-01-005 | INTENT-SEC-013 | P0 | 表达式求值必须防止双重模板渲染（二次求值） |
| SEC-MASK-01-001 | INTENT-SEC-004 | P0 | Secret 值在运行日志中必须被自动脱敏为 *** |
| SEC-MASK-01-002 | INTENT-SEC-004 | P0 | Secret 值在 step summary 和错误堆栈中必须被脱敏 |
| SEC-MASK-01-003 | INTENT-SEC-005 | P0 | Secret 日志脱敏不可通过 base64 编码绕过 |
| SEC-MASK-01-004 | INTENT-SEC-006 | P0 | Secret 日志脱敏不可通过字符串拼接或插值绕过 |
| SEC-MASK-01-005 | INTENT-SEC-007 | P0 | Secret 日志脱敏不可通过多行值输出绕过 |
| SEC-MASK-01-006 | INTENT-SEC-008 | P0 | Secret 日志脱敏不可通过分片输出绕过 |
| SEC-NAME-01-001 | INTENT-SEC-024 | P0 | Secret/变量名含特殊字符时不可导致意外求值或权限绕过 |
| SEC-NAME-01-002 | INTENT-SEC-025 | P0 | 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏 |
| SEC-NET-01-001 | INTENT-SEC-023 | P0 | Runner 网络出站必须受控，防止 SSRF 与内网跳板 |
| SEC-OIDC-01-001 | INTENT-SEC-034 | P1 | OIDC / 短时凭据支持若缺失，必须明确标注为平台限制并提供替代安全方案 |
| SEC-PERM-01-001 | INTENT-SEC-016 | P0 | 显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN |
| SEC-PERM-01-002 | INTENT-SEC-016 | P0 | permissions 声明 read 时写操作被平台拒绝 |
| SEC-PERM-01-003 | INTENT-SEC-017 | P0 | 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only） |
| SEC-PERM-01-004 | INTENT-SEC-017 | P0 | 默认状态下写操作被 403 拒绝 |
| SEC-PRTGT-01-001 | INTENT-SEC-002 | P0 | pull_request_target 下显式 checkout 不可信 PR 时 secrets 仍应受控 |
| SEC-PRTGT-01-002 | INTENT-SEC-002 | P0 | pull_request_target 无审批不执行 fork PR 代码 |
| SEC-RUN-01-001 | INTENT-SEC-020 | P0 | Job 结束后 workspace 与临时文件必须被彻底清理 |
| SEC-RUN-01-002 | INTENT-SEC-021 | P0 | Runner 环境变量与共享目录必须跨 job 隔离 |
| SEC-RUN-01-003 | INTENT-SEC-022 | P0 | 自托管 Runner 跨项目残留必须被隔离 |
| SEC-SIDE-01-001 | INTENT-SEC-032 | P0 | Secret 不经 output 侧信道绕过脱敏外泄 |
| SEC-SIDE-01-002 | INTENT-SEC-032 | P0 | Secret 不经 artifact 侧信道绕过脱敏外泄 |
| SEC-SUPPLY-01-001 | INTENT-SEC-014 | P0 | 第三方 Action 引用应支持完整 commit hash 固定 |
| SEC-SUPPLY-01-002 | INTENT-SEC-014 | P0 | commit hash 不匹配时第三方 Action 应被拒绝执行 |
| SEC-SUPPLY-01-003 | INTENT-SEC-015 | P0 | 第三方 Action 来源应具备信任边界（typosquatting 限制） |
| SEC-TOCTOU-01-001 | INTENT-SEC-031 | P0 | 审批后推送新 commit 不应被已授权特权运行执行 |
| SEC-TOCTOU-01-002 | INTENT-SEC-031 | P0 | 评论触发不应绕过代码固定与 PR 审批 |
| SEC-TOKEN-01-001 | INTENT-SEC-003 | P0 | fork PR 触发 pull_request 时 ATOMGIT_TOKEN 必须仅拥有 read 权限 |
| SEC-TOKEN-01-002 | INTENT-SEC-003 | P0 | fork PR 中 ATOMGIT_TOKEN 写操作被平台拒绝 |
| SEC-WCMD-01-001 | INTENT-SEC-028 | P0 | Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值 |
| SEC-WCMD-01-002 | INTENT-SEC-029 | P0 | 跨运行 artifact 必须被视为不可信数据 |
| SEC-WCMD-01-003 | INTENT-SEC-030 | P0 | ATOMGIT_ENV 不被不可信输入污染提权 |
| SEC-WCMD-01-004 | INTENT-SEC-030 | P0 | ATOMGIT_OUTPUT 不被不可信输入污染提权 |
