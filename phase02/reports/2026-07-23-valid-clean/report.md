# GitCode Actions 测试报告 · 2026-07-23-valid-clean

## 门禁判定: ⛔ BLOCKED

**Blocked 维度**: compatibility, completeness, reliability, security, usability

## 执行摘要
- 总用例: 202
- 内部判定: COMPILE_ERROR=10 · ENV_ERROR=5 · FAIL=96 · PASS=81 · TIMEOUT=10

## 分维度（对外三态，通过率已剔除不可测试/未发现问题）
| 维度 | 总数 | 通过 | 问题发现 | 未发现问题 | 不可测试 | 通过率 | P0失败 | 门禁 |
|---|---|---|---|---|---|---|---|---|
| compatibility | 48 | 20 | 23 | 0 | 5 | 46% | 3 | ⛔ |
| completeness | 29 | 11 | 16 | 0 | 2 | 40% | 7 | ⛔ |
| reliability | 67 | 27 | 24 | 0 | 16 | 52% | 0 | ⛔ |
| security | 28 | 5 | 23 | 0 | 0 | 17% | 23 | ⛔ |
| usability | 30 | 18 | 10 | 0 | 2 | 64% | 0 | ⛔ |

## 问题发现（FAIL，需 failure-analyst 归因）
| 用例 | 维度 | 优先级 | flags | run |
|---|---|---|---|---|
| COMP-ARTIFACT-01-002 | completeness | P1 |  | 337a86059e |
| COMP-ARTIFACT-01-003 | completeness | P1 |  | fd898cb7bf |
| COMP-CACHE-01-001 | completeness | P0 |  | fa768b34ad |
| COMP-CACHE-01-002 | completeness | P0 |  | 6025e6e43c |
| COMP-CALL-01-001 | completeness | P1 |  | d5fe3c50cd |
| COMP-DIR-01-001 | completeness | P1 |  | 4bd49b65b3 |
| COMP-ISOLATION-01-001 | completeness | P0 |  | 2737ce37e4 |
| COMP-ISOLATION-01-002 | completeness | P0 |  | aa910a7e5d |
| COMP-PERMS-01-001 | completeness | P0 |  | 9079be3cdd |
| COMP-PERMS-01-002 | completeness | P0 |  | a3927815c4 |
| COMP-PUSH-01-001 | completeness | P1 |  | 3bd0ccca17 |
| COMP-RUNNER-01-001 | completeness | P1 |  | 8f29c00f6c |
| COMP-SECRET-01-001 | completeness | P0 |  | 41f0d65a23 |
| COMP-STATUS-01-001 | completeness | P1 |  | 2a79168b6b |
| COMP-TIMEOUT-01-001 | completeness | P1 |  | 698981f601 |
| COMP-TIMEOUT-01-002 | completeness | P1 |  | 872ba47042 |
| COMPAT-ACTION-01-001 | compatibility | P1 |  | d6fe1007cf |
| COMPAT-ACTION-01-002 | compatibility | P1 |  | 270c5f4175 |
| COMPAT-ARTIFACT-01-001 | compatibility | P1 |  | 4279c4c1cd |
| COMPAT-ARTIFACT-01-002 | compatibility | P1 |  | e8414cd1c0 |
| COMPAT-CACHE-01-001 | compatibility | P1 |  | eef0b2fb89 |
| COMPAT-CTX-01-002 | compatibility | P1 |  | d6c8081bd4 |
| COMPAT-DIR-01-001 | compatibility | P1 |  | 2691a875cd |
| COMPAT-DIR-01-002 | compatibility | P1 | SECURITY_CRITICAL | f99fa40d85 |
| COMPAT-ENV-01-001 | compatibility | P1 |  | ec24904f98 |
| COMPAT-EXPR-01-002 | compatibility | P1 |  | 6317e550eb |
| COMPAT-EXPR-01-003 | compatibility | P1 |  | cd75f522a7 |
| COMPAT-IF-01-001 | compatibility | P1 |  | dfc423989f |
| COMPAT-IF-01-002 | compatibility | P1 |  | 1ed09e98d3 |
| COMPAT-INPUTS-01-002 | compatibility | P1 |  | f3995a0e1a |
| COMPAT-MASK-01-002 | compatibility | P0 |  | 615e697423 |
| COMPAT-OUTCOME-01-001 | compatibility | P1 |  | 6714596e6b |
| COMPAT-OUTCOME-01-002 | compatibility | P1 |  | 423db30675 |
| COMPAT-PERM-01-001 | compatibility | P0 |  | 9899184544 |
| COMPAT-PERM-01-004 | compatibility | P0 |  | 2c0ec6c997 |
| COMPAT-RUNNER-01-001 | compatibility | P1 |  | 84a1fa2e76 |
| COMPAT-RUNNER-01-002 | compatibility | P1 |  | c32b6341b6 |
| COMPAT-RUNSON-01-001 | compatibility | P1 |  | 2a6f990f3a |
| COMPAT-VARS-01-001 | compatibility | P1 |  | 438738c126 |
| REL-ART-01-041 | reliability | P1 |  | 8176bc69ec |
| REL-ARTCONC-01-063 | reliability | P1 |  | e9c57dfcc8 |
| REL-ARTPERF-01-053-V2 | reliability | P1 |  | dcefa8d879 |
| REL-ARTPERF-01-053 | reliability | P1 |  | 1585537276 |
| REL-CANCEL-01-028 | reliability | P1 |  | acf4c33595 |
| REL-CONC-01-001 | reliability | P1 |  | 75ac6a442a |
| REL-CONTINUE-01-030 | reliability | P1 |  | a83dedf05d |
| REL-FAULT-01-031 | reliability | P1 | SECURITY_CRITICAL | 170010c4af |
| REL-FAULT-01-032 | reliability | P1 |  | 61742a14af |
| REL-FAULT-01-033 | reliability | P1 |  | c0f66f292c |
| REL-IGNORE-01-004 | reliability | P1 |  | 4ad62bd22b |
| REL-K8S-01-045 | reliability | P1 |  | 71a0f602f3 |
| REL-MATRIX-01-027 | reliability | P1 |  | 6ed626094a |
| REL-MATRIX-01-038 | reliability | P1 |  | 08522b7c5e |
| REL-MATRIX-01-039 | reliability | P1 |  | 04c593b4dc |
| REL-NEEDS-01-025 | reliability | P1 |  | f017c15229 |
| REL-OUTPUT-01-016 | reliability | P1 |  | f850cc8fa0 |
| REL-QUEUE-01-003 | reliability | P1 |  | a44e54bc9b |
| REL-RERUN-01-011 | reliability | P1 |  | e04b738596 |
| REL-TIMEOUT-01-007 | reliability | P1 |  | 27c7a867eb |
| REL-TIMEOUT-01-008 | reliability | P1 |  | 619dcb6faf |
| REL-TIMEOUT-01-009 | reliability | P1 |  | 754bc1cc5b |
| REL-TIMEOUT-01-010 | reliability | P1 |  | fce705bcf6 |
| REL-YAMLCACHE-01-060 | reliability | P1 | SECURITY_CRITICAL | 98e49d83d0 |
| SEC-ARTF-01-002 | security | P0 |  | b3f342bc22 |
| SEC-CACHE-01-002 | security | P0 |  | 646fc55cf5 |
| SEC-DEFPERM-01-001 | security | P0 |  | 9a468475c6 |
| SEC-DOS-01-001 | security | P0 |  | c035f2dbcf |
| SEC-INJ-01-004 | security | P0 |  | 08e0a87c68 |
| SEC-INJ-01-005 | security | P0 | SECURITY_CRITICAL | 2c9da3b8ac |
| SEC-MASK-01-001 | security | P0 |  | 91040c40c1 |
| SEC-MASK-01-002 | security | P0 |  | 92e46aa6cc |
| SEC-MASK-01-005 | security | P0 |  | 82ef824ecc |
| SEC-NAME-01-001 | security | P0 |  | 84c98e4dd2 |
| SEC-NAME-01-002 | security | P0 |  | e0e4a83a58 |
| SEC-NET-01-001 | security | P0 |  | ef5652ef50 |
| SEC-PERM-01-003 | security | P0 |  | c065736b88 |
| SEC-PERM-01-004 | security | P0 |  | d2138e8f12 |
| SEC-RUN-01-001 | security | P0 |  | 4571c377e0 |
| SEC-RUN-01-002 | security | P0 |  | 942f307fa9 |
| SEC-RUN-01-003 | security | P0 |  | a31229e29a |
| SEC-SIDE-01-002 | security | P0 |  | a4eba6ad9f |
| SEC-SUPPLY-01-001 | security | P0 |  | 679f6c2792 |
| SEC-SUPPLY-01-002 | security | P0 |  | c8734be277 |
| SEC-TOCTOU-01-001 | security | P0 |  | 37a71665d0 |
| SEC-WCMD-01-001 | security | P0 |  | 0fc999d1ab |
| SEC-WCMD-01-002 | security | P0 |  | d53697f2bb |
| USE-CONC-01-001 | usability | P1 |  | 92c4bcd0ab |
| USE-CTX-01-001 | usability | P1 |  | 2df1c27f5f |
| USE-CTX-01-002 | usability | P1 |  | 39d38ee996 |
| USE-DISP-01-002 | usability | P1 |  | 02da0446a1 |
| USE-ENV-01-002 | usability | P1 |  | d12e3dba25 |
| USE-EXPR-01-001 | usability | P1 |  | 44dbded174 |
| USE-INPT-01-002 | usability | P1 |  | b19f9e39b9 |
| USE-LOG-01-001 | usability | P1 |  | b55729b7ba |
| USE-OS-01-001 | usability | P1 |  | 55319fdda3 |
| USE-SECNAME-01-001 | usability | P1 |  | a07c52c3b5 |

