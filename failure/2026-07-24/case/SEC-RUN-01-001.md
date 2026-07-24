## 失败分诊 · SEC-RUN-01-001 · Job 结束后 workspace 与临时文件必须被彻底清理

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "residual found" — 无残留文件（通过）
- positive, run_logs, equals "cleaned_as_expected" — 实际文本为 `cleaned as expected`（空格），不匹配下划线格式

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量** (13 行):
  ```
  === JOB: Write sensitive file (status=COMPLETED) ===
  [2026/07/23 22:09:32.440 GMT+08:00] [INFO] Job(1529973767860523008_1529973767831162887) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/2be5f0a1-d517-487d-b657-77309a59054d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/2be5f0a1-d517-487d-b657-77309a59054d.sh
  
  
  === JOB: Check cleanup (status=COMPLETED) ===
  [2026/07/23 22:09:32.455 GMT+08:00] [INFO] Job(1529973767860523008_1529973767835357185) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0a3ef073-dbb1-4a4c-834c-628811a1ed80.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0a3ef073-dbb1-4a4c-834c-628811a1ed80.sh
  cleaned as expected
  ```

- **预期行为** (Phase 01 文本用例 SEC-RUN-01-001, 优先级 P0, 维度 security):
  - 前置条件: 仓库支持多 job workflow
  - 操作步骤 1: 提交一个多 job workflow，job A 写入敏感临时文件
  - 操作步骤 2: job B 检查是否存在 job A 的残留文件
  - 预期结果: job B 绝不应读取到 job A 残留的敏感文件；即使 job A 异常崩溃，清理钩子仍应执行

- **实际行为**:
  - Job A: 成功写入 `/tmp/sensitive-temp.txt`（6-7 行为空行，写入操作无输出）
  - Job B: 输出 `cleaned as expected` — 确认 `/tmp/sensitive-temp.txt` 不存在
  - **平台功能正确**: 跨 job workspace/tmp 清理机制正常工作，job B 未发现残留
  - **断言格式差异**: 日志实际输出 `cleaned as expected`（空格），断言期望 `cleaned_as_expected`（下划线）

- **对照 GitCode 规格** `core-concepts/workflow-job-step-action.md`:
  - 第 N-M 行: "每个 job 运行在独立的 runner 节点或经过清理的环境" (预期间接引用)

- **环境前置条件验证**: YAML `setup.repo_fixture: default`, 无 secrets, 无 config_probe, 无 fault_injection。跨 job 清理机制运行正常。

**置信度**: 高 (平台功能正确，仅断言字符串格式不匹配)

**影响**:
- **阻塞性**: ⚪无影响 — 平台清理功能正确，job B 确认无残留
- **静默性**: 🟢明确报错 — "cleaned as expected" 明确传达了清理成功
- **影响面**: 🟢单用例 — 仅断言格式需调整
- **综合**: 平台补函数正确清理了跨 job 的 `/tmp` 残留；断言应使用空格格式而非下划线
- **是否有规避手段**: 是

**建议**:
- 修正 Phase 01 断言: `cleaned_as_expected` → `cleaned as expected`
- 考虑增强测试：在 job A 中故意 `exit 1` 崩溃后验证 job B 仍无残留（崩溃清理钩子验证）
