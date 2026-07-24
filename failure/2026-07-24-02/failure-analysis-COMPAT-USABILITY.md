# Failure Analyst · COMPATIBILITY + USABILITY FAIL Cases · 2026-07-24-valid297-final

## COMPATIBILITY

### 失败分诊 · COMPAT-CACHE-01-001 · cache 在 dispatch 不可用

**判定结果**: FAIL
**失败断言**: assertions[0] (value) — 预期 log contains 'CACHE_HIT'，actual=CACHE_MISS
**根因初判**: 环境问题
**证据**: 日志 L3 `[cache eventValidation] allowlistMatch=false allowlist=[push|pull_request|merge_request]` — cache 插件拒绝 dispatch 事件。
**置信度**: 高

---

### 失败分诊 · COMPAT-DIR-01-002 · .github/workflows/ 不应识别

**判定结果**: FAIL
**失败断言**: assertions[0] (leak) — 预期 'GITHUB_DIR_WORKFLOW_RAN' 0 hits，FOUND
**根因初判**: 产品缺陷
**证据**: 日志 L5 `GITHUB_DIR_WORKFLOW_RAN`。平台识别并执行了 `.github/workflows/` 目录。规格 `workflow-file-location-structure.md` L35-41 仅声明 `.gitcode/workflows/` 为有效目录。
**置信度**: 高

---

### 失败分诊 · COMPAT-INPUTS-01-001 · boolean input 应拒绝

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status_not) — 预期 conclusion != COMPLETED，actual=COMPLETED
**根因初判**: 产品缺陷
**证据**: 日志 L5 `INPUT_OK`。平台静默接受 `type: boolean`。规格 `variables.md` L56-62 声明仅支持 string。
**置信度**: 高

---

### 失败分诊 · COMPAT-OUTCOME-01-002 · outcome vs conclusion

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status) — 预期 FAILED，actual=COMPLETED
**根因初判**: 编译缺口
**证据**: YAML `target: step_status` 被编译为 `kind: run_status`（退化）。continue-on-error 后平台 correctly 返回 COMPLETED。规格 `context.md` L206-207 定义 outcome/conclusion 语义。
**置信度**: 高

---

### 失败分诊 · COMPAT-OUTCOME-01-003 · job 级 outcome

**判定结果**: FAIL
**失败断言**: assertions[1] (run_status) — 预期 FAILED，actual=COMPLETED
**根因初判**: 编译缺口
**证据**: 同 OUTCOME-01-002。`step_status`/`job_status` target 全编译退化为 `run_status`。
**置信度**: 高

---

### 失败分诊 · COMPAT-PERM-01-001 · 默认 TOKEN 读权限

**判定结果**: FAIL
**失败断言**: assertions[1] (value) — 预期 log contains 'README'，absent
**根因初判**: 用例问题
**证据**: 日志 L52-54 显示 `cat README.md` 成功输出文件内容（中文），但不含字面量 "README"。断言 `contains: "README"` 设计错误。
**置信度**: 高

---

### 失败分诊 · COMPAT-RUNSON-01-002 · 单标签字符串应报错

**判定结果**: FAIL
**失败断言**: assertions[0] (leak) — 预期 'RUNSON_STRING_ACCEPTED' 0 hits，FOUND
**根因初判**: 用例问题
**证据**: YAML 自身 `runs-on: [ubuntu-latest, x64, small]` 是合法三段数组，非单标签字符串。未真正测试目标场景。
**置信度**: 高

---

### 失败分诊 · COMPAT-VARS-01-006 · vars 在 Action with 中可用

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status) — 预期 COMPLETED，actual=FAILED
**根因初判**: 环境问题
**证据**: 日志 L2-6 checkout 插件报 `Input required and not supplied: COMMIT_REF_NAME`。vars.ACTION_VAR="action_value" 不是有效 git ref。证明 vars 在 with 参数中可用（值被正确传入），只是值不对。
**置信度**: 高

---

## USABILITY

### 失败分诊 · USE-ANNOT-01-002 · PR annotation

**判定结果**: FAIL
**失败断言**: assertions[0] (status) — 预期 all green，actual job FAILED
**根因初判**: 环境问题
**证据**: 日志 L30-36 checkout 失败 `fatal: couldn't find remote ref refs/merge-requests/16/merge`——PR #16 ref 不存在。
**置信度**: 高

---

