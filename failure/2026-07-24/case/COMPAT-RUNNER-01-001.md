## 失败分诊 · COMPAT-RUNNER-01-001 · runner.os 在 Linux Runner 上应返回 Linux

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (positive, run_logs) — "日志中 runner_os 应等于 Linux（首字母大写），不应为小写 linux"，实际: 待评估

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 7 行）:
  ```
=== JOB: Test runner.os value (status=COMPLETED) ===
[2026/07/23 22:23:37.671 GMT+08:00] [INFO] Job(1529977312760053760_1529977312730693639) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/3be8b7d2-ec6d-4020-9809-502bab3ebdf8.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/3be8b7d2-ec6d-4020-9809-502bab3ebdf8.sh
runner_os=linux
done
  ```

- **预期行为**（Phase 01 文本用例 `COMPAT-RUNNER-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 Actions; 存在 Linux 标签的 Runner
  - 操作步骤:
    1. 在 workflow 的 run 步骤中输出 ${{ runner.os }}
    2. 触发 workflow 运行
  - 预期结果:
    - runner.os 应返回 Linux（首字母大写，与 GitHub 一致）
  - 验证点:
    - [正向] 日志中 runner.os 的值为 Linux
    - [负向] 不应返回小写的 linux

- **实际行为**:
  - Job "Test runner.os value" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-RUNNER-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        test:
          name: Test runner.os value
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Echo runner os
              run: |
                echo "runner_os=${{ runner.os }}"
                echo "done"
    ```
  - **GitCode 规格** `inputs/gitcode-spec/runner-management/selecting-runner-labels.md` 第 3-6 行（选择 Runner 标签）:
    ```yaml
    # 选择 Runner 标签
    
    **适用场景**：当你需要精确控制 job 在哪类 Runner 上执行——指定操作系统、架构、资源规格、或自定义特征（GPU、特定工具链）——需要理解标签匹配规则。
    
    ```
  - **逐项映射**:
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试用例设计源自规格 `inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 Actions; 存在 Linux 标签的 Runner

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-RUNNER-01-001 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-RUNNER-01-001.log`
- 修复后重新验跑 COMPAT-RUNNER-01-001
- 相关用例: COMPAT-RUNNER-01-002
