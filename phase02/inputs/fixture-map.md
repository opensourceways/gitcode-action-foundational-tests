# 夹具资源映射（fixture-map）

> Phase 02 harness 的一等输入。**作用**：把 Phase 01 契约 YAML 里抽象的夹具占位名
> （如 `repo_fixture: with-secrets` / `secrets: [TEST_SECRET]`）绑定到当前测试实例上
> **真实已配置**的资源与已知明文值——供 yaml-checker 编译时替换 secret/var 引用、
> 供 assertion-binder 把 rubric 里的"已知明文值"绑成具体串。
>
> **为什么需要它**：契约 YAML 有意抽象（`TEST_SECRET` 是占位符）；真实 bingo 仓里的
> secret 叫 `SECRET_ORG` 等。没有这层映射就只能像旧 execute_*.py 那样把值手写进代码
> （糊弄）。把绑定沉淀成可审计输入，是"完整基于 harness 跑通"的前提。
>
> 数据来源：测试实例 `ComputingActionTest/bingo` 的实际配置（在 GitCode Web UI 手工创建）。
> 明文值仅用于**负向断言的泄露扫描比对**，属测试夹具、非生产密钥，可入库。

## 被测实例

| 项 | 值 |
|---|---|
| owner/repo | `ComputingActionTest/bingo` |
| 对照仓（隔离性负向） | `ComputingActionTest/akg`（未配同名项目级资源）|
| 默认分支 | `main` |

## Secret 资源

| 抽象占位（契约 YAML）| 实例真实名 | 级别 | 已知明文值 | 用途 |
|---|---|---|---|---|
| `TEST_SECRET` | `SECRET_ORG` | 组织 | `org_secret` | 基础脱敏 / 泄露扫描 |
| `DUP`(secret) | `DUP` | 项目(覆盖组织) | `project_secret` | 项目 secret 覆盖组织 |
| `YYL_TEST`(secret) | `YYL_TEST` | 项目 | `1234` | secret/var 命名空间独立 |

## Variable 资源

| 抽象占位 | 实例真实名 | 级别 | 值 | 用途 |
|---|---|---|---|---|
| `ORG_VAR` | `ORG_VAR` | 组织 | `org_value` | 组织 variable 可用 |
| `DUP`(var) | `DUP` | 项目(覆盖组织) | `project_value` | 项目 var 覆盖组织 |
| `YYL_TEST`(var) | `YYL_TEST` | 项目 | `1234` | secret/var 命名空间独立 |

## repo_fixture 映射

| 契约 `repo_fixture` | 实例落地 | 说明 |
|---|---|---|
| `with-secrets` | bingo（已配上述 secret/var）| 直接复用 bingo |
| `clean` / 其它 | bingo | 当前单实例，暂不区分；`teardown.reset` 由 env-manager 处理 |

## 未配置资源（探到即判 NOT_CONFIGURED，见 rules.md §11）

| 占位 | 状态 |
|---|---|
| `NPM_TOKEN` | 未在 bingo 配置 |
| `SUPERSECRET` | 未在 bingo 配置 |

> 绑定失败（契约要求某 secret 但此表无映射且实例未配）→ 该用例判 `NOT_CONFIGURED`，
> 不当作平台缺陷；如需转真实判定，先在 bingo 配好资源并回填本表。
