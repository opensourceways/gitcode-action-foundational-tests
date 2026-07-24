# 不可脚本化 Case 分析 — 2026-07-23 (32 cases)

**数据源**: `phase02/classify-experiment/2026-07-23/not_scriptable/`
**分类器**: `classify_20260723.py` — 将任何非 `push`/`manual`/`workflow_dispatch` 的触发事件标记为 `not_scriptable`

## 根因

当前测试框架 (`workflow_runner.py`) 只能通过**单一 maintainer 账号的 push** 触发流水线。这 32 个 case 均不使用 `trigger.event: push`，它们各自缺少以下能力：

| 缺少的能力 | Cases | 原因 |
|---|---|---------|
| **第二个用户账号** | 18 | `as: untrusted_contributor` — fork PR、fork cache、token 隔离等安全场景 |
| **PR 创建 API** | 8 | `pull_request` / `pull_request_target` + `as: maintainer` — 主仓库自身 PR 行为 |
| **cron 等待** | 3 | `schedule` — 无法通过 API 强制触发定时任务 |
| **评论 API + 第二账号** | 3 | `issue_comment` + `as: untrusted_contributor` — 不可信评论触发 |

---

## 逐 Case 分析

### A 类：schedule（3 个）— `TRIGGER_CANNOT`

验证 cron 定时触发是否按计划执行。平台没有"立即触发 schedule"的 API。

| Case | 标题 | 断言 |
|------|------|------|
| COMP-SCHEDULE-01-001 | 合法 cron 在默认分支按时触发 | run_status=success, run_event=schedule |
| COMP-SCHEDULE-01-002 | schedule 在非默认分支不触发 | run_status=never_triggered |
| COMP-SCHEDULE-01-003 | schedule 在 forked repo 不触发 | run_status=never_triggered |

**测试方式**:
- **手动**: 将 cron 设为 `* * * * *`，push 后等待 1-2 分钟，检查 run_logs
- **API 变通**: push 一个 `workflow_dispatch` 副本（步骤相同），用 dispatch 触发替代 cron 触发，仅验证业务逻辑
- **长期方案**: 部署定时监控脚本，扫描定时触发的 run 并事后校验（非实时脚本化）

---

### B 类：fork / 不可信 PR（15 个）— 需要第二账号

这些 case 模拟恶意或不可信的 fork PR。平台安全模型要求 PR 来自**不同用户/仓库**，单一 bot token 无法完成。

#### B1：pull_request + untrusted_contributor（12 个）

| Case | 标题 | Fixture |
|------|------|---------|
| COMP-CACHE-01-003 | fork PR 不应覆盖或污染主分支 cache | with-cache |
| COMP-PERMS-01-003 | fork PR 不可写入容器注册表 / 包 | default |
| COMP-PR-01-001 | fork PR 触发 pull_request 时不可读取项目 secrets | with-secrets |
| COMP-PR-01-003 | fork PR 不可修改 protected branch | default |
| COMPAT-CACHE-01-002 | fork PR 的 cache 不应影响同 key 上游 cache | with-cache |
| SEC-ARTF-01-001 | fork PR 不应访问项目 artifacts | with-artifacts |
| SEC-CACHE-01-001 | fork PR 不可污染上游 cache | with-cache |
| SEC-FORK-01-001 | fork PR 触发 pull_request 时不可读取项目 secrets | with-secrets |
| SEC-FORK-01-002 | fork PR 不可覆盖环境变量 | with-secrets |
| SEC-INJ-01-001 | 不可信 PR 标题不可直接插进 run 脚本导致命令注入 | default |
| SEC-INJ-01-002 | 不可信 PR body 不可被 eval 导致注入 | default |
| SEC-TOKEN-01-001 | fork PR CI token 应限制 scope | default |
| SEC-TOKEN-01-002 | fork PR 不应继承仓库级 GITCODE_TOKEN | with-secrets |

#### B2：pull_request_target + untrusted_contributor（2 个）

| Case | 标题 |
|------|------|
| COMPAT-TARGET-01-001 | pull_request_target 默认 checkout 应为 base 分支而非 head 分支 |
| COMPAT-TARGET-01-002 | pull_request_target + 显式 checkout head SHA 的风险 |

#### B3：fork_pr + untrusted_contributor（1 个）

| Case | 标题 |
|------|------|
| COMPAT-PERM-01-002 | fork_pr 权限隔离 |

**测试方式**:
- **双账号方案**: 维护 `GITCODE_BOT_TOKEN` + `GITCODE_CONTRIBUTOR_TOKEN` 两个 token。Bot 准备仓库 → contributor 创建 fork 并发起 PR → Bot 在目标仓库观察结果
- **手动**: 人工用第二个账号创建 fork PR，在目标仓库观察
- **API 模拟**: 如果平台支持 OAuth/impersonation，Bot 可用不同身份创建 PR

