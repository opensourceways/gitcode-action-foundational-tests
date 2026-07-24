## 失败分诊 · SEC-TOCTOU-01-001 · 审批后推送新 commit 不应被已授权特权运行执行

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "unapproved_commit_executed"，未出现（PASS）；assertions[1] (positive, run_logs) — 期望日志含 "approved_sha_matched"，实际该关键词从未被脚本显式 echo 输出

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（仅 6 行）:
  ```
  === JOB: Test TOCTOU protection (status=COMPLETED) ===
  [2026/07/23 22:10:48.247 GMT+08:00] [INFO] Job(1529974085599641600_1529974085566087175) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/89cfca38-c55f-46eb-acf8-5bf6a7c6d07b.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/89cfca38-c55f-46eb-acf8-5bf6a7c6d07b.sh
  Running commit: 
  ```
  脚本 `echo "Running commit: ${{ atomgit.sha }}"` 执行后输出 `Running commit: `（后无内容），表明 `atomgit.sha` 在 workflow_dispatch 事件下被解析为空字符串。没有 commit SHA 可供比较，TOCTOU 检查无法执行。断言关键词 "approved_sha_matched" 是测试设计者期望的验证锚点，但从未被脚本显式 echo——脚本仅输出了 commit SHA 值（此时为空），未输出任何断言标记。

- **预期行为**（Phase 01 文本用例 `SEC-TOCTOU-01-001`，优先级 P0，维度 security）:
  - 操作步骤 1: "管理员审批一个 workflow 运行"
  - 操作步骤 2: "在审批后、执行前，攻击者推送恶意 commit"
  - 操作步骤 3: "观察特权运行是否执行了新 commit"
  - 预期结果: "特权运行应绑定审批时刻的具体 commit SHA；审批后推送的新 commit 不应被已授权的特权运行自动采用"
  - 验证点: "[正向] 特权运行执行的 commit 与审批时锁定的 SHA 一致"

- **实际行为**:
  - `atomgit.sha` 在 workflow_dispatch 事件下返回空字符串——无法确认执行的是什么 commit
  - TOCTOU 保护逻辑无法被验证——因为连审批锁定的 SHA 都获取不到
  - 断言关键词 "approved_sha_matched" 从未被脚本输出——需要脚本显式比较并输出该标记

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `toctou-test` job 的 `Check commit SHA` 步骤:
    ```yaml
    - name: Check commit SHA
      run: |
        echo "Running commit: ${{ atomgit.sha }}"
    ```
  - 这对应 GitCode 规格 `writing-pipelines/configure-conditional-execution.md` 第 9-12 行的前提条件:
    ```
    前提条件:
    - 理解 atomgit 上下文。
    - 理解表达式语法 ${{ }}。
    ```
    规格第 9-10 行承诺 `atomgit` 上下文的存在，第 26-27 行示例中引用了 `atomgit.ref`。但 `atomgit.sha` 在 workflow_dispatch 事件下的行为文档未明确说明——当前为空的行为是否是预期行为存疑。
  - TOCTOU 保护在文档层面更多的是一种安全期望而非明确承诺的 API 行为，测试意图通过 `atomgit.sha` 上下文验证执行 SHA 的锁定。

**置信度**: 中（atomgit.sha 为空是确凿事实，断言关键词 "approved_sha_matched" 从未被脚本输出是测试设计缺陷——脚本需要显式比较并输出标记）

**建议**:
- 脚本需添加显式的比较逻辑和断言标记输出（如 `[ "$ATOMGIT_SHA" = "$APPROVED_SHA" ] && echo approved_sha_matched`）
- 确认 `atomgit.sha` 在 workflow_dispatch 事件下是否应返回非空值
- 相关用例: SEC-TOCTOU-01-002