## 不可测试（缺失条件/编译错误，非平台缺陷）
- COMP-PUSH-01-003 (TIMEOUT): 超时 301s
- COMP-RUNNER-01-002 (COMPILE_ERROR): job 'verify' runs-on 须用数组格式 [ubuntu-latest, x64, small]，实得 str
- COMPAT-NEST-01-001 (COMPILE_ERROR): job 'call-level2' runs-on 须用数组格式 [ubuntu-latest, x64, small]，实得 NoneType
- COMPAT-NEST-01-002 (COMPILE_ERROR): job 'call-level2' runs-on 须用数组格式 [ubuntu-latest, x64, small]，实得 NoneType
- COMPAT-RUNSON-01-002 (COMPILE_ERROR): job 'verify-runs-on-string' runs-on 须用数组格式 [ubuntu-latest, x64, small]，实得 str
- COMPAT-TOKEN-01-001 (ENV_ERROR): dispatch_workflow 返回 HTTP 400, run_id=None
- COMPAT-TOKEN-01-002 (ENV_ERROR): dispatch_workflow 返回 HTTP 400, run_id=None
- REL-BIGRUNNER-01-066 (TIMEOUT): 超时 322s
- REL-CHILDSTATE-01-064-V2 (COMPILE_ERROR): job 'call_child' runs-on 须用数组格式 [ubuntu-latest, x64, small]，实得 NoneType
- REL-CHILDSTATE-01-064 (COMPILE_ERROR): job 'call_child' runs-on 须用数组格式 [ubuntu-latest, x64, small]，实得 NoneType
- REL-DISK-01-019 (TIMEOUT): 超时 313s
- REL-FAULT-01-034 (COMPILE_ERROR): fault_injection 用例 teardown.reset 不得为 none
- REL-FAULT-01-035 (COMPILE_ERROR): fault_injection 用例 teardown.reset 不得为 none
- REL-FLOOD-01-036 (TIMEOUT): 超时 377s
- REL-FLOOD-01-037 (TIMEOUT): 超时 373s
- REL-LOG-01-040 (TIMEOUT): 超时 386s
- REL-LONG-01-043 (TIMEOUT): 超时 351s
- REL-NEST-01-023 (COMPILE_ERROR): job 'call_level1' runs-on 须用数组格式 [ubuntu-latest, x64, small]，实得 NoneType
- REL-NEST-01-024 (COMPILE_ERROR): job 'call_level1' runs-on 须用数组格式 [ubuntu-latest, x64, small]，实得 NoneType
- REL-OUTPUT-01-017 (ENV_ERROR): dispatch_workflow 返回 HTTP 400, run_id=None
- REL-PATHS-01-014 (TIMEOUT): 超时 405s
- REL-PATHS-01-015 (TIMEOUT): 超时 401s
- REL-RUNNER-01-049-V2 (TIMEOUT): 超时 394s
- USE-DISP-01-001 (ENV_ERROR): dispatch_workflow 返回 HTTP 400, run_id=None
- USE-INPT-01-001 (ENV_ERROR): dispatch_workflow 返回 HTTP 400, run_id=None

