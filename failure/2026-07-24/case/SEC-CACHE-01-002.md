## 失败分诊 · SEC-CACHE-01-002 · 主仓 cache restore 对 fork cache miss

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, cache_restore) — must_not_hit "fork_cache_key"（无法验证，cache 未执行）；assertions[1] (positive, run_logs) — 期望日志含 "cache_miss"，实际 cache action 因事件类型不匹配完全未执行

**根因初判**: 平台缺陷

**证据**:

- **Job 日志全量**（仅 4 行）:
  ```
  === JOB: Restore cache from main repo (status=COMPLETED) ===
  [2026/07/23 22:05:10.573 GMT+08:00] [INFO] Job(1529972669225377792_1529972669187629063) duration check: true
  ::warning::Event Validation Error: The event type Manual (normalized: manual) is not supported because it's not tied to a branch or tag ref.
  ::warning::[cache eventValidation] normalized=manual allowlistMatch=false allowlist=[push|pull_request|merge_request] ATOMGIT_EVENT_NAME=Manual GITHUB_EVENT_NAME=Manual ATOMGIT_REF=main GITHUB_REF=main | hint: EVENT_NAME normalized "Manual" -> "manual" for allowlist check; event not in allowlist [push|pull_request|merge_request]
  ```
  cache action 在 `workflow_dispatch`（Manual）事件下拒绝执行。平台 cache 插件仅允许 `push|pull_request|merge_request` 事件，`workflow_dispatch` 不在允许列表中。cache restore/logic 本身从未被测试到。

- **预期行为**（Phase 01 文本用例 `SEC-CACHE-01-002`，优先级 P0，维度 security）:
  - 操作步骤 1: "在主仓触发 workflow，使用与 fork PR 相同的 cache key 尝试 restore"
  - 操作步骤 2: "查看 restore 结果"
  - 预期结果: "cache restore 结果为 miss；日志中显示未找到对应缓存"
  - 验证点: "[正向] cache restore 返回 miss"

- **实际行为**:
  - cache action 在 workflow_dispatch 事件下因事件校验被拒绝，cache 功能完全未执行
  - 无法验证主仓是否命中 fork PR 的缓存——测试逻辑本身被平台事件限制阻断

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `cache-restore` job 的 `Restore cache` 步骤:
    ```yaml
    - name: Restore cache
      uses: cache
      with:
        path: ./node_modules
        key: test-cache-key
    ```
  - 这对应 GitCode 规格 `writing-pipelines/using-dependency-cache.md` 第 15-37 行的快速示例:
    ```yaml
    on:
      push:
        branches:
          - main
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - uses: checkout
          - name: Cache npm dependencies
            uses: cache
            with:
              path: ~/.npm
              key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
              restore-keys: |
                npm-${{ runner.os }}-
    ```
    规格文档的 cache 示例均在 `push` 事件下演示，但未明确声明 cache 不支持 `workflow_dispatch` 事件。平台 cache 插件通过内部 allowlist 限制了事件类型这一行为本身是合理的，但文档缺少说明，导致测试设计基于错误的触发事件假设。
  - 同时对应规格第 60-65 行的缓存匹配机制：
    ```
    缓存匹配机制:
    1. 首先尝试精确匹配 key。
    2. 精确匹配失败时，按 restore-keys 列表顺序尝试前缀匹配。
    3. 前缀匹配恢复的是最近一次同前缀的缓存。
    4. 所有匹配都失败时，step 执行后会将 path 内容保存为新缓存。
    ```
    此描述承诺了 cache miss 时 step 仍然执行并保存新缓存，但平台在事件校验层就拒绝了 cache action，绕过了整个匹配逻辑。

**置信度**: 中（cache 因事件限制未执行是确凿事实，但 fork cache 隔离是否真的有效未被测试）

**建议**:
- 将触发事件从 `workflow_dispatch` 改为 `push` 以通过 cache 插件的事件校验
- 在规格文档 `using-dependency-cache.md` 中补充说明 cache 插件支持的事件类型
- 相关用例: SEC-CACHE-01-001, COMP-CACHE-01-001, COMP-CACHE-01-002
