## 失败分诊 · SEC-WCMD-01-001 · Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain_secret "API_KEY" — 日志无 API_KEY 明文（通过）
- positive, run_logs, equals "mask_command_without_payload" — 实际输出 `::add-mask::` 后为空，不匹配

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Test add-mask response (status=COMPLETED) ===
  [2026/07/23 22:10:58.623 GMT+08:00] [INFO] Job(1529974129308864512_1529974129283698695) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/d93eaaec-61d4-49e4-8d50-dad75070df4d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/d93eaaec-61d4-49e4-8d50-dad75070df4d.sh
  ::add-mask::
  ```

- **预期行为** (Phase 01 文本用例 SEC-WCMD-01-001, 优先级 P0, 维度 security):
  - 前置条件: 仓库配置了 secret `API_KEY`
  - 操作步骤 1: 提交一个 workflow，执行 add-mask 命令遮蔽 secret
  - 操作步骤 2: 触发 workflow 并查看日志中命令的响应
  - 预期结果: workflow 命令的响应中绝不应包含被遮蔽前的 secret 原值；命令执行日志应仅显示命令骨架，不含 payload

- **实际行为**:
  - `echo "::add-mask::${{ secrets.API_KEY }}"` 输出 `::add-mask::` 后为空
  - `secrets.API_KEY` 展开为空值，故 `::add-mask::` 命令无 payload
  - 平台日志仅显示 `::add-mask::`（命令骨架），符合预期
  - 但无法验证当 API_KEY 有值时，命令响应中是否包含原值

- **对照 GitCode 规格** `syntax-reference/workflow-commands.md`:
  - 第 N-M 行: "::add-mask:: 命令用于在工作流日志中遮蔽值"（工作流命令应被平台处理，不在日志中显示 payload）

- **环境前置条件验证**: YAML `setup.secrets: ["API_KEY"]`。无 config_probe。`secrets.API_KEY` 为空导致 `::add-mask::` 无 payload，无法验证命令响应是否泄露原值。

**置信度**: 中 (secret 值为空，但命令骨架无 payload 泄露是正向信号)

**影响**:
- **阻塞性**: 🔴阻塞 — 无法验证 add-mask 命令响应是否泄露 secret 原值
- **静默性**: 🔴静默错误 — 空 payload 与遮蔽成功的显示无法区分
- **影响面**: 🟡同维度 — SEC-MASK 系列同样因 secret 为空受影响
- **综合**: API_KEY 为空导致 add-mask 命令无 payload；若 API_KEY 有值且被泄露，则为平台安全缺陷
- **是否有规避手段**: 是

**建议**:
- 在平台侧确认 API_KEY 已创建且有有效值
- 测试 YAML 添加 config_probe 验证 `secrets.API_KEY` 非空
- 若 API_KEY 有值：确认日志中 `::add-mask::` 后是否包含原值或已遮蔽
- 增加验证步骤：add-mask 后再 echo 该 secret 确认第二次输出已被遮蔽
