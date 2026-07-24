## 失败分诊 · SEC-MASK-01-005 · Secret 日志脱敏不可通过多行值输出绕过

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain_secret "MULTI_LINE_SECRET" — 日志中无原值（形式通过但原因错误）
- positive, run_logs, equals "multiline_masked_with_asterisks" — 日志 0 字节输出，不匹配

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Test multiline masking (status=COMPLETED) ===
  [2026/07/23 22:07:29.425 GMT+08:00] [INFO] Job(1529973251784843264_1529973251751288839) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/53327f0a-5d6c-4192-bfb3-edea180675df.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/53327f0a-5d6c-4192-bfb3-edea180675df.sh

  ```

- **预期行为** (Phase 01 文本用例 SEC-MASK-01-005, 优先级 P0, 维度 security):
  - 前置条件: 仓库配置了多行 secret `MULTI_LINE_SECRET`
  - 操作步骤 1: 提交一个 workflow，直接 echo 多行 secret 到日志
  - 操作步骤 2: 触发 workflow 并查看运行日志
  - 预期结果: 多行 secret 的每一行在日志中均被脱敏；换行符不应成为脱敏边界

- **实际行为**:
  - `echo "${{ secrets.MULTI_LINE_SECRET }}"` 输出完全为空（0 字节）
  - `secrets.MULTI_LINE_SECRET` 在平台侧为空值
  - 无法验证多行脱敏引擎是否支持跨行匹配或整值匹配
  - 失败传导链: 单 job，无传导

- **对照 GitCode 规格** `security-permissions/using-secrets.md`:
  - 第 66 行: "日志遮掩 | Secret 值在日志中自动替换为 `***`"

- **环境前置条件验证**: YAML `setup.secrets: ["MULTI_LINE_SECRET"]`，secret 已声明。无 `config_probe` 步骤。输出 0 字节，说明 secret 未配置或值为空。

**置信度**: 高 (0 字节输出强烈指示 secret 值为空)

**影响**:
- **阻塞性**: 🔴阻塞 — 多行脱敏验证完全无法执行
- **静默性**: 🔴静默错误 — 空输出与脱敏后的 `***` 无法区分
- **影响面**: 🟡同维度 — 同系列 SEC-MASK-01-001/002 同样受影响
- **综合**: MULTI_LINE_SECRET 在平台侧为空，多行脱敏引擎的跨行匹配能力无法测试
- **是否有规避手段**: 是

**建议**:
- 在平台侧创建 `MULTI_LINE_SECRET`，值为多行文本（如 "line1\nline2\nline3"）
- 测试 YAML 添加 config_probe：`echo "line_count:${{ secrets.MULTI_LINE_SECRET }}" | wc -l` 验证多行值存在
- 考虑到无 config_probe，建议优先修复所有 secret 依赖用例的环境前置条件
