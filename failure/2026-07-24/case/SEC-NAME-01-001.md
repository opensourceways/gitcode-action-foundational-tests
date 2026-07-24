## 失败分诊 · SEC-NAME-01-001 · Secret/变量名含特殊字符时不可导致意外求值或权限绕过

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain_secret "MY-VAR" — 日志中无原值（形式通过但原因错误）
- positive, run_status, equals "success_or_yaml_error" — job 状态 COMPLETED（通过但无意义）

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Test special secret name (status=COMPLETED) ===
  [2026/07/23 22:07:51.101 GMT+08:00] [INFO] Job(1529973342604107776_1529973342566359047) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/69d87b28-0d35-4dbf-b109-f07c69b27f7b.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/69d87b28-0d35-4dbf-b109-f07c69b27f7b.sh
  value is 
  ```

- **预期行为** (Phase 01 文本用例 SEC-NAME-01-001, 优先级 P0, 维度 security):
  - 前置条件: 仓库配置了含中划线的 secret `MY-VAR`
  - 操作步骤 1: 提交一个 workflow，引用 `secrets.MY-VAR` 并在 shell 中使用
  - 操作步骤 2: 触发 workflow 并查看运行日志
  - 预期结果: 含中划线的 secret 不应因解析错误而被泄露到日志；若不支持中划线，应在 YAML 校验阶段报错

- **实际行为**:
  - `echo "value is ${{ secrets.MY-VAR }}"` 输出 `value is ` 后为空
  - secret `MY-VAR` 值为空，无法判断平台是否支持中划线 secret 名
  - YAML 校验阶段未报错（workflow 成功提交并运行）
  - 无法验证平台对中划线 secret 的支持策略（接受/拒绝/警告）

- **对照 GitCode 规格** `security-permissions/using-secrets.md`:
  - 第 44-45 行: "Secret 名称规则：仅允许大写字母、数字和下划线；不得以 ATOMGIT_ 开头；不得以数字开头"
  - 明确禁用了中划线！规格要求 secret 名仅允许大写字母、数字和下划线

- **环境前置条件验证**: YAML `setup.secrets: ["MY-VAR"]`，声明含中划线 secret。无 `config_probe` 步骤。输出为空，说明该 secret 在平台侧可能因命名规则被拒绝创建或值为空。

**置信度**: 中 (secret 值为空，规格明确禁止中划线，但无法确认平台行为)

**影响**:
- **阻塞性**: 🟡非阻塞 — secret 命名规则已知（仅允许 `[A-Z0-9_]`），测试可据此更新
- **静默性**: 🔴静默错误 — 使用了不合规的 secret 名但平台未报错，仅静默返回空值
- **影响面**: 🟡同维度 — 可能导致用户误以为特殊字符在 secret 名中可用
- **综合**: Spec 已明确规定 secret 名仅支持大写字母/数字/下划线；平台对中划线 `MY-VAR` 静默返回空值，应在 YAML 校验阶段拒绝
- **是否有规避手段**: 是

**建议**:
- Phase 01 文本用例修正：确认 secret 命名规则的测试应分为两个用例：(a) 合规名 `MY_VAR` 验证正常引用 (b) 不合规名 `MY-VAR` 验证平台在 YAML 校验阶段拒绝
- 平台应在 YAML 校验阶段拒绝含中划线的 secret 引用，而非静默返回空值
- 测试 YAML 添加 config_probe 确认 `MY-VAR` 是否被平台接受
