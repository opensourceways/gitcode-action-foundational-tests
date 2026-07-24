## 失败分诊 · USE-CTX-01-002 · 使用 github 上下文时报错应提示 atomgit 替代

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED（即 YAML 校验或表达式求值应报错），实际 COMPLETED；assertions[1] (nonfunctional, error_message) — 期望报错信息同时出现 github 与 atomgit 字样，实际无任何报错

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（6 行）:
  ```
  === JOB: test github context error (status=COMPLETED) ===
  [2026/07/23 22:41:23.977 GMT+08:00] [INFO] Job(1529981785318375424_1529981785289015303) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/92957af6-0842-4ae9-9faf-134b01a6b96d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/92957af6-0842-4ae9-9faf-134b01a6b96d.sh
  ref=placeholder_ref
  ```
  `${{ github.ref }}` 表达式被静默求值为 `placeholder_ref`，Job 以 COMPLETED 完成。平台未因引用不存在的 `github` 上下文而报错，也未给出应使用 `atomgit` 上下文的引导提示。

- **预期行为**（Phase 01 文本用例 `USE-CTX-01-002`，优先级 P1，维度 usability/compatibility）:
  - 操作步骤 1: "在 workflow 的 run 步骤中引用 ${{ github.ref }}"
  - 预期结果: "YAML 校验或表达式求值阶段报错，提示应使用 atomgit 上下文"
  - 验证点: "[负向] 不应静默求值为空字符串"；"[非功能] 报错信息中应同时出现 github 与 atomgit 字样"

- **实际行为**:
  - 平台对 `${{ github.ref }}` 表达式执行了求值，结果为 `placeholder_ref`（既非空也非错误），Job 正常运行至 COMPLETED。未触发任何 YAML 校验错误或表达式求值错误，用户无法得知应使用 `atomgit` 上下文替代 `github`。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `bad-ctx` job 的 workflow:
    ```yaml
    steps:
      - name: echo github ref
        run: |
          echo "ref=${{ github.ref }}"
    ```
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/context.md` 第 9-21 行的上下文总览表，其中仅列有 `atomgit` 上下文（第 11 行），不存在 `github` 上下文：
    ```
    | `atomgit` | AtomGit 平台与事件信息 | `${{ atomgit.event_name }}`, `${{ atomgit.sha }}` |
    ```
    文档未定义 `github` 上下文，平台应拒绝该引用并提供迁移提示，而非静默求值为占位符值。

**置信度**: 高（日志第 6 行 `ref=placeholder_ref` 证实平台静默求值，Job COMPLETED 无报错，与 context.md 仅定义 `atomgit` 上下文的事实矛盾）

**影响**:
- **阻塞性**: 🟡非阻塞 — github.ref 被静默求值为 placeholder_ref，workflow 仍正常完成，不阻塞执行
- **静默性**: 🔴静默错误 — 平台完全不报错，用户使用 github.* 上下文时收到占位符值却无任何提示
- **影响面**: 🟡同维度 — 所有从 GitHub Actions 迁移并使用 github.* 上下文的 workflow 均会接收到错误值
- **综合**: github.* 上下文被静默求值为占位符值，所有从 GitHub Actions 迁移的 workflow 均会接收到错误值且无任何提示
- **是否有规避手段**: 否 — 平台不提供 github.* → atomgit.* 迁移指引，用户无法得知应替换上下文前缀

**建议**:
- 平台需在表达式求值阶段检测 `github.*` 上下文引用，主动报错并提示用户使用 `atomgit.*` 作为替代，参考 GitHub Actions→GitCode Actions 迁移场景
- 相关用例: USE-CTX-01-001（同一意图 INTENT-USE-002 sibling）
