<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/core-concepts/trigger-events | fetched: 2026-07-20 -->

# 触发事件

**事件概述**：事件是流水线启动的源动力。当仓库中发生特定操作时，系统产生对应事件，触发匹配 `on` 配置的工作流。

## 支持的事件类型

| 事件 | 说明 | 典型配置 |
|------|------|--------|
| `push` | 代码推送 | `on: push: branches: [main]` |
| `pull_request` | PR 事件 | `on: pull_request: branches: [main]` |
| `pull_request_target` | PR 安全事件 | `on: pull_request_target: branches: [main]` |
| `issue_comment` | Issue 评论 | `on: issue_comment: types: [created]` |
| `pull_request_comment` | PR 评论 | `on: pull_request_comment: types: [created]` |
| `workflow_dispatch` | 手动触发 | `on: workflow_dispatch: inputs: {...}` |
| `workflow_call` | 可重用调用 | `on: workflow_call: inputs: {...}` |
| `schedule` | 定时触发 | `on: schedule: - cron: '0 2 * * *'` |

> **重要区别**：`pull_request` 使用 PR 源分支代码运行，`pull_request_target` 使用 base 分支代码运行且拥有仓库写权限。Fork 场景推荐使用 `pull_request_target`。

## 多事件组合

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```
