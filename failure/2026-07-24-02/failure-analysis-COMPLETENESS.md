# Failure Analyst · COMPLETENESS FAIL Cases · 2026-07-24-valid297-final

## 失败分诊 · COMP-ARTIFACT-01-001 · artifact 跨 job 传递

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status) — 预期 COMPLETED，实际 FAILED；assertions[1] (value) — 预期 log contains 'hello artifact'，absent

**根因初判**: 需人工判断

**证据**: 日志仅 1 行 `[INFO] Job(...) duration check: true`，无任何步骤输出。Build job 在步骤执行前即失败。duration=86s。**失败传导链**: Build FAILED → Verify IGNORED。
**对照 GitCode 规格**: `upload-download-artifacts.md` L14-45 给出相同 YAML 示例。

**置信度**: 低 — 零步骤输出无法定位根因。

---

## 失败分诊 · COMP-ARTIFACT-01-002 · 下载全部制品

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status) — 预期 COMPLETED，实际 FAILED；assertions[1] (value) — 预期 'app'；assertions[2] (value) — 预期 'report'

**根因初判**: 需人工判断

**证据**: 日志仅 1 行 duration check。同 ARTIFACT-01-001 模式。duration=77s。
**对照 GitCode 规格**: `upload-download-artifacts.md` L95-103 示例仅传 path 不传 name（下载全部制品）。

**置信度**: 低

---

## 失败分诊 · COMP-ARTIFACT-01-003 · artifact 保留期

**判定结果**: FAIL
**失败断言**: assertions[0] (status) — 预期 all job/step green，实际 job 'Upload with short retention' FAILED

**根因初判**: 需人工判断

**证据**: 日志仅 1 行 duration check，duration=69s。`retention-days` 参数未在 `upload-download-artifacts.md` L60-63 参数表中列出。
**置信度**: 低

---

## 失败分诊 · COMP-CACHE-01-001 · cache hit 正确性

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status) — 预期 COMPLETED，实际 FAILED

**根因初判**: 需人工判断

**证据**: 日志仅 1 行 duration check，duration=109s。
**对照 GitCode 规格**: `using-dependency-cache.md` L24-37 cache action 示例。
**置信度**: 低

---

## 失败分诊 · COMP-CACHE-01-002 · restore-keys 前缀匹配

**判定结果**: FAIL
**失败断言**: assertions[0] (status) — 预期 all job/step green，实际 job 'Verify restore keys fallback' FAILED

**根因初判**: 需人工判断

**证据**: 日志仅 1 行 duration check，duration=99s。
**对照 GitCode 规格**: `using-dependency-cache.md` L60-65 描述 restore-keys 前缀匹配机制。
**置信度**: 低

---

## 失败分诊 · COMP-CALL-01-001 · 2 层 workflow_call 嵌套

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status) — 预期 COMPLETED，实际 FAILED

**根因初判**: 需人工判断

**证据**: 日志仅 1 行 duration check，duration=56s。`repo_fixture: reusable-workflow` 可能影响执行环境。
**对照 GitCode 规格**: `00-overview.md` L15 支持 workflow_call 嵌套，`COMPAT-NOTES.md` L30 限制 2 层。
**置信度**: 低

---

## 失败分诊 · COMP-PERMS-01-001 · permissions 空对象最小权限

**判定结果**: FAIL
**失败断言**: assertions[1] (value) — 预期 log contains '403'，absent（负向断言 PASS）

**根因初判**: 环境问题

**证据**: 日志零 shell 输出。负向断言（run != COMPLETED）PASS。缺 `uses: checkout`，git 命令在非 git 目录失败。
**对照 GitCode 规格**: `token-permissions.md` L103: `permissions: {}` = 最小默认权限 repository:read。
**置信度**: 中

---

## 失败分诊 · COMP-PERMS-01-002 · repository write 权限

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status) — 预期 COMPLETED，实际 FAILED

**根因初判**: 需人工判断

**证据**: 日志仅 1 行 duration check。同 PERMS-01-001 缺 checkout 模式。
**对照 GitCode 规格**: `token-permissions.md` L47: repository:write → 推送/修改仓库。
**置信度**: 低

---

## 失败分诊 · COMP-PERMS-01-003 · fork PR write 降级

**判定结果**: FAIL
**失败断言**: assertions[1] (value) — 预期 log contains 'write failed as expected'，absent

**根因初判**: 用例问题

**证据**: 日志输出 "404"。curl `-w "%{http_code}"` 不导致非零退出码，`|| echo "write failed as expected"` 不触发。负向断言 PASS（run != success_with_write）。
**置信度**: 高

---

## 失败分诊 · COMP-SECRET-01-001 · secret 脱敏为 ***

**判定结果**: FAIL
**失败断言**: assertions[0] (value) — 预期 log contains '***'，absent

**根因初判**: 需人工判断

**证据**: 日志输出 "secret is "（空）。config_probe=configured。可能是 secret 值本身为空或脱敏输出为空。
**对照 GitCode 规格**: `using-secrets.md` L66: "Secret 值在日志中自动替换为 ***"。
**置信度**: 中

---

## 失败分诊 · COMP-SUMMARY-01-001 · ATOMGIT_STEP_SUMMARY

**判定结果**: FAIL
**失败断言**: assertions[0] (value) — 预期 'Test Summary'；assertions[1] (value) — 预期 '<table>'

**根因初判**: 编译缺口

**证据**: 日志无 shell stdout。`step_summary` target 被编译退化为 `run_logs`。step summary 内容写入文件不在 run_logs 中。
**对照 GitCode 规格**: `workflow-commands.md` L49-58: ATOMGIT_STEP_SUMMARY 写入运行摘要页面。
**置信度**: 高

---

## 失败分诊 · COMP-TIMEOUT-01-002 · 超时标记

**判定结果**: FAIL
**失败断言**: assertions[1] (run_status) — 预期 FAILED，实际 CANCELLED

**根因初判**: 标记不匹配

**证据**: 日志有 "starting" + sleep 步骤。run_status=CANCELLED（非 FAILED），duration=205s。负向断言 PASS（run != COMPLETED）。
**对照 GitCode 规格**: `configure-jobs.md` L121: "超时后 job 将被强制终止"，未明确标记状态。
**置信度**: 高

---

## 失败分诊 · COMP-PR-01-001 · fork PR secrets 隔离

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status) — 预期 SUCCESS_OR_BLOCKED，实际 COMPLETED

**根因初判**: 标记不匹配

**证据**: 日志输出 "secret value is "（空）— fork PR 安全隔离正常工作。COMPLETED 未被 assertion engine 归一化为 SUCCESS_OR_BLOCKED。
**置信度**: 高

---

## 失败分诊 · COMP-PR-01-003 · fork PR TOKEN 仅 read

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status) — 预期 SUCCESS_OR_FAILURE，实际 COMPLETED

**根因初判**: 标记不匹配

**证据**: 日志输出 "404"。COMPLETED 未被归一化为 SUCCESS_OR_FAILURE。
**置信度**: 中

---

## 汇总

| 根因 | 数量 |
|---|---|
| 需人工判断（零日志） | 8 |
| 标记不匹配 | 3 |
| 环境问题 | 1 |
| 用例问题 | 1 |
| 编译缺口 | 1 |

**核心发现**: 8/14 为"零步骤输出"——平台调度成功（有 duration）但步骤日志全缺，artifact/cache 内建 Action 全部静默失败。
