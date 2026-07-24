# Failure Analyst · SEC FAIL Cases · 2026-07-24-valid297-final

Run: `2026-07-24-valid297-final` | Analyzed: 2026-07-24 19:13

---

## 摘要分类

| 分类 | 数量 | 案例 |
|---|---|---|
| **用例问题** (断言/触发/fixture) | 16 | SEC-ARTF-01-002, SEC-BASE-01-001, SEC-BASE-01-002, SEC-CACHE-01-002, SEC-DOS-01-001, SEC-INJ-01-005, SEC-MASK-01-001, SEC-MASK-01-005, SEC-NAME-01-001, SEC-NAME-01-002, SEC-PERM-01-003, SEC-PERM-01-004, SEC-SUPPLY-01-001, SEC-SUPPLY-01-002, SEC-TOCTOU-01-001, SEC-WCMD-01-001 |
| **产品缺陷** | 1 | SEC-SIDE-01-002 |
| **需人工判断** (token auth gap) | 2 | SEC-DEFPERM-01-001, SEC-WCMD-01-002 |

---

## 失败分诊 · SEC-ARTF-01-002 · 跨仓库 artifact 下载返回 403 或 404

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains '403_or_404'`，实际 `absent`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:13:09.656 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  000{"error_code":400,"error_code_name":"BAD_REQUEST","error_message":"参数类型错误","trace_id":"131d9774cf6cddfe8bcfff96672c0544"}400
  ```
- **预期行为**（YAML）: `must_not_contain: "200"` + `equals: "403_or_404"` — 期望跨仓库下载被 403/404 拒绝
- **实际行为**: 平台返回 HTTP 400 (BAD_REQUEST, "参数类型错误")，而非 403 或 404。平台确实拒绝了请求，但错误码不同。leak 断言（不出现 200）PASS。
- **对照 GitCode 规格**: token-permissions.md 未定义 artifact 跨仓库访问的具体错误码映射。

**置信度**: 高 — 错误码偏差（400 vs 期望的 403/404），断言 sentinel 字符串过于具体。

---

## 失败分诊 · SEC-BASE-01-001 · pull_request_target 使用 base 分支的 workflow 版本

**判定结果**: FAIL
**失败断言**: assertions[0] (value, run_logs) — 预期 `log contains 'base_branch_workflow_executed'`，实际 `absent`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:13:22.116 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  Executing base branch workflow
  ```
- **预期行为**（YAML）: `equals: "base_branch_workflow_executed"` — 期望日志中出现此哨兵字符串
- **实际行为**: 步骤输出了 "Executing base branch workflow"（正确行为），但不包含哨兵字符串 `base_branch_workflow_executed`。leak 断言（不出现 fork_injected_step）PASS。
- **对照 GitCode 规格**: pr-mr-pipeline-security.md 明确 `pull_request_target` 使用目标仓库代码（base 分支 workflow 版本）。实际行为符合规格。

**置信度**: 高 — 哨兵字符串与步骤实际输出不匹配。

---

## 失败分诊 · SEC-BASE-01-002 · fork PR 改 workflow 不被 pull_request_target 采用

**判定结果**: FAIL
**失败断言**: assertions[1] (run_status, run_status) — 预期 `SUCCESS_WITH_BASE_WORKFLOW`，实际 `COMPLETED`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:14:19.931 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  Only base steps run
  ```
- **预期行为**（YAML）: `target: run_status, equals: "success_with_base_workflow"` — 期望自定义 run_status 值
- **实际行为**: 步骤正确输出 "Only base steps run"，run_status 为标准的 `COMPLETED`。哨兵 `success_or_yaml_error` 在 YAML 但 JSON 断言显示 `SUCCESS_WITH_BASE_WORKFLOW`，两者都不是有效的 GitCode run_status 值。
- **对照 GitCode 规格**: pr-mr-pipeline-security.md §pull_request_target — workflow 使用目标仓库版本。

**置信度**: 高 — 断言使用的 run_status 值并非平台标准状态枚举值。

---

## 失败分诊 · SEC-CACHE-01-002 · 主仓 cache restore 对 fork cache miss

**判定结果**: FAIL
**失败断言**: assertions[0] (value, run_logs) — 预期 `log contains 'cache_miss'`，实际 `absent`

