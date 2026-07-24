## 失败分诊 · SEC-MASK-01-005 · Secret 日志脱敏不可通过多行值输出绕过

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain_secret: "MULTI_LINE_SECRET"` — 无法判定: 日志仅输出空行
  - 正向 `run_logs` `equals: "multiline_masked_with_asterisks"` — **FAIL**: 日志中无 `***` 标记，也无任何多行内容输出

**根因初判**: 环境问题（secret MULTI_LINE_SECRET 为空或未注入）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test multiline masking (status=COMPLETED) ===
  [2026/07/23 22:07:29.425 GMT+08:00] [INFO] Job(1529973251784843264_1529973251751288839) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/53327f0a-5d6c-4192-bfb3-edea180675df.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/53327f0a-5d6c-4192-bfb3-edea180675df.sh

  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库配置了多行 secret MULTI_LINE_SECRET
  - 操作步骤: 1. 提交 workflow，直接 echo 多行 secret 到日志；2. 查看运行日志
  - 预期结果: 多行 secret 的每一行在日志中均被脱敏；换行符不应成为脱敏边界

- **实际行为**:
  - 日志仅输出一个空行，无多行 secret 内容
  - secret 值为空，无任何明文或脱敏标记
  - **失败传导链**: `${{ secrets.MULTI_LINE_SECRET }}` 求值为空 → echo 空内容 → 日志无输出 → 无法验证多行脱敏行为

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `multiline-mask` 的 `Echo multiline secret`:
    ```yaml
    setup:
      secrets: ["MULTI_LINE_SECRET"]
    jobs:
      multiline-mask:
        name: Test multiline masking
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Echo multiline secret
            run: |
              echo "${{ secrets.MULTI_LINE_SECRET }}"
    ```
  - **GitCode 规格** `core-concepts/variables-secrets-context-expressions.md` 第 10-16 行:
    ```
    | `secrets` | Passwords, tokens, private keys | Yes | `${{ secrets.NAME }}` |
    ```
  - **逐项映射**:
    - `${{ secrets.MULTI_LINE_SECRET }}`: 测试 YAML 引用多行 secret — 匹配规格写法
    - `echo "${{ ... }}"`: 使用双引号保留换行符 — 正确用法
    - 规格未定义多行 secret 的脱敏行为（按行匹配 vs 整值匹配）

- **环境前置条件验证**: **FAIL** — MULTI_LINE_SECRET 求值为空。与其他 MASK 系列相同。符合"Secret/token empty → 环境问题 (Phase 02)"

**置信度**: 高（secret 值空，与 SEC-MASK-01-001 同一根因）

**影响**:
- **阻塞性**: 中 — 依赖 secret 注入
- **静默性**: 高 — 多行 secret 泄露是实际攻击向量（如 RSA 私钥），无法验证防护
- **影响面**: 中 — 与其他 MASK 用例共享根因
- **综合**: 多行 secret 未注入（值为空），测试无法验证多行脱敏引擎的跨行匹配能力
- **是否有规避手段**: 是 — 修复 secret 注入后重新测试

**建议**:
- Phase 02: 共享 MASK 系列的 secret 注入修复
- Phase 01: 多行 secret 的值应包含至少 2 行（含特殊字符），以验证跨行匹配
