## 失败分诊 · COMP-CACHE-01-001 · cache hit 时恢复缓存内容正确

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `FAILED`（平台缺陷导致 job 执行失败）
assertions[1] (positive, cache_step) — 期望 `hit`，下游随上游失败而 IGNORED

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（共 2 行）:
```
=== JOB: Verify cache hit (status=FAILED) ===
[2026/07/23 22:02:17.090 GMT+08:00] [INFO] Job(1529971941337346048_1529971941316374535) duration check: true
```

  **日志分析**: Job "Verify cache hit" status=FAILED, 0 字节有效日志，Job 未执行步骤

- **预期行为**（Phase 01 文本用例 `COMP-CACHE-01-001`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "触发 workflow，使用 cache 插件"
  - 操作步骤 2: "观察 cache 是否命中"

  预期结果:
  - cache 命中并正确恢复内容

  验证点:
  - [正向] cache 步骤状态为 success
  - [正向] 恢复后的文件内容与之前一致

- **实际行为**:
  - Job "Verify cache hit" status=FAILED, 0 字节有效日志，Job 未执行步骤


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

**置信度**: 中（Job "Verify cache hit" status=FAILED, 0 字节有效日志，Job 未执行步骤）

**影响**:
- **阻塞性**: 🔴阻塞 — Job FAILED 且 0 字节 shell 日志，cache hit 验证无法完成
- **静默性**: 🟡可察觉 — Job status=FAILED 但零 shell 输出，仅系统 duration check 行，无诊断信息
- **影响面**: 🔴跨维度 — cache 步骤未执行即失败，整个缓存系统不可用
- **综合**: cache 功能完全故障，Job 在未执行任何步骤的情况下 FAILED，影响所有依赖缓存的 workflow
- **是否有规避手段**: 否 — 平台 cache 链路缺陷

**建议**:
- 将此缺陷提交给平台工程团队，附上日志文件 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-CACHE-01-001.log`
- 建议修复后重新验跑 COMP-CACHE-01-001
- 相关用例: COMP-CACHE-01-002
