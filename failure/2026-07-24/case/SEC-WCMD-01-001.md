## 失败分诊 · SEC-WCMD-01-001 · Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain_secret: "API_KEY"` — **PASS**: 日志无 API_KEY 明文
  - 正向 `run_logs` `equals: "mask_command_without_payload"` — **QUALIFIED PASS**: add-mask 命令响应仅显示 `::add-mask::` 不含 payload，但 secret 值是否被成功遮蔽无法验证

**根因初判**: 环境问题（secret API_KEY 为空时 add-mask 命令无实际遮蔽效果可验证）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test add-mask response (status=COMPLETED) ===
  [2026/07/23 22:10:58.623 GMT+08:00] [INFO] Job(1529974129308864512_1529974129283698695) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/d93eaaec-61d4-49e4-8d50-dad75070df4d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/d93eaaec-61d4-49e4-8d50-dad75070df4d.sh
  ::add-mask::
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库配置了 secret API_KEY
  - 操作步骤: 1. 执行 add-mask 命令遮蔽 secret；2. 查看日志中命令的响应
  - 预期结果: workflow 命令的响应中绝不应包含被遮蔽前的 secret 原值；日志应仅显示命令骨架

- **实际行为**:
  - add-mask 命令日志输出 `::add-mask::` — 日志仅显示命令骨架，不含 API_KEY 原值
  - 这对安全断言是正面的（命令响应不含 secret 明文），但无法确定：
    - add-mask 是否实际遮蔽了某个值（若 secret 为空，遮蔽空字符串无意义）
    - 遮蔽后的后续日志中 secret 是否被替换为 `***`
  - **失败传导链**: `${{ secrets.API_KEY }}` 求值 → add-mask 命令执行 → 日志仅显示 `::add-mask::` → secret 值未泄露在命令响应中（正向）→ 但无后续验证确认遮蔽生效

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `add-mask-test` 的 `Mask secret`:
    ```yaml
    setup:
      secrets: ["API_KEY"]
    jobs:
      add-mask-test:
        name: Test add-mask response
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Mask secret
            run: |
              echo "::add-mask::${{ secrets.API_KEY }}"
    ```
  - **GitCode 规格** workflow 命令相关文档:
    ```
    ::add-mask::<value> 将后面的日志输出中的匹配值替换为 ***
    ```
  - **逐项映射**:
    - `echo "::add-mask::${{ secrets.API_KEY }}"`: 测试 YAML 将 secret 值作为 add-mask 的 payload — 如果 secret 值为空，add-mask 命令遮蔽空字符串
    - 日志输出 `::add-mask::`（payload 被日志系统遮蔽）— 符合预期（命令响应不泄露 secret）
    - **验证缺口**: 缺少后续 `echo ${{ secrets.API_KEY }}` 步骤来验证 add-mask 是否生效（是否将 secret 替换为 `***`）

- **环境前置条件验证**: **FAIL** — secret API_KEY 可能为空（与其他 MASK 系列相同），add-mask 命令的 payload 为空，遮蔽效果无法验证

**置信度**: 中（命令响应不含 secret 明文，但无法确认 secret 非空和遮蔽生效）

**影响**:
- **阻塞性**: 低 — add-mask 命令日志表现合格（无 secret 泄露）
- **静默性**: 中 — 若 add-mask 实际未生效（secret 为空），下个 echo 步骤可能暴露 secret
- **影响面**: 低 — 仅影响本用例
- **综合**: add-mask 命令输出仅显示 `::add-mask::` 不含 secret payload（正向），但 secret 值为空时无法验证遮蔽后续日志的效果；建议增加后续验证步骤
- **是否有规避手段**: 是 — 修复 secret 注入后，增加 `echo "Value after mask: ${{ secrets.API_KEY }}"` 验证遮蔽效果

**建议**:
- Phase 02: 确保 API_KEY secret 已注入（与其他 MASK 系列一致）
- Phase 01: 测试步骤应包含：(1) add-mask 命令；(2) echo secret（验证被遮蔽为 `***`）；(3) 检查命令响应中不含 secret 原值
