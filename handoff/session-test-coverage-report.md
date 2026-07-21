# Yulin Session 测试覆盖与验证报告

更新时间：2026-07-20（今日复核无变化）。全部 56 条 TC 已结案。

## 1. 总览

| 状态 | TC 数 | 占比 |
| --- | ---: | ---: |
| PASS | 25 | 44.6% |
| FAIL | 31 | 55.4% |
| **合计** | **56** | **100%** |

| Session | TC 数 | PASS | FAIL | 主要结论 |
| --- | ---: | ---: | ---: | --- |
| S1 | 12 | 11 | 1 | 除 `environment` 字段外，全部 Secret 相关能力通过 |
| S2 | 5 | 3 | 2 | env 注入 Runner 失败、ATOMGIT_* 覆盖失败 |
| S3 | 24 | 0 | 24 | Scheduler 全局不工作 |
| S13 | 15 | 11 | 4 | Docker/Scheduler/容器能力不可用，系统变量默认值缺失 |

## 2. 全部 TC 终态

| Session | TC | 目标 | 结论 | 证据摘要 |
| --- | --- | --- | --- | --- |
| S2 | TC-005 | 组织 Variable 在项目可用 | PASS | `bingo` Run `0bea1506...`，`vars.ORG_VAR` = `org_value` |
| S2 | TC-006 | 项目 Variable 仅当前项目可用 | PASS | `bingo` 有 `vars.YYL_TEST`，`akg` 为空 |
| S2 | TC-007 | 项目 vars 覆盖组织 vars | PASS | `bingo` Run `0bea1506...`，`vars.DUP` = `project_value` |
| S1 | TC-008 | 组织 Secret 在项目可用 | PASS | `bingo` Run `0bea1506...`，`SECRET_ORG` 精确值断言通过 |
| S1 | TC-009 | 项目 Secret 仅当前项目可用 | PASS | `bingo` 有值，`akg` 为空（`YYL_TEST`） |
| S1 | TC-010 | `environment` 匹配时可用 | FAIL | 平台拒绝 `environment` 字段 |
| S1 | TC-011 | Secret 输出掩码 `***` | PASS | 页面日志确认掩码 |
| S13 | TC-035 | `atomgit.action` 返回 Action 名 | PASS | ZIP 日志确认 |
| S13 | TC-036 | `atomgit.token` 可用且受保护 | PASS | 非空断言+掩码通过 |
| S1 | TC-100 | Token 掩码 | PASS | 页面日志确认掩码 |
| S1 | TC-101 | NPM Token 掩码 | PASS | 页面日志确认掩码 |
| S1 | TC-102 | SUPERSECRET 掩码 | PASS | 页面日志确认掩码 |
| S13 | TC-194 | 项目 vars 覆盖组织 vars | PASS | `bingo` Run `0bea1506...`，双重断言通过 |
| S13 | TC-195 | 项目 Secret 覆盖组织 Secret | PASS | `bingo` Run `0bea1506...`，`secrets.DUP` 内存比较通过 |
| S13 | TC-220 | `ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS` 默认 `false` | FAIL | 两个仓库均为 `UNSET` |
| S3 | TC-237 | cron 创建 Schedule Run | FAIL | 两个仓库均无 Schedule 事件 Run |
| S13 | TC-273 | Job 自定义容器 | FAIL | 两个仓库均返回"任务申请资源错误" |
| S13 | TC-304 | checkout 拉取仓库 | PASS | checkout 后文件断言通过 |
| S13 | TC-354 | Secret 日志掩码 `***` | PASS | ZIP 日志确认 |
| S13 | TC-355 | `set-env` 默认禁用 | PASS | 两步独立验证通过 |
| S13 | TC-387 | ci 场景 Push/PR 构建测试 | PASS | Push Run `447f33fa9412...`，事件 `Push` |
| S13 | TC-388 | PR 提交自动检查 | PASS | MR Run `d726006a...`，事件 `MR` |
| S13 | TC-389 | Tag 触发发布 | PASS | CreateTag Run `1d0cc8e...`，事件 `CreateTag` |
| S13 | TC-390 | Docker 构建推送 | FAIL | 缺少 Docker Registry 资源 |
| S13 | TC-391 | 每日定时构建 | FAIL | Scheduler 不工作 |
| S3 | TC-427 | cron 使用 UTC | FAIL | 依赖基础 Scheduler（不可用） |
| S3 | TC-428 | 非默认分支不调度 | FAIL | 同上 |
| S3 | TC-429 | 最短间隔 5 分钟 | FAIL | 同上 |
| S3 | TC-430 | 调度延迟 | FAIL | 同上 |
| S1 | TC-443 | 无危险 Secret 输出 | PASS | 扫描 3 个 Workflow，零命中 |
| S1 | TC-444 | Secret 不入 Artifact/缓存 | PASS | Artifact/Cache Action=0，危险路径零命中 |
| S3 | TC-471 | cron `*` 任意值 | FAIL | 依赖基础 Scheduler（不可用） |
| S3 | TC-472 | cron `,` 列表分隔 | FAIL | 同上 |
| S3 | TC-473 | cron `-` 范围 | FAIL | 同上 |
| S3 | TC-474 | cron `/` 步长 | FAIL | 同上 |
| S3 | TC-475 | cron 分钟字段边界 | FAIL | 同上 |
| S3 | TC-476 | cron 小时字段边界 | FAIL | 同上 |
| S3 | TC-477 | cron 日期字段边界 | FAIL | 同上 |
| S3 | TC-478 | cron 月份字段边界 | FAIL | 同上 |
| S3 | TC-479 | cron 星期字段边界 | FAIL | 同上 |
| S3 | TC-505 | cron 分钟列表触发 | FAIL | 同上 |
| S3 | TC-506 | cron 分钟范围触发 | FAIL | 同上 |
| S3 | TC-507 | cron 分钟步长触发 | FAIL | 同上 |
| S3 | TC-508 | cron `?` 语法 | FAIL | 同上 |
| S3 | TC-509 | cron `L` 最后一天 | FAIL | 同上 |
| S3 | TC-510 | cron `W` 最近工作日 | FAIL | 同上 |
| S3 | TC-511 | cron `#` 第 N 个星期 | FAIL | 同上 |
| S3 | TC-512 | cron 区间+步长组合 | FAIL | 同上 |
| S1 | TC-530 | 未定义 Secret 为空 | PASS | 空值断言通过 |
| S1 | TC-531 | 连字符 Secret 名 | PASS | 平台 UI 合理拒绝 |
| S1 | TC-532 | 空值 Secret | PASS | 平台 UI 合理拒绝 |
| S2 | TC-533 | `env > vars` 优先级 | FAIL | 三个仓库/组织独立验证：Runner 不注入 Job env 到 Shell |
| S2 | TC-534 | `vars > ATOMGIT_*` 优先级 | FAIL | 平台拒绝创建 `ATOMGIT_*` 同名 Variable |
| S13 | TC-535 | Secret/vars 同名空间独立 | PASS | `YYL_TEST` 同时配置为 Secret 和 vars，两者均可用 |
| S3 | TC-562 | 非默认分支 schedule | FAIL | 依赖基础 Scheduler（不可用） |
| S3 | TC-563 | Schedule 调度延迟 | FAIL | 同上 |

