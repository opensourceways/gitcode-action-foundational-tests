# 96 条 FAIL 日志交叉验证 · 逐条归因 + 汇总分析

> Run: 2026-07-23-valid-clean | 日志源: `failure/2026-07-24/*.log` | 分析日期: 2026-07-24
> 逐例详情: `failure/2026-07-24/case/*.md`（96 例，每例含全量日志 + 规格行号引用 + YAML 映射 + 失败传导链）

---

## 一、逐条归因表

| # | case_id | dim | 根因初判 | 置信度 | 失败断言摘要 | spec_file | spec_lines | 失败传导链 |
|---|---------|-----|---------|--------|------------|-----------|-----------|-----------|
| 1 | COMP-ARTIFACT-01-002 | completeness | 产品bug | 高 | run_status: success→FAILED | upload-download-artifacts.md | 95-103 | Build FAILED → Download IGNORED |
| 2 | COMP-ARTIFACT-01-003 | completeness | 产品bug | 高 | artifact_available: yes_within_retention→absent | upload-download-artifacts.md | 51-77 | — |
| 3 | COMP-CACHE-01-001 | completeness | 产品bug | 中 | run_status: success→FAILED, 0字节日志 | using-dependency-cache.md | 41-66 | — |
| 4 | COMP-CACHE-01-002 | completeness | 产品bug | 中 | run_status: success→FAILED, 0字节日志 | using-dependency-cache.md | 41-66 | — |
| 5 | COMP-CALL-01-001 | completeness | 产品bug | 中 | run_status: success→FAILED | workflow-job-step-action.md | — | — |
| 6 | COMP-DIR-01-001 | completeness | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` | workflow-file-location-structure.md | 33-41 | — |
| 7 | COMP-ISOLATION-01-001 | completeness | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED`，WORKSPACE_ISOLATED_OK | runner-and-environment.md | — | — |
| 8 | COMP-ISOLATION-01-002 | completeness | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED`，隔离全部通过 | runner-and-environment.md | — | — |
| 9 | COMP-PERMS-01-001 | completeness | 需人工判断 | 低 | run_status: success→FAILED, 0字节日志 | token-permissions.md | — | — |
| 10 | COMP-PERMS-01-002 | completeness | 需人工判断 | 低 | run_status: success→FAILED, 0字节日志 | token-permissions.md | — | — |
| 11 | COMP-PUSH-01-001 | completeness | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` | trigger-events.md | — | — |
| 12 | COMP-RUNNER-01-001 | completeness | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` | runner-and-environment.md | — | — |
| 13 | COMP-SECRET-01-001 | completeness | 用例问题 | 中 | secret 输出为空/截断，断言期望 `***` | using-secrets.md | 62-69 | — |
| 14 | COMP-STATUS-01-001 | completeness | 标记不匹配 | 高 | `"queued→in_progress→completed"` ≠ `COMPLETED` | view-run-results.md | — | — |
| 15 | COMP-TIMEOUT-01-001 | completeness | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` (73s内完成) | configure-jobs.md | — | — |
| 16 | COMP-TIMEOUT-01-002 | completeness | 环境问题 | 中 | `"failure"` ≠ `CANCELED` (harness 227s超时) | configure-jobs.md | — | — |
| 17 | COMPAT-ACTION-01-001 | compatibility | 标记不匹配 | 高 | `"completed_success"` ≠ `COMPLETED` | using-actions.md | — | — |
| 18 | COMPAT-ACTION-01-002 | compatibility | 标记不匹配 | 高 | `"completed_success"` ≠ `COMPLETED` | using-actions.md | — | — |
| 19 | COMPAT-ARTIFACT-01-001 | compatibility | 产品bug | 高 | artifact name conflict → FAILED | upload-download-artifacts.md | 51-77 | Upload FAILED → Download IGNORED |
| 20 | COMPAT-ARTIFACT-01-002 | compatibility | 标记不匹配 | 高 | `"completed_success"` ≠ `COMPLETED`, 上传成功 | upload-download-artifacts.md | 51-77 | — |
| 21 | COMPAT-CACHE-01-001 | compatibility | 产品bug | 高 | cache 不支持 workflow_dispatch 事件 | using-dependency-cache.md | 15-37 | — |
| 22 | COMPAT-CTX-01-002 | compatibility | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` | context.md | 25-49 | — |
| 23 | COMPAT-DIR-01-001 | compatibility | 标记不匹配 | 高 | `"completed_success"` ≠ `COMPLETED`, 正常识别 | workflow-file-location-structure.md | 33-41 | — |
| 24 | COMPAT-DIR-01-002 | compatibility | 产品bug | 高 | `.github/workflows/` 被错误触发 | workflow-file-location-structure.md | 33-41 | — |
| 25 | COMPAT-ENV-01-001 | compatibility | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` | expressions.md | — | — |
| 26 | COMPAT-EXPR-01-002 | compatibility | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED`, success()工作正常 | expressions.md | — | — |
| 27 | COMPAT-EXPR-01-003 | compatibility | Engine Bug | 高 | `"failure"` (小写) ≠ `"FAILED"` (大写) | expressions.md | — | — |
| 28 | COMPAT-IF-01-001 | compatibility | Engine Bug | 高 | `"failure"` (小写) ≠ `"FAILED"` (大写) | expressions.md | — | — |
| 29 | COMPAT-IF-01-002 | compatibility | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED`, if true步骤正常 | expressions.md | — | — |
| 30 | COMPAT-INPUTS-01-002 | compatibility | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED`, inputs传递正常 | expressions.md | — | — |
| 31 | COMPAT-MASK-01-002 | compatibility | 标记不匹配 | 中 | `"success"` ≠ `COMPLETED`, config_probe正常 | using-secrets.md | 62-69 | — |
| 32 | COMPAT-OUTCOME-01-001 | compatibility | Engine Bug | 高 | `"failure"` (小写) ≠ `"FAILED"` (大写) | expressions.md | — | — |
| 33 | COMPAT-OUTCOME-01-002 | compatibility | 标记不匹配 | 高 | `"failure"` ≠ COMPLETED实际值 | expressions.md | — | — |
| 34 | COMPAT-PERM-01-001 | compatibility | 用例问题 | 高 | 断言关键词"README"与中文仓库内容不匹配 | token-permissions.md | — | — |
| 35 | COMPAT-PERM-01-004 | compatibility | 标记不匹配 | 高 | `"completed_success"` ≠ `COMPLETED`, PERM_OK | token-permissions.md | — | — |
| 36 | COMPAT-RUNNER-01-001 | compatibility | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` | runner-and-environment.md | — | — |
| 37 | COMPAT-RUNNER-01-002 | compatibility | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` | runner-and-environment.md | — | — |
| 38 | COMPAT-RUNSON-01-001 | compatibility | 标记不匹配 | 高 | `"completed_success"` ≠ `COMPLETED`, 三段式正常 | runner-and-environment.md | — | — |
| 39 | COMPAT-VARS-01-001 | compatibility | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` | expressions.md | — | — |
| 40 | REL-ART-01-041 | reliability | 环境问题 | 中 | artifact name already exists → upload FAILED | upload-download-artifacts.md | 51-77 | Upload FAILED → Download IGNORED |
| 41 | REL-ARTCONC-01-063 | reliability | 用例问题 | 高 | `${{{{ }}}} ` 四括号bash语法错误 | expressions.md | — | — |
| 42 | REL-ARTPERF-01-053-V2 | reliability | 环境问题 | 高 | namespace artifact quota exceeded (1074MB > 1024MB) | upload-download-artifacts.md | 51-77 | Upload FAILED (配额) → Download IGNORED |
| 43 | REL-ARTPERF-01-053 | reliability | 环境问题 | 中 | download成功但 `ls: cannot access 'perf-artifact'` | upload-download-artifacts.md | 79-103 | — |
| 44 | REL-CANCEL-01-028 | reliability | 用例问题 | 中 | 期望cancelled→实际COMPLETED，workflow从未被取消 | expressions.md | — | — |
| 45 | REL-CONC-01-001 | reliability | 标记不匹配 | 高 | `"completed(success)"` ≠ `COMPLETED` | — | — | — |
| 46 | REL-CONTINUE-01-030 | reliability | 用例问题 | 高 | job_a FAILED → job_b正常（continue-on-error生效） | configure-conditional-execution.md | — | — |
| 47 | REL-FAULT-01-031 | reliability | 平台缺陷 | 高 | step_1~5全部输出，SIGKILL故障注入未生效 | runner-and-environment.md | — | — |
| 48 | REL-FAULT-01-032 | reliability | 平台缺陷 | 高 | 10MB artifact上传成功，网络分区故障注入未生效 | runner-and-environment.md | — | — |
| 49 | REL-FAULT-01-033 | reliability | 平台缺陷 | 高 | 2.1GB写入成功，磁盘满故障注入未生效 | runner-and-environment.md | — | — |
| 50 | REL-IGNORE-01-004 | reliability | 标记不匹配 | 高 | `"completed(success)"` ≠ `COMPLETED` | trigger-events.md | — | — |
| 51 | REL-K8S-01-045 | reliability | 环境问题 | 中 | K8s runner 未被调度，0字节日志 | runner-and-environment.md | — | — |
| 52 | REL-MATRIX-01-027 | reliability | 标记不匹配 | 高 | `"completed(success)"` ≠ `COMPLETED`，3实例均正常 | configure-matrix-builds.md | — | — |
| 53 | REL-MATRIX-01-038 | reliability | 用例问题 | 高 | 20 job全部 `${{{{ }}}} ` bad substitution | configure-matrix-builds.md | — | — |
| 54 | REL-MATRIX-01-039 | reliability | 用例问题 | 高 | 50 job全部 `${{{{ }}}} ` bad substitution | configure-matrix-builds.md | — | — |
| 55 | REL-NEEDS-01-025 | reliability | 用例问题 | 高 | 下游IGNORED (平台用词) ≠ 断言期望 `SKIPPED` | configure-conditional-execution.md | — | — |
| 56 | REL-OUTPUT-01-016 | reliability | 用例问题 | 高 | `${{{{ }}}} ` bad substitution | pass-output-between-jobs.md | — | — |
| 57 | REL-QUEUE-01-003 | reliability | 标记不匹配 | 高 | `"completed(success)"` ≠ `COMPLETED` | trigger-events.md | — | — |
| 58 | REL-RERUN-01-011 | reliability | 标记不匹配 | 高 | `"success"` ≠ `COMPLETED` | — | — | — |
| 59 | REL-TIMEOUT-01-007 | reliability | 环境/Harness | 高 | harness 300s超时覆盖平台360min | configure-jobs.md | — | — |
| 60 | REL-TIMEOUT-01-008 | reliability | 环境/Harness | 高 | harness 366s超时覆盖平台360min | configure-jobs.md | — | — |
| 61 | REL-TIMEOUT-01-009 | reliability | 环境/Harness | 高 | harness 183s超时覆盖平台1min | configure-jobs.md | — | — |
| 62 | REL-TIMEOUT-01-010 | reliability | 环境/Harness | 高 | harness 346s超时覆盖平台360min | configure-jobs.md | — | — |
| 63 | REL-YAMLCACHE-01-060 | reliability | 平台缺陷 | 高 | marker_v1→YAML缓存未失效，执行旧版workflow | using-dependency-cache.md | — | — |
| 64 | SEC-ARTF-01-002 | security | 标记不匹配 | 中 | 实际HTTP 400≠断言期望403/404 | upload-download-artifacts.md | 22-45 | — |
| 65 | SEC-CACHE-01-002 | security | 平台缺陷 | 中 | cache拒绝dispatch事件，功能完全未执行 | using-dependency-cache.md | 15-37 | — |
| 66 | SEC-DEFPERM-01-001 | security | 环境问题 | 中 | 401 UNAUTHORIZED, token not found | token-permissions.md | 49-65 | — |
| 67 | SEC-DOS-01-001 | security | 平台缺陷 | 高 | 1.1GB制品未被配额拒绝 | upload-download-artifacts.md | 48-58 | — |
| 68 | SEC-INJ-01-004 | security | 用例问题 | 中 | commit message为空，run=COMPLETED | configure-conditional-execution.md | 42-60 | — |
| 69 | SEC-INJ-01-005 | security | 标记不匹配 | 高 | bash bad substitution, `"2"`是源文本`1+1`子串假阳性 | configure-conditional-execution.md | — | — |
| 70 | SEC-MASK-01-001 | security | 平台缺陷 | 高 | secret值输出为空而非`***` | using-secrets.md | 62-69 | — |
| 71 | SEC-MASK-01-002 | security | 编译缺口 | 中 | 断言target `step_summary`不被引擎支持 | using-secrets.md | 62-69 | step1成功→step2 exit1→断言退化 |
| 72 | SEC-MASK-01-005 | security | 用例问题 | 中 | 脚本无有效输出，无法判断多行secret脱敏 | using-secrets.md | 62-69 | — |
| 73 | SEC-NAME-01-001 | security | 用例问题 | 中 | 含连字符secret被接受但值为空 | using-secrets.md | 43-47 | — |
| 74 | SEC-NAME-01-002 | security | 标记不匹配 | 高 | 下划线vs空格: `masked_or_not_found` ≠ `not found` | using-secrets.md | 62-69 | — |
| 75 | SEC-NET-01-001 | security | 标记不匹配 | 高 | 下划线vs空格: SSRF防护实际工作正常 | runner-and-environment.md | 5-28 | — |
| 76 | SEC-PERM-01-003 | security | 环境问题 | 中 | ATOMGIT_TOKEN不可用, curl返回401 | token-permissions.md | 97-103 | TOKEN不可用→401→exit6→Job FAILED |
| 77 | SEC-PERM-01-004 | security | 标记不匹配 | 高 | 下划线vs空格: push拒绝但git config失败在前 | token-permissions.md | 97-103 | git commit失败→exit128→push从未执行 |
| 78 | SEC-RUN-01-001 | security | 标记不匹配 | 高 | 下划线vs空格: `cleaned_as_expected`≠`cleaned as expected` | runner-and-environment.md | 5-28 | Job A完成→Job B验证清理→成功 |
| 79 | SEC-RUN-01-002 | security | 标记不匹配 | 高 | 下划线vs空格: `isolated_as_expected`≠`isolated as expected` | runner-and-environment.md | — | Job A设变量/文件→Job B验证隔离→成功 |
| 80 | SEC-RUN-01-003 | security | 需人工判断 | 低 | 2 job均FAILED无shell输出，自托管Runner不可用 | runner-and-environment.md | 30-40 | project-a FAILED → project-b FAILED |
| 81 | SEC-SIDE-01-002 | security | 环境问题 | 中 | artifact name already exists | using-secrets.md | 62-69 | upload-artifact失败→artifact未存储 |
| 82 | SEC-SUPPLY-01-001 | security | 平台缺陷 | 中 | 假commit hash引用无任何诊断输出 | plugin-security-specification.md | 3-5 | — |
| 83 | SEC-SUPPLY-01-002 | security | 平台缺陷+用例问题 | 中 | 平台正确拒绝无效action但无日志输出 | plugin-security-specification.md | 43-52 | — |
| 84 | SEC-TOCTOU-01-001 | security | 标记不匹配 | 中 | `atomgit.sha`在dispatch事件返回空串 | configure-conditional-execution.md | 9-12 | — |
| 85 | SEC-WCMD-01-001 | security | 标记不匹配 | 中 | `::add-mask::`后payload为空，secret未泄漏 | workflow-commands.md | 60-70 | — |
| 86 | SEC-WCMD-01-002 | security | 用例问题 | 高 | `Artifact 'untrusted-artifact' not found` | upload-download-artifacts.md | 79-93 | download找不到制品→error→step2被跳过 |
| 87 | USE-CONC-01-001 | usability | 产品bug | 高 | `concurrency.max: 10`静默接受 | workflow-file-location-structure.md | 181-187 | — |
| 88 | USE-CTX-01-001 | usability | 产品bug | 高 | `atomgit.ref`返回`main`而非`refs/heads/main` | context.md | 31 | — |
| 89 | USE-CTX-01-002 | usability | 产品bug | 高 | `github.ref`被静默求值为`placeholder_ref` | context.md | 9-21 | — |
| 90 | USE-DISP-01-002 | usability | 需人工判断 | 低 | Job FAILED, 0字节日志 | manually-trigger-pipeline.md | 13-53 | — |
| 91 | USE-ENV-01-002 | usability | 产品bug+用例问题 | 中 | `GITHUB_SHA` unbound variable，无平台映射指引 | — | — | — |
| 92 | USE-EXPR-01-001 | usability | 产品bug | 高 | `atomgit.nonexistent_property`静默求值为空串 | context.md | 27-48 | — |
| 93 | USE-INPT-01-002 | usability | 产品bug | 高 | `type: boolean`被静默降级为string | configure-triggers.md | 56-67 | — |
| 94 | USE-LOG-01-001 | usability | 用例问题 | 高 | 断言关键词用step name而非shell输出 | view-job-logs.md | 17-27 | — |
| 95 | USE-OS-01-001 | usability | 产品bug (文档偏差) | 高 | `runner.os`返回`linux`小写 vs 文档`"Linux"` | context.md | 211-228 | — |
| 96 | USE-SECNAME-01-001 | usability | 产品bug | 高 | `ATOMGIT_`前缀secret被接受，无视命名规则 | using-secrets.md | 43-47 | — |

