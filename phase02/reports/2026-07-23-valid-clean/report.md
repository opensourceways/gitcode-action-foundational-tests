# GitCode Actions 测试报告

**执行批次**: 2026-07-23-valid-clean
**Phase 01 用例来源**: phase02/classify-experiment/2026-07-23/VALID（203 条，经分类筛选）
**执行时间**: 2026-07-23 22:01 ~ 22:47 (46 min)
**执行引擎**: GitCode Actions API v8 · Phase 02 Harness · yyl-support (16ba2a1)

---

## 一、执行摘要

| 指标 | 数值 |
|---|---|
| 总用例数 | 202 |
| ✅ 通过 | 81 (40%) |
| ❌ 失败 | 96 (48%) |
| ⚠️ Flaky | 0 |
| ⏱️ 超时 | 10 (5%) |
| 🔧 环境错误 | 5 (2%) |
| ⏭️ 跳过/编译错误 | 10 |

---

## 二、用例全集

| 序号 | 用例 ID | 标题 | 测试维度 | 是否自动化 | 测试结果 |
|:---:|---|---|---|:---:|---|
| 1 | COMP-ARTIFACT-01-002 | upload-artifact / download-artifact 基础传递 | completeness | ✅ | ❌ 未通过 |
| 2 | COMP-ARTIFACT-01-003 | upload-artifact retention-days 指定保留期 | completeness | ✅ | ❌ 未通过 |
| 3 | COMP-CACHE-01-001 | cache hit 时恢复缓存内容正确 | completeness | ✅ | ❌ 未通过 |
| 4 | COMP-CACHE-01-002 | restore-keys 前缀匹配兜底有效 | completeness | ✅ | ❌ 未通过 |
| 5 | COMP-CALL-01-001 | 2 层 workflow_call 嵌套正常传递 | completeness | ✅ | ❌ 未通过 |
| 6 | COMP-CALL-01-002 | 被调用 workflow 故意失败时调用方收到信号 | completeness | ✅ | ✅ 通过 |
| 7 | COMP-DIR-01-001 | .gitcode/workflows/ 下仅 on:push 文件触发 | completeness | ✅ | ❌ 未通过 |
| 8 | COMP-ISOLATION-01-001 | 同 workflow 先后 job 文件系统互不干扰 | completeness | ✅ | ❌ 未通过 |
| 9 | COMP-ISOLATION-01-002 | 并发并行 job 环境变量不泄漏 | completeness | ✅ | ❌ 未通过 |
| 10 | COMP-PERMS-01-001 | permissions 空对象时 ATOMGIT_TOKEN 仅 repository read | completeness | ✅ | ❌ 未通过 |
| 11 | COMP-PERMS-01-002 | 声明 repository write 后 TOKEN 可推送代码 | completeness | ✅ | ❌ 未通过 |
| 12 | COMP-PUSH-01-001 | on: push 发起 push 时不触发其他 workflow | completeness | ✅ | ❌ 未通过 |
| 13 | COMP-PUSH-01-002 | push 提交包含的 run_id 与 echo 输出一致 | completeness | ✅ | ✅ 通过 |
| 14 | COMP-RERUN-01-001 | rerun 重新执行 workflow 结果可重复 | completeness | ✅ | ✅ 通过 |
| 15 | COMP-RERUN-01-002 | rerun 后日志仍完整可查 | completeness | ✅ | ✅ 通过 |
| 16 | COMP-RERUN-01-003 | 重复 rerun 3 次状态一致 | completeness | ✅ | ✅ 通过 |
| 17 | COMP-RUNNER-01-001 | 合法 runner label 分配成功并执行 | completeness | ✅ | ❌ 未通过 |
| 18 | COMP-SECRET-01-001 | echo secret 在日志中被遮蔽为 *** | completeness | ✅ | ❌ 未通过 |
| 19 | COMP-SECRET-01-002 | secret 通过 env 注入后仍被遮蔽 | completeness | ✅ | ✅ 通过 |
| 20 | COMP-SECRET-01-003 | workflow_dispatch input 引用 secret 被遮蔽 | completeness | ✅ | ✅ 通过 |
| 21 | COMP-STATUS-01-001 | COMPLETED 终态 run 状态字段完整 | completeness | ✅ | ❌ 未通过 |
| 22 | COMP-STATUS-01-002 | FAILED 终态 conclusion 字段正确 | completeness | ✅ | ✅ 通过 |
| 23 | COMP-SUMMARY-01-001 | run 完成后 summary 字段可查 | completeness | ✅ | ✅ 通过 |
| 24 | COMP-SUMMARY-01-002 | run summary 含 init/checkout 耗时 | completeness | ✅ | ✅ 通过 |
| 25 | COMP-TIMEOUT-01-001 | timeout-minutes=360 自动取消超时 run | completeness | ✅ | ❌ 未通过 |
| 26 | COMP-TIMEOUT-01-002 | timeout-minutes=1 及时停止超时 job | completeness | ✅ | ❌ 未通过 |
| 27 | COMP-UNKNOWN-01-002 | 未知 action 引用触发可读报错 | completeness | ✅ | ✅ 通过 |
| 28 | COMPAT-ACTION-01-001 | uses: checkout 拉取正确 ref | compatibility | ✅ | ❌ 未通过 |
| 29 | COMPAT-ACTION-01-002 | uses: checkout 拉取到正确路径 | compatibility | ✅ | ❌ 未通过 |
| 30 | COMPAT-ARTIFACT-01-001 | 跨 job artifact 共享传输正确 | compatibility | ✅ | ❌ 未通过 |
| 31 | COMPAT-ARTIFACT-01-002 | upload-artifact 默认 90 天保留期 | compatibility | ✅ | ❌ 未通过 |
| 32 | COMPAT-CACHE-01-001 | cache hit 日志出现 CACHE_HIT 标记 | compatibility | ✅ | ❌ 未通过 |
| 33 | COMPAT-CTX-01-001 | atomgit.ref 上下文正确 | compatibility | ✅ | ✅ 通过 |
| 34 | COMPAT-CTX-01-002 | atomgit.sha 上下文正确 | compatibility | ✅ | ❌ 未通过 |
| 35 | COMPAT-DIR-01-001 | .gitcode/workflows/ 下文件被正常识别 | compatibility | ✅ | ❌ 未通过 |
| 36 | COMPAT-DIR-01-002 | .github/workflows/ 下文件不被触发 | compatibility | ✅ | ❌ 未通过 |
| 37 | COMPAT-ENV-01-001 | ATOMGIT_SHA 环境变量正确 | compatibility | ✅ | ❌ 未通过 |
| 38 | COMPAT-ENV-01-002 | 非 atomgit 环境变量与 GH 行为一致 | compatibility | ✅ | ✅ 通过 |
| 39 | COMPAT-EXPR-01-001 | success() 表达式正确 | compatibility | ✅ | ✅ 通过 |
| 40 | COMPAT-EXPR-01-002 | success() 表达式依赖 job 正确触发 | compatibility | ✅ | ❌ 未通过 |
| 41 | COMPAT-EXPR-01-003 | failure() 表达式正确 | compatibility | ✅ | ❌ 未通过 |
| 42 | COMPAT-EXPR-01-004 | always() 表达式正确 | compatibility | ✅ | ✅ 通过 |
| 43 | COMPAT-EXPR-01-005 | cancelled() 表达式正确 | compatibility | ✅ | ✅ 通过 |
| 44 | COMPAT-EXPR-01-006 | contains() 函数正确 | compatibility | ✅ | ✅ 通过 |
| 45 | COMPAT-EXPR-01-007 | startsWith() 函数正确 | compatibility | ✅ | ✅ 通过 |
| 46 | COMPAT-EXPR-01-008 | endsWith() 函数正确 | compatibility | ✅ | ✅ 通过 |
| 47 | COMPAT-EXPR-01-009 | format() 函数正确 | compatibility | ✅ | ✅ 通过 |
| 48 | COMPAT-EXPR-01-010 | join() 函数正确 | compatibility | ✅ | ✅ 通过 |
| 49 | COMPAT-EXPR-01-011 | toJSON() 函数正确 | compatibility | ✅ | ✅ 通过 |
| 50 | COMPAT-EXPR-01-012 | fromJSON() 函数正确 | compatibility | ✅ | ✅ 通过 |
| 51 | COMPAT-IF-01-001 | if 条件 false 时 step 跳过 | compatibility | ✅ | ❌ 未通过 |
| 52 | COMPAT-IF-01-002 | if 条件 true 时 step 执行 | compatibility | ✅ | ❌ 未通过 |
| 53 | COMPAT-INPUTS-01-001 | workflow_dispatch inputs 字符串类型 | compatibility | ✅ | ✅ 通过 |
| 54 | COMPAT-INPUTS-01-002 | workflow_dispatch inputs 多参数传递 | compatibility | ✅ | ❌ 未通过 |
| 55 | COMPAT-ISOLATE-01-001 | 两 job 间临时目录互相隔离 | compatibility | ✅ | ✅ 通过 |
| 56 | COMPAT-ISOLATE-01-002 | job 间 process 互相不可见 | compatibility | ✅ | ✅ 通过 |
| 57 | COMPAT-MASK-01-001 | env 注入 secret 值在日志正确遮蔽 | compatibility | ✅ | ✅ 通过 |
| 58 | COMPAT-MASK-01-002 | 通过 env 注入 secret 后值应在日志中遮蔽 | compatibility | ✅ | ❌ 未通过 |
| 59 | COMPAT-OUTCOME-01-001 | step 失败后 outcome=failure | compatibility | ✅ | ❌ 未通过 |
| 60 | COMPAT-OUTCOME-01-002 | continue-on-error 下 outcome 区分 | compatibility | ✅ | ❌ 未通过 |
| 61 | COMPAT-OUTCOME-01-003 | step 成功后 outcome=success | compatibility | ✅ | ✅ 通过 |
| 62 | COMPAT-PERM-01-001 | 未声明 permissions 时默认 TOKEN 仅读权限范围 | compatibility | ✅ | ❌ 未通过 |
| 63 | COMPAT-PERM-01-004 | permissions 各项验证—GitCode repository 权限属性行为生效 | compatibility | ✅ | ❌ 未通过 |
| 64 | COMPAT-RUNNER-01-001 | runner.os 上下文正确 | compatibility | ✅ | ❌ 未通过 |
| 65 | COMPAT-RUNNER-01-002 | runner.arch 上下文正确 | compatibility | ✅ | ❌ 未通过 |
| 66 | COMPAT-RUNSON-01-001 | runs-on 三段数组格式生效 | compatibility | ✅ | ❌ 未通过 |
| 67 | COMPAT-SHELL-01-001 | bash shell 正常执行 | compatibility | ✅ | ✅ 通过 |
| 68 | COMPAT-SHELL-01-002 | python 脚本正常执行 | compatibility | ✅ | ✅ 通过 |
| 69 | COMPAT-VARS-01-001 | vars 上下文正确 | compatibility | ✅ | ❌ 未通过 |
| 70 | COMPAT-VARS-01-002 | vars 多变量正确 | compatibility | ✅ | ✅ 通过 |
| 71 | REL-API-01-065 | API 稳定性—批量操作成功率 | reliability | ✅ | ✅ 通过 |
| 72 | REL-ART-01-041 | 超大 artifact 100MB 上传/下载 | reliability | ✅ | ❌ 未通过 |
| 73 | REL-ARTCONC-01-063 | artifact 并发写入同名称 | reliability | ✅ | ❌ 未通过 |
| 74 | REL-ARTPERF-01-053 | 100MB artifact 下载成功率 | reliability | ✅ | ❌ 未通过 |
| 75 | REL-ARTPERF-01-053-V2 | 1GB artifact 上传成功率 | reliability | ✅ | ❌ 未通过 |
| 76 | REL-CACHE-01-046 | 缓存命中率统计 | reliability | ✅ | ✅ 通过 |
| 77 | REL-CACHEPERF-01-054 | 缓存大批量读写稳定性 | reliability | ✅ | ✅ 通过 |
| 78 | REL-CANCEL-01-028 | 手动取消 run 正常终止 | reliability | ✅ | ❌ 未通过 |
| 79 | REL-CANCELREL-01-061 | run 取消不影响已完成 job | reliability | ✅ | ✅ 通过 |
| 80 | REL-CONC-01-001 | 多并发 run 独立执行结论一致 | reliability | ✅ | ❌ 未通过 |
| 81 | REL-CONC-01-002 | 并发 job 间无干扰 | reliability | ✅ | ✅ 通过 |
| 82 | REL-CONTINUE-01-030 | continue-on-error 后继续执行后续 job | reliability | ✅ | ❌ 未通过 |
| 83 | REL-CPU-01-022 | CPU 密集型任务稳定完成 | reliability | ✅ | ✅ 通过 |
| 84 | REL-DISK-01-018 | 磁盘高负载任务正常完成 | reliability | ✅ | ✅ 通过 |
| 85 | REL-FAIR-01-044 | 多仓库公平调度 | reliability | ✅ | ✅ 通过 |
| 86 | REL-FAULT-01-031 | runner 被 SIGKILL 后日志完整保留 | reliability | ✅ | ❌ 未通过 |
| 87 | REL-FAULT-01-032 | 网络分区下 job 正确失败 | reliability | ✅ | ❌ 未通过 |
| 88 | REL-FAULT-01-033 | 磁盘满时 job 正确失败 | reliability | ✅ | ❌ 未通过 |
| 89 | REL-IGNORE-01-004 | paths-ignore 下匹配文件不触发 | reliability | ✅ | ❌ 未通过 |
| 90 | REL-IMAGE-01-052 | 自定义 Docker 镜像正确加载 | reliability | ✅ | ✅ 通过 |
| 91 | REL-IMAGE-01-052-V2 | 私有镜像 + credentials 正确拉取 | reliability | ✅ | ✅ 通过 |
| 92 | REL-K8S-01-045 | K8s runner 可伸缩性验证 | reliability | ✅ | ❌ 未通过 |
| 93 | REL-LATENCY-01-050 | queue 到 run start 延迟测量 | reliability | ✅ | ✅ 通过 |
| 94 | REL-LATENCY-01-050-V2 | dispatch 触发到 start 延迟 | reliability | ✅ | ✅ 通过 |
| 95 | REL-LOGPERF-01-051 | 大批量日志写入稳定性 | reliability | ✅ | ✅ 通过 |
| 96 | REL-LOGPERF-01-051-V2 | 大批量日志不丢行 | reliability | ✅ | ✅ 通过 |
| 97 | REL-LOGSTABLE-01-059 | 日志输出顺序一致 | reliability | ✅ | ✅ 通过 |
| 98 | REL-MATRIX-01-026 | matrix 4 组合正常完成 | reliability | ✅ | ✅ 通过 |
| 99 | REL-MATRIX-01-027 | matrix max-parallel=4 正确限制 | reliability | ✅ | ❌ 未通过 |
| 100 | REL-MATRIX-01-038 | 20 组合 matrix 扩展能力 | reliability | ✅ | ❌ 未通过 |
| 101 | REL-MATRIX-01-039 | 50 组合 matrix 极限 | reliability | ✅ | ❌ 未通过 |
| 102 | REL-MATRIXFAIR-01-056 | 多 matrix 作业间公平调度 | reliability | ✅ | ✅ 通过 |
| 103 | REL-MEM-01-020 | 内存密集型任务稳定完成 | reliability | ✅ | ✅ 通过 |
| 104 | REL-MEM-01-021 | 低内存任务正常完成 | reliability | ✅ | ✅ 通过 |
| 105 | REL-NEEDS-01-025 | needs 依赖传播失败信号 | reliability | ✅ | ❌ 未通过 |
| 106 | REL-NETFAULT-01-062 | 网络抖动下重试机制 | reliability | ✅ | ✅ 通过 |
| 107 | REL-OUTPUT-01-016 | ATOMGIT_OUTPUT 1MB 上限 | reliability | ✅ | ❌ 未通过 |
| 108 | REL-PRESSURE-01-055 | 压力测试 100 并发 run | reliability | ✅ | ✅ 通过 |
| 109 | REL-QUEUE-01-003 | 排队中 run 正常入队 | reliability | ✅ | ❌ 未通过 |
| 110 | REL-RERUN-01-011 | 重新运行 2 次结果一致 | reliability | ✅ | ❌ 未通过 |
| 111 | REL-RERUN-01-012 | 重新运行耗时稳定 | reliability | ✅ | ✅ 通过 |
| 112 | REL-RERUN-01-013 | 重新运行日志完整 | reliability | ✅ | ✅ 通过 |
| 113 | REL-RETAIN-01-047 | 日志保留期内可查 | reliability | ✅ | ✅ 通过 |
| 114 | REL-RUNNER-01-049 | Runner 自动恢复 | reliability | ✅ | ✅ 通过 |
| 115 | REL-SCHED-01-057 | 定时调度准确性 | reliability | ✅ | ✅ 通过 |
| 116 | REL-STATE-01-058 | run 状态一致性 | reliability | ✅ | ✅ 通过 |
| 117 | REL-TIMEOUT-01-007 | 默认 360 分钟超时有效 | reliability | ✅ | ❌ 未通过 |
| 118 | REL-TIMEOUT-01-008 | 自定义 361 分钟超时正确 | reliability | ✅ | ❌ 未通过 |
| 119 | REL-TIMEOUT-01-009 | 1 分钟超时正常生效 | reliability | ✅ | ❌ 未通过 |
| 120 | REL-TIMEOUT-01-010 | 1 小时超时精确 | reliability | ✅ | ❌ 未通过 |
| 121 | REL-YAMLCACHE-01-060 | YAML 修改后缓存失效 | reliability | ✅ | ❌ 未通过 |
| 122 | SEC-ARTF-01-002 | 跨 artifact 拉取权限 403 或 404 | security | ✅ | ❌ 未通过 |
| 123 | SEC-CACHE-01-002 | 跨分支 cache restore 防 cache miss | security | ✅ | ❌ 未通过 |
| 124 | SEC-DEFPERM-01-001 | ATOMGIT_TOKEN 默认权限范围—job 通过 shell 尝试写操作 | security | ✅ | ❌ 未通过 |
| 125 | SEC-DOS-01-001 | 大 artifact / 大 cache payload 拒绝服务边界 | security | ✅ | ❌ 未通过 |
| 126 | SEC-INJ-01-004 | 控制 commit message 内容直接插入 run 脚本防止命令注入 | security | ✅ | ❌ 未通过 |
| 127 | SEC-INJ-01-005 | 表达式求值防护—防止双重模板求值攻击 | security | ✅ | ❌ 未通过 |
| 128 | SEC-MASK-01-001 | Secret 值在运行日志中必须被自动遮蔽为 *** | security | ✅ | ❌ 未通过 |
| 129 | SEC-MASK-01-002 | Secret 值在 step summary 和错误堆栈中必须被遮蔽 | security | ✅ | ❌ 未通过 |
| 130 | SEC-MASK-01-003 | Secret 通过 env 注入后遮蔽仍有效 | security | ✅ | ✅ 通过 |
| 131 | SEC-MASK-01-004 | 多行 secret 在日志中被遮蔽 | security | ✅ | ✅ 通过 |
| 132 | SEC-MASK-01-005 | Secret 日志遮蔽不会通过引用传递值绕过 | security | ✅ | ❌ 未通过 |
| 133 | SEC-MASK-01-006 | Secret 通过 input 传递时仍被遮蔽 | security | ✅ | ✅ 通过 |
| 134 | SEC-NAME-01-001 | Secret/变量名含特殊字符时可正常创建且值正确 | security | ✅ | ❌ 未通过 |
| 135 | SEC-NAME-01-002 | 通过 printenv 可遍历获取 ATOMGIT_TOKEN/secrets 时日志中必须保护遮蔽 | security | ✅ | ❌ 未通过 |
| 136 | SEC-NET-01-001 | Runner 出网规则受控—防止 SSRF 访问内部服务 | security | ✅ | ❌ 未通过 |
| 137 | SEC-OIDC-01-001 | OIDC token 能正常获取 | security | ✅ | ✅ 通过 |
| 138 | SEC-PERM-01-003 | 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小(仅 read-only) | security | ✅ | ❌ 未通过 |
| 139 | SEC-PERM-01-004 | 缺省状态下写操作应 403 拒绝 | security | ✅ | ❌ 未通过 |
| 140 | SEC-RUN-01-001 | Job 间共享 workspace 残留文件必须被清理 | security | ✅ | ❌ 未通过 |
| 141 | SEC-RUN-01-002 | Runner 级别共享目录须防跨 job 泄漏 | security | ✅ | ❌ 未通过 |
| 142 | SEC-RUN-01-003 | 共享 Runner 跨项目残留必须被清理 | security | ✅ | ❌ 未通过 |
| 143 | SEC-SIDE-01-001 | Secret 不可通过环境变量被另一 job 读取 | security | ✅ | ✅ 通过 |
| 144 | SEC-SIDE-01-002 | Secret 随 artifact 传输仅暂存不可持久化 | security | ✅ | ❌ 未通过 |
| 145 | SEC-SUPPLY-01-001 | 第三方 Action 引用应支持使用 commit hash 固定 | security | ✅ | ❌ 未通过 |
| 146 | SEC-SUPPLY-01-002 | commit hash 不匹配时第三方 Action 应拒绝执行 | security | ✅ | ❌ 未通过 |
| 147 | SEC-TOCTOU-01-001 | 多步间上游 commit 变更应触发重新授权再执行 | security | ✅ | ❌ 未通过 |
| 148 | SEC-WCMD-01-001 | Workflow 命令（如 add-mask）运行中不应泄露在当前遮蔽的 secret 值 | security | ✅ | ❌ 未通过 |
| 149 | SEC-WCMD-01-002 | 非信任 artifact 必须被当作不可信源处理 | security | ✅ | ❌ 未通过 |
| 150 | USE-ACT-01-001 | 官方 action 体验流畅 checkout | usability | ✅ | ✅ 通过 |
| 151 | USE-ACT-01-002 | 官方 action 报错信息可读 setup-node | usability | ✅ | ✅ 通过 |
| 152 | USE-ANNOT-01-001 | 报错信息可理解—指向具体行号 | usability | ✅ | ✅ 通过 |
| 153 | USE-BADGE-01-001 | 状态徽章可正常渲染 | usability | ✅ | ✅ 通过 |
| 154 | USE-CONC-01-001 | concurrency max 非法参数应给出友好错误 | usability | ✅ | ❌ 未通过 |
| 155 | USE-CTX-01-001 | atomgit.ref 上下文值应包含 refs/heads/ 前缀 | usability | ✅ | ❌ 未通过 |
| 156 | USE-CTX-01-002 | 使用 github context 应给出迁移提示 | usability | ✅ | ❌ 未通过 |
| 157 | USE-DEPR-01-001 | 弃用字段应给出警告 | usability | ✅ | ✅ 通过 |
| 158 | USE-DEPR-01-002 | node12 运行时弃用警告 | usability | ✅ | ✅ 通过 |
| 159 | USE-DIR-01-001 | 工作流路径发现正常 | usability | ✅ | ✅ 通过 |
| 160 | USE-DISP-01-002 | workflow_dispatch inputs default 值正确生效 | usability | ✅ | ❌ 未通过 |
| 161 | USE-ENV-01-001 | 环境变量正确获取 | usability | ✅ | ✅ 通过 |
| 162 | USE-ENV-01-002 | GITHUB_SHA 不用给出映射提示 | usability | ✅ | ❌ 未通过 |
| 163 | USE-EXPR-01-001 | 非法表达式给出可读错误 | usability | ✅ | ❌ 未通过 |
| 164 | USE-INPT-01-002 | workflow_dispatch boolean input 应被拒绝 | usability | ✅ | ❌ 未通过 |
| 165 | USE-LBL-01-002 | runner 标签可理解 | usability | ✅ | ✅ 通过 |
| 166 | USE-LOG-01-001 | 日志 step 分组清晰 | usability | ✅ | ❌ 未通过 |
| 167 | USE-MASK-01-001 | secret 被遮蔽但可感知存在 | usability | ✅ | ✅ 通过 |
| 168 | USE-MASK-01-002 | 遮蔽提示信息清晰 | usability | ✅ | ✅ 通过 |
| 169 | USE-MD-01-001 | Markdown 报告可读 | usability | ✅ | ✅ 通过 |
| 170 | USE-OS-01-001 | OS 信息清晰展示 | usability | ✅ | ❌ 未通过 |
| 171 | USE-PERM-01-001 | 权限错误信息清晰 | usability | ✅ | ✅ 通过 |
| 172 | USE-RUN-01-001 | 执行摘要界面可读 | usability | ✅ | ✅ 通过 |
| 173 | USE-SEARCH-01-001 | 日志搜索功能可用 | usability | ✅ | ✅ 通过 |
| 174 | USE-SECNAME-01-001 | ATOMGIT_ 前缀 secret 名应给出提示 | usability | ✅ | ❌ 未通过 |
| 175 | USE-SECNAME-01-002 | 合法 secret 名正常创建 | usability | ✅ | ✅ 通过 |
| 176 | USE-STAT-01-001 | 状态页面信息完整 | usability | ✅ | ✅ 通过 |
| 177 | USE-UNKN-01-002 | 未知 step 类型报错可读 | usability | ✅ | ✅ 通过 |

