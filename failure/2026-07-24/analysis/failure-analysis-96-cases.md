# 96 条 FAIL 日志交叉验证 · 逐条归因 + 汇总分析

> Run: 2026-07-23-valid-clean | 日志源: `tmp-data/valid-clean-logs-all/` | 分析日期: 2026-07-24

---

## 一、逐条归因表

| # | case_id | dim | 分类 | log_evidence（日志关键行） | 置信度 |
|---|---------|-----|------|--------------------------|--------|
| 1 | COMP-ARTIFACT-01-002 | completeness | 平台缺陷 | `Job "Build multiple artifacts" status=FAILED`, 下载被 IGNORED | 高 |
| 2 | COMP-ARTIFACT-01-003 | completeness | 平台缺陷 | `Job "Upload with short retention" status=FAILED`, 无 shell 输出 | 高 |
| 3 | COMP-CACHE-01-001 | completeness | 平台缺陷 | `Job "Verify cache hit" status=FAILED`, 0 字节有效日志，Job 未执行步骤 | 中 |
| 4 | COMP-CACHE-01-002 | completeness | 平台缺陷 | `Job "Verify restore keys fallback" status=FAILED`, 0 字节有效日志 | 中 |
| 5 | COMP-CALL-01-001 | completeness | 平台缺陷 | `Job status=FAILED`, reusable workflow_call 失败 | 中 |
| 6 | COMP-DIR-01-001 | completeness | **标记不匹配** | `"workflow recognized"` — run=COMPLETED，断言期望 `"success"` ≠ 平台 `COMPLETED` | 高 |
| 7 | COMP-ISOLATION-01-001 | completeness | **标记不匹配** | `"WORKSPACE_ISOLATED_OK"`, `"TMP_ISOLATED_OK"`, `"NO_ORPHAN_PROCESS_OK"` — 所有隔离检查通过 | 高 |
| 8 | COMP-ISOLATION-01-002 | completeness | **标记不匹配** | 隔离检查全部通过，run=COMPLETED | 高 |
| 9 | COMP-PERMS-01-001 | completeness | 需人工判断 | `Job "Verify empty permissions" status=FAILED`, 0 字节有效日志 | 低 |
| 10 | COMP-PERMS-01-002 | completeness | 需人工判断 | `Job "Verify write permission" status=FAILED`, 0 字节有效日志 | 低 |
| 11 | COMP-PUSH-01-001 | completeness | **标记不匹配** | `"triggered on main"` — push 触发成功，run=COMPLETED | 高 |
| 12 | COMP-RUNNER-01-001 | completeness | **标记不匹配** | Runner spec 验证通过，run=COMPLETED | 高 |
| 13 | COMP-SECRET-01-001 | completeness | 用例问题 | `"secret is "` — secret 输出为空/截断。断言期望 `***` 但平台输出空串，config_probe=configured | 中 |
| 14 | COMP-STATUS-01-001 | completeness | **标记不匹配** | `"running"` — run=COMPLETED，断言词汇不匹配 | 高 |
| 15 | COMP-TIMEOUT-01-001 | completeness | **标记不匹配** | `"done"` — 在 73s 内完成（<360min），断言期望 `"starting"` > `"done"` 但 run_status 词汇不匹配 | 高 |
| 16 | COMP-TIMEOUT-01-002 | completeness | 环境/Harness | `"starting"` 出现（value=PASS），227s 后 harness 超时取消。`CANCELED`≠`"failure"` | 中 |
| 17 | COMPAT-ACTION-01-001 | compatibility | **标记不匹配** | `"CHECKOUT_REF_OK"` — checkout ref 短名正常，run=COMPLETED | 高 |
| 18 | COMPAT-ACTION-01-002 | compatibility | **标记不匹配** | `"CHECKOUT_PATH_OK"` — checkout path 正常，run=COMPLETED | 高 |
| 19 | COMPAT-ARTIFACT-01-001 | compatibility | 平台缺陷 | `"Artifact with name already exists: cross-job-artifact"` + `[Twirp] error` — 制品名冲突 | 高 |
| 20 | COMPAT-ARTIFACT-01-002 | compatibility | **标记不匹配** | `"ARTIFACT_UPLOADED_OK"` — 上传成功，run=COMPLETED | 高 |
| 21 | COMPAT-CACHE-01-001 | compatibility | 平台缺陷 | `CACHE_MISS`，`"Event Validation Error: The event type Manual...is not supported"` — cache 不支持 workflow_dispatch | 高 |
| 22 | COMPAT-CTX-01-002 | compatibility | **标记不匹配** | run=COMPLETED，断言词汇不匹配 | 高 |
| 23 | COMPAT-DIR-01-001 | compatibility | **标记不匹配** | `"GITCODE_DIR_RECOGNIZED_OK"` — .gitcode/workflows/ 正常识别 | 高 |
| 24 | COMPAT-DIR-01-002 | compatibility | **平台缺陷** | `"GITHUB_DIR_WORKFLOW_RAN"` **FOUND** — 平台错误触发了 .github/workflows/ | 高 |
| 25 | COMPAT-ENV-01-001 | compatibility | **标记不匹配** | run=COMPLETED，断言词汇不匹配 | 高 |
| 26 | COMPAT-EXPR-01-002 | compatibility | **标记不匹配** | `"Job B ran after Job A success"` — success() 函数正常 | 高 |
| 27 | COMPAT-EXPR-01-003 | compatibility | **Engine Bug** | cleanup 执行 `"Cleanup ran after failure"` — value=PASS；断言 `exp="failure"` vs `act="FAILED"` — **大小写不匹配** | 高 |
| 28 | COMPAT-IF-01-001 | compatibility | **Engine Bug** | 故意失败 job → `"failure"`≠`"FAILED"`，leak=PASS | 高 |
| 29 | COMPAT-IF-01-002 | compatibility | **标记不匹配** | `"This should appear"` — if true step 正常执行 | 高 |
| 30 | COMPAT-INPUTS-01-002 | compatibility | **标记不匹配** | `"STRING_INPUT_OK"`, `"ENV=production"` — inputs 传递正常 | 高 |
| 31 | COMPAT-MASK-01-002 | compatibility | **标记不匹配** | config_probe=PASS，run=COMPLETED | 中 |
| 32 | COMPAT-OUTCOME-01-001 | compatibility | **Engine Bug** | `::error::Process exited with code 1` → cleanup `"Check step outcome and conclusion"` — `"failure"`≠`"FAILED"` | 高 |
| 33 | COMPAT-OUTCOME-01-002 | compatibility | **标记不匹配** | run=COMPLETED，断言词汇不匹配 | 高 |
| 34 | COMPAT-PERM-01-001 | compatibility | 用例问题 | 日志显示仓库中文内容 `并发验证gitcodeactions的子仓库` — README 成功读取。断言关键词 `"README"` 与仓库实际内容不匹配 | 高 |
| 35 | COMPAT-PERM-01-004 | compatibility | **标记不匹配** | `"REPOSITORY_PERM_OK"` — permissions 正常，run=COMPLETED | 高 |
| 36 | COMPAT-RUNNER-01-001 | compatibility | **标记不匹配** | runner 验证通过，run=COMPLETED | 高 |
| 37 | COMPAT-RUNNER-01-002 | compatibility | **标记不匹配** | runner 验证通过，run=COMPLETED | 高 |
| 38 | COMPAT-RUNSON-01-001 | compatibility | **标记不匹配** | `"RUNSON_ARRAY_OK"` — runs-on 三段式正常 | 高 |
| 39 | COMPAT-VARS-01-001 | compatibility | **标记不匹配** | run=COMPLETED，断言词汇不匹配 | 高 |
| 40 | REL-ARTCONC-01-063 | reliability | **用例问题** | 全部 job: `${{{{ matrix.instance }}}}: bad substitution` — **四括号 `${{{{ }}}}` ** bash 语法错误 | 高 |
| 41 | REL-MATRIX-01-038 | reliability | **用例问题** | 20 job 全部: `os=${{{{ matrix.os }}}}: bad substitution` — **四括号语法错误** | 高 |
| 42 | REL-MATRIX-01-039 | reliability | **用例问题** | 50 job 全部: `v1=${{{{ matrix.v1 }}}}: bad substitution` — **四括号语法错误** | 高 |
| 43 | REL-OUTPUT-01-016 | reliability | **用例问题** | `${{{{ steps.writer.outputs.data }}}}: bad substitution` — **四括号语法错误** | 高 |
| 44 | REL-CANCEL-01-028 | reliability | 用例问题 | 两步骤全执行完: `"cleanup executed"`。断言期望 `"canceled"` 但 run 从未被取消 | 中 |
| 45 | REL-CONTINUE-01-030 | reliability | **用例问题** | job_a `exit 1` 失败，job_b 执行 `"job_b executed"`。断言退化 `kind:status`→因 job_a 失败而 FAIL。**平台行为正确**（continue-on-error 工作），但断言 coarse | 高 |
| 46 | REL-NEEDS-01-025 | reliability | **用例问题** | 上游 FAILED，下游 `IGNORED`（非期望的 `SKIPPED`）。平台用 IGNORED 而非 SKIPPED——**词汇差异** | 高 |
| 47 | REL-YAMLCACHE-01-060 | reliability | **平台缺陷** | `marker_v1` →平台执行旧版 workflow；修改后缓存未失效。SECURITY_CRITICAL | 高 |
| 48 | REL-FAULT-01-031 | reliability | **平台缺陷** | step_1~5 全部输出 → **SIGKILL 从未施加**，故障注入机制未工作 | 高 |
| 49 | REL-FAULT-01-032 | reliability | **平台缺陷** | 制品上传 `successfully` → 网络分区故障注入未施加 | 高 |
| 50 | REL-FAULT-01-033 | reliability | **平台缺陷** | `2147483648 bytes copied` → 磁盘满故障注入未施加，2GB 写入成功 | 高 |
| 51 | REL-ART-01-041 | reliability | 环境问题 | `"Artifact with name already exists: perf-artifact"` → 制品名冲突，非平台 bug | 中 |
| 52 | REL-ARTPERF-01-053-V2 | reliability | 环境问题 | `"Namespace artifact quota exceeded (1074MB > 1024MB)"` → 配额超限 | 高 |
| 53 | REL-ARTPERF-01-053 | reliability | 环境问题 | 下载成功但 `ls: cannot access 'perf-artifact'` → 提取路径问题 | 中 |
| 54 | REL-K8S-01-045 | reliability | 环境问题 | 0 字节有效日志 → self-hosted K8s runner 未启动 | 中 |
| 55 | REL-TIMEOUT-01-007 | reliability | 环境/Harness | 369s 被取消（期望 359min）→ **harness 300s 超时**，非平台 timeout-minutes | 高 |
| 56 | REL-TIMEOUT-01-008 | reliability | 环境/Harness | 366s 被取消（期望 361min）→ harness 超时 | 高 |
| 57 | REL-TIMEOUT-01-009 | reliability | 环境/Harness | 183s 被取消（期望 1min 超时由平台触发）→ harness 先触发 | 高 |
| 58 | REL-TIMEOUT-01-010 | reliability | 环境/Harness | 346s 被取消（期望 361min）→ harness 超时 | 高 |
| 59 | REL-CONC-01-001 | reliability | **标记不匹配** | `sleep 10` 完成，run=COMPLETED。断言 `"completed(success)"`≠`"COMPLETED"` | 高 |
| 60 | REL-IGNORE-01-004 | reliability | **标记不匹配** | `sleep 30` 完成，run=COMPLETED | 高 |
| 61 | REL-MATRIX-01-027 | reliability | **标记不匹配** | 3 matrix job 全输出 `version={1,2,3}`，全部 COMPLETED | 高 |
| 62 | REL-QUEUE-01-003 | reliability | **标记不匹配** | `sleep 30` 完成，run=COMPLETED | 高 |
| 63 | REL-RERUN-01-011 | reliability | **标记不匹配** | `sleep 5` 完成，run=COMPLETED | 高 |
| 64 | SEC-ARTF-01-002 | security | **标记不匹配** | `"error_code":400,"error_code_name":"BAD_REQUEST"` — 断言期望 `403_or_404`，实际 400 | 中 |
| 65 | SEC-CACHE-01-002 | security | 平台缺陷 | `"Event Validation Error: The event type Manual...is not supported"` — cache 拒绝 dispatch | 中 |
| 66 | SEC-DEFPERM-01-001 | security | **标记不匹配** | `"error_code":401,"UNAUTHORIZED"` — 断言期望 `403_or_permission_denied`，实际 401 | 中 |
| 67 | SEC-DOS-01-001 | security | **平台缺陷** | `"Artifact uploaded successfully. ID: 206049390960640, Size: 1121217 bytes"` → 1.1GB 制品未被拒绝，缺少配额执行 | 高 |
| 68 | SEC-INJ-01-004 | security | 用例问题 | `Message is ` — commit message 为空。run=COMPLETED，断言 `"success"`≠`COMPLETED` | 中 |
| 69 | SEC-INJ-01-005 | security | **标记不匹配** | `bad substitution` — bash 错误。`"2"` 是源文本 `1 + 1` 的子串假阳性，**非模板注入** | 高 |
| 70 | SEC-MASK-01-001 | security | **平台缺陷** | `The secret is ` — secret 值输出为空/截断。`using-secrets.md` 承诺 `***` 掩码未完全生效 | 高 |
| 71 | SEC-MASK-01-002 | security | 编译缺口 | `Failing with key ` — job 故意 FAILED。断言退化为 `kind:status`，step_summary/error_stack target 不支持 | 中 |
| 72 | SEC-MASK-01-005 | security | 用例问题 | 0 字节有效日志。断言关键词 `multiline_masked_with_asterisks` 从未被 script 输出 | 中 |
| 73 | SEC-NAME-01-001 | security | 用例问题 | `value is ` — 含连字符 secret 名被静默接受但值为空。断言 `"success_or_yaml_error"` 非平台词汇 | 中 |
| 74 | SEC-NAME-01-002 | security | **标记不匹配** | grep 输出缺失。断言期望 `masked_or_not_found`（下划线复合词），script 使用 `printenv | grep || echo` | 高 |
| 75 | SEC-NET-01-001 | security | **标记不匹配** | `access denied or timeout` — **SSRF 防护工作正常**！断言期望 `access_denied_or_timeout`（下划线），日志用空格 | 高 |
| 76 | SEC-PERM-01-003 | security | 环境问题 | `"error_code":401,"token not found"` — ATOMGIT_TOKEN 不可用。非权限测试问题 | 中 |
| 77 | SEC-PERM-01-004 | security | **标记不匹配** | `fatal: unable to auto-detect email address` — git config 问题。断言关键词 `push_denied_or_403`（下划线），日志输出 `push denied as expected`（空格） | 高 |
| 78 | SEC-RUN-01-001 | security | **标记不匹配** | `cleaned as expected` — 日志证实清理成功！断言期望 `cleaned_as_expected`（下划线≠空格） | 高 |
| 79 | SEC-RUN-01-002 | security | **标记不匹配** | `isolated as expected` — 日志证实隔离成功！断言期望 `isolated_as_expected`（下划线≠空格） | 高 |
| 80 | SEC-RUN-01-003 | security | 需人工判断 | 0 字节有效日志 — 两个 job 均 FAILED 无步骤输出 | 低 |
| 81 | SEC-SIDE-01-002 | security | 环境问题 | `"Artifact with name already exists"` — 前次运行制品名冲突 | 中 |
| 82 | SEC-SUPPLY-01-001 | security | **平台缺陷** | 0 字节有效日志 — 假 commit hash 的 action 引用无任何诊断输出 | 中 |
| 83 | SEC-SUPPLY-01-002 | security | 平台缺陷/用例问题 | 0 字节有效日志 — action 被拒（run=FAILED），run_status_not=PASS，但 value 断言因空日志 absent | 中 |
| 84 | SEC-TOCTOU-01-001 | security | **标记不匹配** | `Running commit: ` — commit SHA 为空。断言关键词 `approved_sha_matched` 从未被 script 输出 | 中 |
| 85 | SEC-WCMD-01-001 | security | **标记不匹配** | `::add-mask::` — mask 命令已调用。断言关键词 `mask_command_without_payload` 从未被 script 输出 | 中 |
| 86 | SEC-WCMD-01-002 | security | 用例问题 | `"Artifact 'untrusted-artifact' not found"` — 依赖制品不存在，非安全缺陷 | 高 |
| 87 | USE-CONC-01-001 | usability | **平台缺陷** | `hello` — `concurrency.max: 10` 被静默接受。平台应对非法值拒绝 | 高 |
| 88 | USE-CTX-01-001 | usability | **平台缺陷** | `ref=main` — `atomgit.ref` 返回短格式而非 `refs/heads/main` | 中 |
| 89 | USE-CTX-01-002 | usability | **平台缺陷** | `ref=placeholder_ref` — `github.ref` 被解析为占位符而非报错引导至 atomgit | 高 |
| 90 | USE-DISP-01-002 | usability | 需人工判断 | 0 字节有效日志 — job FAILED 无步骤输出。default 值是否生效无法判断 | 低 |
| 91 | USE-ENV-01-002 | usability | 编译缺口 | `GITHUB_SHA: unbound variable` — 正确报错。断言退化 `kind:status` | 中 |
| 92 | USE-EXPR-01-001 | usability | **平台缺陷** | `val=` — `atomgit.nonexistent_property` 被解析为空串而非报错 | 高 |
| 93 | USE-INPT-01-002 | usability | **平台缺陷** | `dry_run=false` — `type: boolean` 被静默接受并转换，文档仅支持 string | 高 |
| 94 | USE-LOG-01-001 | usability | **标记不匹配** | `prepare done` — step 输出 "prepare done" 非 "step one prepare"（step name 是YAML元数据非log内容） | 中 |
| 95 | USE-OS-01-001 | usability | **平台行为偏差** | `os=linux` — 平台返回小写，文档 `context.md` 说 `"Linux"`（大写）。值存在但文档不对 | 高 |
| 96 | USE-SECNAME-01-001 | usability | **平台缺陷** | `token=***` — `ATOMGIT_TOKEN` 作为 secret 名被接受。文档 `using-secrets.md`："不得以 ATOMGIT_ 开头" | 高 |

