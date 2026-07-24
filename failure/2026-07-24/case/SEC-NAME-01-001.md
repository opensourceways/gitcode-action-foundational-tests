## 失败分诊 · SEC-NAME-01-001 · Secret/变量名含特殊字符时不可导致意外求值或权限绕过

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain_secret: "MY-VAR"` — 无法判定: 日志输出 "value is " 后为空
  - 正向 `run_status` `equals: "success_or_yaml_error"` — **PASS**（status=COMPLETED）

**根因初判**: 环境问题（secret MY-VAR 为空或未注入）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test special secret name (status=COMPLETED) ===
  [2026/07/23 22:07:51.101 GMT+08:00] [INFO] Job(1529973342604107776_1529973342566359047) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/69d87b28-0d35-4dbf-b109-f07c69b27f7b.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/69d87b28-0d35-4dbf-b109-f07c69b27f7b.sh
  value is 
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库配置了含中划线的 secret MY-VAR
  - 操作步骤: 1. 提交 workflow，引用 secrets.MY-VAR 并在 shell 中使用；2. 查看运行日志
  - 预期结果: 含中划线的 secret 不应因解析错误而被泄露到日志

- **实际行为**:
  - Job 正常完成（status=COMPLETED），说明含中划线的 secret 引用未导致 YAML 解析错误
  - 但输出 "value is " 后为空，secret 值未显示
  - **失败传导链**: `${{ secrets.MY-VAR }}` 求值为空 → 无法确认是 secret 未注入、被正确脱敏为空、还是解析异常导致

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `special-name` 的 `Use hyphen secret`:
    ```yaml
    setup:
      secrets: ["MY-VAR"]
    jobs:
      special-name:
        name: Test special secret name
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Use hyphen secret
            run: |
              echo "value is ${{ secrets.MY-VAR }}"
    ```
  - **GitCode 规格** `core-concepts/variables-secrets-context-expressions.md` 第 10-16 行:
    ```
    | `secrets` | Passwords, tokens, private keys | Yes | `${{ secrets.NAME }}` |
    ```
  - **逐项映射**:
    - `secrets.MY-VAR`: 测试 YAML 引用含中划线的 secret 名 — 规格中 `NAME` 未定义允许字符集
    - 测试 YAML 语法 `${{ secrets.MY-VAR }}` 中 `MY-VAR` 含中划线，可能被表达式引擎解释为减法表达式 `MY - VAR`
    - 若 YAML 解析不支持中划线，应在解析阶段报错而非静默通过

- **环境前置条件验证**: **FAIL** — secret MY-VAR 求值为空。符合"Secret/token empty → 环境问题 (Phase 02)"

**置信度**: 中（secret 值为空且未触发 YAML 解析错误，无法区分是环境问题还是平台对中划线的静默处理）

**影响**:
- **阻塞性**: 低 — secret 值未泄露（空输出），但无法验证安全性
- **静默性**: 高 — 若平台静默吞掉不支持的 secret 名，用户将无法发现配置问题
- **影响面**: 低 — 仅影响含特殊字符的 secret 命名场景
- **综合**: 含中划线的 secret MY-VAR 引用未报错但求值为空，无法验证特殊字符 secret 的安全性
- **是否有规避手段**: 是 — 修复 secret 注入；或改为无中划线的 secret 名对比测试

**建议**:
- Phase 02: 确保 MY-VAR secret 已配置且非空
- Phase 01: 增加对照测试：使用无中划线的 secret 名（如 MY_VAR）验证注入是否正常，再对比特殊字符名
