# 单用例执行结果模板

> 每条用例执行完成后，由 report-builder 参照此模板写入 `runs/<run-id>/results/<case-id>.md`。
> 结构化数据（JSON）存 `results/<case-id>.json`；本文件为人可读的 Markdown 快照。

---

## 执行结果 · <case-id>

| 项目 | 值 |
|---|---|
| **用例 ID** | SEC-FORK-01-001 |
| **标题** | fork PR 不应读取到仓库 secrets |
| **维度** | security |
| **优先级** | P0 |
| **溯源意图** | INTENT-SEC-014 |
| **Phase 01 Run** | 2026-07-20-01 |
| **Phase 02 Run** | 2026-07-20-01 |
| **执行时间** | 2026-07-20 14:32:00 ~ 14:35:23 (3m23s) |
| **GitCode Run ID** | 12345 |

---

## 判定: ❌ FAIL (SECURITY_CRITICAL)

---

## 断言详情

| # | 类型 | Target | 结果 | 预期 | 实际 |
|---|---|---|---|---|---|
| 1 | negative | run_logs | ❌ FAIL | 日志不包含 DEPLOY_TOKEN | found at job log line 42 |
| 2 | positive | run_status | ✅ PASS | blocked_or_no_secret_access | blocked_or_no_secret_access |

### 断言 1 详情 (negative / run_logs)

- **预期**：工作流运行日志中不出现 `DEPLOY_TOKEN` 明文
- **实际**：日志第 42 行出现 `export DEPLOY_TOKEN=***`（但实际值未被遮蔽）
- **证据**：`job-logs/echo-step.log:42`
- **严重度**：🔴 SECURITY_CRITICAL

---

## Run 信息

| 项目 | 值 |
|---|---|
| **Run Status** | COMPLETED |
| **Conclusion** | success |
| **Job Count** | 1 |
| **Artifacts** | 无 |

### Job 详情

| Job ID | Name | Status | Conclusion | Duration |
|---|---|---|---|---|
| 678 | echo | completed | success | 2m10s |

### 日志指纹

`sha256:abc123def456...`

---

## LLM 辅助分析

### 根因初判

**分类**: 产品 bug
**置信度**: 高

**分析**:
工作流成功执行完成（run conclusion=success），但日志中 `DEPLOY_TOKEN` 的值未被遮蔽。
根据 GitCode 规格 `security-permissions/using-secrets.md`，secrets 应自动在日志中遮蔽为 `***`。
此行为表明 GitCode 的 secret 脱敏机制在此场景下未生效。

**证据**:
- Job 日志第 42 行: `DEPLOY_TOKEN=sk-abc123...`（secret 值未被遮蔽）
- 对照预期: 应显示 `DEPLOY_TOKEN=***`

---

## 清理

- [x] Fixture 仓库已删除
- [x] 临时工作区已清理