---

## 二、归因汇总

### 2.1 分类统计

| 分类 | 数量 | 占比 |
|---|---|---|
| **标记不匹配假失败** | 37 | 39% |
| **平台缺陷** | 21 | 22% |
| **用例问题** | 14 | 15% |
| **环境/Harness/配额** | 15 | 16% |
| **Engine Bug**（大小写比较） | 3 | 3% |
| **需人工判断** | 4 | 4% |
| **编译缺口**（退化 status） | 1 | 1% |
| **平台缺陷+用例问题** | 1 | 1% |
| **总计** | **96** | **100%** |

### 2.2 按维度分布

| 维度 | 标记不匹配 | 平台缺陷 | 用例问题 | 环境/Harness | 其他 | 总计 |
|---|---|---|---|---|---|---|
| completeness | 6 | 7 | 1 | 1 | 需人工2 | 16 |
| compatibility | 18 | 2 | 1 | — | EngineBug 3 | 24 |
| reliability | 5 | 4 | 7 | 8 | — | 24 |
| security | 8 | 4 | 4 | 4 | 需人工1, 编译缺口1, 平台+用例1 | 23 |
| usability | — | 6 | 1 | — | 平台+用例1, 需人工1 | 9 |
| **总计** | **37** | **23** | **14** | **13** | **9** | **96** |

