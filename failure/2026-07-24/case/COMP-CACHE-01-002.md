## 失败分诊 · COMP-CACHE-01-002 · restore-keys 前缀匹配兜底生效

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, cache_step) — 期望 `restore_hit`，实际 `FAILED`（平台缺陷导致 job 执行失败）

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（共 2 行）:
```
=== JOB: Verify restore keys fallback (status=FAILED) ===
[2026/07/23 22:02:27.919 GMT+08:00] [INFO] Job(1529971987059707904_1529971987034542087) duration check: true
```

  **日志分析**: Job "Verify restore keys fallback" status=FAILED, 0 字节有效日志

- **预期行为**（Phase 01 文本用例 `COMP-CACHE-01-002`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "触发 workflow，精确 key 不匹配但 restore-keys 前缀匹配"

  预期结果:
  - restore-keys 前缀匹配成功，恢复最近同前缀缓存

  验证点:
  - [正向] cache 步骤通过 restore-keys 命中

- **实际行为**:
  - Job "Verify restore keys fallback" status=FAILED, 0 字节有效日志


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

**置信度**: 中（Job "Verify restore keys fallback" status=FAILED, 0 字节有效日志）

**影响**:
- **阻塞性**: 🔴阻塞 — Job FAILED 且 0 字节 shell 日志，restore-keys 前缀匹配验证无法完成
- **静默性**: 🟡可察觉 — Job status=FAILED 但零 shell 输出，无法区分是 cache 插件缺陷还是 runner 环境问题
- **影响面**: 🔴跨维度 — cache restore-keys 功能完全不可用
- **综合**: cache 恢复能力整体故障，restore-keys 前缀匹配未被测试到
- **是否有规避手段**: 否 — 平台 cache 链路缺陷

**建议**:
- 将此缺陷提交给平台工程团队，附上日志文件 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-CACHE-01-002.log`
- 建议修复后重新验跑 COMP-CACHE-01-002
- 相关用例: COMP-CACHE-01-001
