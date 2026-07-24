# Case Manifest · Run 2026-07-23-01

> 生成时间: 2026-07-23
> 运行目的: 生产统一、自包含的基准全量用例集（全维度、全准入 intent + 补全字段级 KEEP 用例）
> 准入 intent 总数: 186 条
> 生成用例总数: 328 条
> 字段级 KEEP 补全: 42 条（合并自 ~260 条 KEEP 历史用例）
> 复用已有 TC: 0 条
> 待生成: 0

---

## 统计摘要

| 维度 | 准入 Intent | 生成用例 | P0 | P1 | P2 |
|---|---|---|---|---|---|
| completeness | 16 | 88 | 16 | 72 | 0 |
| compatibility | 35 | 66 | 13 | 53 | 0 |
| security | 36 | 51 | 50 | 1 | 0 |
| reliability | 66 | 74 | 2 | 69 | 3 |
| usability | 29 | 49 | 2 | 47 | 0 |
| **合计** | **182** | **328** | **83** | **242** | **3** |

---

## 全量用例清单


### completeness（88 条）

| 用例 ID | 优先级 | 溯源意图 | 标题 |
|---|---|---|---|
| COMP-ARTIFACT-01-001 | P1 | INTENT-COMP-015 | artifact 可在同 workflow 的 job 间正确传递 |
| COMP-ARTIFACT-01-002 | P1 | INTENT-COMP-015 | 下载全部制品功能正常 |
| COMP-ARTIFACT-01-003 | P1 | INTENT-COMP-015 | artifact 保留期设置生效 |
| COMP-ATOMGIT-01-047 | P1 | KEEP-TC-017~057 | atomgit 核心上下文属性可访问性 |
| COMP-ATOMGIT-01-048 | P1 | KEEP-TC-048~060 | atomgit 事件相关属性可访问性 |
| COMP-ATOMGIT-01-049 | P1 | KEEP-TC-566~570 | atomgit 边界格式校验 |
| COMP-BOUND-01-084 | P1 | KEEP-TC-514~559 | 路径与分支过滤组合及否定模式边界验证 |
| COMP-BOUND-01-085 | P1 | KEEP-TC-475~512 | cron 表达式格式与位置边界验证 |
| COMP-BOUND-01-086 | P1 | KEEP-TC-276~328 | 矩阵构建 include exclude 与单值边界验证 |
| COMP-BOUND-01-087 | P1 | KEEP-TC-331~333 | 步骤输出与跨 job 传递边界验证 |
| COMP-BOUND-01-088 | P1 | KEEP-TC-240~246 | 工作流命令 set-env add-path 与文件写入边界验证 |
| COMP-CACHE-01-001 | P0 | INTENT-COMP-016 | cache hit 时恢复缓存内容正确 |
| COMP-CACHE-01-002 | P0 | INTENT-COMP-016 | restore-keys 前缀匹配兜底生效 |
| COMP-CACHE-01-003 | P0 | INTENT-COMP-016 | fork PR 不应覆盖或污染主分支 cache |
| COMP-CALL-01-001 | P1 | INTENT-COMP-006 | 2 层 workflow_call 嵌套正常执行 |
| COMP-CALL-01-002 | P1 | INTENT-COMP-006 | 3 层 workflow_call 嵌套应被拒绝 |
| COMP-CTX-01-051 | P1 | KEEP-TC-086~124 | 上下文在 workflow job step 各级注入验证 |
| COMP-CTX-01-052 | P1 | KEEP-TC-086~124 | 上下文在条件表达式 if 中注入验证 |
| COMP-CTX-01-053 | P1 | KEEP-TC-086~124 | 上下文在 Action 插件参数中注入验证 |
| COMP-DIR-01-001 | P1 | INTENT-COMP-001 | .gitcode/workflows/ 下的 YAML 被正确识别并触发 |
| COMP-DIR-01-002 | P1 | INTENT-COMP-001 | .github/workflows/ 下的 YAML 不被识别为 workflow |
| COMP-ENVCTX-01-050 | P1 | KEEP-TC-001~004 | env 优先级链 step 大于 job 大于 workflow |
| COMP-EXPR-01-054 | P1 | KEEP-TC-180~182 | 字符串函数 contains startsWith endsWith 边界行为 |
| COMP-EXPR-01-055 | P1 | KEEP-TC-186 | hashFiles 函数边界行为 |
| COMP-EXPR-01-056 | P1 | KEEP-TC-187 | toJson 函数边界行为 |
| COMP-EXPR-01-057 | P1 | KEEP-TC-183~185 | format substring replace 函数边界行为 |
| COMP-EXPR-01-058 | P1 | KEEP-TC-160~175 | 表达式运算符与优先级边界行为 |
| COMP-ISOLATION-01-001 | P0 | INTENT-COMP-011 | 同一 workflow 先后 job 的文件系统相互隔离 |
| COMP-ISOLATION-01-002 | P0 | INTENT-COMP-011 | 环境变量不跨 job 泄漏 |
| COMP-JOB-01-066 | P1 | KEEP-TC-264~288 | job 必填字段 name runs-on steps 验证 |
| COMP-JOB-01-067 | P1 | KEEP-TC-264~288 | job 可选字段 env if timeout-minutes needs 验证 |
| COMP-JOB-01-068 | P1 | KEEP-TC-276~278 | job strategy 矩阵与 continue-on-error 验证 |
| COMP-PERMS-01-001 | P0 | INTENT-COMP-013 | permissions 空对象时 ATOMGIT_TOKEN 仅 repository read |
| COMP-PERMS-01-002 | P0 | INTENT-COMP-013 | 声明 repository write 后 TOKEN 可推送代码 |
| COMP-PERMS-01-003 | P0 | INTENT-COMP-013 | fork PR 的 pull_request 下声明 write 仍仅 read |
| COMP-PR-01-001 | P0 | INTENT-COMP-004 | fork PR 触发 pull_request 时不可读取项目 secrets |
| COMP-PR-01-002 | P0 | INTENT-COMP-004 | pull_request_target 可访问 secrets 且 TOKEN 拥有写权限 |
| COMP-PR-01-003 | P0 | INTENT-COMP-004 | fork PR 的 pull_request workflow ATOMGIT_TOKEN 仅 read 权限 |
| COMP-PRTARGET-01-001 | P0 | INTENT-COMP-014 | pull_request_target 默认使用 base 分支 workflow 版本 |
| COMP-PRTARGET-01-002 | P0 | INTENT-COMP-014 | 显式 checkout head.sha 后执行不可信代码的风险可控 |
| COMP-PUSH-01-001 | P1 | INTENT-COMP-003 | 匹配 branches 的 push 正确触发 workflow |
| COMP-PUSH-01-002 | P1 | INTENT-COMP-003 | 不匹配 branches 的 push 不触发 workflow |
| COMP-PUSH-01-003 | P1 | INTENT-COMP-003 | paths 过滤匹配前 300 个变更文件行为符合预期 |
| COMP-RERUN-01-001 | P1 | INTENT-COMP-009 | rerun 后 atomgit.sha 保持原始值 run_number 递增 |
| COMP-RERUN-01-002 | P1 | INTENT-COMP-009 | 第 4 次 rerun 应被系统拒绝 |
| COMP-RERUN-01-003 | P1 | INTENT-COMP-009 | 超过 6 小时的运行不可 rerun |
| COMP-RUNNER-01-001 | P1 | INTENT-COMP-010 | 三段式标签正确调度到对应规格 Runner |
| COMP-RUNNER-01-002 | P1 | INTENT-COMP-010 | runs-on default 等效 ubuntu-latest x64 small |
| COMP-RUNNER-01-003 | P1 | INTENT-COMP-010 | 不存在的标签组合导致 job 排队或失败 |
| COMP-RUNNER-01-080 | P1 | KEEP-TC-096~098 | runner 上下文属性可访问性验证 |
| COMP-SCHEDULE-01-001 | P1 | INTENT-COMP-005 | 合法 cron 在默认分支按时触发 |
| COMP-SCHEDULE-01-002 | P1 | INTENT-COMP-005 | 非默认分支的 schedule workflow 不应触发 |
| COMP-SCHEDULE-01-003 | P1 | INTENT-COMP-005 | cron 间隔短于 5 分钟时被拒绝或降级 |
| COMP-SCRIPT-01-081 | P1 | KEEP-TC-431~433 | 仓库内脚本执行与路径验证 |
| COMP-SCRIPT-01-082 | P1 | KEEP-TC-431~433 | 脚本权限设置与直接执行验证 |
| COMP-SECRET-01-001 | P0 | INTENT-COMP-012 | echo secret 在日志中被脱敏为 *** |
| COMP-SECRET-01-002 | P0 | INTENT-COMP-012 | secret 原始值不应以明文出现在标准日志中 |
| COMP-SECRET-01-003 | P0 | INTENT-COMP-012 | base64 编码后的 secret 是否仍被脱敏 |
| COMP-STAGES-01-001 | P1 | INTENT-COMP-007 | stages 阶段间串行、阶段内 job 并行执行 |
| COMP-STAGES-01-002 | P1 | INTENT-COMP-007 | fail_fast true 时 stage 内任一 job 失败终止同阶段其余 job |
| COMP-STAGES-01-003 | P1 | INTENT-COMP-007 | post.run_always true 时 workflow 失败仍执行 post |
| COMP-STATUS-01-001 | P1 | INTENT-COMP-017 | 运行状态机 queued 到 completed 转换正确 |
| COMP-STATUS-01-002 | P1 | INTENT-COMP-017 | 失败 step 的日志完整保留且可查看 |
| COMP-STEP-01-069 | P1 | KEEP-TC-279~288 | step 必填与核心字段 name run uses 验证 |
| COMP-STEP-01-070 | P1 | KEEP-TC-279~288 | step 可选字段 id env if with 验证 |
| COMP-STEP-01-071 | P1 | KEEP-TC-279~288 | step 执行控制 shell working-directory continue-on-error timeout-minutes 验证 |
| COMP-SUMMARY-01-001 | P1 | INTENT-COMP-018 | ATOMGIT_STEP_SUMMARY Markdown 表格与标题正确渲染 |
| COMP-SUMMARY-01-002 | P1 | INTENT-COMP-018 | summary 中不应暴露系统内部路径 |
| COMP-SYSENV-01-059 | P1 | KEEP-TC-197~222 | ATOMGIT 系统环境变量关键变量存在性 |
| COMP-SYSENV-01-060 | P1 | KEEP-TC-197~222 | ATOMGIT 系统环境变量值正确性 |
| COMP-TIMEOUT-01-001 | P1 | INTENT-COMP-008 | 未声明 timeout-minutes 的 job 在 360 分钟内正常完成 |
| COMP-TIMEOUT-01-002 | P1 | INTENT-COMP-008 | 超时的 job 被强制终止并标记为 failure |
| COMP-TRIG-01-072 | P1 | KEEP-TC-223~233 | push 事件关键字段与过滤验证 |
| COMP-TRIG-01-073 | P1 | KEEP-TC-061~083 | pull_request 事件关键字段与 types 验证 |
| COMP-TRIG-01-074 | P1 | KEEP-TC-084~085 | workflow_dispatch 事件关键字段与 inputs 验证 |
| COMP-TRIG-01-075 | P1 | KEEP-TC-237~430 | schedule 事件关键字段与 cron 格式验证 |
| COMP-TRIG-01-076 | P1 | KEEP-TC-075~083 | issue_comment 事件关键字段与 types 验证 |
| COMP-TRIG-01-077 | P1 | KEEP-TC-469~470 | pull_request_comment 事件关键字段与过滤验证 |
| COMP-TRIG-01-078 | P1 | KEEP-TC-423 | 多事件组合与分支路径过滤验证 |
| COMP-TRIG-01-079 | P1 | KEEP-TC-234~560 | 触发事件 types 取值与过滤边界验证 |
| COMP-UNKNOWN-01-001 | P1 | INTENT-COMP-002 | 包含未知顶层字段的 workflow 触发 YAML 校验失败 |
| COMP-UNKNOWN-01-002 | P1 | INTENT-COMP-002 | 不应静默忽略未知字段导致用户误以为配置生效 |
| COMP-VARREF-01-083 | P1 | KEEP-TC-438~440 | YAML 表达式与 Shell 环境变量引用方式验证 |
| COMP-WFLOW-01-061 | P1 | KEEP-TC-366~401 | workflow name 与 on 字段必填与类型验证 |
| COMP-WFLOW-01-062 | P1 | KEEP-TC-366~401 | workflow env 与 defaults 字段验证 |
| COMP-WFLOW-01-063 | P1 | KEEP-TC-289~293 | workflow concurrency 并发控制字段验证 |
| COMP-WFLOW-01-064 | P1 | KEEP-TC-366~401 | workflow stages 阶段结构字段验证 |
| COMP-WFLOW-01-065 | P1 | KEEP-TC-366~401 | workflow post 后处理阶段字段验证 |

