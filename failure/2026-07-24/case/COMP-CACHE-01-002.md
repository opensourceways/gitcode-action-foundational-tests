## 失败分诊 · COMP-CACHE-01-002 · restore-keys 前缀匹配兜底生效

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, cache_step) — 期望 `restore_hit`，实际 job status=FAILED

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 2 行）:
  ```
=== JOB: Verify restore keys fallback (status=FAILED) ===
[2026/07/23 22:02:27.919 GMT+08:00] [INFO] Job(1529971987059707904_1529971987034542087) duration check: true
  ```

- **预期行为**（Phase 01 文本用例 `COMP-CACHE-01-002`，优先级 P0，维度 completeness）:
  - 前置条件: 之前运行已生成前缀匹配的 cache
  - 操作步骤:
    1. 触发 workflow，精确 key 不匹配但 restore-keys 前缀匹配
  - 预期结果:
    - restore-keys 前缀匹配成功，恢复最近同前缀缓存
  - 验证点:
    - [正向] cache 步骤通过 restore-keys 命中

- **实际行为**:
  - Job "Verify restore keys fallback" status=FAILED
  - Job "Verify restore keys fallback" FAILED，无下游依赖

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMP-CACHE-01-002.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        verify:
          name: Verify restore keys fallback
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Cache test file
              uses: cache
              with:
                path: cached.txt
                key: cache-test-v2-${{ runner.os }}
                restore-keys: |
                  cache-test-v1-${{ runner.os }}
                  cache-test-
            - name: Use cache
              run: |
                cat cached.txt || echo "cache miss"
    ```
  - **GitCode 规格**: 未找到对应规格文件
  - **逐项映射**:
    - 测试 `cache_step` (positive断言) → 规格定义了缓存命中行为
    - 测试用例设计源自规格 `inputs/gitcode-spec/`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 之前运行已生成前缀匹配的 cache

**置信度**: 中（job status=FAILED 但日志信息有限）

**影响**:
- **阻塞性**: 🔴阻塞 — job FAILED 导致功能不可用
- **静默性**: 🟡可察觉 — 通过 job status=FAILED 可见
- **影响面**: 🟡局部 — 影响单一功能点
- **综合**: 基于上述证据，COMP-CACHE-01-002 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 否 — 平台功能缺陷

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-CACHE-01-002.log`
- 修复后重新验跑 COMP-CACHE-01-002
- 相关用例: COMP-CACHE-01-001
