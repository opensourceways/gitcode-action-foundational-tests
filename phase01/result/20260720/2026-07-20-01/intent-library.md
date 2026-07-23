# Intent Library · Run 2026-07-20-01

> 阶段A 发散完成，5 个维度共 **144 条 intent**，按维度与风险项对齐。
> 状态：汇聚完成 → 待评审门禁（STOP①）。

## 汇总统计

| 维度 | Intent 数 | ID 范围 |
|---|---|---|
| completeness (spec) | 25 | INTENT-COMP-001 ~ 025 |
| compatibility (compat) | 31 | INTENT-COMPAT-001 ~ 031 |
| security | 36 | INTENT-SEC-001 ~ 036 |
| reliability | 29 | INTENT-REL-001 ~ 029 |
| usability | 23 | INTENT-USE-001 ~ 023 |
| **合计** | **144** | |

## 意图清单

### completeness（25 条）

| ID | 优先级 | 标题 | 覆盖能力项 |
|---|---|---|---|
| INTENT-COMP-001 | P1 | push 事件触发语义 | 触发事件 push |
| INTENT-COMP-002 | P1 | pull_request 事件类型与活动类型 | 触发事件 pull_request |
| INTENT-COMP-003 | P1 | job needs DAG 执行 | job 依赖 needs |
| INTENT-COMP-004 | P1 | strategy matrix 展开正确性 | matrix 构建 |
| INTENT-COMP-005 | P1 | concurrency group 取消/排队 | 并发控制 |
| INTENT-COMP-006 | P1 | artifact 上传/下载跨 job 传递 | artifact 生命周期 |
| INTENT-COMP-007 | P1 | cache 命中与恢复 | cache 机制 |
| INTENT-COMP-008 | P1 | job outputs 传递到下游 | outputs 传递 |
| INTENT-COMP-009 | P0 | stages 阶段依赖与 jobs 嵌套 | stages 执行模型 |
| INTENT-COMP-010 | P1 | post step 执行语义 | job post 阶段 |
| INTENT-COMP-011 | P1 | 变量优先级覆盖链 | variables 系统 |
| INTENT-COMP-012 | P1 | 表达式函数 fromJSON/contains 等 | 表达式系统 |
| INTENT-COMP-013 | P1 | hashFiles 函数行为 | 表达式函数 |
| INTENT-COMP-014 | P1 | atomgit context 属性完整性 | context 对象 |
| INTENT-COMP-015 | P0 | permissions 默认值与收窄语义 | 权限模型 |
| INTENT-COMP-016 | P0 | workflow_call 可复用 workflow | 复用 workflow |
| INTENT-COMP-017 | P1 | runs-on runner 标签解析 | runner 选择 |
| INTENT-COMP-018 | P1 | 非法 YAML schema 报错质量 | 语法解析静态校验 |
| INTENT-COMP-019 | P1 | workflow 命令 ::group::/::error:: 等 | 可观测性 workflow 命令 |
| INTENT-COMP-020 | P1 | run 状态机流转 | 可观测性状态机 |
| INTENT-COMP-021 | P1 | schedule cron 触发 | 定时触发 |
| INTENT-COMP-022 | P0 | 第三方 action 引用 uses 语法 | action 复用 |
| INTENT-COMP-023 | P0 | matrix fail-fast 与 include/exclude | matrix 策略 |
| INTENT-COMP-024 | P1 | if 条件 always()/failure()/success() | 条件执行 |
| INTENT-COMP-025 | P1 | matrix max-parallel 控制 | matrix 并发 |

### compatibility（31 条）

