## 失败分诊 · USE-CTX-01-002 · 使用 github 上下文时报错应提示 atomgit 替代

**判定结果**: FAIL
**失败断言**:
- negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝 `github.ref`）
- nonfunctional/error_message: rubric "报错信息必须同时出现 github 与 atomgit 字样，并给出替换建议" — 无任何报错

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: test github context error (status=COMPLETED) ===
  [2026/07/23 22:41:23.977 GMT+08:00] [INFO] Job(1529981785318375424_1529981785289015303) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/92957af6-0842-4ae9-9faf-134b01a6b96d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/92957af6-0842-4ae9-9faf-134b01a6b96d.sh
  ref=placeholder_ref
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: workflow 文件位于 .gitcode/workflows/
  - 操作步骤: 在 workflow 的 run 步骤中引用 ${{ github.ref }}
  - 预期结果: YAML 校验或表达式求值阶段报错，提示应使用 atomgit 上下文

- **实际行为**:
  - 平台**静默接受** `github` 上下文，将其求值为 `placeholder_ref`，不报任何错误或警告
  - **失败传导链**: 平台 → `github.ref` 静默求值为 `placeholder_ref` → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `bad-ctx` job 的 `echo github ref` step:
    ```yaml
    steps:
      - name: echo github ref
        run: |
          echo "ref=${{ github.ref }}"
    ```
  - **GitCode 规格** `syntax-reference/context.md` 第9-21行:
    ```markdown
    | 上下文 | 说明 |
    |------|------|
    | `atomgit` | AtomGit 平台与事件信息 |
    | `env` | 当前步骤/Job/Workflow 的自定义环境变量 |
    | `vars` | 组织/项目级别配置变量 |
    | `job` | 当前 Job 信息 |
    ```
    上下文列表中**不存在** `github` 上下文
  - **逐项映射**:
    - 测试 `${{ github.ref }}` → 规格中无 `github` 上下文定义，应为非法引用
    - 平台行为：`github` 被当作未知上下文，静默求值为 `placeholder_ref` 空占位
    - 差异：期望报错并提示 atomgit 替代，实际静默替换为占位值

- **环境前置条件验证**: workflow_dispatch 触发，Runner [dedicate-hosted, x64, large]，仓库默认分支 main

**置信度**: 高（日志直接证明 github.ref 静默求值为 placeholder_ref；规格中明确不存在 github 上下文）

**影响**:
- **阻塞性**: 🔴 GitHub Actions 迁移用户引用 `github.*` 上下文时不会有任何报错，但获得错误值
- **静默性**: 🔴 完全静默 — 无任何错误、警告或提示
- **影响面**: 🔴 所有从 GitHub Actions 迁移的 workflow（`github.ref`、`github.sha`、`github.event_name` 等高频使用）
- **综合**: 用户使用 github 上下文会获得占位值而非报错，排障极端困难
- **是否有规避手段**: 否（用户不知道 github 上下文不被支持，且无反馈机制告知）

**建议**:
- 平台方应在表达式求值阶段对 `github` 上下文做专门的检测和报错，报错信息需包含 "请使用 atomgit 上下文替代 github"
- 建议增加YAML校验规则：检测到 `${{ github.` 模式即警告
- 短期可在官方文档首页增加兼容性迁移指引
