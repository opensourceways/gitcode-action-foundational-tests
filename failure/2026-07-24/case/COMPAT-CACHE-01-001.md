## 失败分诊 · COMPAT-CACHE-01-001 · cache 行为等价性——缓存命中场景

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_logs) — "第二次运行日志中应出现 CACHE_HIT"，实际: 待评估
assertions[1] (negative, run_logs) — "命中场景下不应出现持久化失败或 key 冲突报错"，实际: 待评估

**根因初判**: 断言失败
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 12 行）:
  ```
=== JOB: Verify cache hit behavior (status=COMPLETED) ===
[2026/07/23 22:17:14.476 GMT+08:00] [INFO] Job(1529975705632784384_1529975705595035655) duration check: true
::warning::Event Validation Error: The event type Manual (normalized: manual) is not supported because it's not tied to a branch or tag ref.
::warning::[cache eventValidation] normalized=manual allowlistMatch=false allowlist=[push|pull_request|merge_request] ATOMGIT_EVENT_NAME=Manual GITHUB_EVENT_NAME=Manual ATOMGIT_REF=main GITHUB_REF=main | hint: EVENT_NAME normalized "Manual" -> "manual" for allowlist check; event not in allowlist [push|pull_request|merge_request]

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/39d53118-33e1-4736-9483-446a1fe38d6d.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/39d53118-33e1-4736-9483-446a1fe38d6d.sh
CACHE_MISS

::warning::Event Validation Error: The event type Manual (normalized: manual) is not supported because it's not tied to a branch or tag ref.
::warning::[cache eventValidation] normalized=manual allowlistMatch=false allowlist=[push|pull_request|merge_request] ATOMGIT_EVENT_NAME=Manual GITHUB_EVENT_NAME=Manual ATOMGIT_REF=main GITHUB_REF=main | hint: EVENT_NAME normalized "Manual" -> "manual" for allowlist check; event not in allowlist [push|pull_request|merge_request]
  ```

- **预期行为**（Phase 01 文本用例 `COMPAT-CACHE-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 cache 插件; 首次运行已生成缓存条目
  - 操作步骤:
    1. 在工作流中使用 `uses: cache` 配置 key 和 path
    2. 首次运行生成缓存后，再次触发同一工作流
    3. 观察第二次运行的缓存恢复行为
  - 预期结果:
    - 第二次运行时 cache 步骤识别到已有缓存并命中
    - 命中后无需重新生成，直接恢复缓存目录内容
    - cache 插件裸名写法行为与 GitHub 全名写法等价
  - 验证点:
    - [正向] 第二次运行日志中出现缓存命中标识
    - [正向] 缓存目录内容正确恢复
    - [负向] 不应因 key 匹配而实际未恢复内容

- **实际行为**:
  - Job "Verify cache hit behavior" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-CACHE-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        verify-cache-hit:
          name: Verify cache hit behavior
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: (TC) restore cache
              uses: cache
              with:
                path: ~/.cache/test-dir
                key: compat-cache-test-${{ atomgit.run_id }}
                restore-keys: compat-cache-test-
            - name: (TC) verify cache state
              run: |
                if [ -f "$HOME/.cache/test-dir/marker.txt" ]; then
                  echo "CACHE_HIT"
                else
                  echo "CACHE_MISS"
                  mkdir -p "$HOME/.cache/test-dir"
                  echo "marker" > "$HOME/.cache/test-dir/marker.txt"
                fi
            - name: (TC) save cache
              if: ${{ always() }}
              uses: cache
              with:
                path: ~/.cache/test-dir
                key: compat-cache-test-${{ atomgit.run_id }}
    ```
  - **GitCode 规格** `inputs/gitcode-spec/core-concepts/artifacts-and-cache.md` 第 21-34 行（缓存（Cache））:
    ```yaml
    ## 缓存（Cache）
    
    缓存用于加速依赖安装，避免重复下载：
    
    ```yaml
    steps:
      - uses: cache
        with:
          key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
          path: ~/.npm
          restore-keys: |
            npm-${{ runner.os }}-
    ```
    
    ```
  - **逐项映射**:
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `run_logs` (negative断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/artifacts-and-cache.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 cache 插件; 首次运行已生成缓存条目

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-CACHE-01-001 的失败根因初步判定为 **断言失败**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-CACHE-01-001.log`
- 修复后重新验跑 COMPAT-CACHE-01-001
- 相关用例: 无
