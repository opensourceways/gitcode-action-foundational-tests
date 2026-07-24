## 失败分诊 · SEC-MASK-01-001 · Secret 值在运行日志中必须被自动脱敏为 ***

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain_secret "DEPLOY_TOKEN"，secret 值未出现在日志中（PASS）；assertions[1] (positive, run_logs) — 期望日志含 "masked_with_asterisks"，实际 secret 输出为空/截断，无 `***` 掩码标记

**根因初判**: 平台缺陷

**证据**:

- **Job 日志全量**（仅 6 行）:
  ```
  === JOB: Test log masking (status=COMPLETED) ===
  [2026/07/23 22:06:47.001 GMT+08:00] [INFO] Job(1529973073862340608_1529973073841369095) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/d8632be4-a2dc-499d-b389-bd86311dcd28.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/d8632be4-a2dc-499d-b389-bd86311dcd28.sh
  The secret is 
  ```
  日志输出 `The secret is ` 后无内容。`${{ secrets.DEPLOY_TOKEN }}` 模板展开后的值在日志中为空——既不是原值也不是 `***`。说明平台的 secret 脱敏机制将原值替换为了空字符串而非文档承诺的 `***`。原值确实未泄漏（negative 断言 PASS），但脱敏行为不符合文档描述的"替换为 `***`"。

- **预期行为**（Phase 01 文本用例 `SEC-MASK-01-001`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个 workflow，在 run 步骤中直接 echo secrets.DEPLOY_TOKEN"
  - 操作步骤 2: "触发 workflow 并查看运行日志"
  - 预期结果: "日志中 DEPLOY_TOKEN 的原值被替换为 `***`；日志全文搜索 DEPLOY_TOKEN 原值命中数为 0"
  - 验证点: "[正向] 脱敏标记 `***` 出现在对应位置"

- **实际行为**:
  - Secret 原值确实未泄漏（negative 断言通过，`The secret is ` 后无敏感内容）
  - 但脱敏后的输出是空字符串而非 `***`——文档承诺的掩码格式未被遵守

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `mask-test` job 的 `Echo secret directly` 步骤:
    ```yaml
    - name: Echo secret directly
      run: |
        echo "The secret is ${{ secrets.DEPLOY_TOKEN }}"
    ```
  - 这对应 GitCode 规格 `security-permissions/using-secrets.md` 第 62-69 行的 Secret 安全机制表:
    ```
    | 安全措施 | 说明 |
    |--------|------|
    | 日志遮掩 | Secret 值在日志中自动替换为 *** |
    | 不可查看 | 创建后无法在界面查看原值，只能更新覆盖 |
    | Fork 隔离 | pull_request 来自 fork 的 workflow 不可访问项目级 Secret |
    | 环境审批 | 环境级 Secret 可配置审批人，未经审批 job 不可访问 |
    ```
    规格第 66 行明确承诺："Secret 值在日志中自动替换为 `***`"。平台实际行为是将 secret 值替换为空字符串而非 `***`，违反了文档承诺的掩码格式。
  - 同时对应规格第 29-41 行的引用语法示例:
    ```yaml
    steps:
      - run: |
          ssh -i ${{ secrets.PROD_DEPLOY_KEY }} \
            user@prod-server.example.com \
            "deploy.sh ${{ secrets.PROD_API_TOKEN }}"
    ```
    规格文档展示了 `${{ secrets.SECRET_NAME }}` 的标准引用语法，测试 YAML 完全遵循此写法。

**置信度**: 高（日志确凿显示 secret 值被替换为空字符串而非 `***`，与文档第 66 行承诺的 `***` 掩码明确矛盾）

**影响**:
- **阻塞性**: 🔴阻塞 — 文档承诺 secret 在日志中"自动替换为 ***"，实际平台将 secret 值替换为空字符串，违反文档承诺的脱敏格式
- **静默性**: 🔴静默错误 — log 输出 `The secret is ` 后为空，无任何 `***` 掩码标记也无错误信息，用户无法判断是 secret 为空还是被脱敏
- **影响面**: 🔴跨维度 — 影响所有使用 secret 的 workflow（包括 SEC-MASK 全系列、SEC-WCMD 系列等），所有 `${{ secrets.* }}` 在日志中的输出均为空而非 `***`
- **综合**: Secret 日志脱敏机制存在缺陷，明文中替换为空字符串而非文档承诺的 `***` 掩码，影响所有 secret 相关功能的可观测性
- **是否有规避手段**: 否 — 平台内部脱敏逻辑需修复，用户无法通过配置改变脱敏输出格式

**建议**:
- 平台修复 secret 脱敏逻辑，确保日志中显示 `***` 而非空字符串
- 相关用例: SEC-MASK-01-002, SEC-MASK-01-003, SEC-MASK-01-004, SEC-MASK-01-005, SEC-MASK-01-006