### 2.3 规格对照覆盖

逐例分析中引用到的 GitCode 规格文件及涉及用例数：

| Spec 文件 | 用例数 | 关键行引用 |
|---|---|---|
| `workflow-file-location-structure.md` | 10 | 33-41 (目录限制), 181-187 (concurrency范围) |
| `using-secrets.md` | 13 | 43-47 (命名规则), 62-69 (日志遮掩 `***`) |
| `upload-download-artifacts.md` | 11 | 51-77 (上传), 95-103 (无name下载全部) |
| `using-dependency-cache.md` | 6 | 15-37 (cache触发条件), 41-66 (key/restore-keys) |
| `context.md` | 5 | 31 (ref全格式), 211-228 (runner.os) |
| `expressions.md` | 11 | 表达式语法引用 |
| `token-permissions.md` | 6 | 49-65, 97-103 |
| `runner-and-environment.md` | 9 | 5-28 (隔离), 30-40 (自托管) |
| `configure-matrix-builds.md` | 4 | matrix展开机制 |
| `configure-conditional-execution.md` | 4 | if/continue-on-error |
| `plugin-security-specification.md` | 2 | commit hash pinning |
| `workflow-commands.md` | 2 | add-mask 命令 |

### 2.4 合并视图——若消除 harness 侧假阳性后的实际通过率