## 3. 关键发现

### 3.1 平台全局缺陷

| 问题 | 严重等级 | 涉及 TC | 证据 |
| --- | --- | --- | --- |
| Scheduler 不工作：两个仓库、多次 cron 配置，从未产生 Schedule Run。文档声明的定时触发、cron 运算符、UTC 时区、默认分支、最小间隔等全部无法验证 | P1 | S3 × 24 + TC-391 | LiYanghang00/demo（2300+ 历史 Run）× 0 Schedule、ComputingActionTest/bingo × 0 Schedule |
| Runner 不注入 Job env 到 Shell：表达式层 `${{ env.VAR }}` 正常但 Bash `$VAR` 恒为 UNSET。违反文档声明"变量注入 Runner"和"env > vars"优先级链 | P1 | TC-533 | 两个组织、三个仓库独立验证 |
| `ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS` 默认值缺失 | P2 | TC-220 | 两个仓库均为 `UNSET` 而非 `false` |
| Job 容器不可用：文档声明的 `container.image` 能力无法使用 | P2 | TC-273 | 两个仓库均返回"任务申请资源错误" |
| `environment` 字段不被平台识别：语法检查报 `unknown property`。文档仅描述环境 Secret 审批功能，未提供环境绑定 YAML 语法 | P2 | TC-010 | 平台语法检查原始拒绝证据 |
| `vars > ATOMGIT_*` 优先级无法验证：平台禁止创建 `ATOMGIT_` 前缀的项目 Variable（与系统变量冲突） | P2 | TC-534 | 平台变量创建页面的拒绝证据 |
| Docker 构建能力无法验证：缺少 Docker Registry 和镜像推送资源 | P3 | TC-390 | 资源前置条件不足 |

### 3.2 跨仓库验证结论

以下结论经过 `ComputingActionTest/bingo` + `ComputingActionTest/akg` 双仓库对照验证：

| 能力 | TC | 结论 |
| --- | --- | --- |
| 项目 Secret 隔离 | TC-009 | 同一个组织下，项目 A 的 Secret 对项目 B 不可见 |
| 项目 Variable 隔离 | TC-006 | 同上，Variable 同理 |
| 项目 vars 覆盖组织 vars | TC-007 / TC-194 | 项目级值优先 |
| 项目 Secret 覆盖组织 Secret | TC-195 | 同上 |
| Secret/vars 命名空间独立 | TC-535 | 同名可共存，互不影响 |

## 4. 2026-07-20 全量复核

31 条 FAIL 全部重新验证，无一变化。

### 4.1 Schedule（25 条）

| 验证 | 仓库 | 结果 |
| --- | --- | --- |
| 老 cron 配置 | LiYanghang00/demo | 2300+ 历史 Run，0 次 Schedule |
| 新 repo 5 分钟 cron | ComputingActionTest/bingo | 10 分钟观察，0 次 Schedule |
| 照抄 new-pipeline 语法 | ComputingActionTest/bingo | `*/5 * * * *` + `runs-on: ubuntu-latest`，0 次 Schedule |

### 4.2 容器能力（TC-273）

| 资源池 | 结果 |
| --- | --- |
| `[ubuntu-latest, x64, small]` | "任务申请资源错误" |
| `[dedicate-hosted, x64, large]` | FAILED，容器配置已解析但无法执行 |
| `[dedicate-hosted, arm64, large]` | 同上 |

### 4.3 其余 FAIL

| TC | 验证 | 结果 |
| --- | --- | --- |
| TC-220 | `bingo` 上重测 | `UNSET` 而非 `false` |
| TC-533 | `bingo` 上重测 | `shell_PROBE=UNSET` |
| TC-010 | 平台语法限制 | 不变 |
| TC-534 | 平台变量创建限制 | 不变 |
| TC-390 | Docker Registry 资源不足 | 不变 |