> **数据来源**: `runs/2026-07-23-valid-clean/results/*.json`。列说明见模板。共 202 条，表仅列关键用例，完整清单见 summary.json。

---

## 三、门禁判定

**结论**: ⛔ BLOCKED

**Blocked 维度**: completeness, compatibility, security, reliability, usability

**P0 失败数**: 33 条（P0 失败即整体 BLOCKED）

---

## 四、分维度通过率

| 维度 | 总数 | 通过 | 失败 | 通过率 | P0 失败 | 门禁阈值 | 判定 |
|---|---|---|---|---|---|---|---|
| completeness | 29 | 11 | 16 | 40% | 7 | ≥95% | ⛔ |
| compatibility | 48 | 20 | 23 | 46% | 3 | ≥90% | ⛔ |
| reliability | 67 | 27 | 24 | 52% | 0 | ≥85% | ⛔ |
| security | 28 | 5 | 23 | 17% | 23 | ≥90% | ⛔ |
| usability | 30 | 18 | 10 | 64% | 0 | ≥80% | ⛔ |

---

## 五、P0 失败（Blocker）

| 用例 ID | 标题 | 维度 | 失败断言 | LLM 根因初判 |
|---|---|---|---|---|
| COMP-CACHE-01-001 | cache hit 时恢复缓存内容正确 | completeness | run_status≠success | 平台缺陷（高）— cache action FAILED |
| COMP-CACHE-01-002 | restore-keys 前缀匹配兜底有效 | completeness | status≠green | 平台缺陷（高）— cache action FAILED |
| COMP-ISOLATION-01-001 | 同 workflow 先后 job 文件系统互不干扰 | completeness | run_status≠success | 标记不匹配（高）— run=COMPLETED，断言期望词汇不匹配 |
| COMP-ISOLATION-01-002 | 并发并行 job 环境变量不泄漏 | completeness | run_status≠success | 标记不匹配（高）— 同上 |
| COMP-PERMS-01-001 | permissions 空对象时 TOKEN 仅 repository read | completeness | value=absent | 需人工判断（低）— job 未执行任何步骤 |
| COMP-PERMS-01-002 | 声明 repository write 后 TOKEN 可推送代码 | completeness | run_status≠success | 需人工判断（低）— job 未执行任何步骤 |
| COMP-SECRET-01-001 | echo secret 在日志中被遮蔽为 *** | completeness | value='***' absent | 平台缺陷（高）— GitCode 文档承诺 `***` 混淆，实测未生效 |
| COMPAT-MASK-01-002 | 通过 env 注入 secret 后值应在日志中遮蔽 | compatibility | run_status≠success | 标记不匹配（中）— run=COMPLETED 功能正常 |
| COMPAT-PERM-01-001 | 未声明 permissions 时默认 TOKEN 仅读权限范围 | compatibility | run_status≠success, value absent | 用例问题（高）— 日志证实 README 成功读取，功能正常，断言关键词不匹配 |
| COMPAT-PERM-01-004 | permissions 各项验证 | compatibility | run_status≠success | 标记不匹配（高）— 断言期望词汇不匹配 |
| SEC-ARTF-01-002 | 跨 artifact 拉取权限 403 或 404 | security | value=absent | 标记不匹配（高）— 编译器提取抽象关键词 `403_or_404`，workflow 不输出 |
| SEC-CACHE-01-002 | 跨分支 cache restore 防 cache miss | security | value=absent | 标记不匹配（中）— 合约 `equals: cache_miss` 非 workflow 输出 |
| SEC-DEFPERM-01-001 | ATOMGIT_TOKEN 默认权限范围 | security | value=absent | 标记不匹配（高）— 编译器提取抽象关键词 |
| SEC-DOS-01-001 | 大 artifact / 大 cache payload 拒绝服务边界 | security | value=absent | 标记不匹配（中）— 平台错误消息文本与提取关键词不同 |
| SEC-INJ-01-004 | 控制 commit message 内容直接插入 run 脚本 | security | run_status≠success | 用例问题（高）— 断言期望 `success` 但平台返回 `COMPLETED` |
| SEC-INJ-01-005 | 表达式求值防护—防止双重模板求值攻击 | security | leak FOUND `2`, value absent | **★日志修正** 标记不匹配假失败（高）— bash `bad substitution` 错误，`2` 为源文本 `1+1` 的子串假阳性，平台未做二次求值 |
| SEC-MASK-01-001 | Secret 值在运行日志中必须被自动遮蔽 | security | value=absent | 标记不匹配（高）— 合约提取关键词 `masked_with_asterisks`，workflow 不输出此字符串 |
| SEC-MASK-01-002 | Secret 值在 step summary 和错误堆栈中必须遮蔽 | security | status≠green | 用例问题（高）— 断言退化为 status，合约 target 不被引擎支持 |
| SEC-MASK-01-005 | Secret 日志遮蔽不会通过引用传递值绕过 | security | value=absent | 标记不匹配（高）— 同上模式 |
| SEC-NAME-01-001 | Secret/变量名含特殊字符时可正常创建 | security | run_status≠success | **★日志修正** 用例问题（中）— 含连字符的 secret 名被静默接受但值未注入，断言词汇不匹配 |
| SEC-NAME-01-002 | 通过 printenv 可遍历获取 secrets 时日志保持遮蔽 | security | value=absent | 标记不匹配（高）— 合约提取复合关键词 `masked_or_not_found` |
| SEC-NET-01-001 | Runner 出网规则受控—防止 SSRF 访问内部服务 | security | value=absent | 平台缺陷（中）— curl 成功访问 169.254.169.254 元数据端点 |
| SEC-PERM-01-003 | 未声明 permissions 时 TOKEN 默认权限最小 | security | run_status≠success | **★日志修正** 环境问题（高）— curl exit 6=DNS 不可达，非权限测试 |
| SEC-PERM-01-004 | 缺省状态下写操作应 403 拒绝 | security | value=absent | 标记不匹配（高）— 合约关键词 `push_denied_or_403` vs 实际输出 `push denied as expected` |
| SEC-RUN-01-001 | Job 间共享 workspace 残留文件必须清理 | security | value=absent | **★日志修正** 用例问题（高）— 日志含 `cleaned as expected`（空格），断言期望 `cleaned_as_expected`（下划线） |
| SEC-RUN-01-002 | Runner 级别共享目录须防跨 job 泄漏 | security | value=absent | **★日志修正** 用例问题（高）— 同模式空格vs下划线 |
| SEC-RUN-01-003 | 共享 Runner 跨项目残留必须清理 | security | run_status≠success | 环境问题（中）— self-hosted runner 不可用 |
| SEC-SIDE-01-002 | Secret 随 artifact 传输仅暂存 | security | status≠green | 用例问题（高）— 断言 `blocked_or_masked` 非有效 conclusion 值 |
| SEC-SUPPLY-01-001 | 第三方 Action 引用应支持使用 commit hash 固定 | security | status≠green | 需人工判断（中）— job 未执行任何步骤，0 字节日志 |
| SEC-SUPPLY-01-002 | commit hash 不匹配时第三方 Action 应拒绝执行 | security | value=absent | 标记不匹配（高）— 合约关键词 `action_not_found_or_sha_mismatch` |
| SEC-TOCTOU-01-001 | 多步间上游 commit 变更应触发重新授权 | security | value=absent | 标记不匹配（高）— 合约关键词 `approved_sha_matched` |
| SEC-WCMD-01-001 | Workflow 命令不应泄露当前遮蔽的 secret 值 | security | value=absent | 标记不匹配（高）— 合约关键词 `mask_command_without_payload` |
| SEC-WCMD-01-002 | 非信任 artifact 必须被当作不可信源处理 | security | run_status≠success | **★日志修正** 用例问题（高）— `download-artifact` 报 artifact 不存在，测试夹具缺失 |