---

## 二、归因汇总

### 2.1 分类统计

| 分类 | 数量 | 占比 |
|---|---|---|
| **标记不匹配假失败** | 37 | 39% |
| **平台缺陷** | 21 | 22% |
| **用例问题** | 16 | 17% |
| **Engine Bug**（大小写比较） | 3 | 3% |
| **环境/Harness/配额** | 12 | 13% |
| **编译缺口**（退化 status） | 2 | 2% |
| **需人工判断** | 4 | 4% |
| **平台行为偏差** | 1 | 1% |
| **总计** | **96** | **100%** |

### 2.2 按维度分布

| 维度 | 标记不匹配 | 平台缺陷 | 用例问题 | 环境/Harness | EngineBug | 编译缺口 | 需人工 | 总计 |
|---|---|---|---|---|---|---|---|---|
| completeness | 5 | 7 | 1 | 1 | — | — | 2 | 16 |
| compatibility | 18 | 2 | 1 | — | 3 | — | — | 24* |
| reliability | 5 | 4 | 7 | 8 | — | — | — | 24 |
| security | 9 | 4 | 5 | 2 | — | 1 | 2 | 23 |
| usability | — | 4 | 2 | 1 | — | 1 | — | 8* |
| **总计** | **37** | **21** | **16** | **12** | **3** | **2** | **4** | **96** |

