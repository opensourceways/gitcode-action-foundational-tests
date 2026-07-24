## 失败分诊 · REL-MATRIX-01-039 · 大规模 matrix——50 个组合应全部生成并正确调度

**判定结果**: FAIL
**失败断言**: 正向/generated_jobs_count expected=50 actual=所有50个job因bad substitution失败; 非功能/scheduling_latency_seconds ≤300 actual=无法验证

**根因初判**: 标记不匹配
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（451 行，摘要）:
  ```
  === JOB: matrix 50 combos test (status=FAILED) ===
  [2026/07/23 22:32:53.743] [INFO] Job(1529979624610467840_1529979624618856486) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/bc0a3896-6449-4bde-abd5-4b3ad88d8a81.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/bc0a3896-6449-4bde-abd5-4b3ad88d8a81.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/bc0a3896-6449-4bde-abd5-4b3ad88d8a81.sh: line 1: v1=${{{{ matrix.v1 }}}}: bad substitution
  ::error::Process exited with code 1
  ```
  *(以上模式重复 50 次，每次不同的 job ID 但相同的 `bad substitution` 错误)*

- **预期行为**（Phase 01 文本用例 REL-MATRIX-01-039，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤 1: 触发含 5 维×10 值=50 组合的 matrix workflow
  - 预期结果: 50 个 jobs 全部生成; 无重复/遗漏组合; 调度时延 ≤300 秒

- **实际行为**:
  - 50 个 matrix job 被正确生成并调度
  - 所有 50 个 job 在脚本执行时失败：`v1=${{{{ matrix.v1 }}}}: bad substitution`
  - 与 REL-ARTCONC-01-063、REL-MATRIX-01-038 完全相同的根因：四重花括号被 bash 解释为非法替换

- **对照 GitCode 规格**:
  - 无直接相关规格段落；此为 YAML 模板转义错误

- **环境前置条件验证**: matrix 展开正确（50 个 job 生成），说明 platform 调度能力正常

**置信度**: 高 (bad substitution 错误与 REL-ARTCONC-01-063、REL-MATRIX-01-038 模式完全一致)

**影响**:
- **阻塞性**: 🔴阻塞 — 所有 50 个 matrix job 失败
- **静默性**: 🟢明确报错 — `bad substitution` 明确提示
- **影响面**: 🔴跨维度 — 影响所有 `{{{{ }}}}` 模板用例
- **综合**: 50 个 job 全部因四重花括号 bad substitution 失败，matrix 生成和调度本身正常
- **是否有规避手段**: 是（修正 YAML 模板中所有 `{{{{ }}}}` 为 `${{ }}`）

**建议**:
- 同 REL-MATRIX-01-038，统一修正 Phase 02 YAML 模板的表达式转义
- 可能还需检查 Phase 02 中 `{{{{ }}}}` 是否有特定语义（如字面量转义），若有则应通过模板引擎正确处理