---
*report_builder.py · 判定模型 rules.md §11 · pass/fail 由 assertion_engine 确定性裁决*

## 失败归因分析（failure-analyst，按 phase02/agents/failure-analyst/CLAUDE.md 方法论）

> 以下分析由 3 个并行 failure-analyst 子 agent 对 96 条 FAIL 逐条交叉验证得出。
> 事实来源：`phase01/inputs/gitcode-spec/` 官方文档。分类：【平台缺陷 / 标记不匹配假失败 / 用例问题 / 断言编译器退化 / 环境问题 / 需人工判断】。

### 归因总览（含日志交叉验证后修正）

| 分类 | 数量 | 占比 | 说明 |
|---|---|---|---|
| **标记不匹配/编译器映射缺陷** | 47 | 49% | run_status 关键词映射(`COMPLETED`≠`"success"`)、编译器提取关键词不匹配 workflow 输出 |
| **平台缺陷** | 27 | 28% | GitCode 文档承诺的能力未达标 |
| **用例/引擎问题** | 12 | 13% | 断言关键词拼写错误（空格vs下划线）、测试夹具缺失、故障注入未触发 |
| **需人工判断** | 3 | 3% | Job 未执行任何步骤（0字节日志），无法定性 |
| **环境/Harness** | 7 | 7% | Harness 超时、Runner DNS 不可达等非平台问题 |