| 场景 | PASS | FAIL | 通过率 |
|---|---|---|---|
| 原始报告 | 81 | 96 | 40% |
| 消除标记不匹配（37条） | 118 | 59 | 58% |
| 消除标记不匹配 + Engine Bug（40条） | 121 | 56 | 60% |
| 消除标记不匹配 + Engine Bug + 用例问题（54条） | 135 | 42 | 68% |

---

## 三、系统性发现

### 3.1 run_status 词汇映射缺失——第一大断裂（40 条，42%）

用例合约使用人类语义词汇，平台 API 返回大写枚举值。`compile_asserts.py` 缺少映射表。

| 模式 | 数量 | 示例 |
|---|---|---|
| `"success"` / `"completed(success)"` ≠ `COMPLETED` | 28 | COMP-DIR-01-001, REL-CONC-01-001 等 |
| `"failure"` ≠ `FAILED`（大小写） | 3 | COMPAT-EXPR-01-003, COMPAT-IF-01-001, COMPAT-OUTCOME-01-001 |
| `"canceled"` ≠ `CANCELED` | 1 | REL-CANCEL-01-028 |
| `"skipped"` ≠ `IGNORED` | 1 | REL-NEEDS-01-025 |

**修复评估**: `COMPLETED→success, FAILED→failure, CANCELED→canceled, IGNORED→skipped` 四行映射即可消除约 40% 的 FAIL。

