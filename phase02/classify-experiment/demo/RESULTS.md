# Demo Results — PR Trigger Automation Test

**时间**: 2026-07-23 20:08 – 20:35  
**脚本**: `demo_pr_trigger.py`, `demo_push_sanity.py`

## 做了什么

3 轮完整的 "push workflow → create PR → poll" 循环，覆盖了两个关键假设的验证。

## 发现

### 1. `POST /api/v5/repos/.../pulls` 创建 PR 成功

| PR # | iid | 结果 |
|------|-----|------|
| 8925xxx | 1 | 创建成功，关闭成功 |
| 8925020 | 2 | 创建成功，关闭成功 |
| 8925111 | 3 | 创建成功，关闭成功 |

GitCode 的 PR body 格式与 GitHub 类似：`{title, head, base, body}`。

### 2. `on: pull_request` 工作流未触发

| 尝试 | 关键配置 | 结果 |
|------|----------|------|
| v1 | workflow 只在 feature 分支 | 无触发（预期 — 需在 base 分支） |
| v2 | workflow 先推 main，等 3s，再开 PR | 无触发 |
| v3 | workflow 先推 main，等 30s+git pull 同步，再开 PR | 无触发 |

### 3. `on: push` 触发正常

- 仓库有 347 个历史 run，全部 `event=Manual`
- 平台将**所有 run** 的 event 字段统一标为 `Manual`（包括 push 触发的）—— 这是平台 API 的已知行为
- `executor` 参数不影响结果

### 4. PR 详情中的 `base.sha` 滞后

PR API 返回的 `base.sha` 可能是 PR 创建时的 main 分支 SHA，而不是最新 main。`git pull` 同步后创建分支对此无影响。

## 结论

| 能力 | 状态 |
|------|------|
| API 创建 PR | ✅ 可用 |
| API 关闭 PR | ✅ 可用 |
| API 推送 workflow 到 main | ✅ 可用 |
| PR 触发 workflow run | ❌ 未触发（3 次尝试，0 run） |
| Poll run by pull_request_id | ❌ 始终返回 0 结果 |

## 待验证假设

1. **API-created PR 不触发 workflow** — 平台可能只对 Web UI 创建的 PR 触发 `on: pull_request`
2. **`on: pull_request` 需要 repo 级开关** — GitCode 可能有 "Enable merge request pipelines" 设置，默认关闭
3. **同一仓库内 PR 不触发** — `on: pull_request` 可能只对 fork PR 而非 same-repo PR 触发
4. **Web UI 手动创建 PR 可以触发** — 尚未验证

## 下一步建议

1. **Web UI 测试**：在 GitCode Web UI 创建一个 PR（workflow 文件已在 main），观察是否触发 pipeline
2. **检查 repo settings**：查看 `Settings > CI/CD > Merge Request Pipelines` 是否有开关
3. **尝试 fork PR**：用 `CONTRIBUTOR_GITCODE_TOKEN` fork 仓库，从 fork 创建 PR
4. **联系平台方**：确认 API 创建的 PR 是否会触发 workflow