**根因初判**: 环境问题 / 用例问题

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:14:27.368 GMT+08:00] [INFO] Job(...) duration check: true
  ::warning::Event Validation Error: The event type Manual (normalized: manual) is not supported because it's not tied to a branch or tag ref.
  ::warning::[cache eventValidation] normalized=manual allowlistMatch=false allowlist=[push|pull_request|merge_request] ...
  ```
- **预期行为**（YAML）: `uses: cache` → 期望 cache restore 时出现 `cache_miss`
- **实际行为**: cache action 因触发事件类型不匹配完全未执行。GitCode cache 系统的 allowlist 仅支持 `[push|pull_request|merge_request]`，而用例用 `workflow_dispatch` (Manual) 触发。
- **对照 GitCode 规格**: 无 cache event filter 明确文档。但从 warning 可推断平台对 cache 的 event 限制。

**置信度**: 高 — cache 系统不支持 workflow_dispatch 触发；用例触发方式与 cache 系统不兼容。

---

## 失败分诊 · SEC-DEFPERM-01-001 · ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains '403_or_permission_denied'`，实际 `absent`

**根因初判**: 需人工判断 (token 认证异常)

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:14:48.252 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  000{"error_code":401,"error_code_name":"UNAUTHORIZED","error_message":"401, token not found","trace_id":"08573a375ec34186040dc88d7db1e2a3"}401000000::error::Process exited with code 6
  ```
- **预期行为**（YAML）: `permissions: { repository: read }` + 调用 `${{ atomgit.token }}` 发起写操作 → 期望 403/Permission Denied
- **实际行为**: 收到 401 UNAUTHORIZED "token not found"。不是权限不足(403)，而是 token 本身未被平台识别。leak 断言（不出现 write_successful）PASS。
- **对照 GitCode 规格**: token-permissions.md 声明 `顶层声明 permissions | 所有 job 继承顶层权限`。预期 token 可用但权限受限。401 表示 token 可能未正确注入。

**置信度**: 中 — 401 vs 403 的差异可能是平台 token 注入机制问题（产品缺陷），也可能是测试仓库 token 配置不完整（环境问题）。需 leader 核实 token 在 permissions: {repository: read} 下是否应可用。

---

## 失败分诊 · SEC-DOS-01-001 · 大 artifact / 大 cache 必须受配额与边界限制

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains 'size_limit_exceeded_error'`，实际 `absent`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量** (30 lines, 关键行):
  - L5-7: 1.2GB 文件成功创建（`1153433600 bytes ... copied`）
  - L10-25: Zip 压缩后仅 ~1MB，上传尝试
  - L30: `::error::Upload artifact failed: Artifact with name already exists: large-artifact, repoId=10431336, workflowId=ba5629eb6c374fb6a43202d0cf9c6aba`
- **预期行为**（YAML）: 上传 1100MB 文件 → 期望 `size_limit_exceeded_error`
- **实际行为**: 1.2GB 源文件被压缩到 ~1MB zip（零字节压缩），上传失败原因是 **artifact 名称冲突（already exists）**，而非大小限制。大小配额检查从未被执行。
- **对照 GitCode 规格**: 未定义 artifact 大小限制。名称冲突先于大小检查触发了失败。

**置信度**: 高 — 名称冲突导致测试无法触达大小配额检查逻辑；用例需使用唯一 artifact 名。

---

## 失败分诊 · SEC-INJ-01-005 · 表达式求值必须防止双重模板渲染（二次求值）

**判定结果**: FAIL
**失败断言**: assertions[0] (leak, run_logs) — 预期 `plaintext '2' 0 hits`，实际 `FOUND`；assertions[1] (value, run_logs) — 预期 `log contains 'template_chars_escaped'`，实际 `absent`

