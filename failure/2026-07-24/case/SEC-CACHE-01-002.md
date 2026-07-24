## 失败分诊 · SEC-CACHE-01-002 · 主仓 cache restore 对 fork cache miss

**判定结果**: FAIL
**失败断言**:
  - 负向 `cache_restore` `must_not_hit: "fork_cache_key"` — 无法验证: cache action 被跳过，未实际执行 restore
  - 正向 `run_logs` `equals: "cache_miss"` — 无法验证: 日志显示 Event Validation Error，cache action 未运行

**根因初判**: 测试 YAML 事件 trigger 与平台允许列表不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Restore cache from main repo (status=COMPLETED) ===
  [2026/07/23 22:05:10.573 GMT+08:00] [INFO] Job(1529972669225377792_1529972669187629063) duration check: true
  ::warning::Event Validation Error: The event type Manual (normalized: manual) is not supported because it's not tied to a branch or tag ref.
  ::warning::[cache eventValidation] normalized=manual allowlistMatch=false allowlist=[push|pull_request|merge_request] ATOMGIT_EVENT_NAME=Manual GITHUB_EVENT_NAME=Manual ATOMGIT_REF=main GITHUB_REF=main | hint: EVENT_NAME normalized "Manual" -> "manual" for allowlist check; event not in allowlist [push|pull_request|merge_request]
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: fork PR 已写入 cache
  - 操作步骤: 1. 在主仓触发 workflow，使用与 fork PR 相同的 cache key 尝试 restore；2. 查看 restore 结果
  - 预期结果: cache restore 结果为 miss；日志中显示未找到对应缓存

- **实际行为**:
  - cache action 因 Event Validation Error 被跳过，未执行 restore
  - 平台 cache 组件只允许 `[push|pull_request|merge_request]` 事件，`workflow_dispatch`（Manual）不在允许列表中
  - 实际未产生 cache miss/hit 结果
  - **失败传导链**: 测试 YAML trigger 设为 `workflow_dispatch` → 平台 cache 组件 Event Validation 拒绝 Manual 事件 → cache action 被跳过 → 无法验证跨仓库 cache 隔离

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `cache-restore` 的 `Restore cache`:
    ```yaml
    steps:
      - name: Restore cache
        uses: cache
        with:
          path: ./node_modules
          key: test-cache-key
    ```
  - **GitCode 规格** `core-concepts/artifacts-and-cache.md` 第 25-33 行:
    ```yaml
    steps:
      - uses: cache
        with:
          key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
          path: ~/.npm
          restore-keys: |
            npm-${{ runner.os }}-
    ```
  - **逐项映射**:
    - `path`: 测试 `./node_modules` vs 规格 `~/.npm` — 合法，仅为路径差异
    - `key`: 测试 `test-cache-key` vs 规格 `npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}` — 合法，测试用静态 key
    - `restore-keys`: 测试未指定 vs 规格指定了 — 非必填
    - **trigger 事件**: 测试 `workflow_dispatch` 不在 cache 组件允许列表 `[push|pull_request|merge_request]` 中

- **环境前置条件验证**: 未发现 secrets/token 缺失；平台运行环境正常但 trigger 不匹配

**置信度**: 高（日志明确显示 Event Validation Error，trigger 不匹配为直接原因）

**影响**:
- **阻塞性**: 中 — 测试无法达到验证目标，但核心功能（跨仓库 cache 隔离）未测试
- **静默性**: 低 — 平台明确报出 warning，行为可观测
- **影响面**: 低 — 仅限于本用例；修改 trigger 即可回复测试能力
- **综合**: 测试 YAML 使用 `workflow_dispatch` 触发 cache action，但平台 cache 组件仅允许 `push`/`pull_request`/`merge_request` 事件，导致测试跳过核心验证
- **是否有规避手段**: 是 — 修改 trigger 为 `push` 或 `pull_request`

**建议**:
- Phase 01: 更新测试用例的 trigger 条件，将 `workflow_dispatch` 改为平台 cache 组件支持的 `push` 事件
- Phase 02: 重新生成测试 YAML，trigger.event 改为 `push`，确保 cache action 正常触发