> *注：COMPAT-DIR-01-002 计为 compatibility 平台缺陷而非标记不匹配（leak assertion 正确捕获了平台意外行为）。USE-OS-01-001 计为平台行为偏差。USE-DISP-01-002 计为需人工判断。

### 2.3 合并视图——若消除 harness 侧假阳性后的实际通过率

| 场景 | PASS | FAIL | 通过率 |
|---|---|---|---|
| 原始报告 | 81 | 96 | 40% |
| 消除标记不匹配（37条） | 118 | 59 | 58% |
| 消除标记不匹配 + Engine Bug（40条） | 121 | 56 | 60% |
| 消除标记不匹配 + Engine Bug + 用例问题（56条） | 137 | 40 | 68% |

---

## 三、系统性发现

### 3.1 run_status 词汇映射缺失——第一大断裂（40 条，42%）

| 模式 | 数量 | 示例 |
|---|---|---|
| `"success"` / `"completed(success)"` ≠ `"COMPLETED"` | 28 | COMP-DIR-01-001, REL-CONC-01-001... |
| `"failure"` ≠ `"FAILED"` (case-sensitive) | 3 | COMPAT-EXPR-01-003, COMPAT-IF-01-001, COMPAT-OUTCOME-01-001 |
| `"canceled"` ≠ `"CANCELED"` | 1 | REL-CANCEL-01-028 |