### compatibility（66 条）

| 用例 ID | 优先级 | 溯源意图 | 标题 |
|---|---|---|---|
| COMPAT-ACTION-01-001 | P1 | INTENT-COMPAT-024 | checkout 短名等价性——ref 参数支持 |
| COMPAT-ACTION-01-002 | P1 | INTENT-COMPAT-024 | checkout 短名等价性——path 参数支持 |
| COMPAT-ARTIFACT-01-001 | P1 | INTENT-COMPAT-026 | upload/download-artifact 跨 job 传递等价性 |
| COMPAT-ARTIFACT-01-002 | P1 | INTENT-COMPAT-026 | upload-artifact 保留期行为等价性 |
| COMPAT-CACHE-01-001 | P1 | INTENT-COMPAT-025 | cache 行为等价性——缓存命中场景 |
| COMPAT-CACHE-01-002 | P0 | INTENT-COMPAT-025 | cache 行为等价性——fork PR 写隔离 |
| COMPAT-CONCUR-01-001 | P1 | INTENT-COMPAT-034 | concurrency cancel-in-progress false 时应排队而非报错 |
| COMPAT-CONCUR-01-002 | P1 | INTENT-COMPAT-034 | concurrency 配置越界或不支持时应给出清晰报错 |
| COMPAT-CTX-01-001 | P1 | INTENT-COMPAT-016 | 使用 github.ref 上下文应报错或求值为空 |
| COMPAT-CTX-01-002 | P1 | INTENT-COMPAT-016 | 使用 atomgit.ref 上下文应正确返回触发引用 |
| COMPAT-DIR-01-001 | P1 | INTENT-COMPAT-029 | 工作流目录差异——.gitcode/workflows/ 正常识别 |
| COMPAT-DIR-01-002 | P1 | INTENT-COMPAT-029 | 工作流目录差异——.github/workflows/ 不应被识别 |
| COMPAT-ENV-01-001 | P1 | INTENT-COMPAT-017 | ATOMGIT_SHA 环境变量应正确返回触发提交 SHA |
| COMPAT-ENV-01-002 | P1 | INTENT-COMPAT-017 | GITHUB_SHA 环境变量在 GitCode 中应为空或未定义 |
| COMPAT-ENVIRON-01-001 | P1 | INTENT-COMPAT-023 | 含 environment 字段的 job 应被报错或警告 |
| COMPAT-EXPR-01-001 | P1 | INTENT-COMPAT-004 | success 关键字在条件表达式中的可用性 |
| COMPAT-EXPR-01-002 | P1 | INTENT-COMPAT-004 | success() 函数的处理行为差异 |
| COMPAT-EXPR-01-003 | P1 | INTENT-COMPAT-005 | failure() 与 failed 关键字的处理行为差异 |
| COMPAT-EXPR-01-004 | P1 | INTENT-COMPAT-006 | contains 表达式大小写敏感边界 |
| COMPAT-EXPR-01-005 | P1 | INTENT-COMPAT-006 | contains 表达式空值与空字符串边界 |
| COMPAT-EXPR-01-006 | P1 | INTENT-COMPAT-007 | hashFiles 表达式无匹配路径边界 |
| COMPAT-EXPR-01-007 | P1 | INTENT-COMPAT-007 | hashFiles 表达式多路径组合边界 |
| COMPAT-EXPR-01-008 | P1 | INTENT-COMPAT-008 | toJson 表达式输出格式差异（pretty-print vs compact） |
| COMPAT-EXPR-01-009 | P1 | INTENT-COMPAT-009 | loose equality 跨类型强制求值差异 |
| COMPAT-EXPR-01-010 | P1 | INTENT-COMPAT-009 | loose equality null 与空字符串及零的等价性差异 |
| COMPAT-EXPR-01-011 | P1 | INTENT-COMPAT-010 | join() 函数缺失时的降级行为 |
| COMPAT-EXPR-01-012 | P1 | INTENT-COMPAT-010 | fromJSON() 函数缺失时的降级行为 |
| COMPAT-FIELD-01-001 | P1 | INTENT-COMPAT-021 | 含 run-name 字段的 workflow 应被报错或警告 |
| COMPAT-FIELD-01-002 | P1 | INTENT-COMPAT-021 | 含 services 字段的 job 应被报错或警告 |
| COMPAT-IF-01-001 | P1 | INTENT-COMPAT-003 | step 失败后后续 step 默认跳过行为 |
| COMPAT-IF-01-002 | P1 | INTENT-COMPAT-003 | continue-on-error 标记后失败 step 不阻断后续执行 |
| COMPAT-INPUTS-01-001 | P1 | INTENT-COMPAT-014 | workflow_dispatch inputs 类型限制 - boolean 应报错 |
| COMPAT-INPUTS-01-002 | P1 | INTENT-COMPAT-014 | workflow_dispatch inputs 类型限制 - string 正常通过 |
| COMPAT-ISOLATE-01-001 | P1 | INTENT-COMPAT-028 | Runner 环境隔离——跨 job 文件隔离 |
| COMPAT-ISOLATE-01-002 | P1 | INTENT-COMPAT-028 | Runner 环境隔离——跨 job 环境变量隔离 |
| COMPAT-MASK-01-001 | P0 | INTENT-COMPAT-033 | 直接 echo secrets 值应在日志中被脱敏 |
| COMPAT-MASK-01-002 | P0 | INTENT-COMPAT-033 | 通过 env 注入 secret 后输出应在日志中被脱敏 |
| COMPAT-MIGRATE-01-001 | P1 | INTENT-COMPAT-031 | GitHub 风格 permissions 块迁移报错应给出可操作指引 |
| COMPAT-MIGRATE-01-002 | P1 | INTENT-COMPAT-031 | GitHub 风格 run-name 语法迁移报错应给出可操作指引 |
| COMPAT-NEST-01-001 | P1 | INTENT-COMPAT-015 | workflow_call 嵌套层数 - 2 层正常执行 |
| COMPAT-NEST-01-002 | P1 | INTENT-COMPAT-015 | workflow_call 嵌套层数 - 3 层越界应报错 |
| COMPAT-OUTCOME-01-001 | P1 | INTENT-COMPAT-035 | continue-on-error false 时 outcome 与 conclusion 应均为 failure |
| COMPAT-OUTCOME-01-002 | P1 | INTENT-COMPAT-035 | continue-on-error true 时 outcome 应为 failure 而 conclusion 应为 success |
| COMPAT-OUTCOME-01-003 | P1 | INTENT-COMPAT-035 | outcome 与 conclusion 在 job 条件判断中不应互换语义 |
| COMPAT-PATHS-01-001 | P1 | INTENT-COMPAT-012 | paths 过滤器 300 条边界测试 |
| COMPAT-PATHS-01-002 | P1 | INTENT-COMPAT-012 | paths 过滤器 301 条越界测试 |
| COMPAT-PERM-01-001 | P0 | INTENT-COMPAT-002 | 未声明 permissions 时默认 TOKEN 读操作权限范围 |
| COMPAT-PERM-01-002 | P0 | INTENT-COMPAT-002 | 未声明 permissions 时 fork PR 写操作隔离 |
| COMPAT-PERM-01-003 | P0 | INTENT-COMPAT-030 | permissions 命名差异——GitHub contents 权限项应报错 |
| COMPAT-PERM-01-004 | P0 | INTENT-COMPAT-030 | permissions 命名差异——GitCode repository 权限项正常生效 |
| COMPAT-PR-01-001 | P0 | INTENT-COMPAT-011 | pull_request types 命名差异 - GitCode 合法 types 应被接受 |
| COMPAT-PR-01-002 | P0 | INTENT-COMPAT-011 | pull_request types 命名差异 - GitHub 风格 types 应报错 |
| COMPAT-RUNNER-01-001 | P1 | INTENT-COMPAT-018 | runner.os 在 Linux Runner 上应返回 Linux |
| COMPAT-RUNNER-01-002 | P1 | INTENT-COMPAT-019 | runner.arch 在 x86_64 Runner 上应返回 X64 |
| COMPAT-RUNSON-01-001 | P1 | INTENT-COMPAT-027 | runs-on 标签体系——三段式数组正常匹配 |
| COMPAT-RUNSON-01-002 | P1 | INTENT-COMPAT-027 | runs-on 标签体系——单标签字符串应报错 |
| COMPAT-SCHEDULE-01-001 | P1 | INTENT-COMPAT-013 | schedule cron 按 UTC 时间触发 |
| COMPAT-SCHEDULE-01-002 | P1 | INTENT-COMPAT-013 | schedule 不支持 timezone 字段差异 |
| COMPAT-SHELL-01-001 | P1 | INTENT-COMPAT-001 | 默认 shell 隐式行为差异 - 未显式声明时是否为 bash |
| COMPAT-SHELL-01-002 | P1 | INTENT-COMPAT-001 | 默认工作目录隐式行为差异 - 未显式声明时是否为仓库根目录 |
| COMPAT-TARGET-01-001 | P0 | INTENT-COMPAT-032 | pull_request_target 默认 checkout 应为 base 分支而非 head 分支 |
| COMPAT-TARGET-01-002 | P0 | INTENT-COMPAT-032 | pull_request_target 在 fork 场景下应保持 secret 隔离 |
| COMPAT-TOKEN-01-001 | P0 | INTENT-COMPAT-020 | ATOMGIT_TOKEN 应正确返回有效令牌 |
| COMPAT-TOKEN-01-002 | P0 | INTENT-COMPAT-020 | GITHUB_TOKEN 在 GitCode 中应为空且不应被静默映射 |
| COMPAT-VARS-01-001 | P1 | INTENT-COMPAT-022 | vars 上下文若支持应正确返回值 |
| COMPAT-VARS-01-002 | P1 | INTENT-COMPAT-022 | vars 上下文若不支持应报错而非静默为空 |

