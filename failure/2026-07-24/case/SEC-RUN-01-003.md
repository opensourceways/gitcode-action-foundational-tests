## 失败分诊 · SEC-RUN-01-003 · 自托管 Runner 跨项目残留必须被隔离

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "cross project leak"` — 无法判定: 两个 job 均 FAILED，无有用输出
  - 正向 `run_logs` `equals: "isolated_as_expected"` — **FAIL**: 两个 job 均在 FAILED 状态，无输出

**根因初判**: 环境问题（自托管 runner 不可用或 job 在启动阶段即失败）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Write project A data (status=FAILED) ===
  [2026/07/23 22:09:54.688 GMT+08:00] [INFO] Job(1529973861045248000_1529973861007499271) duration check: true


  === JOB: Check project B isolation (status=FAILED) ===
  [2026/07/23 22:09:54.659 GMT+08:00] [INFO] Job(1529973861045248000_1529973861007499273) duration check: true
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 自托管 runner 被多个项目共享
  - 操作步骤: 1. 项目 A 的 workflow 写入临时文件和环境变量；2. 项目 B 的 workflow 在同一 runner 上检查残留
  - 预期结果: 项目 B 的 job 绝不应读取到项目 A 残留的敏感文件或环境变量

- **实际行为**:
  - 两个 job 均为 FAILED 状态但日志中无任何步骤执行信息
  - 无 shell 创建日志、无脚本执行日志 — job 在启动阶段就失败了
  - 自托管 runner (`self-hosted` 标签) 不可用或未被正确调度
  - **失败传导链**: 自托管 runner 不可用 → job 无法被调度 → 进入 FAILED 状态 → 测试完全未执行

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `project-a` 和 `project-b`:
    ```yaml
    setup:
      repo_fixture: self-hosted-shared
    jobs:
      project-a:
        name: Write project A data
        runs-on: [self-hosted, x64, large]
        steps:
          - name: Write temp
            run: |
              echo project-a-secret > /tmp/project-a-temp.txt
      project-b:
        name: Check project B isolation
        runs-on: [self-hosted, x64, large]
        steps:
          - name: Check no cross project leak
            run: |
              if [ -f /tmp/project-a-temp.txt ]; then
                echo "cross project leak"
                exit 1
              else
                echo "isolated as expected"
              fi
    ```
  - **GitCode 规格** `runner-management/selecting-runner-labels.md`（自托管配置）:
    ```yaml
    runs-on:
      type: self-hosted
      group: my-runner-group
      labels:
        - linux
        - x64
        - gpu
    ```
  - **逐项映射**:
    - `runs-on: [self-hosted, x64, large]`: 测试 YAML 使用自托管标签 — 匹配规格支持的自托管 runner
    - `setup.repo_fixture: self-hosted-shared`: 测试框架声明需要共享自托管 runner
    - 规格中自托管 runner 仅作为概念描述，未说明测试环境如何为此场景准备

- **环境前置条件验证**: **FAIL** — 无 shell 创建，无脚本执行，job 在调度阶段即失败。自托管 runner 环境不可用。

**置信度**: 高（job 零输出，自托管 runner 不可用）

**影响**:
- **阻塞性**: 高 — 自托管 runner 测试场景完全不可用
- **静默性**: 低 — FAILED 状态明确
- **影响面**: 中 — 影响所有依赖自托管 runner 的测试
- **综合**: 自托管 runner（`[self-hosted, x64, large]`）不可用，两个 job 均零输出直接 FAILED，跨项目隔离测试完全未执行
- **是否有规避手段**: 是 — 部署或配置自托管 runner；或使用 dedicate-hosted runner 模拟

**建议**:
- Phase 02: (1) 确认测试环境中是否有可用自托管 runner；(2) 若否，注册自托管 runner 或修改测试为使用 `dedicate-hosted` runner + `needs` 约束模拟跨 runner 场景
- 平台方: 提供测试用自托管 runner 模板或 mock
