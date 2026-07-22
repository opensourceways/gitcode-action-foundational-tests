# Yulin GitCode 契约测试交接文档

## 仓库与资源

| 仓库 | 用途 |
| --- | --- |
| `https://gitcode.com/ComputingActionTest/bingo` | 主测试仓库，组织 `ComputingActionTest` 下，已配置全部测试用 Secret/Variable |
| `https://gitcode.com/ComputingActionTest/akg` | 对照仓库，同组织，未配置同名项目级资源，用于隔离性验证 |
| `https://gitcode.com/LiYanghang00/demo` | 原始测试仓库，Session 级聚合 Workflow 存放处 |
| `https://github.com/yyl-support/common` | 文档和交接材料 |

### 前置配置（bingo 仓库）

| 资源类型 | 级别 | 名称 | 值 | 用途 |
| --- | --- | --- | --- | --- |
| Secret | 组织 | `SECRET_ORG` | `org_secret` | TC-008 验证组织 Secret 可用 |
| Variable | 组织 | `ORG_VAR` | `org_value` | TC-005 验证组织 Variable 可用 |
| Variable | 组织 | `DUP` | `org_value` | TC-007/194 验证项目覆盖组织 |
| Variable | 项目 | `DUP` | `project_value` | 同上 |
| Secret | 组织 | `DUP` | `org_secret` | TC-195 验证项目 Secret 覆盖组织 Secret |
| Secret | 项目 | `DUP` | `project_secret` | 同上 |
| Secret | 项目 | `YYL_TEST` | `1234` | TC-009/535 命名空间独立性 |
| Variable | 项目 | `YYL_TEST` | `1234` | TC-006/535 命名空间独立性 |

所有资源需在 GitCode Web UI 手动创建，组织级在组织设置页面，项目级在项目设置页面。需确保 bingo 已获得组织资源的授权。

---

## 测试策略

### 判定原则（见 `GITCODE-DOC-CONTRACT-TEST-RULES.md` 第 3 节）
- **PASS**：严格按文档语法编写 YAML，满足全部前置条件，平台行为与文档/Excel 预期一致，有可复核证据
- **FAIL**：严格按文档操作后平台行为不符，或文档方法不足以完成其声明的验证
- 不做 PARTIAL/BLOCKED，不能在条件不齐备时规避失败判断

### 证据层级
1. **Run API 元数据**：事件类型、状态、时间
2. **Job API 状态**：Step 退出码
3. **页面/下载日志**：实际输出值（非 Workflow 自打印的 PASS/FAIL 文本）
4. **设置页面/API 拒绝响应**：平台 UI 层的原始拒绝

### 三层验证方法
- **表达式层**：`${{ env.VAR }}`、`${{ vars.VAR }}` 验证上下文值
- **Shell 注入层**：`$VAR` 验证 Runner 环境变量
- **平台元数据层**：Run API 验证事件类型

### 跨仓库对比验证
对"仅当前项目可用"类断言，用 bingo（有资源）做正向、akg（无资源）做负向，形成完整证据链。

---

## Workflow 清单

### demo-workflows/ （LiYanghang00/demo 仓库）

| 文件 | 触发 | 包含 TC | 备注 |
| --- | --- | --- | --- |
| `yyl-session1-secrets.yml` | workflow_dispatch | TC-008/009/011/100/101/102/443/444/530/531/532 | S1 Secret 聚合 |
| `yyl-session13-workflows.yml` | workflow_dispatch + pull_request + push | TC-035/036/194/195/220/273/304/354/355/387/388/389/391/535 | S13 聚合 |
| `yyl-session3-schedule.yml` | schedule | TC-237/427-430/471-479/505-512/562/563 | S3 定时任务（全部 FAIL） |
| `yyl-tc387-ci.yml` | push | TC-387 | 独立 CI 触发验证 |

### bingo-workflows/ （ComputingActionTest/bingo 仓库）

| 文件 | 触发 | 包含 TC | 备注 |
| --- | --- | --- | --- |
| `yyl-blocked-tests.yml` | workflow_dispatch + schedule | TC-008/005/007/194/195/391 | 解封阻塞用例的五合一验证 |
| `yyl-tc-retest.yml` | workflow_dispatch | TC-534/220/273 | 跨仓库复测 |
| `yyl-tc533-priority.yml` | workflow_dispatch | TC-533 | env 注入极简测试 |
| `yyl-tc533-env-vars.yml` | workflow_dispatch | TC-533 | env vs vars 冲突测试 |
| `yyl-container-test.yml` | workflow_dispatch | TC-273 | 用 dedicate-hosted 资源池测试容器 |
| `test_schedule.yml` | push + schedule | Schedule 探针 | 照抄 new-pipeline 语法验证 |

### akg-workflows/ （ComputingActionTest/akg 仓库）

| 文件 | 触发 | 包含 TC | 备注 |
| --- | --- | --- | --- |
| `yyl-tc006-isolation.yml` | workflow_dispatch | TC-006 | 验证项目 Variable 跨项目不可见 |
| `yyl-tc009-isolation.yml` | workflow_dispatch | TC-009 | 验证项目 Secret 跨项目不可见 |

---

## 最终结论

| 状态 | 数量 | 占比 |
| --- | ---: | ---: |
| PASS | 25 | 44.6% |
| FAIL | 31 | 55.4% |
| **合计** | **56** | **100%** |

### 7 个平台缺陷（影响 31 条 FAIL）

| # | 问题 | 严重等级 | 涉及 TC 数 |
| --- | --- | --- | --- |
| 1 | Scheduler 不工作：两个仓库多次 cron 配置从未产生 Schedule Run | P1 | 25 |
| 2 | Runner 不注入 Job env 到 Shell：表达式层正常但 Bash $VAR 恒为 UNSET | P1 | 1 |
| 3 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS 默认值缺失 | P2 | 1 |
| 4 | Job 容器不可用 | P2 | 1 |
| 5 | environment 字段不被平台识别 | P2 | 1 |
| 6 | vars > ATOMGIT_* 优先级无法验证（平台禁止创建同名变量） | P2 | 1 |
| 7 | Docker 构建能力无法验证（资源不足） | P3 | 1 |

详见 `session-test-coverage-report.md`。