---

## 八、失败详情（代表样本）

### COMP-CACHE-01-001 — cache hit 时恢复缓存内容正确

| 项目 | 值 |
|---|---|
| **判定** | FAIL |
| **维度** | completeness |
| **优先级** | P0 |
| **失败断言** | run_status: expected=success, actual=FAILED |
| **日志指纹** | fa768b34ad16 |
| **LLM 根因初判** | 平台缺陷（置信度：高） |
| **分析** | Cache action (`uses: cache`) 执行使 workflow 以 FAILED 结案。GitCode `using-dependency-cache.md` 文档化 cache 支持，但实际 cache action 不可用。 |

### COMP-SECRET-01-001 — echo secret 在日志中被遮蔽为 ***

| 项目 | 值 |
|---|---|
| **判定** | FAIL |
| **维度** | completeness |
| **优先级** | P0 |
| **失败断言** | value: expected='***' present, actual=absent |
| **日志指纹** | 41f0d65a2362 |
| **LLM 根因初判** | 平台缺陷（置信度：高） |
| **分析** | `using-secrets.md` 承诺 "Secret 值在日志中自动替换为 ***"，但 `echo ${{ secrets.DEPLOY_TOKEN }}` 输出未被执行遮蔽，config_probe 确认 secret 已配置。 |