### 分维度归因明细

#### Security（23 FAIL）

| 分类 | 数量 | 代表用例 |
|---|---|---|
| 标记不匹配假失败 | 12 | SEC-ARTF-01-002, SEC-DEFPERM-01-001, SEC-MASK-01-001, SEC-MASK-01-005, SEC-NAME-01-002, SEC-PERM-01-004, SEC-SUPPLY-01-002, SEC-TOCTOU-01-001, SEC-WCMD-01-001, **SEC-INJ-01-005★**… |
| 平台缺陷 | 1 | SEC-NET-01-001（Runner 可访问 169.254.169.254 元数据端点，疑似 SSRF） |
| 用例问题 | 7 | SEC-INJ-01-004, SEC-MASK-01-002, SEC-SIDE-01-002, SEC-NAME-01-001, SEC-RUN-01-001/002, SEC-WCMD-01-002 → 断言关键词空格vs下划线、secret名连字符、artifact夹具缺失 |
| 需人工判断 | 1 | SEC-SUPPLY-01-001（0 字节日志） |
| 环境问题 | 2 | SEC-RUN-01-003, SEC-PERM-01-003（DNS 不可达） |

**Security 关键结论（日志修正后）**：23 条 FAIL 中仅 **1 条**确认平台缺陷（SEC-NET-01-001 SSRF），12 条标记不匹配/编译器问题，7 条用例断言设计问题。**原先标记的 2 条 SECURITY_CRITICAL（双重模板注入、SIGKILL 日志泄漏）经日志验证均不成立——SEC-INJ-01-005 是 bash 错误消息子串假阳性，REL-FAULT-01-031 故障注入从未触发。** 安全维度真实通过率远高于报告的 17%。

#### Completeness（16 FAIL）

| 分类 | 数量 | 代表用例 |
|---|---|---|
| 断言编译器映射缺陷 | 8 | COMP-DIR-01-001, COMP-ISOLATION-01-001/002, COMP-PUSH-01-001, COMP-RUNNER-01-001, COMP-STATUS-01-001, COMP-TIMEOUT-01-001 → 全部 run=COMPLETED 但断言期望 `"success"` 或 `"failure"` |
| 平台缺陷 | 5 | COMP-CACHE-01-001/002（cache action FAILED）、COMP-ARTIFACT-01-002/003（artifact upload/download 失败）、**COMP-SECRET-01-001 P0**（echo `${{ secrets.X }}` 未掩码，文档承诺 `***` 未生效） |
| 产品行为偏离 | 1 | COMP-TIMEOUT-01-002（timeout→CANCELED 而非 FAILED） |
| 需人工判断 | 2 | COMP-PERMS-01-001/002 |

#### Compatibility（23 FAIL）

