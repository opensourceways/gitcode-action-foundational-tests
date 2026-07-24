## 失败分诊 · REL-NEEDS-01-025 · needs 失败传播——上游 job 失败时下游 job 应被 skip

**判定结果**: FAIL
**失败断言**: 正向/job_a_status expected=failure actual=FAILED; 正向/job_b_status expected=skipped actual=IGNORED

**根因初判**: 平台缺陷（job_b 状态为 IGNORED 而非 skipped）
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: upstream failing job (status=FAILED) ===
  [2026/07/23 22:33:52.461 GMT+08:00] [INFO] Job(1529979891682521088_1529979891657355271) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c1c13e84-9d75-4ff3-b3ad-c9e88d6a8a55.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c1c13e84-9d75-4ff3-b3ad-c9e88d6a8a55.sh
  ::error::Process exited with code 1

  === JOB: downstream dependent job (status=IGNORED) ===
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: 触发含 job_a(失败) 和 job_b(needs: job_a) 的 workflow
  - 预期结果: job_a 状态=failure; job_b 状态=skipped; job_b 不应执行

- **实际行为**:
  - job_a 执行 `exit 1` 后正确 FAILED
  - job_b (needs: job_a) 被标记为 IGNORED（未执行任何 step）
  - 断言期望 `job_b_status=skipped`，但平台返回 `IGNORED`
  - 语义等价（都没执行），但状态标签不匹配
  - **失败传导链**: job_a FAILED → needs 依赖导致 job_b IGNORED（非 skipped）→ 断言字符串匹配失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `job_a`:
    ```yaml
    job_a:
      name: upstream failing job
      runs-on: [dedicate-hosted, x64, large]
      steps:
        - name: fail step
          run: |
            exit 1
    ```
  - **测试 YAML** 中 `job_b`:
    ```yaml
    job_b:
      name: downstream dependent job
      runs-on: [dedicate-hosted, x64, large]
      needs: job_a
      steps:
        - name: should be skipped
          run: |
            echo this should not run
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 73-95 行:
    ```yaml
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - run: echo "build"
      test:
        runs-on: [ubuntu-latest, x64, small]
        needs: build
        steps:
          - run: echo "test"
    ```
  - **GitCode 规格** `writing-pipelines/configure-dependencies-order.md` 第 83 行:
    依赖的 job 失败时，当前 job 默认不执行
  - **逐项映射**: `needs: job_a` → 匹配规格; `exit 1` → 正确触发失败。规格描述 "当前 job 默认不执行" 但未明确定义不执行时的状态标签。平台使用 `IGNORED` 而测试断言期望 `skipped`——这是标签语义的标准化/对齐问题。

- **环境前置条件验证**: runner 可用，job_a 正确失败，job_b 正确未执行

**置信度**: 高（IGNORED vs skipped 是确定的字符串不匹配；功能行为正确——job_b 未执行）

**影响**:
- **阻塞性**: 🟢不阻塞 — 功能正确（needs 失败传播生效，job_b 未执行）
- **静默性**: 🟢明确 — job_b 状态 IGNORED 清晰
- **影响面**: 🟡断言层 — 仅影响状态标签断言
- **综合**: 平台 needs 依赖失败传播功能正确，但状态标签 `IGNORED` vs `skipped` 与测试期望不匹配
- **是否有规避手段**: 是（将断言从 `equals: "skipped"` 改为 `equals: "IGNORED"` 或 `in: ["IGNORED", "skipped"]`）

**建议**:
- 统一 needs 失败传播的下游 job 状态标签：是 IGNORED 还是 skipped
- 更新断言以接受 IGNORED（或不严格要求 skipped）
