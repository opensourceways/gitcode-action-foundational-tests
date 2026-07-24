## 失败分诊 · REL-YAMLCACHE-01-060 · Workflow YAML 缓存失效——修改后无旧代码残留

**判定结果**: FAIL
**失败断言**: 正向/日志打印 marker_v2 actual=marker_v1; 负向/不应打印 marker_v1 actual=found(marker_v1)

**根因初判**: 平台缺陷 / 环境/Harness（workflow YAML 修改后 runner 仍使用缓存旧版本）
**责任人**: 平台方 / Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: YAML cache invalidation test (status=COMPLETED) ===
  [2026/07/23 22:39:31.470 GMT+08:00] [INFO] Job(1529981313643851776_1529981313627074567) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/3b5dcf9a-66a1-4b08-b131-8a31993711ae.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/3b5dcf9a-66a1-4b08-b131-8a31993711ae.sh
  marker_v1
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 修改与触发权限
  - 操作步骤: 第一轮执行记录输出 marker_v1; 修改 workflow 输出为 marker_v2 并 push; 立即触发 workflow
  - 预期结果: 新触发运行日志中出现 marker_v2; 不应出现 marker_v1 缓存残留

- **实际行为**:
  - Job 输出 `marker_v1` 而非 `marker_v2`
  - 说明 runner 使用的仍然是修改前的旧版本 workflow YAML
  - 可能原因：(1) test harness 在修改 YAML 后 push 未成功; (2) 平台缓存了旧 YAML 未失效; (3) 触发时机在 push 完成之前
  - **失败传导链**: YAML 未更新到 v2 → job 执行旧 v1 代码 → marker_v1 出现 → marker_v2 断言失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` step（版本 v1——修改前）:
    ```yaml
    - name: echo marker
      run: |
        echo marker_v1
    ```
  - **GitCode 规格** `writing-pipelines/workflow-file-location-structure.md` — workflow 文件应在 commit 后即时生效
  - **GitCode 规格** `running-pipelines/manually-trigger-pipeline.md` 第 79-89 行:
    手动触发（workflow_dispatch）使用 `workflow_dispatch` 事件触发，应使用当前分支上的 `.gitcode/workflows/` 文件版本
  - **逐项映射**: workflow_dispatch 触发应使用最新 commit 的 YAML; 但实际执行了旧版本 marker_v1。这表明以下至少一项成立：(1) test harness push 未成功; (2) 平台缓存未在 push 后失效; (3) workflow_dispatch 触发时的 ref 指向了 pre-push 的 commit。

- **环境前置条件验证**: runner 可用，job 正常执行但运行的是旧版本 workflow YAML

**置信度**: 中（输出 marker_v1 明确，但根因可能是 push 失败、平台缓存延迟、或 test harness 触发顺序问题）

**影响**:
- **阻塞性**: 🟡中等 — workflow YAML 缓存/更新机制待验证
- **静默性**: 🟡中等 — job 静默成功但输出了旧版本内容
- **影响面**: 🟡同用例 — 仅影响 YAML 缓存失效验证
- **综合**: 无法确认是平台缓存问题还是 test harness 的 push 未成功——需进一步排查
- **是否有规避手段**: 是（检查 test harness push 后等待时间；确认 git push 返回码；手动验证 YAML 修改是否生效）

**建议**:
- 检查 test harness 的 push 操作是否成功（git push 返回码和 log）
- 在 push 后增加等待时间（如 5-10 秒）确保平台缓存失效
- 考虑使用不同 workflow 文件名称的两阶段版本而非同一文件的修改，避免缓存问题