**根因初判**: 用例问题（单字符 leak 模式在时间戳上误匹配）

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:16:37.644 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  /home/slave1/runner/workers/.../xxx.sh: line 1: Input: ${{ '{{ 1 + 1 }}' }}: bad substitution
  ::error::Process exited with code 1
  ```
- **预期行为**（YAML）: `must_not_contain: "2"` — 期望双重模板渲染不发生（2 = 1+1 不应出现）；`equals: "template_chars_escaped"` — 期望模板字符被转义
- **实际行为**: bash 抛出 `bad substitution` 错误，表达式 `{{ 1 + 1 }}` 未被求值。leak 检测的 "2" **来自日志时间戳中的日期数字**（`2026/07/24`），而非来自表达式求值。模板渲染实际上被阻止（bash 报错），哨兵 `template_chars_escaped` 不匹配因步骤输出为 bash error。
- **对照 GitCode 规格**: 无直接相关文档。

**置信度**: 高 — 单字符 leak pattern `"2"` 匹配到时间戳 `24` 中的 `2`，为误报。双重模板实际未发生（bash 报 bad substitution）。

---

## 失败分诊 · SEC-MASK-01-001 · Secret 值在运行日志中必须被自动脱敏为 ***

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains 'masked_with_asterisks'`，实际 `absent`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:16:48.629 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  The secret is 
  ```
- **预期行为**（YAML）: `equals: "masked_with_asterisks"` — 期望日志中出现此哨兵
- **实际行为**: 日志显示 "The secret is " 后为空（secret 值已被平台脱敏/移除，不在日志中显示）。config_probe PASS（secret 已配置）。哨兵字符串 `masked_with_asterisks` 是断言专用标记，步骤并不输出。
- **对照 GitCode 规格**: using-secrets.md 明确 "Secret 值在日志中自动替换为 `***`"。

**置信度**: 高 — secret 实际已被脱敏（日志中值为空），断言依赖步骤不输出的哨兵字符串。

---

## 失败分诊 · SEC-MASK-01-005 · Secret 日志脱敏不可通过多行值输出绕过

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains 'multiline_masked_with_asterisks'`，实际 `absent`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:18:04.869 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  (empty line 5)
  ```
- **预期行为**（YAML）: `equals: "multiline_masked_with_asterisks"` — 期望哨兵
- **实际行为**: 步骤执行后日志仅有一空行（secret 值被完全脱敏）。config_probe PASS。
- **对照 GitCode 规格**: using-secrets.md — 日志遮掩机制。同 SEC-MASK-01-001 模式。

**置信度**: 高 — 哨兵字符串不匹配，secret 实际表现符合脱敏预期。

---

## 失败分诊 · SEC-NAME-01-001 · Secret/变量名含特殊字符时不可导致意外求值或权限绕过

**判定结果**: FAIL
**失败断言**: assertions[1] (run_status, run_status) — 预期 `SUCCESS_OR_YAML_ERROR`，实际 `COMPLETED`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:18:26.619 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  value is 
  ```
- **预期行为**（YAML）: `equals: "success_or_yaml_error"` — 期望自定义 run_status
- **实际行为**: `${{ secrets.MY-VAR }}` 的值为空（"value is " 后无内容），含连字符的 secret 名可能无法正常解析。但 run_status 为标准 `COMPLETED`。断言期望的自定义状态值不是平台标准枚举。
- **对照 GitCode 规格**: using-secrets.md — Secret 名称规则："仅允许大写字母、数字和下划线"。**MY-VAR 含连字符，违反 Secret 命名规范。**

**置信度**: 高 — secret 名称 `MY-VAR` 含连字符违反 GitCode 规格的 secret 命名规则（仅允许大写字母、数字、下划线）。另，断言 run_status 值为非标准枚举。

---

## 失败分诊 · SEC-NAME-01-002 · 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains 'masked_or_not_found'`，实际 `absent`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量** (12 lines):
  ```
  L1: [2026/07/24 17:18:37.285 GMT+08:00] [INFO] Job(...) duration check: true
  L2: No shell specified, using platform default: default-bash
  L3: ::debug::Script file created: ...
  L4: ::debug::Executing: bash -e ...
  L5: INPUT_SCHEDULER_ACTION_PARAMS={"working-directory":"","script":"printenv | grep API_KEY || echo not found\n"...}
  L6: INPUT_SCRIPT=printenv | grep API_KEY || echo not found
  L7-9: (second step debug lines)
  L10: ::debug::Executing: bash -e ...
  L11: INPUT_SCHEDULER_ACTION_PARAMS={..."script":"cat /proc/self/environ | tr '\\0' '\\n' | grep API_KEY || echo not found\n"...}
  L12: INPUT_SCRIPT=cat /proc/self/environ | tr '\0' '\n' | grep API_KEY || echo not found
  ```
- **预期行为**（YAML）: `printenv | grep API_KEY || echo not found` + `cat /proc/self/environ | tr '\0' '\n' | grep API_KEY || echo not found` + `equals: "masked_or_not_found"`
- **实际行为**: 日志仅捕获了 `official_shell` action 的参数回显（INPUT_SCRIPT），但 **步骤的实际 stdout（grep 结果 / echo not found）未出现在日志中**。哨兵 `masked_or_not_found` 不匹配。
- **对照 GitCode 规格**: using-secrets.md — 日志遮掩机制。

