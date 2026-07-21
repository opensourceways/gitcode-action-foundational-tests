# GitCode 测试实例配置快照

> 来源：handoff 交接材料（Yulin GitCode 契约测试）。本文件记录真实测试实例的仓库、组织/项目级资源与 runner 配置，供 Phase 02 执行采集与 report-builder 溯源。
> **凭据纪律**：Access Token 只经环境变量 `GITCODE_ACCESS_TOKEN` 注入，不硬编码、不落库、不出现在日志/报告。本文件不含任何明文 token。

## 平台元信息

| 项目 | 值 |
|---|---|
| 平台 | GitCode Actions（类 GitHub Actions，上下文命名空间为 `atomgit.*`） |
| API Base URL | `https://api.gitcode.com`（v8 端点，见 `phase01/inputs/gitcode-api/api-reference.md`） |
| 认证 | GitCode OAuth2.0 Access Token → 环境变量 `GITCODE_ACCESS_TOKEN` |
| Workflow 目录 | `.gitcode/workflows/`（注意：非 `.github/workflows/`） |
| Runner 池 | `[ubuntu-latest, x64, small]`（默认）· `[dedicate-hosted, x64/arm64, large]`（容器测试用） |

## 测试仓库

| 仓库 | 用途 | 资源状态 |
|---|---|---|
| `ComputingActionTest/bingo` | 主测试仓库 | 已配置全部测试用 Secret/Variable |
| `ComputingActionTest/akg` | 对照仓库（同组织） | **未**配置项目级同名资源，用于隔离性负向验证 |
| `LiYanghang00/demo` | 原始测试仓库 | Session 级聚合 Workflow 存放处（2300+ 历史 Run） |
| `yyl-support/common`（GitHub） | 文档与交接材料 | 非被测实例 |

## 前置资源配置（bingo 仓库，人工在 Web UI 创建）

| 资源类型 | 级别 | 名称 | 值 | 服务的 TC |
|---|---|---|---|---|
| Secret | 组织 | `SECRET_ORG` | `org_secret` | TC-008 |
| Variable | 组织 | `ORG_VAR` | `org_value` | TC-005 |
| Variable | 组织 | `DUP` | `org_value` | TC-007/194 |
| Variable | 项目 | `DUP` | `project_value` | TC-007/194 |
| Secret | 组织 | `DUP` | `org_secret` | TC-195 |
| Secret | 项目 | `DUP` | `project_secret` | TC-195 |
| Secret | 项目 | `YYL_TEST` | `1234` | TC-009/535 |
| Variable | 项目 | `YYL_TEST` | `1234` | TC-006/535 |

> 上表值为**测试夹具值**（非真实生产凭据），用于精确断言比对。组织级资源需确保 bingo 已获组织授权。

## 已知平台工具限制（影响采集策略）

- Run API / Job API 可读取结构化状态（事件、SHA、分支、状态、退出码）。
- Job 日志下载 API 可能返回 404 → 需从页面导出日志作为证据。
- 无稳定的 Workflow 列表 API。
- 仓库存在多人并发修改 → 采集前须确认目标 workflow 仍在 `.gitcode/workflows/`。
- 新文件可能未被平台注册 → 优先复用已注册的 workflow 文件名。

*快照日期：2026-07-20 · 来源：handoff/README.md + GITCODE-DOC-CONTRACT-TEST-RULES.md*