### COMPAT-DIR-01-002 — .github/workflows/ 下文件不被触发

| 项目 | 值 |
|---|---|
| **判定** | FAIL (SECURITY_CRITICAL) |
| **维度** | compatibility |
| **优先级** | P1 |
| **失败断言** | leak: forbidden='GITHUB_DIR_WORKFLOW_RAN', actual=FOUND |
| **日志指纹** | f99fa40d85ab |
| **LLM 根因初判** | 平台缺陷（置信度：高） |
| **分析** | GitCode 文档明确 "仅 .gitcode/workflows/ 目录下文件被识别"，但实际平台也触发执行了 `.github/workflows/` 下的 workflow YAML。安全边界破坏。 |

### SEC-INJ-01-005 — ★ 日志修正：非双重模板注入

| 项目 | 值 |
|---|---|
| **判定** | FAIL (SECURITY_CRITICAL) |
| **维度** | security |
| **优先级** | P0 |
| **失败断言** | leak: forbidden='2', actual=FOUND; value: expected='template_chars_escaped', actual=absent |
| **日志指纹** | 2c9da3b8ac22 |
| **LLM 根因初判** | 标记不匹配假失败（置信度：高） |
| **分析** | **★经实际日志交叉验证**：bash 错误消息 `Input: ${{ '{{ 1 + 1 }}' }}: bad substitution`——平台正确地将 `${{}}` 原样传递给 bash 而未做二次模板求值。"2" 是错误消息中源文本 `1 + 1` 的子串假阳性。非真实安全缺陷。 |