| ID | 优先级 | 标题 | 热点 |
|---|---|---|---|
| INTENT-COMPAT-001 | P0 | atomgit context 属性对齐 GitHub github context | context 字段差异 |
| INTENT-COMPAT-002 | P1 | runner.os/runner.arch 格式对齐 | context 格式 |
| INTENT-COMPAT-003 | P0 | 表达式括号语法兼容 | 表达式差异 |
| INTENT-COMPAT-004 | P1 | 表达式函数集差异 | 表达式差异 |
| INTENT-COMPAT-005 | P1 | 表达式大小写敏感性 | 表达式差异 |
| INTENT-COMPAT-006 | P1 | 表达式类型强制转换 | 表达式差异 |
| INTENT-COMPAT-007 | P0 | pull_request types 命名差异 | 触发过滤语义 |
| INTENT-COMPAT-008 | P1 | paths 过滤 300 文件限制 | 触发过滤语义 |
| INTENT-COMPAT-009 | P0 | permissions 域/值命名差异 | 权限模型差异 |
| INTENT-COMPAT-010 | P1 | runs-on runner 标签映射 | runner 差异 |
| INTENT-COMPAT-011 | P0 | runner context 属性完整性 | context 差异 |
| INTENT-COMPAT-012 | P0 | 内置 actions/checkout 行为等价 | 内置 action 差异 |
| INTENT-COMPAT-013 | P1 | GITHUB_* 环境变量对应映射 | 环境变量差异 |
| INTENT-COMPAT-014 | P0 | 默认 shell 差异 | 默认值差异 |
| INTENT-COMPAT-015 | P0 | 默认 permissions 差异 | 默认值差异 |
| INTENT-COMPAT-016 | P1 | continue-on-error 语义差异 | 执行模型差异 |
| INTENT-COMPAT-017 | P1 | concurrency cancel-in-progress | 执行模型差异 |
| INTENT-COMPAT-018 | P1 | workflow_call 复用限制差异 | 复用差异 |
| INTENT-COMPAT-019 | P0 | schedule cron 语义与时区 | 触发差异 |
| INTENT-COMPAT-020 | P0 | pull_request_target 行为对齐 | 触发差异 |
| INTENT-COMPAT-021 | P1 | tag 触发语义 | 触发差异 |
| INTENT-COMPAT-022 | P1 | 不支持能力的降级方式 | 不支持降级 |
| INTENT-COMPAT-023 | P1 | outputs 传递协议差异 | 执行模型差异 |
| INTENT-COMPAT-024 | P1 | env context 变量注入差异 | 环境变量差异 |
| INTENT-COMPAT-025 | P1 | job 级 if 条件作用域差异 | 执行模型差异 |
| INTENT-COMPAT-026 | P1 | steps context 属性差异 | context 差异 |
| INTENT-COMPAT-027 | P1 | needs context 属性差异 | context 差异 |
| INTENT-COMPAT-028 | P1 | secret 日志遮蔽行为差异 | 安全特性差异 |
| INTENT-COMPAT-029 | P1 | workflow_dispatch inputs 类型限制 | 触发差异 |
| INTENT-COMPAT-030 | P1 | matrix 空值处理差异 | 执行模型差异 |
| INTENT-COMPAT-031 | P1 | artifact/cache 作用域与保留期差异 | 内置 action 差异 |

### security（36 条）