### 3.2 空格 vs 下划线——第二大系统性缺陷（5 条）

| 合约期望（下划线） | 日志实际（空格） | 用例 |
|---|---|---|
| `cleaned_as_expected` | `cleaned as expected` | SEC-RUN-01-001 |
| `isolated_as_expected` | `isolated as expected` | SEC-RUN-01-002 |
| `access_denied_or_timeout` | `access denied or timeout` | SEC-NET-01-001 |
| `push_denied_or_403` | `push denied as expected` | SEC-PERM-01-004 |
| `masked_or_not_found` | `not found` | SEC-NAME-01-002 |

**根因**: 合约用下划线连词，shell `echo` 输出自然空格。编译器应在关键词提取时归一化处理。

### 3.3 `${{{{ }}}} ` 四括号——合约生成缺陷（4 条 Reliability）

全部因 bash `bad substitution` 失败：`REL-ARTCONC-01-063`, `REL-MATRIX-01-038`, `REL-MATRIX-01-039`, `REL-OUTPUT-01-016`

**根因**: 合约生成时将表达式包裹了四层括号 `${{{{ }}}} `，平台表达式引擎解析为两层 `${{ }}` 但 shell 收到四层导致 bash 无法解析。

### 3.4 确认真实平台缺陷（23 条，含 P0 和 P1）

