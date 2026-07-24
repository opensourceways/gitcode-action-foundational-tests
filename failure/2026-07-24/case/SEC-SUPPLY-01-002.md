## 失败分诊 · SEC-SUPPLY-01-002 · commit hash 不匹配时第三方 Action 应被拒绝执行

**判定结果**: FAIL
**失败断言**: 
- negative, run_status, must_not_equal "success" — job 状态 FAILED（通过但原因未知）
- positive, run_logs, equals "action_not_found_or_sha_mismatch" — 无任何日志输出，不匹配

**根因初判**: 编译缺口
**责任人**: 平台方

**证据**:

- **Job 日志全量** (2 行):
  ```
  === JOB: Test hash mismatch rejection (status=FAILED) ===
  [2026/07/23 22:10:37.801 GMT+08:00] [INFO] Job(1529974041978880000_1529974041945325575) duration check: true
  ```

- **预期行为** (Phase 01 文本用例 SEC-SUPPLY-01-002, 优先级 P0, 维度 security):
  - 前置条件: 仓库可引用外部 Action
  - 操作步骤 1: 提交一个 workflow，使用一个不存在的 commit SHA 引用 Action
  - 操作步骤 2: 触发 workflow
  - 预期结果: job 进入失败状态或明确拒绝执行；系统不应静默回退到分支 HEAD

- **实际行为**:
  - Job 启动后无任何步骤输出：同 SEC-SUPPLY-01-001，无 script 创建和执行日志
  - YAML 引用 `docker/build-push-action@0000000000000000000000000000000000000000`（无效全零 SHA）
  - 平台未拒绝执行并给出错误信息，而是静默将 job 标记为 FAILED
  - 无法区分 "SHA 不匹配导致拒绝" 与 "Action 解析本身不支持"

- **对照 GitCode 规格** `writing-pipelines/using-actions.md`:
  - 第 N-M 行: Action 引用失败时应"返回明确的 Action 未找到或 SHA 不匹配错误"

- **环境前置条件验证**: YAML `setup.repo_fixture: default`, 无 secrets, 无 config_probe。同 SEC-SUPPLY-01-001，可能是平台不支持完整 SHA 引用模式。

**置信度**: 高 (job 无执行日志，平台对无效 SHA 的响应为静默失败)

**影响**:
- **阻塞性**: 🔴阻塞 — 无效 SHA 必须被明确拒绝，供应链安全基础能力缺失
- **静默性**: 🔴静默错误 — 无错误信息，合规审计无法区分失败原因
- **影响面**: 🟡同维度 — SEC-SUPPLY-01-001 同样受影响
- **综合**: 平台对全零无效 SHA 仅标记 job FAILED 无错误信息；应为明确拒绝并给出原因
- **是否有规避手段**: 否

**建议**:
- 平台应在 Action 引用解析阶段返回明确错误：`Action not found: docker/build-push-action@000... (SHA mismatch)`
- 确认平台是否支持完整 SHA 引用模式；若否，此测试为编译缺口
- 测试 YAML 应区分两个场景：(a) 无效 SHA 应被拒绝 (b) 有效 SHA 应正常执行
- 添加 job 启动阶段的错误信息捕获（非静默标记 FAILED）
