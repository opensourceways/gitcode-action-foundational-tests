<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/running-pipelines/rerun-failed-jobs | fetched: 2026-07-20 -->

# 重新运行失败任务

## 概述

当流水线因偶发错误（如网络抖动、Runner 临时不可用、第三方服务超时）失败时，可以通过重新运行来确认是否为可恢复问题。

## 配置说明

### 重新运行整条流水线

1. 进入运行详情页，点击右上角 **Re-run all jobs** 按钮
2. 系统创建一条新的运行记录，所有 job 重新执行，运行编号递增

### 重新运行失败 job

1. 进入运行详情页，点击右上角 **Re-run failed jobs** 按钮
2. 系统仅重新执行本次运行中失败的 job，成功的 job 保持原结果不变

> **注意**：若 workflow 包含 `stages` 定义且某 stage 设置了 `fail_fast: true`，重新运行 failed jobs 时，被跳过的后续 stage 中的 job 也会一并重新执行，因为它们的失败是上游传递导致的，而非自身问题。

### 重新运行时上下文变量保持

重新运行时，`atomgit` 上下文中的 `sha`、`ref`、`event_name` 等值与原始运行保持一致，但 `ATOMGIT_RUN_ID` 和 `ATOMGIT_RUN_NUMBER` 会更新为新值。

### 重新运行限制

| 限制项 | 说明 |
|------|------|
| 最大重试次数 | 单条运行最多重新运行 3 次 |
| 超时运行 | 超过 6 小时的运行不可重新运行 |
| 配置变更 | 重新运行使用原始 commit 上的 workflow 配置，不会读取最新配置 |

## 常见问题

**Q：重新运行后仍然失败，日志报相同错误？**

A：这不是偶发问题，属于确定性失败。请查看日志定位根因，修复代码或 workflow 配置后重新 push 触发。

**Q：Re-run failed jobs 后，之前成功的 job 日志消失了？**

A：成功 job 的日志和结果被保留在新运行的详情页中，状态徽标显示"已缓存"或"已通过"，可展开查看原始日志。

**Q：能否修改参数后重新运行？**

A：不支持。重新运行使用原始触发参数（包括 `workflow_dispatch` 的 inputs）。若需修改参数，请通过 workflow_dispatch 重新手动触发。