**置信度**: 中 — 可能有两种原因：(a) 哨兵字符串不匹配（用例问题）；(b) 子脚本 stdout 未被日志采集系统捕获（环境/采集问题）。需检查日志采集是否覆盖 action 子进程输出。

---

## 失败分诊 · SEC-PERM-01-003 · 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only）

**判定结果**: FAIL
**失败断言**: assertions[1] (run_status, run_status) — 预期 `COMPLETED`，实际 `FAILED`

**根因初判**: 用例问题（bash -e + 401 导致非预期失败）

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:18:58.916 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  000{"error_code":401,"error_code_name":"UNAUTHORIZED","error_message":"401, token not found","trace_id":"a881a829ca1e8b974b3ec68ea3b88da6"}401000000::error::Process exited with code 6
  ```
- **预期行为**（YAML）: 不声明 `permissions` → 用默认权限 → curl POST 写操作 → 期望被拒绝但 run_status=COMPLETED
- **实际行为**: curl 收到 401 "token not found"，bash -e 模式导致脚本以 code 6 退出，run_status=FAILED。leak 断言（不出现 write_permission_granted）PASS。
- **对照 GitCode 规格**: token-permissions.md — `未声明 permissions | 使用仓库设置中定义的权限`。默认应至少有 read 权限，token 应可用。401 "token not found" 与 SEC-DEFPERM-01-001 相同的异常模式。

**置信度**: 中 — 两重问题：(a) 用例应当预期 curl 非 200 返回，不应在 `bash -e` 下直接依赖 curl 返回码（用例问题）；(b) 401 "token not found" 而非预期的 403 权限拒绝 — 与 SEC-DEFPERM-01-001 相同异常，需 leader 判断是 token 注入机制问题还是环境配置问题。

---

## 失败分诊 · SEC-PERM-01-004 · 默认状态下写操作被 403 拒绝

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains 'push_denied_or_403'`，实际 `absent`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量** (19 lines):
  ```
  L1-4: Job start + debug lines
  L5: Cloning into 'repo'...
  L6: Author identity unknown
  L7-18: git config error messages ("Please tell me who you are...")
  L19: ::error::Process exited with code 128
  ```
- **预期行为**（YAML）: git clone → git push → 期望 push 被 403 拒绝，输出 "push denied as expected"
- **实际行为**: git commit 在 push 前因 **git user.email/name 未配置** 而失败（`fatal: unable to auto-detect email address`），测试从未到达 push 步骤。leak 断言（不出现 push_successful）PASS，但这只是因为 push 根本未执行。
- **对照 GitCode 规格**: 无相关 git config 要求文档。

**置信度**: 高 — git 未配置 user identity 导致 commit 失败，测试无法触达目标断言（push 权限检查）。

---

## 失败分诊 · SEC-SIDE-01-002 · Secret 不经 artifact 侧信道绕过脱敏外泄

**判定结果**: FAIL
**失败断言**: assertions[1] (run_status, run_status) — 预期 `BLOCKED_OR_MASKED`，实际 `COMPLETED`

**根因初判**: 产品缺陷

**证据**:
- **Job 日志全量** (35 lines, 关键行):
  ```
  L22: Creating artifact "secret-artifact" (size: 143 bytes, workflow: ...)
  L24: Artifact created with ID 206339954610176, upload mode: simple
  L26: Upload complete. SHA-256: 24d234151974d9446ea9e940340600f746fbc39e8fcb679bb416f56bc2f013ef
  L29: Artifact "secret-artifact" finalized successfully.
  L34: Artifact "secret-artifact" uploaded successfully. ID: 206339954610176, Size: 143 bytes
  L35: Artifact portal URL: https://gitcode.com/ComputingActionTest/gitcode-test-4/actions/artifacts/206339954610176
  ```
