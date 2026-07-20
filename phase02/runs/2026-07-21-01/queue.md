# 执行队列 2026-07-21-01

> Schema: 127 PASS / 1 REJECTED

| # | ID | 维度 | 优先级 | 标题 |
|---|---|---|---|---|
| 1 | COMP-ACTION-02-001 | completeness | P1 | 验证 Action 引用方式官方短名、第三方全路径、本地相对路径 |
| 2 | COMP-ARTIFACT-02-001 | completeness | P1 | 验证 artifact 跨 job 上传/下载及保留策略 |
| 3 | COMP-CACHE-02-001 | completeness | P1 | 验证缓存 cache key 精确/前缀匹配与跨 run 持久性 |
| 4 | COMP-CONCUR-02-001 | completeness | P1 | 验证并发控制 concurrency max / exceed-action / preemption |
| 5 | COMP-CONTERR-02-001 | completeness | P1 | 验证 continue-on-error 对 job DAG 失败传播的影响 |
| 6 | COMP-CONTEXT-02-001 | completeness | P1 | 验证上下文对象 atomgit.* 的所有文档属性实际可用 |
| 7 | COMP-DAG-02-001 | completeness | P1 | 验证 job DAG needs 依赖拓扑的正确执行与失败传播 |
| 8 | COMP-ENV-02-001 | completeness | P1 | 验证环境变量四级优先级链 step > job > workflow > vars > ATOMGIT_* |
| 9 | COMP-EXPR-02-001 | completeness | P1 | 验证表达式状态函数不带括号语法 success/always/failed/cancelled |
| 10 | COMP-EXPRFN-02-001 | completeness | P1 | 验证表达式函数边界行为 contains/startsWith/endsWith/format/hashFiles/to |
| 11 | COMP-FILTER-02-001 | completeness | P1 | 验证 trigger 过滤器 branches/paths/tags 的通配、否定与互斥规则 |
| 12 | COMP-MATIF-02-001 | completeness | P1 | 验证 job 级 if 对 matrix 展开的独立求值 |
| 13 | COMP-MATRIX-02-001 | completeness | P1 | 验证矩阵构建 include/exclude/fail-fast/max-parallel 语义 |
| 14 | COMP-OUTPUT-02-001 | completeness | P1 | 验证 outputs 三级传递链 step → job → workflow |
| 15 | COMP-PARSE-02-001 | completeness | P1 | 验证 workflow 文件 YAML 合法性检查与错误信息 |
| 16 | COMP-PERM-02-001 | completeness | P1 | 验证 permissions 权限模型 6 个权限域与快捷语法 |
| 17 | COMP-POST-02-001 | completeness | P1 | 验证 post 后处理阶段 run_always 与时序保证 |
| 18 | COMP-RERUN-02-001 | completeness | P1 | 验证重运行机制 re-run all / re-run failed 的隔离性与状态保持 |
| 19 | COMP-RUNNER-02-001 | completeness | P1 | 验证 runner 标签匹配三段式标签、default 等效、自托管全匹配 |
| 20 | COMP-SCHEDULE-02-001 | completeness | P1 | 验证 schedule 定时触发最短间隔（5 分钟）与 UTC 时区 |
| 21 | COMP-STAGES-02-001 | completeness | P1 | 验证 stages 阶段机制串行推进、fail_fast 与 job 并行 |
| 22 | COMP-TIMEOUT-02-001 | completeness | P1 | 验证 timeout-minutes 超时终止与 job 状态标记 |
| 23 | COMP-TRIGGER-02-001 | completeness | P1 | 验证 8 种触发事件类型均能产生运行记录 |
| 24 | COMP-WF-CALL-02-001 | completeness | P1 | 验证可重用工作流 workflow_call 的调用传参与 2 层嵌套限制 |
| 25 | COMPAT-ACTION-02-001 | compatibility | P1 | 验证内置 action 引用格式差异 checkout vs actions/checkout@v4 |
| 26 | COMPAT-ART-CACHE-02-001 | compatibility | P1 | 验证内置 upload-artifact/download-artifact 等价性及 cache 作用域隔离 |
| 27 | COMPAT-CONCUR-02-001 | compatibility | P1 | concurrency 并发模型差异：验证 GitCode enable/max/exceed-action 模型与 G |
| 28 | COMPAT-CONTEXT-02-001 | compatibility | P1 | 验证 atomgit.* 核心属性集对齐 github.* 语义完整性 |
| 29 | COMPAT-CTX-AVAIL-02-001 | compatibility | P1 | 上下文可用性矩阵：验证 atomgit/env/secrets/runner/matrix 在各作用域的可用性 |
| 30 | COMPAT-DEF-SHELL-02-001 | compatibility | P1 | 默认值差异：验证 defaults.run.shell 与默认 permissions 行为是否与 GitHub 对齐 |
| 31 | COMPAT-EXPRCO-02-001 | compatibility | P1 | 表达式类型强转规则：验证空字符串/null/NaN 比较行为是否与 GitHub 一致 |
| 32 | COMPAT-EXPRCS-02-001 | compatibility | P1 | 验证 startsWith/endsWith 大小写敏感性与 GitHub 相反 |
| 33 | COMPAT-EXPRFN-02-001 | compatibility | P1 | 验证 GitCode 独有 substring/replace 函数，缺失 join/fromJSON 时报错 |
| 34 | COMPAT-EXPRSYN-02-001 | compatibility | P1 | 验证状态函数不带括号时语法等价于 GitHub success()/failure() |
| 35 | COMPAT-IN-TYPE-02-001 | compatibility | P1 | inputs 类型限制：验证非 string 类型（boolean/number/choice）的拒绝行为 |
| 36 | COMPAT-INJECT-02-001 | compatibility | P1 | 不可信输入注入防护对标：验证 PR 标题/分支名/commit message 在表达式中的处理安全 |
| 37 | COMPAT-MATFF-02-001 | compatibility | P1 | matrix fail-fast 双层语义：strategy.fail-fast vs stages.fail_fast |
| 38 | COMPAT-MIGR-02-001 | compatibility | P1 | 端到端迁移摩擦清单：从 GitHub workflow 到 GitCode workflow 的最小改写路线验证 |
| 39 | COMPAT-OUTPUT-02-001 | compatibility | P1 | job outputs 传递：ATOMGIT_OUTPUT 协议对标 + steps.outputs + jobs.ou |
| 40 | COMPAT-PATHS-02-001 | compatibility | P1 | 验证 paths 过滤器 300 文件上限与 GitHub 3000 阈值差异 |
| 41 | COMPAT-PERMS-02-001 | compatibility | P1 | 验证 permissions 权限域命名差异 project/pr/repository vs contents/pul |
| 42 | COMPAT-POST-02-001 | compatibility | P1 | post 后处理阶段：验证 run_always 默认行为 + 与 always() 的交互 |
| 43 | COMPAT-PR-TARGET-02-001 | compatibility | P0 | pull_request_target 语义对齐：验证 base 上下文运行 + fork PR 拥有完整权限隔离 |
| 44 | COMPAT-PR-TYPES-02-001 | compatibility | P1 | 验证 pull_request types 命名差异 open vs opened / update vs synchr |
| 45 | COMPAT-RUN-CTX-02-001 | compatibility | P1 | 验证 runner.os/arch 返回值格式与文档/一致性问题 |
| 46 | COMPAT-RUN-LBL-02-001 | compatibility | P1 | 验证 runs-on 三段式标签格式差异与 GitHub 单标签不兼容 |
| 47 | COMPAT-SCHEDULE-02-001 | compatibility | P1 | schedule 定时触发差异：验证时区限制、默认分支限制、最短间隔 |
| 48 | COMPAT-SECRET-M-02-001 | compatibility | P1 | secrets 日志脱敏行为对标：验证 *** 遮蔽的覆盖范围与 GitHub 一致性 |
| 49 | COMPAT-STAGES-02-001 | compatibility | P1 | stages 阶段机制：验证阶段间串行语义 + fail_fast 正确性 |
| 50 | COMPAT-SYSENV-02-001 | compatibility | P1 | 验证 ATOMGIT_* 系统环境变量注入完整性 |
| 51 | COMPAT-UNSUPP-02-001 | compatibility | P1 | 验证不支持特征的降级行为不静默忽略 |
| 52 | COMPAT-WF-CMD-02-001 | compatibility | P1 | 验证 workflow 命令 ::group::/::error::/::warning::/::add-mask::  |
| 53 | COMPAT-WF-NEST-02-001 | compatibility | P1 | workflow_call 嵌套深度限制：验证最多 2 层嵌套，超过应报错 |
| 54 | REL-ART-CACHE-02-001 | reliability | P1 | artifact 上传过程中 workflow 被取消，artifact 状态为 incomplete 且不污染后续下载 |
| 55 | REL-CANCEL-02-001 | reliability | P1 | 手动取消 sleep step，step 收到终止信号且清理步骤仍执行 |
| 56 | REL-CANCEL-02-002 | reliability | P1 | stages.fail_fast=true 时，stage 内第一个 job 失败后同一 stage 内其他仍在运行的  |
| 57 | REL-CANCEL-02-003 | reliability | P1 | Post 后处理阶段在 workflow 被取消时仍应执行（run_always: true） |
| 58 | REL-CHAOS-02-001 | reliability | P0 | 在 job 执行中 kill runner 进程，下游 job 应失败且可重跑恢复 |
| 59 | REL-CHAOS-02-002 | reliability | P1 | step 运行中网络中断 60s 后恢复，受影响 step 应失败但后续 step 和 job 状态正确 |
| 60 | REL-CHAOS-02-003 | reliability | P1 | runner 在 checkout 步骤前意外崩溃，重新运行后 workflow 可完整完成 |
| 61 | REL-CONCUR-02-001 | reliability | P1 | 同一 workflow 10s 内被 push 连续触发 20 次，排队与执行行为可预测 |
| 62 | REL-CONCUR-02-002 | reliability | P1 | concurrency max=2, exceed-action=QUEUE 时 5 个同时触发按排队语义执行 |
| 63 | REL-CONCUR-02-003 | reliability | P1 | concurrency max=1, exceed-action=CANCEL 时新触发取消旧运行 |
| 64 | REL-CONCUR-02-004 | reliability | P1 | concurrency max=1 且 exceed-action=IGNORE 时，并发超限的触发被直接拒绝 |
| 65 | REL-CONTERR-02-001 | reliability | P1 | continue-on-error: true 后 job 失败不阻断 workflow 但下游 if: success |
| 66 | REL-MATRIX-02-001 | reliability | P1 | 二维矩阵生成 16 个 job 实例时全部正确展开并独立执行 |
| 67 | REL-MATRIX-02-002 | reliability | P1 | matrix include/exclude 总数正确：基础组合 + include - exclude = 最终实例数 |
| 68 | REL-MATRIX-02-003 | reliability | P1 | strategy.fail-fast=true 时，矩阵中 1 个 job 失败应立即取消其余未完成实例 |
| 69 | REL-MATRIX-02-004 | reliability | P1 | strategy.max-parallel=3 时，6 实例矩阵的并发峰值不超过 3 |
| 70 | REL-NEEDS-02-001 | reliability | P1 | needs 链 A→B→C 中 job A 失败时，B 和 C 默认被跳过 |
| 71 | REL-NEEDS-02-002 | reliability | P1 | needs 指向 matrix 父 job 时下游等待所有实例完成后执行 |
| 72 | REL-NEEDS-02-003 | reliability | P1 | needs 指向 matrix 父 job 时，下游 job 正确等待所有矩阵实例完成后执行（复测 TC-486） |
| 73 | REL-RACE-02-001 | reliability | P1 | job 级 concurrency 跨 workflow 排程无死锁 |
| 74 | REL-RERUN-02-001 | reliability | P1 | Re-run failed jobs 仅失败 job 重执行，成功 job 状态保留 |
| 75 | REL-RERUN-02-002 | reliability | P1 | 同一 Run 重新运行超过 3 次时，第 4 次重新运行被拒绝 |
| 76 | REL-RERUN-02-003 | reliability | P1 | Re-run all jobs 后，ATOMGIT_RUN_ID 和 ATOMGIT_RUN_NUMBER 更新为新值， |
| 77 | REL-RUNNER-02-001 | reliability | P1 | step 尝试分配超过 runner 可用内存时被 OOM kill 且 job 标记失败 |
| 78 | REL-RUNNER-02-002 | reliability | P1 | step 填充 runner 磁盘超过 50GB 上限时，job 失败并给出磁盘空间相关错误 |
| 79 | REL-RUNNER-02-003 | reliability | P1 | 前一个 job 的 workspace 文件残留不污染下一次调度的新 job |
| 80 | REL-TIMEOUT-02-001 | reliability | P1 | job timeout-minutes=5 时超过 5 分钟的 step 被强制终止 |
| 81 | REL-TIMEOUT-02-002 | reliability | P1 | 多个 job 设置不同 timeout-minutes（5/360），各自按独立时钟超时 |
| 82 | REL-TIMEOUT-02-003 | reliability | P1 | timeout-minutes=0 或负数的非法值被配置校验拒绝 |
| 83 | SEC-FORK-02-001 | security | P0 | fork PR 触发 pull_request 时 ATOMGIT_TOKEN 应为只读 |
| 84 | SEC-FORK-02-002 | security | P0 | fork PR 触发 pull_request 时不可访问项目/组织级 Secret |
| 85 | SEC-FORK-02-003 | security | P0 | pull_request_target 仅执行 base 分支 workflow 定义，不执行 fork 侧 YAML |
| 86 | SEC-FORK-02-004 | security | P0 | pull_request_target 下 checkout head.sha 后不应自动信任 fork 侧代码 |
| 87 | SEC-FORK-02-005 | security | P0 | fork PR workflow 不应能修改目标仓库的 workflow 文件 |
| 88 | SEC-INJECT-02-001 | security | P0 | PR 标题中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入 |
| 89 | SEC-INJECT-02-002 | security | P0 | PR 正文中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入 |
| 90 | SEC-INJECT-02-003 | security | P0 | 分支名中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入 |
| 91 | SEC-INJECT-02-004 | security | P0 | 提交信息中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入 |
| 92 | SEC-INJECT-02-005 | security | P0 | 不可信输入注入到 ATOMGIT_ENV/ATOMGIT_OUTPUT 文件不导致环境变量污染 |
| 93 | SEC-INJECT-02-006 | security | P1 | 通过环境变量安全引用不可信输入应不触发脚本注入 |
| 94 | SEC-PERMS-02-001 | security | P0 | permissions: {}（空对象）使 ATOMGIT_TOKEN 持有最小默认权限 |
| 95 | SEC-PERMS-02-002 | security | P0 | 未声明 permissions 时 ATOMGIT_TOKEN 使用仓库设置中的默认权限 |
| 96 | SEC-PERMS-02-003 | security | P1 | job 级 permissions 声明可覆盖 workflow 级声明 |
| 97 | SEC-SECRET-MASK-02-001 | security | P0 | Secret 值直接 echo 到日志时应被脱敏为 *** |
| 98 | SEC-SECRET-MASK-02-002 | security | P1 | Secret 经过 base64 编码后 echo 到日志仍应被脱敏 |
| 99 | SEC-SECRET-MASK-02-003 | security | P1 | Secret 通过子字符串拼接后 echo 应仍被脱敏 |
| 100 | SEC-SECRET-MASK-02-004 | security | P1 | Secret 包含多行文本时应整体被脱敏 |
| 101 | SEC-SECRET-MASK-02-005 | security | P1 | ::add-mask:: 命令的正确性与安全性 |
| 102 | SEC-SUPPLY-02-001 | security | P1 | 第三方 action 引用未 pin 到 commit SHA 时有平台警告 |
| 103 | SEC-SUPPLY-02-002 | security | P1 | fork PR 不应能写入或污染主分支的依赖缓存 |
| 104 | SEC-TOKEN-02-001 | security | P0 | 平台内置 ATOMGIT_TOKEN 在 fork PR 下不应为有效完整 token |
| 105 | USE-DEBUG-02-001 | usability | P1 | 日志中 ::group::/::endgroup:: workflow 命令的实际支持情况 |
| 106 | USE-DEBUG-02-002 | usability | P2 | 运行状态机的完整性与可观察性：queued/cancelled/skipped 状态的展示 |
| 107 | USE-DEBUG-02-003 | usability | P1 | 日志中 ATOMGIT_* 系统变量的注入完整性 |
| 108 | USE-DEBUG-02-004 | usability | P2 | 运行详情页 post 阶段的展示与文档一致性 |
| 109 | USE-DOC-02-001 | usability | P2 | 文档声明的 runner.os/runner.arch 返回值与平台实际返回值的一致性 |
| 110 | USE-DOC-02-002 | usability | P1 | 文档声明的 environment 绑定语法与实际校验行为的一致性（复测 TC-010） |
| 111 | USE-DOC-02-003 | usability | P1 | 文档声明的 runner.os / runner.arch 返回值与平台实际返回值的一致性 |
| 112 | USE-ERR-MSG-02-001 | usability | P1 | 必填字段缺失时的错误信息可诊断性 |
| 113 | USE-ERR-MSG-02-002 | usability | P1 | 触发器 types 取值无效时的错误信息可诊断性 |
| 114 | USE-ERR-MSG-02-003 | usability | P1 | 上下文对象命名差异 github.* vs atomgit.* 的错误信息可诊断性 |
| 115 | USE-ERR-MSG-02-004 | usability | P1 | 字段类型错误时的错误信息可诊断性 |
| 116 | USE-ERR-MSG-02-005 | usability | P1 | 未知字段/不支持属性时的错误信息可诊断性 |
| 117 | USE-ERR-MSG-02-006 | usability | P1 | 表达式括号语法差异（failure() vs failed）的错误信息可诊断性 |
| 118 | USE-MIGR-02-001 | usability | P1 | 直接搬运 .github/workflows/ci.yml 到 .gitcode/workflows/ 后的开箱报错路径 |
| 119 | USE-MIGR-02-002 | usability | P1 | runs-on 使用 GitHub 风格标签时的错误信息质量与迁移指引 |
| 120 | USE-MIGR-02-003 | usability | P0 | permissions 使用 GitHub 命名体系时应报错而不可静默忽略 |
| 121 | USE-MIGR-02-004 | usability | P1 | uses: actions/checkout@v4 等 GitHub 风格内置 action 引用在 GitCode 下 |
| 122 | USE-MIGR-02-005 | usability | P1 | workflow_dispatch inputs 使用 GitHub 支持的非 string 类型时的行为与报错 |
| 123 | USE-MIGR-02-006 | usability | P1 | 迁移清单文档的完整性与可操作性：从 GitHub 迁移到 GitCode 的官方指南 |
| 124 | USE-NEST-02-001 | usability | P2 | workflow_call 嵌套超过 2 层时的错误信息可诊断性 |
| 125 | USE-QUEUE-02-001 | usability | P2 | concurrency 排队时用户的等待信息可见性 |
| 126 | USE-RERUN-02-001 | usability | P1 | Re-run failed jobs 后成功 job 的结果和日志保留与展示 |
| 127 | USE-RERUN-02-002 | usability | P2 | 重新运行限制条件（3次/6小时/原始配置）的用户可见性与反馈 |
