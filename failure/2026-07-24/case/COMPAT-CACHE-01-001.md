## 失败分诊 · COMPAT-CACHE-01-001 · cache 行为等价性——缓存命中场景

**判定结果**: FAIL
**失败断言**: 

**根因初判**: 产品bug

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

  **日志分析**: CACHE_MISS, "Event Validation Error: The event type Manual...is not supported" — cache 不支持 workflow_dispatch

- **预期行为**（Phase 01 文本用例 `COMPAT-CACHE-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在工作流中使用 `uses: cache` 配置 key 和 path"
  - 操作步骤 2: "首次运行生成缓存后，再次触发同一工作流"
  - 操作步骤 3: "观察第二次运行的缓存恢复行为"

  预期结果:
  - 第二次运行时 cache 步骤识别到已有缓存并命中
  - 命中后无需重新生成，直接恢复缓存目录内容
  - cache 插件裸名写法行为与 GitHub 全名写法等价

  验证点:
  - [正向] 第二次运行日志中出现缓存命中标识
  - [正向] 缓存目录内容正确恢复
  - [负向] 不应因 key 匹配而实际未恢复内容

- **实际行为**:
  - CACHE_MISS, "Event Validation Error: The event type Manual...is not supported" — cache 不支持 workflow_dispatch


- **测试 YAML 与规格精确对照**:
  - 规格文件: `using-dependency-cache.md` (路径: `phase01/inputs/gitcode-spec/writing-pipelines/using-dependency-cache.md`)
  - 规格节选:
```yaml
steps:
  - name: Cache dependencies
    uses: cache
    with:
      path: ~/.npm
      key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
      restore-keys: |
        npm-${{ runner.os }}-
```
    该规格明确声明: 43-52行的 cache 插件参数示例

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（CACHE_MISS, "Event Validation Error: The event type Manual...is not supported" — cache 不支持 workflow_dispatch）

**建议**:
- 将此缺陷提交给平台工程团队，附上日志文件 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-CACHE-01-001.log`
- 建议修复后重新验跑 COMPAT-CACHE-01-001