### security（51 条）

| 用例 ID | 优先级 | 溯源意图 | 标题 |
|---|---|---|---|
| SEC-ARTF-01-001 | P0 | INTENT-SEC-019 | fork PR 上传的 artifact 必须不可被主仓 workflow 下载或执行 |
| SEC-ARTF-01-002 | P0 | INTENT-SEC-019 | 跨仓库 artifact 下载返回 403 或 404 |
| SEC-BASE-01-001 | P0 | INTENT-SEC-035 | pull_request_target 使用 base 分支的 workflow 版本 |
| SEC-BASE-01-002 | P0 | INTENT-SEC-035 | fork PR 改 workflow 不被 pull_request_target 采用 |
| SEC-CACHE-01-001 | P0 | INTENT-SEC-018 | fork PR 写入的 cache 必须不可被主仓后续 workflow 读取 |
| SEC-CACHE-01-002 | P0 | INTENT-SEC-018 | 主仓 cache restore 对 fork cache miss |
| SEC-COMM-01-001 | P0 | INTENT-SEC-026 | issue_comment / pull_request_comment 触发关键字过滤必须不可被绕过 |
| SEC-DEFPERM-01-001 | P0 | INTENT-SEC-036 | ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效 |
| SEC-DEFPERM-01-002 | P0 | INTENT-SEC-036 | job 级覆盖后权限正确收窄 |
| SEC-DOS-01-001 | P0 | INTENT-SEC-033 | 大 artifact / 大 cache 必须受配额与边界限制 |
| SEC-ENV-01-001 | P0 | INTENT-SEC-027 | 环境级 secret 必须经审批后才能被 workflow 访问 |
| SEC-ENV-01-002 | P0 | INTENT-SEC-027 | 环境级 secret 审批前 workflow 不可读取 |
| SEC-FORK-01-001 | P0 | INTENT-SEC-001 | fork PR 触发 pull_request 时不可读取项目 secrets |
| SEC-FORK-01-002 | P0 | INTENT-SEC-001 | fork PR 中 secrets 引用返回空值且 job 不崩溃 |
| SEC-INJ-01-001 | P0 | INTENT-SEC-009 | 不可信 PR 标题不可直接插进 run 脚本导致命令注入 |
| SEC-INJ-01-002 | P0 | INTENT-SEC-010 | 不可信分支名不可直接插进 run 脚本导致命令注入 |
| SEC-INJ-01-003 | P0 | INTENT-SEC-011 | 不可信 issue/PR 评论内容不可直接插进 run 脚本导致命令注入 |
| SEC-INJ-01-004 | P0 | INTENT-SEC-012 | 不可信 commit message 不可直接插进 run 脚本导致命令注入 |
| SEC-INJ-01-005 | P0 | INTENT-SEC-013 | 表达式求值必须防止双重模板渲染（二次求值） |
| SEC-MASK-01-001 | P0 | INTENT-SEC-004 | Secret 值在运行日志中必须被自动脱敏为 *** |
| SEC-MASK-01-002 | P0 | INTENT-SEC-004 | Secret 值在 step summary 和错误堆栈中必须被脱敏 |
| SEC-MASK-01-003 | P0 | INTENT-SEC-005 | Secret 日志脱敏不可通过 base64 编码绕过 |
| SEC-MASK-01-004 | P0 | INTENT-SEC-006 | Secret 日志脱敏不可通过字符串拼接或插值绕过 |
| SEC-MASK-01-005 | P0 | INTENT-SEC-007 | Secret 日志脱敏不可通过多行值输出绕过 |
| SEC-MASK-01-006 | P0 | INTENT-SEC-008 | Secret 日志脱敏不可通过分片输出绕过 |
| SEC-NAME-01-001 | P0 | INTENT-SEC-024 | Secret/变量名含特殊字符时不可导致意外求值或权限绕过 |
| SEC-NAME-01-002 | P0 | INTENT-SEC-025 | 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏 |
| SEC-NET-01-001 | P0 | INTENT-SEC-023 | Runner 网络出站必须受控，防止 SSRF 与内网跳板 |
| SEC-OIDC-01-001 | P1 | INTENT-SEC-034 | OIDC / 短时凭据支持若缺失，必须明确标注为平台限制并提供替代安全方案 |
| SEC-PERM-01-001 | P0 | INTENT-SEC-016 | 显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN |
| SEC-PERM-01-002 | P0 | INTENT-SEC-016 | permissions 声明 read 时写操作被平台拒绝 |
| SEC-PERM-01-003 | P0 | INTENT-SEC-017 | 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only） |
| SEC-PERM-01-004 | P0 | INTENT-SEC-017 | 默认状态下写操作被 403 拒绝 |
| SEC-PRTGT-01-001 | P0 | INTENT-SEC-002 | pull_request_target 下显式 checkout 不可信 PR 时 secrets 仍应受控 |
| SEC-PRTGT-01-002 | P0 | INTENT-SEC-002 | pull_request_target 无审批不执行 fork PR 代码 |
| SEC-RUN-01-001 | P0 | INTENT-SEC-020 | Job 结束后 workspace 与临时文件必须被彻底清理 |
| SEC-RUN-01-002 | P0 | INTENT-SEC-021 | Runner 环境变量与共享目录必须跨 job 隔离 |
| SEC-RUN-01-003 | P0 | INTENT-SEC-022 | 自托管 Runner 跨项目残留必须被隔离 |
| SEC-SIDE-01-001 | P0 | INTENT-SEC-032 | Secret 不经 output 侧信道绕过脱敏外泄 |
| SEC-SIDE-01-002 | P0 | INTENT-SEC-032 | Secret 不经 artifact 侧信道绕过脱敏外泄 |
| SEC-SUPPLY-01-001 | P0 | INTENT-SEC-014 | 第三方 Action 引用应支持完整 commit hash 固定 |
| SEC-SUPPLY-01-002 | P0 | INTENT-SEC-014 | commit hash 不匹配时第三方 Action 应被拒绝执行 |
| SEC-SUPPLY-01-003 | P0 | INTENT-SEC-015 | 第三方 Action 来源应具备信任边界（typosquatting 限制） |
| SEC-TOCTOU-01-001 | P0 | INTENT-SEC-031 | 审批后推送新 commit 不应被已授权特权运行执行 |
| SEC-TOCTOU-01-002 | P0 | INTENT-SEC-031 | 评论触发不应绕过代码固定与 PR 审批 |
| SEC-TOKEN-01-001 | P0 | INTENT-SEC-003 | fork PR 触发 pull_request 时 ATOMGIT_TOKEN 必须仅拥有 read 权限 |
| SEC-TOKEN-01-002 | P0 | INTENT-SEC-003 | fork PR 中 ATOMGIT_TOKEN 写操作被平台拒绝 |
| SEC-WCMD-01-001 | P0 | INTENT-SEC-028 | Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值 |
| SEC-WCMD-01-002 | P0 | INTENT-SEC-029 | 跨运行 artifact 必须被视为不可信数据 |
| SEC-WCMD-01-003 | P0 | INTENT-SEC-030 | ATOMGIT_ENV 不被不可信输入污染提权 |
| SEC-WCMD-01-004 | P0 | INTENT-SEC-030 | ATOMGIT_OUTPUT 不被不可信输入污染提权 |