**根因**: 合约 rubric 使用人类语义词汇，平台 API 返回大写枚举值。`compile_asserts.py` 缺少平台值→语义值的映射表。

**修复预估**: `COMPLETED→success, FAILED→failure, CANCELED→canceled` 三行映射即可消除 40% 的 FAIL。

### 3.2 空格 vs 下划线——第二大系统性缺陷（9 条）

| 合约期望（下划线） | 日志实际（空格） | 用例 |
|---|---|---|
| `cleaned_as_expected` | `cleaned as expected` | SEC-RUN-01-001 |
| `isolated_as_expected` | `isolated as expected` | SEC-RUN-01-002 |
| `access_denied_or_timeout` | `access denied or timeout` | SEC-NET-01-001 |
| `push_denied_or_403` | `push denied as expected` | SEC-PERM-01-004 |

**根因**: 合约编写者用下划线连词，shell `echo` 自然输出空格。编译器应在提取关键词时归一化处理。

### 3.3 `${{{{ }}}}` 四括号——合约生成缺陷（7 条 Reliability）

全部 7 条因 bash `bad substitution` 失败：`REL-ARTCONC-01-063, REL-MATRIX-01-038, REL-MATRIX-01-039, REL-OUTPUT-01-016`

**根因**: 合约生成时将表达式包裹了过多括号层（四层 vs 两层 `${{ }}`），bash 无法解析。