- **预期行为**（YAML）: `echo "token=${{ secrets.DEPLOY_TOKEN }}" > secret.txt` → upload artifact → 期望 `artifact_content` 不含 secret 或 `run_status = blocked_or_masked`
- **实际行为**: 包含 secret 值的文件 **成功上传为 artifact** (ID 206339954610176)，run_status=COMPLETED。平台未在 artifact 上传阶段检测/阻止/脱敏包含 secret 的文件。config_probe PASS（secret 已配置）。
- **对照 GitCode 规格**: using-secrets.md 描述的安全机制包括日志遮掩、不可查看、Fork 隔离、环境审批，但 **未提及 artifact 内容扫描或 secret 泄露阻断**。此项可能是规格未覆盖的安全缺口。

**置信度**: 高 — 日志清晰显示 artifact 上传成功；平台未对 artifact 内容做 secret 扫描。这是真实的安全侧信道。（但需 leader 确认：GitCode 规格中是否定义了 artifact 侧信道防护；若无，此缺口属「平台未实现」而非「平台实现错误」。）

---

## 失败分诊 · SEC-SUPPLY-01-001 · 第三方 Action 引用应支持完整 commit hash 固定

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status, run_status) — 预期 `SUCCESS_OR_ACTION_EXECUTED`，实际 `FAILED`

**根因初判**: 用例问题 / 环境问题

**证据**:
- **Job 日志全量** (1 line):
  ```
  [2026/07/24 17:21:17.580 GMT+08:00] [INFO] Job(1530263615489974272_1530263615456419847) duration check: true
  ```
- **预期行为**（YAML）: `uses: docker/build-push-action@1234567890abcdef1234567890abcdef12345678` → 期望 action 被执行或拒绝但 run_status=SUCCESS_OR_ACTION_EXECUTED
- **实际行为**: 日志仅 1 行（duration check），无任何 action 解析/下载/执行日志。run_status=FAILED。leak 断言（不出现 unauthorized_action_execution）PASS，但这是因为 action 根本没执行。
- **对照 GitCode 规格**: 无第三方 action commit pinning 的明确规格。

**置信度**: 中 — 日志近乎空（仅 1 行），无法判断是 action 解析失败无日志、还是日志采集缺失。与 SEC-SUPPLY-01-002 相同模式。

---

