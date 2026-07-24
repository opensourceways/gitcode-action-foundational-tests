## 失败分诊 · USE-CTX-01-001 · 使用 atomgit 上下文时表达式正常求值

**判定结果**: FAIL
**失败断言**:
- positive/run_logs: contains `"ref=refs/heads/"` — actual log contains `"ref=main"`（不含 `refs/heads/` 前缀）

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: test atomgit context (status=COMPLETED) ===
  [2026/07/23 22:41:13.287 GMT+08:00] [INFO] Job(1529981740632387584_1529981740607221767) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/07ce60ee-d901-44a3-834d-112858aaee91.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/07ce60ee-d901-44a3-834d-112858aaee91.sh
  ref=main
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: workflow 文件位于 .gitcode/workflows/
  - 操作步骤: 在 workflow 的 run 步骤中引用 ${{ atomgit.ref }}
  - 预期结果: 表达式正确求值为当前分支引用

- **实际行为**:
  - `atomgit.ref` 求值结果为 `main`（短名），而非规格声明的全名 `refs/heads/main`
  - **失败传导链**: 平台 → `atomgit.ref` 返回短引用名 `main` → 日志中不含 `refs/heads/` → 测试断言包含匹配失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test-ctx` job 的 `echo atomgit ref` step:
    ```yaml
    steps:
      - name: echo atomgit ref
        run: |
          echo "ref=${{ atomgit.ref }}"
    ```
  - **GitCode 规格** `syntax-reference/context.md` 第27-31行:
    ```markdown
    | `atomgit.ref` | string | 触发引用（分支或标签全名，如 `refs/heads/main`） |
    ```
  - **逐项映射**:
    - 测试 `${{ atomgit.ref }}` → 规格定义返回全名 `refs/heads/main`
    - 实际运行时 `atomgit.ref` 返回短名 `main`，与规格声明不一致
    - 运行成功（COMPLETED），表达式本身语法正确，求值行为错误

- **环境前置条件验证**: workflow_dispatch 触发，仓库在 main 分支，Runner [dedicate-hosted, x64, large]

**置信度**: 高（日志直接证明 atomgit.ref 返回 `main` 而非 `refs/heads/main`；规格明确声明应返回全名）

**影响**:
- **阻塞性**: 🟡 如果用户依赖 `${{ atomgit.ref == 'refs/heads/main' }}` 做条件判断，条件恒为 false
- **静默性**: 🔴 完全静默 — job 正常完成，无任何警告
- **影响面**: 🟡 所有使用 `atomgit.ref` 做字符串匹配（如条件执行、分支判断）的 workflow
- **综合**: atomgit.ref 返回短名而非规格声明的全名，破坏条件表达式和分支判断逻辑
- **是否有规避手段**: 是（使用 `atomgit.ref_name` 获取短名、或拼接 `refs/heads/${{ atomgit.ref_name }}` 构造全名；但用户无法在事先知晓的情况下适配）

**建议**:
- 平台方应修正 `atomgit.ref` 返回值，使其返回全名 `refs/heads/<branch>` 符合规格定义
- 或若当前行为是有意设计（仅返回短名），则需更新 context.md 规格文档
- 兼容性风险：GitHub Actions 用户迁移时可能直接使用 `github.ref` 做分支比较，此处行为差异会增加迁移成本