### 失败分诊 · USE-CONC-01-001 · concurrency.max=10 应报错

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status_not) — 预期 conclusion != COMPLETED，actual=COMPLETED
**根因初判**: 产品缺陷
**证据**: 日志 L5 `hello`。`max: 10` 超出规格范围 1-5 但静默接受。
**对照 GitCode 规格**: `workflow-file-location-structure.md` L181-187: max 范围 1-5。
**置信度**: 高

---

### 失败分诊 · USE-CTX-01-001 · atomgit.ref 格式

**判定结果**: FAIL
**失败断言**: assertions[0] (value) — 预期 log contains 'ref=refs/heads/'，absent
**根因初判**: 产品缺陷
**证据**: 日志 L5 `ref=main`。`atomgit.ref` 返回短格式 `main` 而非 `refs/heads/main`。
**对照 GitCode 规格**: `context.md` L31: 声明返回 `refs/heads/main`。
**置信度**: 高

---

### 失败分诊 · USE-CTX-01-002 · github 上下文应报错

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status_not) — 预期 conclusion != COMPLETED，actual=COMPLETED
**根因初判**: 产品缺陷
**证据**: 日志 L5 `ref=placeholder_ref`。`${{ github.ref }}` 静默返回占位值。
**对照 GitCode 规格**: `context.md` 仅有 `atomgit` 上下文无 `github` 上下文。
**置信度**: 高

---

### 失败分诊 · USE-DISP-01-002 · dispatch 默认值

**判定结果**: FAIL
**失败断言**: assertions[0] (value) — 预期 log contains 'env=staging'，absent
**根因初判**: 产品缺陷
**证据**: 日志仅 1 行 duration check，零 shell 输出。dispatch 未应用 `default: staging`。
**对照 GitCode 规格**: `manually-trigger-pipeline.md` L21-22: dispatch inputs 支持 default 值。
**置信度**: 中

---

### 失败分诊 · USE-ENV-01-002 · GITHUB_SHA 无映射提示

**判定结果**: FAIL
**失败断言**: assertions[0] (status) — 预期 all green，actual job FAILED
**根因初判**: 产品缺陷
**证据**: 日志 L5 `GITHUB_SHA: unbound variable`。仅报 unbound variable，无 `GITHUB_* → ATOMGIT_*` 映射提示。
**置信度**: 高

---

### 失败分诊 · USE-EXPR-01-001 · 不存在属性应报错

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status_not) — 预期 conclusion != COMPLETED，actual=COMPLETED
**根因初判**: 产品缺陷
**证据**: 日志 L5 `val=`。`${{ atomgit.nonexistent }}` 静默求值为空字符串。
**置信度**: 高

---

### 失败分诊 · USE-INPT-01-002 · boolean input 应报错

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status_not) — 预期 conclusion != COMPLETED，actual=COMPLETED
**根因初判**: 产品缺陷
**证据**: 日志 L5 `dry_run=false`。boolean 被静默转为字符串。同 COMPAT-INPUTS-01-001。
**置信度**: 高

---

### 失败分诊 · USE-LOG-01-001 · 多 step 日志组织

**判定结果**: FAIL
**失败断言**: assertions[0] (value) — 预期 log contains 'step one prepare'，absent
**根因初判**: 用例问题
**证据**: 日志有 `prepare done`/`build done`/`test done` 等输出。断言查找 step name 而非 step output。
**置信度**: 高

---

### 失败分诊 · USE-MD-01-001 · ATOMGIT_STEP_SUMMARY

**判定结果**: FAIL
**失败断言**: assertions[0] (value) — 预期 log contains 'Test Report'，absent
**根因初判**: 编译缺口
**证据**: 日志无 shell 输出。`step_summary` target 退化为 `run_logs`。step summary 内容写入 UI 不在日志中。
**置信度**: 高

---

### 失败分诊 · USE-OS-01-001 · runner.os 大小写

**判定结果**: FAIL
**失败断言**: assertions[0] (value) — 预期 log contains 'os=Linux'，absent
**根因初判**: 产品缺陷
**证据**: 日志 L5 `os=linux`（小写）。`context.md` L223 声明 `Linux`（大写）。
**置信度**: 高

---

### 失败分诊 · USE-SECNAME-01-001 · ATOMGIT_ 前缀 secret

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status_not) — 预期 conclusion != COMPLETED，actual=COMPLETED
**根因初判**: 产品缺陷
**证据**: 日志 L5 `token=***`。`secrets.ATOMGIT_TOKEN` 被平台静默接受并脱敏输出。
**置信度**: 中

---

## 汇总

| 根因 | 数量 |
|---|---|
| 产品缺陷 | 11 |
| 编译缺口 | 3 |
| 用例问题 | 3 |
| 环境问题 | 3 |