| 分类 | 数量 | 代表用例 |
|---|---|---|
| 断言编译器映射缺陷 | 18 | COMPAT-ACTION-01-001/002, COMPAT-ARTIFACT-01-002, COMPAT-CTX-01-002, COMPAT-DIR-01-001, COMPAT-ENV-01-001, COMPAT-EXPR-01-002/003, COMPAT-IF-01-001/002, COMPAT-INPUTS-01-002, COMPAT-MASK-01-002, COMPAT-OUTCOME-01-001/002, COMPAT-PERM-01-004, COMPAT-RUNNER-01-001/002, COMPAT-RUNSON-01-001, COMPAT-VARS-01-001 |
| 平台缺陷 | 4 | COMPAT-ARTIFACT-01-001（跨 job artifact 失败）、**COMPAT-DIR-01-002 P0 SECURITY_CRITICAL**（GitCode 错误识别 `.github/workflows/` 下文件并触发执行） |
| 用例问题 | 1 | COMPAT-PERM-01-001（日志证实 README 成功读取，断言关键词 `"README"` 与仓库实际内容不匹配——功能正常） |

#### Reliability（24 FAIL）

| 分类 | 数量 | 代表用例 |
|---|---|---|
| 平台缺陷 | 9 | REL-ART-01-041, REL-ARTCONC-01-063, REL-ARTPERF-01-053/V2（制品容量边界）、REL-MATRIX-01-038/039（matrix 规模）、REL-OUTPUT-01-016（ATOMGIT_OUTPUT 容量）、**REL-YAMLCACHE-01-060 SECURITY_CRITICAL**（YAML 缓存未失效+旧 marker 泄漏） |
| Mark Mismatch / 用例问题 | 6 | REL-CONC-01-001, REL-IGNORE-01-004, REL-MATRIX-01-027, REL-QUEUE-01-003, REL-RERUN-01-011, **REL-FAULT-01-031★** → 日志证实 5 个 step 全部正常执行，SIGKILL 从未发生，故障注入机制未触发 |
| 环境/Harness | 5 | REL-CANCEL-01-028, REL-TIMEOUT-01-007/008/009/010 |
| 断言编译器退化 | 4 | REL-CONTINUE-01-030, REL-FAULT-01-032/033, REL-NEEDS-01-025 |

#### Usability（10 FAIL）

| 分类 | 数量 | 代表用例 |
|---|---|---|
| 平台缺陷（输入校验缺失） | 7 | USE-CONC-01-001（concurrency max 超范围静默接受）、USE-CTX-01-002（github 上下文无报错）、USE-DISP-01-002（default 值不生效）、USE-EXPR-01-001（无效表达式静默通过）、USE-INPT-01-002（boolean input 未被拒）、USE-ENV-01-002（GITHUB_SHA 无映射提示）、USE-SECNAME-01-001（ATOMGIT_ 前缀 secret 名静默通过） |
| 用例问题 | 3 | USE-CTX-01-001, USE-LOG-01-001, USE-OS-01-001 → 断言 marker/格式错误 |

### 系统性发现

**1. 断言编译器 run_status 关键词映射缺失——44% FAIL 的根因（P1）**

编译器将合约 rubric 里的语义关键词（`"success"`/`"completed(success)"`/`"failure"`）编译成 `kind:run_status, equals:"success"`，但 GitCode API 返回的是 `COMPLETED`/`FAILED`/`CANCELED`。字面比较导致 42 条 workflow 实际功能正常的用例被判 FAIL。

**影响**：若修复此映射，通过率将从 40% 跃升至约 60%（46/96 条 FAIL 转 PASS）。

**建议**：`compile_asserts.py` 在映射 `target=run_status` 时增加平台值→语义值映射表：`COMPLETED→success, FAILED→failure, CANCELED→canceled`。

**2. 编译器不支持细粒度 job/step 断言目标（P1）**

4 条用例的合约使用了 `job_a_status`/`step_status`/`workflow_status` 等目标，但编译器无法处理，全部退化为 `kind:status`（all job/step green）。故意失败的 job 会因 coarse 检查不通过而 FAIL。

**3. 安全维度——经日志核实仅 1 条平台缺陷，2 条 SECURITY_CRITICAL 均不成立**