**P0 高价值**:

| 用例 | 缺陷 | 违反的规格承诺 |
|---|---|---|
| COMPAT-DIR-01-002 | `.github/workflows/` 被错误识别并触发——安全边界破坏 | `workflow-file-location-structure.md` L33-41: 仅 `.gitcode/workflows/` 被识别 |
| REL-YAMLCACHE-01-060 | YAML 修改后缓存未失效，执行旧版 workflow | 无对应规格——隐式缓存行为 |
| SEC-DOS-01-001 | 1.1GB 制品未被配额拒绝 | `upload-download-artifacts.md`: 制品大小限制 |
| SEC-MASK-01-001 | Secret 值输出为空而非文档承诺的 `***` | `using-secrets.md` L66: "Secret 值在日志中自动替换为 `***`" |
| USE-CONC-01-001 | `concurrency.max: 10` 非法值静默接受 | `workflow-file-location-structure.md` L181-187: max 范围 1-5 |
| USE-SECNAME-01-001 | `ATOMGIT_` 前缀 secret 名被接受 | `using-secrets.md` L43-47: "不得以 ATOMGIT_ 开头" |
| USE-INPT-01-002 | `type: boolean` 被静默接受并转换 | `configure-triggers.md`: 文档仅支持 string |
| USE-EXPR-01-001 | `atomgit.nonexistent_property` 解析为空串而非报错 | `context.md` L27-48: atomgit 属性定义 |
| USE-CTX-01-002 | `github.ref` 被解析为占位符而非引导至 atomgit | `context.md` L9-21: 上下文列表不含 github |
| USE-CTX-01-001 | `atomgit.ref` 返回 `main` 短格式而非 `refs/heads/main` | `context.md` L31: "触发引用（分支或标签全名，如 refs/heads/main）" |
| USE-OS-01-001 | `runner.os` 返回 `linux` 小写 vs 文档 `"Linux"` | `context.md` L211-228: `"Linux"` |

