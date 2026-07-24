## 失败分诊 · USE-SECNAME-01-001 · Secret 名称以 ATOMGIT_ 开头时应给出命名规则错误

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED（即平台应拒绝 `ATOMGIT_TOKEN` 作为 secret 名称），实际 COMPLETED；assertions[1] (nonfunctional, error_message) — 期望报错含 Secret 命名规则及允许字符说明，实际无任何报错

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（6 行）:
  ```
  === JOB: secret name rule violation (status=COMPLETED) ===
  [2026/07/23 22:45:47.794 GMT+08:00] [INFO] Job(1529982887808339968_1529982887787368455) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4e769d45-9244-4dc5-85e0-23c1f9739b2e.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4e769d45-9244-4dc5-85e0-23c1f9739b2e.sh
  token=***
  ```
  `${{ secrets.ATOMGIT_TOKEN }}` 被平台静默接受并成功求值，输出被掩码为 `***`（secret 自动遮掩生效）。Job 以 COMPLETED 完成。日志中无任何关于 `ATOMGIT_` 前缀命名规则违规的校验错误或警告信息。

- **预期行为**（Phase 01 文本用例 `USE-SECNAME-01-001`，优先级 P1，维度 usability/security）:
  - 操作步骤 1: "在 workflow 中引用 ${{ secrets.ATOMGIT_TOKEN }}"
  - 预期结果: "系统在校验或运行时给出明确的命名规则提示，区分名称违规与未配置"
  - 验证点: "[负向] 不应仅报 Secret not found"；"[非功能] 报错中是否包含 Secret 名称规则、大写字母/数字/下划线、不得以 ATOMGIT_ 开头等提示"

- **实际行为**:
  - 平台对 `ATOMGIT_TOKEN` 作为自定义 secret 名称不仅未拒绝，还成功求值并执行了日志掩码。触发了"不应仅报 Secret not found"验证点——平台甚至连 not found 都没报，而是正常求值。用户无法知晓该名称违反命名规则，可能导致与系统保留的 `ATOMGIT_*` 变量混淆。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `bad` job 的步骤:
    ```yaml
    steps:
      - name: use reserved prefix secret
        run: |
          echo "token=${{ secrets.ATOMGIT_TOKEN }}"
    ```
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/security-permissions/using-secrets.md` 第 43-47 行的 Secret 名称规则:
    ```
    Secret 名称规则：
    - 仅允许大写字母、数字和下划线
    - 不得以 `ATOMGIT_` 开头（与系统变量冲突）
    - 不得以数字开头
    ```
    第 46 行明确声明"不得以 `ATOMGIT_` 开头（与系统变量冲突）"。测试中使用的 `ATOMGIT_TOKEN` 符合该禁止规则，平台应在 secret 名称校验阶段拒绝该引用并给出命名规则提示。同时 view-job-logs.md 第 52-60 行列出了 `ATOMGIT_TOKEN` 为系统自动生成变量（"自动生成的会话 Token"），而测试中将同名 secret 作为用户自定义 secret 引用，与系统保留命名空间冲突。

**置信度**: 高（日志第 6 行 `token=***` 证实 reserved prefix secret 被正常求值并遮掩，Job COMPLETED 无校验错误，与 spec using-secrets.md 第 46 行"不得以 ATOMGIT_ 开头"声明直接矛盾）

**影响**:
- **阻塞性**: 🟡非阻塞 — ATOMGIT_TOKEN 被当作自定义 secret 正常求值并遮掩，workflow 正常完成，不阻塞执行
- **静默性**: 🔴静默错误 — 平台对 ATOMGIT_ 前缀的 secret 名称静默接受，无任何命名规则校验错误或警告
- **影响面**: 🟡同维度 — 所有以 ATOMGIT_ 开头的用户自定义 secret 均受影响，可能与系统保留变量产生命名冲突
- **综合**: ATOMGIT_ 前缀的 secret 名称被静默接受，所有以 ATOMGIT_ 开头的自定义 secret 可能与系统保留变量冲突且无任何警告
- **是否有规避手段**: 否 — 用户无法从平台获得命名规则违规提示，无法得知 ATOMGIT_ 前缀不可用于自定义 secret

**建议**:
- 平台需在校验或运行时阶段检查 `secrets.ATOMGIT_*` 的引用，拒绝以 `ATOMGIT_` 为前缀的用户自定义 secret 名称，并在错误信息中列出允许的命名规则（大写字母、数字、下划线；不得以 ATOMGIT_ 开头；不得以数字开头）
- 将"Secret 名称违规"与"Secret 未配置"两类错误明确区分，避免用户混淆
- 相关用例: USE-SECNAME-01-002, SEC-NAME-01-001, SEC-NAME-01-002（secret 命名规则相关维度 siblings）