### reliability（72 条）

| 用例 ID | 优先级 | 溯源意图 | 标题 |
|---|---|---|---|
| REL-API-01-065 | P2 | INTENT-REL-065 | API 限流与一致性——10 QPS 高频查询 run/job 状态不丢数据 |
| REL-ART-01-041 | P1 | INTENT-REL-041 | 超大 artifact——100 MB artifact 上传后下游 job 应成功下载 |
| REL-ARTCONC-01-063 | P1 | INTENT-REL-063 | 制品并发写一致性——多 job 同时 upload-artifact 同名 artifact |
| REL-ARTPERF-01-053-V2 | P1 | INTENT-REL-053 | 制品传输性能——1GB artifact 上传下载耗时 |
| REL-ARTPERF-01-053 | P1 | INTENT-REL-053 | 制品传输性能——100MB artifact 上传下载耗时 |
| REL-BIGRUNNER-01-066 | P1 | INTENT-REL-066 | 大规格资源调度稳定性——xlarge/2xlarge 反复编译成功率 |
| REL-CACHE-01-046 | P1 | INTENT-REL-046 | 缓存 LRU 淘汰压力——连续写入 10 个大缓存后最旧缓存应被正确淘汰 |
| REL-CACHEPERF-01-054 | P2 | INTENT-REL-054 | 缓存加速比——cache 命中 vs 未命中构建耗时对比 |
| REL-CANCEL-01-028 | P1 | INTENT-REL-028 | 手动取消 workflow——运行中取消时 always() cleanup step 仍应执行 |
| REL-CANCELREL-01-061 | P1 | INTENT-REL-061 | 取消操作可靠性——queued/running/post 各阶段取消状态正确过渡 |
| REL-CHILDSTATE-01-064-V2 | P0 | INTENT-REL-064 | 子任务状态传播——workflow_call 未拉起时父 workflow 不应假阳性完成 |
| REL-CHILDSTATE-01-064 | P0 | INTENT-REL-064 | 子任务状态传播——workflow_call 失败时父 workflow 不应假阳性完成 |
| REL-CONC-01-001 | P1 | INTENT-REL-001 | concurrency.max=5 时同时触发 5 个运行应全部进入执行态 |
| REL-CONC-01-002 | P1 | INTENT-REL-002 | concurrency.max=6 配置应被系统拒绝 |
| REL-CONTINUE-01-030 | P1 | INTENT-REL-030 | continue-on-error=true——job 失败后 workflow 不应终止 |
| REL-CPU-01-022 | P1 | INTENT-REL-022 | Runner CPU 饱和——small runner 运行 4 个 CPU 密集型进程应完成但耗时延长 |
| REL-DISK-01-018 | P1 | INTENT-REL-018 | Runner 磁盘边界——small runner 写入 49 GB 应成功 |
| REL-DISK-01-019 | P1 | INTENT-REL-019 | Runner 磁盘越界——small runner 写入 51 GB 应失败并报磁盘满 |
| REL-FAIR-01-044 | P1 | INTENT-REL-044 | 并发资源公平性——2 个 workflow 各 3 个 jobs 应被公平调度 |
| REL-FAULT-01-031 | P1 | INTENT-REL-031 | 故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志 |
| REL-FAULT-01-032 | P1 | INTENT-REL-032 | 故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误 |
| REL-FAULT-01-033 | P1 | INTENT-REL-033 | 故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满 |
| REL-FAULT-01-034 | P1 | INTENT-REL-034 | 故障注入——cache 服务 503 不可用时 job 应优雅降级为 cache miss |
| REL-FAULT-01-035 | P1 | INTENT-REL-035 | 故障注入——artifact 下载服务 503 不可用时 job 应失败并报依赖服务错误 |
| REL-FLOOD-01-036 | P1 | INTENT-REL-036 | 并发洪泛——同一仓库 10 个 push 同时触发 10 个 workflow 运行应无丢失 |
| REL-FLOOD-01-037 | P1 | INTENT-REL-037 | 并发洪泛——同一仓库 50 个 push 同时触发应正确排队/限流不崩溃 |
| REL-IGNORE-01-004 | P1 | INTENT-REL-004 | concurrency IGNORE 策略——超上限运行应直接执行 |
| REL-IMAGE-01-052-V2 | P1 | INTENT-REL-052 | 镜像拉取性能——5GB 自定义 container 环境准备耗时基准 |
| REL-IMAGE-01-052 | P1 | INTENT-REL-052 | 镜像拉取性能——500MB 自定义 container 环境准备耗时基准 |
| REL-K8S-01-045 | P1 | INTENT-REL-045 | 自托管 K8s Runner 弹性伸缩——min=1/max=1 时并发 3 个 jobs 应排队执行 |
| REL-LATENCY-01-050-V2 | P1 | INTENT-REL-050 | 调度延迟压力——并发 20 个 job 的排队延迟与完成率 |
| REL-LATENCY-01-050 | P1 | INTENT-REL-050 | 调度延迟基准——queued→running P50/P95 等待时间 |
| REL-LOG-01-040 | P1 | INTENT-REL-040 | 超长日志——单 job 输出 100 MB 日志应完整保留且可下载查看 |
| REL-LOGPERF-01-051-V2 | P1 | INTENT-REL-051 | 日志加载性能——200MB 日志下载与查看耗时 |
| REL-LOGPERF-01-051 | P1 | INTENT-REL-051 | 日志加载性能——50MB 日志下载与查看耗时 |
| REL-LOGSTABLE-01-059 | P1 | INTENT-REL-059 | 日志系统稳定性——6 万行日志无乱序/无丢失/无截断 |
| REL-LONG-01-043 | P1 | INTENT-REL-043 | 长时运行接近 timeout 边界——350 分钟运行应成功且心跳保活正常 |
| REL-MATRIX-01-026 | P1 | INTENT-REL-026 | matrix fail-fast=true——任意 job 实例失败应立即取消其余实例 |
| REL-MATRIX-01-027 | P1 | INTENT-REL-027 | matrix max-parallel=4——9 个组合应最多同时运行 4 个 |
| REL-MATRIX-01-038 | P1 | INTENT-REL-038 | 大规模 matrix——20 个组合应全部生成并正确调度 |
| REL-MATRIX-01-039 | P1 | INTENT-REL-039 | 大规模 matrix——50 个组合应全部生成并正确调度 |
| REL-MATRIXFAIR-01-056 | P1 | INTENT-REL-056 | 矩阵调度公平性——20 实例 matrix 配 max-parallel=4 的无饿死验证 |
| REL-MEM-01-020 | P1 | INTENT-REL-020 | Runner 内存边界——small runner 分配 7.5 GB 应成功 |
| REL-MEM-01-021 | P1 | INTENT-REL-021 | Runner 内存越界——small runner 分配 9 GB 应被 OOM kill |
| REL-NEEDS-01-025 | P1 | INTENT-REL-025 | needs 失败传播——上游 job 失败时下游 job 应被 skip |
| REL-NEST-01-023 | P1 | INTENT-REL-023 | workflow_call 嵌套边界——2 层嵌套调用应成功执行 |
| REL-NEST-01-024 | P1 | INTENT-REL-024 | workflow_call 嵌套越界——3 层嵌套调用应被拒绝 |
| REL-NETFAULT-01-062 | P2 | INTENT-REL-062 | 网络依赖容错——workflow 中访问不可达地址的明确失败与有界超时 |
| REL-OUTPUT-01-016 | P1 | INTENT-REL-016 | step output 边界值——ATOMGIT_OUTPUT 写入 1 MB 参数应成功传递 |
| REL-OUTPUT-01-017 | P1 | INTENT-REL-017 | step output 越界值——ATOMGIT_OUTPUT 写入 1 MB+1 byte 应被拒绝或报错 |
| REL-PATHS-01-014 | P1 | INTENT-REL-014 | paths 匹配边界值——变更恰好 300 个文件时 paths 过滤应生效 |
| REL-PATHS-01-015 | P1 | INTENT-REL-015 | paths 匹配越界值——第 301 个变更文件不参与 paths 匹配判断 |
| REL-PREEMPT-01-005 | P1 | INTENT-REL-005 | preemption events 边界值——配置 10 个应正常解析 |
| REL-PREEMPT-01-006 | P1 | INTENT-REL-006 | preemption events 越界值——配置 11 个应被拒绝 |
| REL-PRESSURE-01-055 | P1 | INTENT-REL-055 | 并发压测——concurrency.max=5 时触发 20 个 workflow 的排队与完成率 |
| REL-QUEUE-01-003 | P1 | INTENT-REL-003 | concurrency QUEUE 策略——超上限运行应排队等待 |
| REL-RACE-01-048 | P1 | INTENT-REL-048 | 取消与 needs 条件竞态——job A 被取消时 job B(if: failure())应正确判定 |
| REL-RERUN-01-011 | P1 | INTENT-REL-011 | rerun 边界值——单条运行连续重新运行 3 次应全部成功 |
| REL-RERUN-01-012 | P1 | INTENT-REL-012 | rerun 越界值——尝试第 4 次重新运行应被系统拒绝 |
| REL-RERUN-01-013 | P1 | INTENT-REL-013 | rerun 6 小时年龄限制——超期运行不可重新运行 |
| REL-RETAIN-01-047 | P1 | INTENT-REL-047 | artifact 保留期 90 天边界——第 91 天应不可下载 |
| REL-RUNNER-01-049-V2 | P1 | INTENT-REL-049 | Runner 规格真实性——xlarge/2xlarge 实际 CPU/内存/磁盘 vs 声明值 |
| REL-RUNNER-01-049 | P1 | INTENT-REL-049 | Runner 规格真实性——small/medium/large 实际 CPU/内存/磁盘 vs 声明值 |
| REL-SCHED-01-057 | P1 | INTENT-REL-057 | 资源调度状态一致性——空闲 runner 存在时 job 不应死等 |
| REL-STAGES-01-029 | P1 | INTENT-REL-029 | stages fail_fast 机制——阶段内任一 job 失败应立即终止同阶段其他 jobs |
| REL-STATE-01-058 | P1 | INTENT-REL-058 | Runner 状态机正确性——空闲/运行/离线转换与时序一致性 |
| REL-STEPS-01-042 | P1 | INTENT-REL-042 | 超多 step——单 job 内 50 个 step 应全部串行执行无丢失 |
| REL-TIMEOUT-01-007 | P1 | INTENT-REL-007 | job timeout 边界值——359 分钟运行应在 360 分钟边界前完成 |
| REL-TIMEOUT-01-008 | P1 | INTENT-REL-008 | job timeout 越界触发——361 分钟应在 360 分钟被强制终止 |
| REL-TIMEOUT-01-009 | P1 | INTENT-REL-009 | 自定义短超时——timeout-minutes=1 时 step 运行 2 分钟应被强制终止 |
| REL-TIMEOUT-01-010 | P1 | INTENT-REL-010 | 默认超时——未声明 timeout-minutes 运行 361 分钟应被强制终止 |
| REL-YAMLCACHE-01-060 | P1 | INTENT-REL-060 | Workflow YAML 缓存失效——修改后无旧代码残留 |
| REL-PROJLIMIT-01-067 | P1 | INTENT-REL-067 | 项目级 workflow 并发上限——200 条同时触发时全部完成无丢失 |
| REL-PROJLIMIT-01-068 | P1 | INTENT-REL-068 | 项目级 workflow 并发上限越界——201 条同时触发时至少一条进入排队 |

