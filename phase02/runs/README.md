# Run 目录说明

每次 `/phase02-exec` 在此目录下创建 `YYYY-MM-DD-NN`（NN 为当日序号）的 run 目录。

## run 目录结构

```
runs/<run-id>/
├── run.md                    # 元信息：参数、输入快照、时间线、状态
├── queue.md                  # 执行队列（通过校验的用例清单，按优先级排序）
├── rejected.md               # 拒收清单（schema 校验不通过）
├── results/<case-id>.json    # 每条用例的完整执行结果（RunResult + AssertionResult）
├── summary.json              # 结构化汇总（分维度统计）
└── timeline.md               # 执行时间线
```

## run.md 模板

```markdown
# Run <run-id>

## 元信息
- **状态**: running | completed | aborted
- **Phase 01 run**: <source-run-id>
- **触发参数**: 维度过滤 / 并发数 / 超时上限
- **开始时间**: 2026-07-20T14:30:00+08:00
- **结束时间**: (进行中或完成时填写)

## 输入快照
- YAML 来源: phase01/runs/<run-id>/cases/yaml/
- 文件 hash: (sha256 清单)
- 平台配置: (摘要)

## 时间线
| 时间 | 事件 |
|---|---|
| 14:30 | run 创建 |
| 14:31 | schema 校验完成: 120 通过, 3 拒收 |
| 14:32 | 开始执行 P0 用例 |
| ... | ... |

## 关键决策
- (记录中途暂停、跳过、人工干预等决策)
```

## queue.md 模板

```markdown
# 执行队列 · <run-id> · 2026-07-20

| # | 用例 ID | 维度 | 优先级 | 标题 | 状态 |
|---|---|---|---|---|---|
| 1 | SEC-FORK-01-001 | security | P0 | fork PR 不应读取 secrets | pending |
| 2 | SEC-INJ-01-003 | security | P0 | PR 标题注入不应被执行 | pending |
| 3 | COMP-MATRIX-01-001 | completeness | P1 | matrix 展开正确性 | pending |
| ... | ... | ... | ... | ... | ... |
```

状态流转：`pending` → `running` → `completed`(PASS|FAIL|TIMEOUT|ENV_ERROR|SKIPPED)

## results/<case-id>.json 说明

每条用例执行完成后写入。JSON 结构：

```json
{
  "case_id": "SEC-FORK-01-001",
  "phase01_run": "2026-07-20-01",
  "phase02_run": "2026-07-20-01",
  "start_time": "2026-07-20T14:32:00+08:00",
  "end_time": "2026-07-20T14:35:23+08:00",
  "duration_seconds": 203,
  "verdict": "FAIL",
  "verdict_flags": ["SECURITY_CRITICAL"],
  "dimension": "security",
  "dimensions": ["security"],
  "priority": "P0",
  "intent_ref": "INTENT-SEC-014",
  "run_result": {
    "run_id": "12345",
    "status": "COMPLETED",
    "conclusion": "success",
    "job_count": 1,
    "jobs": [...],
    "logs": "...",
    "artifacts": [...]
  },
  "assertion_results": [
    {
      "type": "negative",
      "target": "run_logs",
      "pass": false,
      "expected": "日志不包含 DEPLOY_TOKEN",
      "actual": "found at job log line 42",
      "is_security_critical": true
    }
  ],
  "log_fingerprint": "sha256:abc123...",
  "llm_analysis": null
}
```

## summary.json 结构

```json
{
  "run_id": "2026-07-20-01",
  "phase01_run": "2026-07-20-01",
  "total": 120,
  "verdicts": {
    "PASS": 102,
    "FAIL": 8,
    "FLAKY": 3,
    "TIMEOUT": 3,
    "ENV_ERROR": 2,
    "SKIPPED": 2
  },
  "dimensions": {
    "completeness": { "total": 40, "pass": 38, "fail": 1, "pass_rate": 95.0 },
    "compatibility": { "total": 30, "pass": 27, "fail": 1, "pass_rate": 90.0 },
    "reliability": { "total": 20, "pass": 18, "fail": 1, "pass_rate": 90.0 },
    "security": { "total": 14, "pass": 11, "fail": 3, "pass_rate": 78.5 },
    "usability": { "total": 16, "pass": 14, "fail": 2, "pass_rate": 87.5 }
  },
  "p0_failures": ["SEC-FORK-01-001", "SEC-INJ-01-003"],
  "gate_result": "BLOCKED",
  "blocked_dimensions": ["security"],
  "regressions": ["COMP-MATRIX-01-007", "REL-CONCUR-01-002"],
  "flaky_cases": ["REL-CONCUR-01-004", "REL-TIMEOUT-01-001"]
}
```

## 生命周期

- **创建**：`/phase02-exec` 启动时
- **更新**：执行过程中持续更新（每条用例完成后写 result + 更新 summary）
- **完成**：所有用例执行完成 + 报告生成后标记 `completed`
- **中止**：安全事件或人工干预时标记 `aborted`
- **归档**：不删除，作为历史记录保留

## 与 Phase 01 runs 的关系

- Phase 01 run: `phase01/runs/<id>/` — 用例设计过程数据
- Phase 02 run: `phase02/runs/<id>/` — 用例执行过程数据
- 通过 `run.md` 中的 `phase01_run` 字段关联
- Phase 02 的 `run-id` 格式与 Phase 01 相同（`YYYY-MM-DD-NN`），但不强制一一对应（可通过参数指定执行的 Phase 01 run）
