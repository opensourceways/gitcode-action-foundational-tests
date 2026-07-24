## 失败分诊 · SEC-MASK-01-002 · Secret 值在 step summary 和错误堆栈中必须被脱敏

**判定结果**: FAIL
**失败断言**: 
- negative, step_summary, must_not_contain_secret "API_KEY" — 无法验证（空值）
- negative, error_stack, must_not_contain_secret "API_KEY" — 无法验证（空值）

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (11 行):
  ```
  === JOB: Test summary masking (status=FAILED) ===
  [2026/07/23 22:06:57.709 GMT+08:00] [INFO] Job(1529973118867476480_1529973118842310663) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/11ffd625-7ee1-4a2b-8f49-3b4fddc20001.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/11ffd625-7ee1-4a2b-8f49-3b4fddc20001.sh
  
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9cb3636a-c161-490a-95cb-ab53c2167329.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9cb3636a-c161-490a-95cb-ab53c2167329.sh
  Failing with key 
  ::error::Process exited with code 1
  ```

- **预期行为** (Phase 01 文本用例 SEC-MASK-01-002, 优先级 P0, 维度 security):
  - 前置条件: 仓库配置了 secret `API_KEY`
  - 操作步骤 1: 提交一个 workflow，将 `secrets.API_KEY` 写入 ATOMGIT_STEP_SUMMARY
  - 操作步骤 2: 触发 workflow 并查看 step summary 与日志
  - 预期结果: step summary 中 API_KEY 的原值被替换为 `***`；若步骤失败产生堆栈，堆栈中亦不应出现原值

- **实际行为**:
  - Step 1: `echo "Key: ${{ secrets.API_KEY }}" >> $ATOMGIT_STEP_SUMMARY` — 输出为空（空行）
  - Step 2: `echo "Failing with key ${{ secrets.API_KEY }}"` + `exit 1` — 输出 `Failing with key ` 后为空
  - `secrets.API_KEY` 在平台侧为空值，summary 和错误输出均无 secret 内容（因无内容可泄露）
  - 失败传导链: step 2 的 `exit 1` 导致 job 状态 FAILED

- **对照 GitCode 规格** `security-permissions/using-secrets.md`:
  - 第 66 行: "日志遮掩 | Secret 值在日志中自动替换为 `***`"
  - 第 67 行: "不可查看 | 创建后无法在界面查看原值，只能更新覆盖"

- **环境前置条件验证**: YAML `setup.secrets: ["API_KEY"]`，secret 已声明。无 `config_probe` 步骤。总结内容 (`$ATOMGIT_STEP_SUMMARY`) 和错误堆栈中 API_KEY 均为空。

**置信度**: 高 (两个 step 均输出空值，明确表明 API_KEY 为空)

**影响**:
- **阻塞性**: 🔴阻塞 — step summary 和错误堆栈脱敏验证完全无法执行
- **静默性**: 🔴静默错误 — 空值输出来区分是脱敏生效还是未配置
- **影响面**: 🟡同维度 — SEC-MASK-01-001 同样因 secret 未配置失败
- **综合**: API_KEY 在平台侧未实际创建或无值，无法验证 summary 和堆栈脱敏
- **是否有规避手段**: 是

**建议**:
- 在平台侧为测试仓库创建 `API_KEY` secret 并赋予有效值
- 测试 YAML 添加 config_probe 步骤确认 `secrets.API_KEY` 存在且非空
- 可增加 `[[ -n "${{ secrets.API_KEY }}" ]] || echo "SECRET_EMPTY"` 作为前置检查