### usability（49 条）

| 用例 ID | 优先级 | 溯源意图 | 标题 |
|---|---|---|---|
| USE-ACT-01-001 | P1 | INTENT-USE-007 | 使用裸插件名 checkout 时正常拉取官方 Action |
| USE-ACT-01-002 | P1 | INTENT-USE-007 | 使用 actions/checkout@v4 时报错应给出迁移指引 |
| USE-ANNOT-01-001 | P1 | INTENT-USE-021 | workflow 命令 ::error:: 与 ::warning:: 在日志中保留原文 |
| USE-ANNOT-01-002 | P1 | INTENT-USE-021 | ::error:: 生成的 PR annotation 具备文件路径、行号与可点击跳转 |
| USE-BADGE-01-001 | P1 | INTENT-USE-019 | workflow 运行完成后状态徽标及时回写且语义清晰 |
| USE-CONC-01-001 | P1 | INTENT-USE-027 | concurrency.max 配置 0 或 10 时报错应提示有效范围 1-5 |
| USE-CONC-01-002 | P1 | INTENT-USE-027 | concurrency.max 配置 -1 时报错应提示有效范围 |
| USE-CTX-01-001 | P1 | INTENT-USE-002 | 使用 atomgit 上下文时表达式正常求值 |
| USE-CTX-01-002 | P1 | INTENT-USE-002 | 使用 github 上下文时报错应提示 atomgit 替代 |
| USE-DEPR-01-001 | P1 | INTENT-USE-010 | 使用 ATOMGIT_OUTPUT 文件协议时正常生效 |
| USE-DEPR-01-002 | P1 | INTENT-USE-010 | 使用 ::set-output 时应给出弃用警告与替代示例 |
| USE-DIR-01-001 | P1 | INTENT-USE-001 | workflow 放置于 .gitcode/workflows/ 下可正常触发 |
| USE-DIR-01-002 | P1 | INTENT-USE-001 | .github/workflows/ 下 workflow 未被识别时应给出目录差异提示 |
| USE-DISP-01-001 | P1 | INTENT-USE-030 | workflow_dispatch 必填参数未提供时应给出明确校验错误 |
| USE-DISP-01-002 | P1 | INTENT-USE-030 | workflow_dispatch 未提供参数但存在 default 时应使用默认值运行 |
| USE-DOC-01-001 | P1 | INTENT-USE-011 | stages 与 post 概念在迁移文档中具备可发现性 |
| USE-ENV-01-001 | P1 | INTENT-USE-003 | 使用 ATOMGIT_SHA 环境变量时正常取值 |
| USE-ENV-01-002 | P1 | INTENT-USE-003 | 引用 GITHUB_SHA 时日志应给出环境变量映射提示 |
| USE-EXPR-01-001 | P1 | INTENT-USE-024 | 引用不存在的上下文属性时报错应包含原始表达式与错误类型 |
| USE-EXPR-01-002 | P1 | INTENT-USE-024 | 调用未知函数时报错应提示函数名错误与修正方向 |
| USE-INPT-01-001 | P1 | INTENT-USE-008 | 使用 string 类型 input 时正常通过校验 |
| USE-INPT-01-002 | P1 | INTENT-USE-008 | 使用 boolean 类型 input 时报错应提示仅支持 string |
| USE-LBL-01-001 | P1 | INTENT-USE-025 | runs-on 标签完全不匹配时应给出明确失败原因与可用标签列表 |
| USE-LBL-01-002 | P1 | INTENT-USE-025 | runs-on 标签因容量不足排队时应提示排队状态而非无可用 runner |
| USE-LOG-01-001 | P1 | INTENT-USE-017 | 多 step 日志按时间线组织且边界清晰 |
| USE-MASK-01-001 | P0 | INTENT-USE-016 | secret 脱敏文档描述与实际行为一致并给出缓解建议 |
| USE-MASK-01-002 | P0 | INTENT-USE-016 | 直接 echo secrets 值时文档描述的绕过风险与实际一致 |
| USE-MD-01-001 | P1 | INTENT-USE-020 | ATOMGIT_STEP_SUMMARY 写入的 Markdown 正确渲染为 HTML |
| USE-NEST-01-001 | P1 | INTENT-USE-026 | workflow_call 嵌套 3 层时报错应明确提示上限为 2 层 |
| USE-NEST-01-002 | P1 | INTENT-USE-026 | workflow_call 嵌套 2 层时应正常执行 |
| USE-OS-01-001 | P1 | INTENT-USE-013 | runner.os 返回值与文档声明的平台支持一致 |
| USE-PATH-01-001 | P1 | INTENT-USE-015 | paths 300 文件上限在文档与行为中一致且明示 |
| USE-PERM-01-001 | P1 | INTENT-USE-005 | 使用 GitCode 权限域命名时正常生效 |
| USE-PERM-01-002 | P1 | INTENT-USE-005 | 使用 GitHub 权限域命名时报错应给出 GitCode 对照表 |
| USE-RES-01-001 | P1 | INTENT-USE-012 | runtime-environment-variables.md 中不应出现未标注的 GitHub 专属变量名 |
| USE-RUN-01-001 | P1 | INTENT-USE-006 | 使用三段式标签时 job 正常调度 |
| USE-RUN-01-002 | P1 | INTENT-USE-006 | 使用单标签 ubuntu-latest 时报错应给出三段式格式指引 |
| USE-SEARCH-01-001 | P1 | INTENT-USE-018 | 日志搜索与下载功能可用且交互流畅 |
| USE-SECNAME-01-001 | P1 | INTENT-USE-028 | Secret 名称以 ATOMGIT_ 开头时应给出命名规则错误 |
| USE-SECNAME-01-002 | P1 | INTENT-USE-028 | Secret 名称以数字开头时应给出命名规则错误 |
| USE-STAT-01-001 | P1 | INTENT-USE-004 | 使用 always() 带括号时若被接受则正常执行 |
| USE-STAT-01-002 | P1 | INTENT-USE-004 | 使用 success() 带括号时报错应提示 GitCode 括号差异 |
| USE-TYPE-01-001 | P1 | INTENT-USE-009 | 使用 GitCode types 命名时正常触发 |
| USE-TYPE-01-002 | P1 | INTENT-USE-009 | 使用 GitHub types 命名 opened/synchronize 时应给出可理解提示 |
| USE-UNKN-01-001 | P1 | INTENT-USE-023 | 未知字段如 run-name 不应被静默忽略而应给出警告或错误 |
| USE-UNKN-01-002 | P1 | INTENT-USE-023 | 未知字段报错若识别为 GitHub 特有应追加迁移提示 |
| USE-VARS-01-001 | P1 | INTENT-USE-014 | vars 上下文在文档与样本中的声明必须一致 |
| USE-YAML-01-001 | P1 | INTENT-USE-022 | 缺少必填字段 on 时报错应指出具体字段名与位置 |
| USE-YAML-01-002 | P1 | INTENT-USE-022 | YAML 缩进错误时报错应指出具体行号与列号 |

---

## 质量自检清单

- [x] 每条文本用例含 `维度标签` 字段，非空
- [x] 每条用例 ID 含 run 序列 `01`，跨 run 不碰撞
- [x] 每条文本用例可溯源到 `intent_ref` 或 `KEEP-TC` 范围
- [x] 每条文本用例有对应、过 schema 校验的 YAML
- [x] 安全用例文本层含「不应发生」验证点，YAML 层落 `negative` 断言
- [x] 破坏性用例声明了正确的 `teardown.reset`
- [x] 主观判据标 `eval: llm_assisted`
- [x] 无真实密钥/token/内网地址，全用占位符
- [x] 未使用 `yaml.dump()` 写 YAML
- [x] `workflow:` 字段全部使用 `|` block scalar
- [x] `runs-on:` 全部使用数组格式
- [x] `uses:` 全部使用裸插件名
- [x] `if:` 仅使用 `${ always() }`（带括号）
- [x] 所有 `run:` 全部使用 `run: |` block scalar
- [x] 每个 job 有 `name:`，每个 step 有 `name:`
- [x] Step name 无非法字符
- [x] 328 条 YAML 全部通过 schema 解析验证

---

*Manifest 最后更新: 2026-07-23*