---

### C 类：maintainer PR（8 个）— 需要 PR 创建 API

不需要第二账号（以 maintainer 身份运行），但触发事件是 `pull_request` 或 `pull_request_target`，当前框架没有调用创建 PR 的 API。

| Case | 触发 | 标题 |
|------|------|------|
| COMP-PR-01-002 | pull_request_target + maintainer | pull_request_target 默认 checkout base |
| COMP-PRTARGET-01-001 | pull_request_target + maintainer | pull_request_target 触发时 secrets 可访问 |
| COMP-PRTARGET-01-002 | pull_request_target + maintainer | pull_request_target + 显式 checkout head |
| SEC-BASE-01-001 | pull_request_target + maintainer | pull_request_target 下 checkout ref 只允许 base |
| SEC-BASE-01-002 | pull_request_target + maintainer | pull_request_target 下强制指定 head ref 被拒绝 |
| SEC-PRTGT-01-001 | pull_request_target + maintainer | 显式 checkout 不可信 PR 时 secrets 应受控 |
| SEC-PRTGT-01-002 | pull_request_target + maintainer | run 不应被不可信 PR 内容污染 |
| COMPAT-PR-01-001 | pull_request + maintainer | 主仓库自身 PR 行为验证 |
| USE-ANNOT-01-002 | pull_request + maintainer | PR annotation 在 PR UI 展示正确 |
| USE-TYPE-01-001 | pull_request + maintainer | 使用 GitCode types 命名时正常触发 |

**测试方式**:
- **扩展 harness**: 在 `workflow_runner.py` 中添加 `POST /api/v4/projects/:id/merge_requests` 调用，创建 PR 后轮询流水线状态
- **手动**: 通过 GitCode UI 或 curl API 创建 PR，观察结果
- **成本最低**: 这是最容易脚本化的一类——只需一次 API 调用

---

### D 类：issue_comment + untrusted_contributor（3 个）

| Case | 标题 |
|------|------|
| SEC-COMM-01-001 | issue_comment 触发时不可信评论不泄露 secrets |
| SEC-INJ-01-003 | issue_comment body 不允许注入 |
| SEC-TOCTOU-01-002 | issue_comment 触发 CI 检查的 TOCTOU 攻击 |

**测试方式**: 需要第二账号发表评论，或在 issue 中以不同用户身份评论。同 B 类的双账号方案。

---

## 断言层分析

绝大多数 case 断言**完全可映射**（run_status、run_logs、cache_pollution、artifact_download）。只有以下 case 存在断言层额外阻断：

| Case | 断言 | 问题 |
|------|------|------|
| USE-ANNOT-01-002 | `target=pr_ui, eval=llm_assisted` | 需 Playwright 检查 PR UI 中的 annotation 展示 |
| COMPAT-TARGET-01-001 | 2× `eval=llm_assisted` on run_logs | LLM 辅助判断 SHA 比对 |
| SEC-ARTF-01-001 | `target=artifact_download` ×2 | 需 artifact assertion kind（尚未加入 ENGINE_KINDS） |

**结论**: 阻断在**触发层**，而非断言层。一旦触发可脚本化，约 29/32 的 case 可直接跑通。

---

## 测试策略建议

### 短期（手动 / 半自动）

| 类别 | 方式 | 工作量 |
|------|------|--------|
| schedule (3) | cron 设为 `* * * * *`，push 后等 1-2 分钟，验证 run_logs | 低 |
| maintainer PR (10) | curl 调 `POST /merge_requests` 创建 PR，轮询流水线 | 低 |
| untrusted (15) | 人工用第二账号 fork + 发 PR，bot 观察 | 中 |
| issue_comment (3) | 人工用第二账号发评论，bot 观察 | 中 |

### 中期（harness 扩展）

1. **添加 PR 触发支持**（`workflow_runner.py`）: `POST /merge_requests` → 轮询 pipeline → 取 run_logs，一次搞定 10 个 maintainer PR case
2. **添加 schedule 等待模式**: push cron `* * * * *` → sleep 90s → `GET /pipelines` 检查，覆盖 3 个 schedule case
3. **双账号配置**: 环境变量 `GITCODE_BOT_TOKEN` + `GITCODE_CONTRIBUTOR_TOKEN`，Bot 准备仓库 → contributor 发 PR/评论 → Bot 校验，覆盖 18 个 untrusted + 3 个 comment case

### 长期（全自动化）

一旦 harness 支持 PR 创建 API + 双账号，所有 32 个 case 均可脚本化。唯一"无法自动触发"的 schedule 可通过短 cron + 轮询变通。