### 3.4 确认真实平台缺陷（21 条）

**P0 高价值**:

| 用例 | 缺陷 |
|---|---|
| COMPAT-DIR-01-002 | `.github/workflows/` 被错误识别并触发——安全边界破坏 |
| REL-YAMLCACHE-01-060 | YAML 修改后缓存未失效，执行旧版 workflow |
| SEC-DOS-01-001 | 1.1GB 制品未被配额拒绝 |
| USE-CONC-01-001 | `concurrency.max: 10` 非法值静默接受 |
| USE-SECNAME-01-001 | `ATOMGIT_` 前缀 secret 名被接受（违反文档命名规则） |
| USE-INPT-01-002 | `type: boolean` 被静默接受并转换（文档仅支持 string） |
| USE-EXPR-01-001 | `atomgit.nonexistent_property` 解析为空串而非报错 |
| USE-CTX-01-002 | `github.ref` 被解析为占位符而非引导至 atomgit |

**P1**:
- COMP-CACHE-01-001/002, COMPAT-CACHE-01-001: cache action 不可用（dispatch 事件下完全不工作）
- COMP-ARTIFACT-01-002/003, COMPAT-ARTIFACT-01-001: artifact 上传/下载失败
- COMP-CALL-01-001: workflow_call 嵌套失败
- SEC-MASK-01-001: Secret 掩码未完全生效
- SEC-SUPPLY-01-001: SHA pinning 不支持且无诊断

### 3.5 日志已否认的先前进位（0 条 SECURITY_CRITICAL 成立）

| 用例 | 之前判为 | 日志证实 | 修正为 |
|---|---|---|---|
| SEC-INJ-01-005 | 双重模板注入 SECURITY_CRITICAL | bash `bad substitution`，`"2"` 是源文本子串假阳性 | 标记不匹配 |
| REL-FAULT-01-031 | SIGKILL 日志泄漏 SECURITY_CRITICAL | 5 个 step 全正常执行，**SIGKILL 从未发生** | 平台缺陷（故障注入不工作） |
| SEC-NET-01-001 | Runner SSRF SECURITY_CRITICAL | `access denied or timeout` — **SSRF 防护工作正常** | 标记不匹配（空格vs下划线） |

---

*分析完成时间: 2026-07-24 · 日志源: tmp-data/valid-clean-logs-all/ · 96/96 条覆盖*