| ID | 优先级 | 标题 | 攻击面 |
|---|---|---|---|
| INTENT-SEC-001 | P0 | fork PR ATOMGIT_TOKEN 只读 | fork PR 隔离 |
| INTENT-SEC-002 | P0 | fork PR 不应读取仓库 secrets | fork PR 隔离 |
| INTENT-SEC-003 | P0 | pull_request_target base 分支执行语义 | pr_target 安全 |
| INTENT-SEC-004 | P0 | pull_request_target checkout head.sha 风险 | pr_target 安全 |
| INTENT-SEC-005 | P0 | secret 日志基础脱敏 | secret 脱敏 |
| INTENT-SEC-006 | P0 | secret base64 编码绕过脱敏 | secret 脱敏 |
| INTENT-SEC-007 | P0 | secret 拼接绕过脱敏 | secret 脱敏 |
| INTENT-SEC-008 | P1 | secret 多行值脱敏 | secret 脱敏 |
| INTENT-SEC-009 | P0 | PR 标题表达式注入 | 表达式注入 |
| INTENT-SEC-010 | P0 | PR 正文表达式注入 | 表达式注入 |
| INTENT-SEC-011 | P0 | 分支名表达式注入 | 表达式注入 |
| INTENT-SEC-012 | P0 | commit message 表达式注入 | 表达式注入 |
| INTENT-SEC-013 | P1 | env context 安全模式 | 表达式注入 |
| INTENT-SEC-014 | P1 | GITHUB_ENV 文件污染 | 表达式注入 |
| INTENT-SEC-015 | P0 | permissions 空声明权限收窄 | 权限模型 |
| INTENT-SEC-016 | P0 | permissions 默认值安全审计 | 权限模型 |
| INTENT-SEC-017 | P1 | job 级 permissions 覆盖 | 权限模型 |
| INTENT-SEC-018 | P0 | 第三方 action SHA pin 安全 | 供应链 |
| INTENT-SEC-019 | P0 | fork PR cache 投毒防护 | cache 投毒 |
| INTENT-SEC-020 | P1 | cache 跨事件隔离 | cache 安全 |
| INTENT-SEC-021 | P1 | secret 命名规则安全 | secret 管理 |
| INTENT-SEC-022 | P1 | environment 保护规则审批 | 部署安全 |
| INTENT-SEC-023 | P1 | ATOMGIT_TOKEN 过期/轮换 | token 生命周期 |
| INTENT-SEC-024 | P1 | workflow 递归触发防护 | 防护机制 |
| INTENT-SEC-025 | P1 | runner 残留数据清理 | runner 隔离 |
| INTENT-SEC-026 | P1 | artifact 跨仓库/边界访问 | artifact 安全 |
| INTENT-SEC-027 | P1 | add-mask workflow 命令安全 | 日志安全 |
| INTENT-SEC-028 | P1 | add-mask 跨 job 可见性 | 日志安全 |
| INTENT-SEC-029 | P1 | workflow 文件篡改检测 | 供应链 |
| INTENT-SEC-030 | P0 | 第三方 action inputs 信任边界 | 供应链 |
| INTENT-SEC-031 | P1 | composite action 安全 | 供应链 |
| INTENT-SEC-032 | P1 | reusable workflow 跨边界 secret | 复用安全 |
| INTENT-SEC-033 | P1 | runner 并发 job 隔离 | runner 隔离 |
| INTENT-SEC-034 | P1 | PAT/Token 文档安全指引 | 文档安全 |
| INTENT-SEC-035 | P1 | 表达式类型安全（类型混淆） | 表达式注入 |
| INTENT-SEC-036 | P0 | 内置 ATOMGIT_TOKEN 权限范围 | token 安全 |

### reliability（29 条）

| ID | 优先级 | 标题 | 集群 |
|---|---|---|---|
| INTENT-REL-001 | P1 | 并发 push 洪泛（20 次/10s） | 并发洪泛 |
| INTENT-REL-002 | P1 | 并发上限排队行为 | 并发洪泛 |
| INTENT-REL-003 | P1 | cancel-in-progress 抢占 | 并发洪泛 |
| INTENT-REL-004 | P1 | IGNORE 并发策略 | 并发洪泛 |
| INTENT-REL-005 | P1 | matrix 16 实例展开 | 大规模 matrix |
| INTENT-REL-006 | P1 | matrix include/exclude 正确性 | 大规模 matrix |
| INTENT-REL-007 | P0 | matrix fail-fast 级联传播 | 大规模 matrix |
| INTENT-REL-008 | P1 | matrix max-parallel 限额 | 大规模 matrix |
| INTENT-REL-009 | P1 | timeout-minutes 强制终止 | 长时运行 |
| INTENT-REL-010 | P1 | 独立 job timeout 时钟 | 长时运行 |
| INTENT-REL-011 | P1 | 非法 timeout 值拒绝 | 长时运行 |
| INTENT-REL-012 | P1 | OOM kill（12GB on 8GB runner） | 资源耗尽 |
| INTENT-REL-013 | P1 | disk full（50GB 上限） | 资源耗尽 |
| INTENT-REL-014 | P1 | 跨 job workspace 隔离 | 资源耗尽 |
| INTENT-REL-015 | P0 | kill runner mid-job + 重试恢复 | 故障注入 |
| INTENT-REL-016 | P1 | 网络断连 60s 恢复 | 故障注入 |
| INTENT-REL-017 | P1 | runner 崩溃前 checkout | 故障注入 |
| INTENT-REL-018 | P1 | post 阶段 run_always on cancel | 故障注入 |
| INTENT-REL-019 | P1 | 手动取消 + cleanup step 执行 | 取消语义 |
| INTENT-REL-020 | P1 | stages.fail_fast 级内取消 | 取消语义 |
| INTENT-REL-021 | P1 | 跨 workflow job-concurrency 死锁防护 | 并发控制 |
| INTENT-REL-022 | P0 | needs 链 A→B→C 失败跳过后置 | 故障传播 |
| INTENT-REL-023 | P1 | fan-in 依赖失败 | 故障传播 |
| INTENT-REL-024 | P0 | needs→matrix 父级失败回归 | 故障传播 |
| INTENT-REL-025 | P1 | rerun-failed-jobs 局部重跑 | 重跑可靠性 |
| INTENT-REL-026 | P1 | 重试上限 3 次强制 | 重跑可靠性 |
| INTENT-REL-027 | P1 | RUN_ID/RUN_NUMBER vs SHA 一致性 | 重跑可靠性 |
| INTENT-REL-028 | P1 | continue-on-error + if:success() | 条件传播 |
| INTENT-REL-029 | P1 | 上传中止 artifact 不完整 | artifact 韧性 |

