## 失败分诊 · COMPAT-CACHE-01-001 · cache 行为等价性——缓存命中场景

**判定结果**: FAIL
**失败断言**:
assertions (cache hit) — job COMPLETED，但 Event Validation Error: Manual event 不在 cache allowlist [push|pr|merge_request]
用例以 workflow_dispatch 触发，cache 插件要求 push/pr/merge_request 事件

**根因初判**: 环境问题
**责任人**: Phase 02

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
  - 前置条件: - 仓库已启用 cache 插件
    - 首次运行已生成缓存条目
  - 操作步骤: 1. 在工作流中使用 `uses: cache` 配置 key 和 path
    2. 首次运行生成缓存后，再次触发同一工作流
    3. 观察第二次运行的缓存恢复行为
  - 预期结果: - 第二次运行时 cache 步骤识别到已有缓存并命中
    - 命中后无需重新生成，直接恢复缓存目录内容
    - cache 插件裸名写法行为与 GitHub 全名写法等价
  - 验证点: - [正向] 第二次运行日志中出现缓存命中标识
    - [正向] 缓存目录内容正确恢复
    - [负向] 不应因 key 匹配而实际未恢复内容

- **实际行为**:
  - Job "Verify cache hit behavior" status=COMPLETED
  - Event Validation Error: Manual 不在 cache 插件 allowlist 中

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/artifacts-and-cache.md`:
  - 规格摘要:
    ```
# 制品与缓存
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
## 缓存（Cache）
    ```
  - 测试 YAML 工作流模式与此规格承诺一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库已启用 cache 插件
    - 首次运行已生成缓存条目

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-CACHE-01-001 的失败根因初步判定为 **环境问题**（责任人: **Phase 02**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-CACHE-01-001 的判断逻辑
- 在 Phase 02 补充环境配置（config_probe、secret 注入、event 匹配等）