### REL-FAULT-01-031 — ★ 日志修正：SIGKILL 从未触发

| 项目 | 值 |
|---|---|
| **判定** | FAIL (SECURITY_CRITICAL) |
| **维度** | reliability |
| **优先级** | P1 |
| **失败断言** | leak: forbidden='step_four_marker', actual=FOUND |
| **日志指纹** | 170010c4af2f |
| **LLM 根因初判** | 用例问题（置信度：高） |
| **分析** | **★经实际日志交叉验证**：全部 5 个 step (step_one~step_five_marker) 正常执行完成。SIGKILL 从未发生——故障注入机制未触发。`step_four_marker` 出现在日志中是因为 Step 4 正常执行完毕，并非日志泄漏。非平台安全缺陷。 |

### USE-CONC-01-001 — concurrency max 非法参数应给出友好错误

| 项目 | 值 |
|---|---|
| **判定** | FAIL |
| **维度** | usability |
| **优先级** | P1 |
| **失败断言** | run_status_not: expected≠success, actual=COMPLETED |
| **日志指纹** | 92c4bcd0ab3b |
| **LLM 根因初判** | 平台缺陷（置信度：高） |
| **分析** | concurrency.max=10（超出文档范围 1-5），平台静默接受并 COMPLETED 了 run——输入校验缺失。 |

> **注**：96 条 FAIL 中 P0 33 条已在上表列出，P1 63 条完整清单和逐条详情见 `runs/2026-07-23-valid-clean/results/*.json` 和 `summary.json`。

---

## 十、执行环境

| 项目 | 值 |
|---|---|
| API Base URL | `https://api.gitcode.com` |
| Runner 标签 | ubuntu-latest, x64, small |
| 并发执行数 | 5 仓 × 3 per-repo = 15 |
| 单用例超时 | 300 s |
| 环境重置级别 | batch_end teardown |
| GITCODE_COOKIE | ~/.gitcode-cookie |
| GITCODE_ACCESS_TOKEN | ~/.gitcode-token |

---

*报告由 Phase 02 report-builder 生成 · 2026-07-24*
*基线参照: `phase01/baseline/quality-gate.md`*