### usability（23 条）

| ID | 优先级 | 标题 | 类别 |
|---|---|---|---|
| INTENT-USE-001 | P1 | 必填字段缺失报错质量 | 错误信息 |
| INTENT-USE-002 | P1 | 字段类型错误报错质量 | 错误信息 |
| INTENT-USE-003 | P1 | GitHub-only 未知字段处理 | 错误信息 |
| INTENT-USE-004 | P1 | PR types 命名差异报错 | 错误信息 |
| INTENT-USE-005 | P1 | 表达式语法错误报错 quality | 错误信息 |
| INTENT-USE-006 | P1 | context 命名差异报错 | 错误信息 |
| INTENT-USE-007 | P1 | 文档中 GITHUB_* 残余文本 | 文档一致性 |
| INTENT-USE-008 | P1 | environment 字段文档与实际 | 文档一致性 |
| INTENT-USE-009 | P1 | runner.os/arch 大小写文档 | 文档一致性 |
| INTENT-USE-010 | P1 | ::group::/::error::/::warning:: 命令 | 调试体验 |
| INTENT-USE-011 | P1 | run 状态机可见性 | 调试体验 |
| INTENT-USE-012 | P1 | ATOMGIT_* 系统变量完整性 | 调试体验 |
| INTENT-USE-013 | P1 | post stage UI 呈现 | 调试体验 |
| INTENT-USE-014 | P0 | 端到端 GitHub→GitCode workflow 迁移 | 迁移摩擦 |
| INTENT-USE-015 | P0 | runs-on 标签映射报错 | 迁移摩擦 |
| INTENT-USE-016 | P0 | permissions 命名差异报错 | 迁移摩擦 |
| INTENT-USE-017 | P1 | actions/checkout@v4 可用性 | 迁移摩擦 |
| INTENT-USE-018 | P1 | workflow_dispatch inputs 类型限制 | 迁移摩擦 |
| INTENT-USE-019 | P1 | 官方迁移指南完整性 | 迁移摩擦 |
| INTENT-USE-020 | P1 | re-run 缓存日志保留 | 重跑体验 |
| INTENT-USE-021 | P1 | re-run 限制提示（3 次/6h） | 重跑体验 |
| INTENT-USE-022 | P1 | workflow_call 2 层嵌套限制报错 | 组合 |
| INTENT-USE-023 | P1 | concurrency queue 可见性 | 组合 |

## 优先级分布

| 维度 | P0 | P1 | P2 | 合计 |
|---|---|---|---|---|
| completeness | 5 | 20 | 0 | 25 |
| compatibility | 9 | 22 | 0 | 31 |
| security | 14 | 22 | 0 | 36 |
| reliability | 3 | 26 | 0 | 29 |
| usability | 3 | 20 | 0 | 23 |
| **合计** | **34** | **110** | **0** | **144** |

## 输入缺失退化标注

以下维度因输入缺失而退化，intent 中已显式标注：
- `workflow-samples/` ☐: compat-diff（差异发现偏理论）、usability（迁移摩擦基于推测）
- `security-knowledge/` ☐: security（缺 OWASP CI/CD Top 10 / CVE 分析）
- `platform-config/` ☐: reliability（配额/容量边界值为推断值）、spec（某些 Fuzzy 项无法验证）
- `business-context/` ☐: usability（无真实迁移场景参照）

---

*下一步：评审门禁（review-gate + orchestrator）→ 去重 · 定优先级 · 查覆盖盲区 → STOP①*