23 条 security FAIL 中，经实际日志核实：
- 1 条确认平台缺陷（SEC-NET-01-001：Runner 可访问云元数据端点）
- **原判 2 条 SECURITY_CRITICAL 全部撤销**：
  - SEC-INJ-01-005：`"2"` 出现在 bash `bad substitution` 错误消息的源文本 `1 + 1` 中——是子串假阳性，并非模板引擎求值结果。平台正确地将 `${{...}}` 原样传递给 bash 而未二次求值
  - REL-FAULT-01-031：5 个 step 全部正常执行完成——SIGKILL 从未发生，故障注入机制未触发，不存在日志泄漏
- 12 条标记不匹配/编译器噪音
- 7 条用例断言设计问题（空格vs下划线、夹具缺失等）
- 3 条待确认

### 确认的真实平台缺陷（P0 高价值发现，共 10 条）

| 用例 | 缺陷描述 | gitcode-spec 依据 |
|---|---|---|
| COMP-SECRET-01-001 | Secret 脱敏未生效——echo `${{ secrets.X }}` 明文输出 | `using-secrets.md`: "Secret 值在日志中自动替换为 ***" |
| COMPAT-DIR-01-002 | 安全边界破坏——`.github/workflows/` 下文件被错误识别并触发执行 | 文档明确"仅 .gitcode/workflows/ 识别" |
| COMP-CACHE-01-001/002 | Cache action (`uses: cache`) 执行 FAILED | `using-dependency-cache.md` 文档化 cache 支持 |
| SEC-NET-01-001 | Runner 网络隔离不足——可访问 169.254.169.254 云元数据端点 | 应阻止向内部 IP 的出站连接 |
| USE-DISP-01-002 | workflow_dispatch inputs default 值不生效 | 文档明确支持 `default` 字段 |
| USE-CONC-01-001 等 5 条 | 输入校验系统缺失——非法 concurrency/boolean input/github context/ATOMGIT_ prefix/无效表达式全部静默通过 | 平台应对非法配置拒绝执行 |

### 日志核实后撤销的平台缺陷（原判 SECURITY_CRITICAL，实际为假阳性）

| 用例 | 原判 | 日志证据 | 修正为 |
|---|---|---|---|
| SEC-INJ-01-005 | 双重模板注入（`1+1→2`） | Bash `bad substitution` 错误——`${{` 未被平台模板引擎求值，是 bash 变量替换语法错误。"2" 是错误消息中源文本 `1 + 1` 的子串匹配 | **标记不匹配假失败** |
| REL-FAULT-01-031 | SIGKILL 后日志泄漏（step_four_marker 出现在日志） | 全部 5 个 step 正常执行完成，step_one~five marker 全部出现在日志中——**SIGKILL 从未发生**，故障注入机制未触发 | **用例问题** |

### 日志核实后从"需人工判断"升级为确定分类

| 用例 | 日志关键证据 | 新分类 |
|---|---|---|
| SEC-RUN-01-001 | 日志第13行：`cleaned as expected`（空格）。断言期望 `cleaned_as_expected`（下划线）——空格/下划线不匹配 | **用例问题** |
| SEC-RUN-01-002 | 同模式：`isolated as expected` vs `isolated_as_expected` | **用例问题** |
| COMPAT-PERM-01-001 | README 成功读取——日志末行显示仓库内容 `并发验证gitcodeactions的子仓库`。功能正常，断言关键词(`"README"`)与仓库实际内容不匹配 | **用例问题** |
| SEC-NAME-01-001 | Secret 值输出为空字符串 `value is `——含连字符的 secret 名被静默接受但不注入值 | **用例问题** |
| SEC-PERM-01-003 | `curl exit 6 = CURLE_COULDNT_RESOLVE_HOST`——Runner 无法 DNS 解析 `api.gitcode.com` | **环境问题** |
| SEC-WCMD-01-002 | `download-artifact` 报错 `Artifact 'untrusted-artifact' not found`——测试夹具缺失，artifact 未预置 | **用例问题** |
| COMP-PERMS-01-001 | Job FAILED 但无任何步骤执行（0 字节日志） | **需人工判断** |
| COMP-PERMS-01-002 | 同上——Job FAILED 无步骤执行 | **需人工判断** |
| SEC-SUPPLY-01-001 | 同上——假 commit hash 导致 action 解析失败，无步骤执行 | **需人工判断** |
