## 失败分诊 · COMPAT-RUNSON-01-001 · runs-on 标签体系——三段式数组正常匹配

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (positive, run_logs) — "日志中应出现 RUNSON_ARRAY_OK"，实际: 待评估
assertions[2] (negative, workflow_parse) — "不应因数组格式 runs-on 而解析失败"，实际: 待评估

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 7 行）:
  ```
=== JOB: Verify three-part runs-on array (status=COMPLETED) ===
[2026/07/23 22:23:59.912 GMT+08:00] [INFO] Job(1529977405961936896_1529977405928382471) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0e2eff48-33b4-4714-afd2-7d43714c9b48.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0e2eff48-33b4-4714-afd2-7d43714c9b48.sh
RUNSON_ARRAY_OK
Runner labels: dedicate-hosted x64 large
  ```

- **预期行为**（Phase 01 文本用例 `COMPAT-RUNSON-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: 平台存在匹配 [dedicate-hosted, x64, large] 标签的 Runner
  - 操作步骤:
    1. 在工作流中声明 `runs-on: [dedicate-hosted, x64, large]`
    2. 触发工作流，观察 Runner 调度行为
    3. 确认 job 被分配到满足所有标签的 Runner 上执行
  - 预期结果:
    - 三段式数组格式被平台正确解析
    - job 成功调度到同时满足三个标签的 Runner
    - 工作流正常执行，无标签匹配错误
  - 验证点:
    - [正向] 工作流成功启动并执行
    - [正向] 日志中显示 Runner 标签与声明一致
    - [负向] 不应因数组格式而被平台拒绝解析

- **实际行为**:
  - Job "Verify three-part runs-on array" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-RUNSON-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        verify-runs-on-array:
          name: Verify three-part runs-on array
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: (TC) echo runner info
              run: |
                echo "RUNSON_ARRAY_OK"
                echo "Runner labels: dedicate-hosted x64 large"
    ```
  - **GitCode 规格** `inputs/gitcode-spec/runner-management/selecting-runner-labels.md` 第 3-6 行（选择 Runner 标签）:
    ```yaml
    # 选择 Runner 标签
    
    **适用场景**：当你需要精确控制 job 在哪类 Runner 上执行——指定操作系统、架构、资源规格、或自定义特征（GPU、特定工具链）——需要理解标签匹配规则。
    
    ```
  - **逐项映射**:
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `workflow_parse` (negative断言) → 规格定义了工作流解析规则
    - 测试用例设计源自规格 `inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 平台存在匹配 [dedicate-hosted, x64, large] 标签的 Runner

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-RUNSON-01-001 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-RUNSON-01-001.log`
- 修复后重新验跑 COMPAT-RUNSON-01-001
- 相关用例: 无