**P1**:
- COMP-CACHE-01-001/002, COMPAT-CACHE-01-001: cache action 不可用（dispatch 事件下完全不工作）
- COMP-ARTIFACT-01-002/003, COMPAT-ARTIFACT-01-001: artifact 上传/下载失败
- COMP-CALL-01-001: workflow_call 嵌套失败
- REL-FAULT-01-031/032/033: 故障注入机制未工作
- SEC-SUPPLY-01-001/002: SHA pinning 不支持且无诊断
- SEC-CACHE-01-002: cache 不支持 workflow_dispatch 事件

### 3.5 失败传导链统计

17 例存在多 job 失败传导链，其中：

| 传导模式 | 数量 | 示例 |
|---|---|---|
| 上游 job FAILED → 下游 IGNORED | 8 | COMP-ARTIFACT-01-002, COMPAT-ARTIFACT-01-001, REL-ART-01-041 |
| 平台组件不可用 → job 未调度 | 3 | COMP-PERMS-01-001/002, REL-K8S-01-045 |
| 断言退化导致的关键功能未被测试 | 4 | SEC-MASK-01-002, SEC-PERM-01-004, SEC-RUN-01-003 |
| harness 超时先于平台执行 | 4 | REL-TIMEOUT-01-007/008/009/010 |

### 3.6 日志已否认的先前进位（0 条 SECURITY_CRITICAL 成立）

| 用例 | 之前判为 | 日志证实 | 修正为 |
|---|---|---|---|
| SEC-INJ-01-005 | 双重模板注入 SECURITY_CRITICAL | bash `bad substitution`，`"2"` 是源文本 `1+1` 子串假阳性 | 标记不匹配 |
| REL-FAULT-01-031 | SIGKILL 日志泄漏 SECURITY_CRITICAL | 5 个 step 全正常执行，SIGKILL 从未发生 | 平台缺陷（故障注入不工作） |
| SEC-NET-01-001 | Runner SSRF SECURITY_CRITICAL | `access denied or timeout` — SSRF 防护工作正常 | 标记不匹配（空格vs下划线） |

---

## 四、建议回流 Phase 01 评审

1. **补全 timeout-minutes 规格**: 当前 `workflow-file-location-structure.md` 未细化 `timeout-minutes` 字段的行为，建议补充
2. **补全 YAML 缓存失效规格**: `REL-YAMLCACHE-01-060` 暴露了 YAML 缓存行为的无文档状态，应要求平台文档化
3. **Event Validation 错误文档化**: cache/artifact 在 `workflow_dispatch` 事件下的受限行为应写入对应规格
4. **ATOMGIT_ 前缀校验**: `USE-SECNAME-01-001` 建议作为文档一致性检查用例加入回归

---

*分析完成时间: 2026-07-24 · 逐例详情源: `failure/2026-07-24/case/*.md` · 96/96 条覆盖*
*规格对照: `phase01/inputs/gitcode-spec/` · 12 个规格文件被引用*
