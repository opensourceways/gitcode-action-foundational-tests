## 失败分诊 · USE-CTX-01-001 · 使用 atomgit 上下文时表达式正常求值

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_logs) — 期望日志含 `"ref=refs/heads/"`，实际日志仅含 `ref=main`（短格式，不含 `refs/heads/` 前缀）

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（6 行）:
  ```
  === JOB: test atomgit context (status=COMPLETED) ===
  [2026/07/23 22:41:13.287 GMT+08:00] [INFO] Job(1529981740632387584_1529981740607221767) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/07ce60ee-d901-44a3-834d-112858aaee91.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/07ce60ee-d901-44a3-834d-112858aaee91.sh
  ref=main
  ```
  `${{ atomgit.ref }}` 表达式求值结果为 `main`（短引用名），非文档声明的完整引用格式 `refs/heads/main`。

- **预期行为**（Phase 01 文本用例 `USE-CTX-01-001`，优先级 P1，维度 usability/compatibility）:
  - 操作步骤 1: "在 workflow 的 run 步骤中引用 ${{ atomgit.ref }}"
  - 预期结果: "表达式正确求值为当前分支引用"
  - 验证点: "[正向] 日志中输出当前分支引用值"；"[正向] 运行成功完成"

- **实际行为**:
  - Job 状态为 COMPLETED，表达式求值未报错，但 `atomgit.ref` 返回的是短格式 `main` 而非文档承诺的全格式 `refs/heads/main`。该返回值在功能上可用但格式与文档声明不一致。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `test-ctx` job 的 echo 步骤:
    ```yaml
    steps:
      - name: echo atomgit ref
        run: |
          echo "ref=${{ atomgit.ref }}"
    ```
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/context.md` 第 31 行的 `atomgit.ref` 属性定义:
    ```
    | `atomgit.ref` | string | 触发引用（分支或标签全名，如 `refs/heads/main`） |
    ```
    文档明确承诺 `atomgit.ref` 返回"分支或标签全名"，并给出示例值 `refs/heads/main`。平台实际返回短格式 `main`，与文档声明的格式不一致。

**置信度**: 高（日志第 6 行 `ref=main` 不含 `refs/heads/` 前缀，与 spec context.md 第 31 行声明直接矛盾）

**影响**:
- **阻塞性**: 🟡非阻塞 — `atomgit.ref` 返回短格式仍能完成 CI pipeline，workflow 正常 COMPLETED
- **静默性**: 🔴静默错误 — 平台不报错，但值格式与文档不符。用户若在脚本中按文档示例写 `echo ${{ atomgit.ref }} | cut -d'/' -f3` 期望提取分支名，在短格式下会得到空串或错误截断，且不会触发任何错误提示
- **影响面**: 🟡同维度 — 所有引用 `${{ atomgit.ref }}` 并依赖 `refs/heads/` 前缀的 workflow 均受影响（包括所有使用该上下文做条件判断、脚本路径拼接的场景）
- **综合**: 非阻塞但静默——`atomgit.ref` 返回短格式可导致所有依赖全格式 `refs/heads/main` 的下游脚本静默出错，用户无法从平台获得任何错误提示
- **是否有规避手段**: 是，用户可用 `${{ atomgit.ref_name }}` 代替 `${{ atomgit.ref }}` 获得相同短格式值；若需要全格式，需手动拼接 `refs/heads/${{ atomgit.ref_name }}`

**建议**:
- 平台需确认 `atomgit.ref` 的规范行为：若按文档承诺应返回全格式 `refs/heads/main`，需修复实现；若平台选择短格式，需更新文档 context.md 第 31 行的属性说明及示例值
- 无论哪种修复方向，当前「实现与文档不一致」的状态是最危险的——用户信任文档写脚本，却得到格式不符的值且无任何警告
- 相关用例: USE-CTX-01-002（同一意图 INTENT-USE-002 sibling）
