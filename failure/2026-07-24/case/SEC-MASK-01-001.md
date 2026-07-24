## 失败分诊 · SEC-MASK-01-001 · Secret 值在运行日志中必须被自动脱敏为 ***

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain_secret "DEPLOY_TOKEN" — 日志中无 DEPLOY_TOKEN 原值（形式通过）
- positive, run_logs, equals "masked_with_asterisks" — 实际输出 `The secret is ` 后为空，不匹配

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Test log masking (status=COMPLETED) ===
  [2026/07/23 22:06:47.001 GMT+08:00] [INFO] Job(1529973073862340608_1529973073841369095) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/d8632be4-a2dc-499d-b389-bd86311dcd28.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/d8632be4-a2dc-499d-b389-bd86311dcd28.sh
  The secret is 
  ```

- **预期行为** (Phase 01 文本用例 SEC-MASK-01-001, 优先级 P0, 维度 security):
  - 前置条件: 仓库配置了 secret `DEPLOY_TOKEN`
  - 操作步骤 1: 提交一个 workflow，在 run 步骤中直接 echo `secrets.DEPLOY_TOKEN`
  - 操作步骤 2: 触发 workflow 并查看运行日志
  - 预期结果: 日志中 DEPLOY_TOKEN 的原值被替换为 `***`；日志全文搜索 DEPLOY_TOKEN 原值命中数为 0

- **实际行为**:
  - `echo "The secret is ${{ secrets.DEPLOY_TOKEN }}"` 输出 `The secret is ` 后为空
  - 未见 `***` 脱敏标记
  - `secrets.DEPLOY_TOKEN` 展开为空值（非已脱敏的形式），表明 secret 在平台中未实际配置或值为空

- **对照 GitCode 规格** `security-permissions/using-secrets.md`:
  - 第 44-45 行: "引用语法为 `${{ secrets.SECRET_NAME }}`，Secret 名称规则：仅允许大写字母、数字和下划线"
  - 第 66 行: "日志遮掩 | Secret 值在日志中自动替换为 `***`"

- **环境前置条件验证**: YAML `setup.secrets: ["DEPLOY_TOKEN"]`，表明 secret 在 YAML 中已声明。但无 `config_probe` 步骤确认 secret 在平台侧是否实际创建且有值。日志输出为空说明 `DEPLOY_TOKEN` 可能未在平台创建。

**置信度**: 高 (输出为空而非 `***`，说明 platform 未注入 secret 值)

**影响**:
- **阻塞性**: 🔴阻塞 — 无法验证核心安全机制（secret 日志脱敏）
- **静默性**: 🔴静默错误 — 空输出不报错，看不出是未配置还是脱敏生效
- **影响面**: 🟡同维度 — SEC-MASK-01-002/005 及 SEC-NAME-01-001 同样受影响
- **综合**: Secret 在 YAML 声明但平台侧未实际配置，导致脱敏验证无从进行
- **是否有规避手段**: 是

**建议**:
- 测试 YAML 添加 `config_probe` 步骤：`echo "probe:${{ secrets.DEPLOY_TOKEN }}" | wc -c` 输出长度验证 secret 存在
- 在平台侧确认 `DEPLOY_TOKEN` 在测试仓库的 "项目设置 → 密钥与变量 → 仓库密钥" 中已创建且有值
- 若平台未提供 secret 注入，需先修复环境前置条件
