## 失败分诊 · SEC-TOCTOU-01-001 · 审批后推送新 commit 不应被已授权特权运行执行

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "unapproved_commit_executed"` — 无法判定: commit SHA 输出为空
  - 正向 `run_logs` `equals: "approved_sha_matched"` — **FAIL**: 输出 "Running commit: " 后为空，无法确认 SHA

**根因初判**: 测试环境缺少审批流程和 commit SHA 上下文
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test TOCTOU protection (status=COMPLETED) ===
  [2026/07/23 22:10:48.247 GMT+08:00] [INFO] Job(1529974085599641600_1529974085566087175) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/89cfca38-c55f-46eb-acf8-5bf6a7c6d07b.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/89cfca38-c55f-46eb-acf8-5bf6a7c6d07b.sh
  Running commit: 
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库配置了审批触发 workflow
  - 操作步骤: 1. 管理员审批一个 workflow 运行；2. 在审批后、执行前，攻击者推送恶意 commit；3. 观察特权运行是否执行了新 commit
  - 预期结果: 特权运行应绑定审批时刻的具体 commit SHA

- **实际行为**:
  - 测试通过 `workflow_dispatch`（手动触发）运行，不存在审批流程
  - `${{ atomgit.sha }}` 求值为空 → 输出 "Running commit: " 无 SHA
  - 手动触发的工作流没有对应的 push commit SHA
  - **失败传导链**: `workflow_dispatch` trigger → 无 commit SHA 上下文 → `atomgit.sha` 为空 → 无法绑定审批时刻的 commit → TOCTOU 验证无法进行

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `toctou-test` 的 `Check commit SHA`:
    ```yaml
    on:
      workflow_dispatch:
    jobs:
      toctou-test:
        name: Test TOCTOU protection
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Check commit SHA
            run: |
              echo "Running commit: ${{ atomgit.sha }}"
    ```
  - **GitCode 规格** `syntax-reference/runner-images-tools.md` 及 `writing-pipelines/using-script-commands.md`:
    ```
    规格中 atomgit.sha 上下文的定义
    ```
  - **逐项映射**:
    - `${{ atomgit.sha }}`: 测试 YAML 引用 commit SHA — 在 `workflow_dispatch` 事件下可能为空
    - `on.workflow_dispatch`: 手动触发 — 不产生 commit SHA，与 TOCTOU 攻击场景的前提（审批 → 推送恶意 commit）不兼容
    - **测试设计缺陷**: TOCTOU 攻击需要审批流程 + push 事件，手动触发无法模拟

- **环境前置条件验证**: `workflow_dispatch` 下 `atomgit.sha` 为空，前置条件（审批触发 workflow）不满足

**置信度**: 高（`atomgit.sha` 为空，与测试设计不符）

**影响**:
- **阻塞性**: 高 — 测试场景与平台能力不匹配（审批流程未就绪）
- **静默性**: 高 — 当前测试无法发现 TOCTOU 漏洞
- **影响面**: 中 — TOCTOU 是审批类 CI/CD 的关键安全威胁
- **综合**: 测试使用 `workflow_dispatch`（无审批、无 commit SHA）模拟需要审批 + push 事件联动的 TOCTOU 攻击场景，`atomgit.sha` 为空导致测试完全无效
- **是否有规避手段**: 是 — 等待平台审批流程功能就绪后重新设计测试

**建议**:
- Phase 01: 重新评估 TOCTOU 测试流程：(1) 确认平台是否支持审批触发（approval gate / protected environment）；(2) 若支持，将 trigger 从 `workflow_dispatch` 改为审批相关的事件类型；(3) 在用例文档中标记为"前置依赖：审批流程已上线"
- 平台方: 明确审批流程与 commit SHA 绑定的文档说明
