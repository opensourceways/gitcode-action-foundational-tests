# 非 FAIL 用例统计 · 2026-07-24-valid297-final

## COMPILE_ERROR（63 条）

| 原因 | 数量 | 说明 |
|---|---|---|
| intent_ref 格式不合规 | 54 | 新增用例使用 `KEEP-TC-*` 等格式，不匹配 `^INTENT-(COMP|COMPAT|REL|SEC|USE|ACT)-[0-9]+$` |
| runs-on 格式不合规 | 6 | job runs-on 不是数组格式（字符串/NoneType） |
| fault_injection 声明错误 | 2 | teardown.reset 不是合法值 |
| step name 非法字符 | 1 | step name 含 `+` 号的非字母数字字符 |

**根因**: 54/63 为新增 VALID 用例的 intent_ref 未对齐 schema 规范 → 需回流 Phase 01 修正。

---

## TIMEOUT（15 条）

| 维度 | 数量 | 说明 |
|---|---|---|
| reliability | 9 | 长时运行测试（350min）/ 超时边界 / push 队列等待 |
| security | 3 | fork PR / issue_comment / dispatch 等待超时 |
| compatibility | 2 | push 队列 + dispatch 等待 |
| completeness | 1 | push 队列 |

**根因**: harness 全局 300s 超时截断（9 条）+ push 队列/平台响应慢（6 条）。长时测试需要 per-case 超时白名单。

---

## ENV_ERROR（4 条）

| 原因 | 数量 | 说明 |
|---|---|---|
| dispatch_workflow HTTP 400 | 4 | COMPAT-TOKEN-01-001/002, USE-DISP-01-001, USE-INPT-01-001 — workflow YAML 含 token 操作/invalid input，dispatch API 拒绝 |

---

## INCONCLUSIVE（1 条）

| 原因 | 说明 |
|---|---|
| fork_pr 需第二账号 | COMPAT-PERM-01-002 — fork PR 场景需第二个 GitCode 账号/Token |
