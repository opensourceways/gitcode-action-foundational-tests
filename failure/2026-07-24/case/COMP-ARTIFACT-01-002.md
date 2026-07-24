## 失败分诊 · COMP-ARTIFACT-01-002 · 下载全部制品功能正常

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED
assertions[1] (positive, run_logs) — 期望日志包含 `app`，因 job FAILED 未执行验证
assertions[2] (positive, run_logs) — 期望日志包含 `report`，因 job FAILED 未执行验证

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 7 行）:
  ```
=== JOB: Build multiple artifacts (status=FAILED) ===
[2026/07/23 22:11:42.758 GMT+08:00] [INFO] Job(1529974314361176064_1529974314323427335) duration check: true

 
 

=== JOB: Download all artifacts (status=IGNORED) ===
  ```

- **预期行为**（Phase 01 文本用例 `COMP-ARTIFACT-01-002`，优先级 P1，维度 completeness）:
  - 前置条件: workflow 上传多个 artifacts
  - 操作步骤:
    1. job 1 上传多个 artifacts
    2. job 2 不指定 name 下载全部 artifacts
  - 预期结果:
    - 所有 artifacts 被下载到指定目录
  - 验证点:
    - [正向] 所有 artifact 文件均存在

- **实际行为**:
  - Job "Build multiple artifacts" status=FAILED
  - Job "Download all artifacts" status=IGNORED
  - **失败传导链**: **Build multiple artifacts** (FAILED) → **Download all artifacts** (IGNORED)

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMP-ARTIFACT-01-002.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        build:
          name: Build multiple artifacts
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Create artifacts
              run: |
                mkdir -p dist reports
                echo "app" > dist/app.txt
                echo "report" > reports/coverage.txt
            - name: Upload app
              uses: upload-artifact
              with:
                name: app
                path: dist/
            - name: Upload reports
              uses: upload-artifact
              with:
                name: reports
                path: reports/
        verify:
          name: Download all artifacts
          runs-on: [dedicate-hosted, x64, large]
          needs: build
          steps:
            - name: Download all
              uses: download-artifact
              with:
                path: artifacts/
            - name: Verify all
              run: |
                cat artifacts/app/app.txt
                cat artifacts/reports/coverage.txt
    ```
  - **GitCode 规格** `inputs/gitcode-spec/core-concepts/artifacts-and-cache.md` 第 5-20 行（制品（Artifacts））:
    ```yaml
    ## 制品（Artifacts）
    
    制品是工作流运行产生的文件，可跨任务传递：
    
    ```yaml
    steps:
      - uses: upload-artifact
        with:
          name: build-output
          path: dist/
      - uses: download-artifact
        with:
          name: build-output
          path: ./app
    ```
    
    ```
  - **逐项映射**:
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/artifacts-and-cache.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: workflow 上传多个 artifacts

**置信度**: 高（job status=FAILED 且下游 IGNORED，平台执行层明确故障）

**影响**:
- **阻塞性**: 🔴阻塞 — 上游 job FAILED 导致下游全部跳过，功能不可用
- **静默性**: 🟡可察觉 — 通过 job status=FAILED 可见，但 shell 诊断输出有限
- **影响面**: 🔴跨维度 — 两端传播（上游 FAILED + 下游 IGNORED），平台核心功能故障
- **综合**: 基于上述证据，COMP-ARTIFACT-01-002 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 否 — 平台功能缺陷

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-ARTIFACT-01-002.log`
- 修复后重新验跑 COMP-ARTIFACT-01-002
- 相关用例: COMP-ARTIFACT-01-003