## 失败分诊 · SEC-SUPPLY-01-002 · commit hash 不匹配时第三方 Action 应被拒绝执行

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains 'action_not_found_or_sha_mismatch'`，实际 `absent`

**根因初判**: 用例问题 / 环境问题

**证据**:
- **Job 日志全量** (1 line):
  ```
  [2026/07/24 17:22:00.516 GMT+08:00] [INFO] Job(1530263795782004736_1530263795761033221) duration check: true
  ```
- **预期行为**（YAML）: `uses: docker/build-push-action@0000000000000000000000000000000000000000` → 期望出现 `action_not_found_or_sha_mismatch`
- **实际行为**: 日志仅 1 行，无任何 action 解析错误信息。leak 断言（不出现 success）PASS。与 SEC-SUPPLY-01-001 相同：action 解析过程无日志输出。
- **对照 GitCode 规格**: 无 commit hash 校验的明确规格。

**置信度**: 中 — 无法判断是平台不输出 action 解析错误，还是日志采集遗漏了该阶段输出。两例均为单行空日志，强烈暗示日志采集问题。

---

## 失败分诊 · SEC-TOCTOU-01-001 · 审批后推送新 commit 不应被已授权特权运行执行

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains 'approved_sha_matched'`，实际 `absent`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:22:12.676 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  Running commit: 
  ```
- **预期行为**（YAML）: `echo "Running commit: ${{ atomgit.sha }}"` → 期望 `approved_sha_matched`
- **实际行为**: `atomgit.sha` 在 workflow_dispatch 上下文中为空。步骤输出了 "Running commit: " 而非哨兵。leak 断言 PASS。
- **对照 GitCode 规格**: 无 workflow_dispatch 下 atomgit.sha 行为的明确文档。

**置信度**: 高 — 哨兵不匹配 + `atomgit.sha` 在 workflow_dispatch 事件下为空（需 git ref 事件才有 SHA）。

---

## 失败分诊 · SEC-WCMD-01-001 · Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值

**判定结果**: FAIL
**失败断言**: assertions[1] (value, run_logs) — 预期 `log contains 'mask_command_without_payload'`，实际 `absent`

**根因初判**: 用例问题

**证据**:
- **Job 日志全量**:
  ```
  [2026/07/24 17:22:53.273 GMT+08:00] [INFO] Job(...) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: ...
  ::debug::Executing: bash -e ...
  ::add-mask::
  ```
- **预期行为**（YAML）: `echo "::add-mask::${{ secrets.API_KEY }}"` → `must_not_contain_secret: "API_KEY"` + `equals: "mask_command_without_payload"`
- **实际行为**: 日志显示 `::add-mask::` — secret 值已被平台在 add-mask 命令输出前脱敏（为空），platform 正确防御了 secret 泄露。但哨兵 `mask_command_without_payload` 不匹配步骤输出。config_probe PASS。
- **对照 GitCode 规格**: using-secrets.md — 日志遮掩机制。

**置信度**: 高 — secret 值已被脱敏（add-mask 参数为空），哨兵不匹配。

---

## 失败分诊 · SEC-WCMD-01-002 · 跨运行 artifact 必须被视为不可信数据

**判定结果**: FAIL
**失败断言**: assertions[1] (run_status, run_status) — 预期 `COMPLETED`，实际 `FAILED`

**根因初判**: 需人工判断 / 用例问题

**证据**:
- **Job 日志全量** (12 lines):
  ```
  L1: [2026/07/24 17:23:04.199 GMT+08:00] [INFO] Job(...) duration check: true
  L2: ::debug::run-id input: '' (length: 0)
  L6: Downloading single artifact
  L7: ::debug::Listing artifacts for workflow e1a87059abb6433e8824fd994031f936 with name filter "untrusted-artifact"
  L9: ::debug::Found 0 artifact(s)
  L10: ::error::Unable to download artifact(s): Artifact 'untrusted-artifact' not found. Available artifacts: (none)
  ```
- **预期行为**（YAML）: `uses: download-artifact, name: untrusted-artifact` → 期望下载成功但不自动执行 → run_status=COMPLETED
- **实际行为**: artifact `untrusted-artifact` 不存在（0 artifacts found），download-artifact action 报错退出。leak 断言（不出现 auto_executed）PASS。
- **对照 GitCode 规格**: 无 artifact trust boundary 相关文档。

**置信度**: 中 — 测试依赖前置 artifact `untrusted-artifact` 存在，但当前运行前未创建。artifact not found 导致 job FAILED 是预期中的环境缺失，不影响安全性判断。但断言期望 COMPLETED 不合理——artifact 缺失不应视为测试通过。需确认：(a) 是否应在前置步骤创建 artifact；(b) download-artifact 缺失时是否应优雅降级。

---

## 汇总模式

### 用例共性问题（高频）

| 模式 | 命中案例 | 说明 |
|---|---|---|
| **哨兵字符串不匹配** | SEC-ARTF-01-002, SEC-BASE-01-001, SEC-MASK-01-001, SEC-MASK-01-005, SEC-NAME-01-002, SEC-TOCTOU-01-001, SEC-WCMD-01-001, 等多个 | 断言期望的 magic string 未在步骤中输出；步骤行为正确但 sentinel 不匹配 |
| **自定义 run_status 非标准枚举** | SEC-BASE-01-002, SEC-NAME-01-001, SEC-SIDE-01-002, SEC-SUPPLY-01-001 | 断言使用 `SUCCESS_WITH_BASE_WORKFLOW`, `BLOCKED_OR_MASKED` 等非平台标准 run_status |
| **bash -e 导致预期错误变失败** | SEC-DEFPERM-01-001, SEC-PERM-01-003 | curl 返回非 200 → bash -e 退出非零 → FAILED；应处理预期错误码 |
| **git 未配置 user 导致无法到达断言** | SEC-PERM-01-004 | commit 前缺 git config |
| **单字符 leak 模式误匹配** | SEC-INJ-01-005 | `must_not_contain: "2"` 匹配到时间戳数字 |
| **日志近乎空/仅 1 行** | SEC-SUPPLY-01-001, SEC-SUPPLY-01-002 | action 解析阶段无日志输出；疑似日志采集缺口 |

### 值得关注的产品行为

| 案例 | 现象 | 说明 |
|---|---|---|
| SEC-DEFPERM-01-001, SEC-PERM-01-003 | 401 "token not found" 而非 403 | 权限受限/未声明时 token 完全不可用——可能违反"至少 read"的预期 |
| SEC-SIDE-01-002 | 含 secret 文件成功上传为 artifact | 无 artifact 内容扫描——真实侧信道泄露 |
| SEC-CACHE-01-002 | cache 仅支持 push/PR/MR 事件 | 平台限制但无文档 → 用例不兼容 |
