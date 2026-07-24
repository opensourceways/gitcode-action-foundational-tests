## 失败分诊 · REL-NEEDS-01-025 · needs 失败传播——上游 job 失败时下游 job 应被 skip

**判定结果**: FAIL
**失败断言**: 正向/job_a_status expected=failure actual=FAILED(满足); 正向/job_b_status expected=skipped actual=IGNORED

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（9 行）:
  ```
  === JOB: upstream failing job (status=FAILED) ===
  [2026/07/23 22:33:52.461] [INFO] Job(1529979891682521088_1529979891657355271) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c1c13e84-9d75-4ff3-b3ad-c9e88d6a8a55.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c1c13e84-9d75-4ff3-b3ad-c9e88d6a8a55.sh
  ::error::Process exited with code 1

  === JOB: downstream dependent job (status=IGNORED) ===
  ```

- **预期行为**（Phase 01 文本用例 REL-NEEDS-01-025，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤 1: 触发含 job_a(失败) 和 job_b(needs: job_a) 的 workflow
  - 预期结果: job_a 状态=failure; job_b 状态=skipped; job_b 不应执行

- **实际行为**:
  - job_a 正确失败（exit 1），状态 FAILED，满足预期
  - job_b 因 needs job_a 失败而未执行，状态为 IGNORED
  - 但断言期望 job_b 状态为 "skipped"，实际平台返回的是 "IGNORED"
  - 行为语义正确（needs 失败传播生效），但状态标签名不匹配

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/workflow-job-step-action.md`:
  - 无直接相关规格段落；GitHub Actions 中 needs 失败的下游 job 状态为 "skipped"，GitCode 平台使用 "IGNORED"

- **环境前置条件验证**: runner 可用，needs 依赖传播机制正常

**置信度**: 中 (行为正确但状态标签不匹配；可能是 GitCode 平台特有术语 "IGNORED" 替代了 GitHub Actions 的 "skipped")

**影响**:
- **阻塞性**: 🟡非阻塞 — needs 传播机制本身工作正常，只是状态标签不同
- **静默性**: 🟡可察觉 — 断言因标签名不匹配而失败
- **影响面**: 🟡同维度 — 影响所有检查 needs 传播状态的测试
- **综合**: 平台使用 "IGNORED" 而不是 "skipped" 表示 needs 未满足的 job，Phase 01 文本用例使用了 GitHub Actions 术语
- **是否有规避手段**: 是（断言中将 "skipped" 改为 "IGNORED" 以匹配平台术语）

**建议**:
- Phase 01 更新文本用例预期的 job_b 状态为 "IGNORED"（若为平台规范术语）
- 或平台方统一术语，将 "IGNORED" 改为 "skipped" 以兼容 GitHub Actions 生态
