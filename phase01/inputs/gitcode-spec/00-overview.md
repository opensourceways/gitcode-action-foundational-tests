<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/overview | fetched: 2026-07-20 -->

# 产品总览

## 什么是 AtomGit Action

AtomGit Action 是 AtomGit 平台原生的自动化流水线引擎，采用 **Pipeline as Code** 理念，让你通过在代码仓库中编写 YAML 配置文件来定义、触发和执行软件交付流程。流水线配置与业务代码共仓存放、版本同溯，遵循 Everything as Code 的 GitOps 实践。

### 核心理念

| 理念 | 说明 |
|------|------|
| **代码即流水线** | 流水线定义存放在 `.gitcode/workflows/` 目录下，与业务代码共享提交、检视与审核流程，所有变更可追溯 |
| **声明式配置** | 通过简洁的 YAML 语法定义流水线结构，无需编写编排脚本，降低上手门槛 |
| **可复用编排** | Action 插件和可重用工作流（`workflow_call`）支持跨仓库引用与嵌套调用，避免重复维护 |
| **安全隔离** | 内置 `pull_request` / `pull_request_target` 双事件模型、Secret 加密存储、Token 最小权限控制，保障 Fork 场景下的流水线安全 |

## 平台能力全景

### 事件驱动：多种触发方式

AtomGit Action 支持丰富的事件触发机制，覆盖代码协作全场景：

| 触发方式 | 说明 | 典型场景 |
|---------|------|---------|
| `push` | 代码推送触发 | 主分支合并后自动构建部署 |
| `pull_request` | PR 创建、更新、合并时触发 | PR 代码检查、构建验证 |
| `pull_request_target` | 安全模式 PR 触发（目标分支上下文） | Fork PR 自动标签、评论（可访问 Secret） |
| `issue_comment` | Issue 评论触发 | `/deploy` 指令式部署 |
| `pull_request_comment` | PR 评论触发（支持正则过滤） | PR 评论中执行特定操作 |
| `workflow_dispatch` | 手动触发（支持输入参数） | 发布特定版本、紧急热修复 |
| `workflow_call` | 可重用工作流调用 | 组织级标准化流程编排 |
| `schedule` | 定时触发（cron 表达式） | 每日构建、定期巡检 |

每个事件均支持 `branches`、`paths`、`tags` 等过滤规则，精确控制触发范围。同一工作流可组合多种触发事件。

### 执行编排：阶段 + 任务 + 步骤

AtomGit Action 提供两级编排机制，兼顾灵活性与可管控性：

```
Event → Workflow → Stages（串行） → Jobs（阶段内并行） → Steps（串行）
                                    ├─ run（Shell 命令）
                                    └─ uses（Action 插件）
```

- **Stages 阶段机制**：AtomGit Action 特有，阶段间串行执行、阶段内 Job 默认并行，支持 `fail_fast` 快速失败策略，适合需要严格门禁管控的交付流程
- **Needs 依赖机制**：Job 级别的 DAG 依赖编排，实现灵活的拓扑关系
- **Post 后处理**：AtomGit Action 特有的后处理阶段，默认 `run_always: true`，用于通知、清理、报告等收尾操作
- **矩阵策略**：通过 `strategy.matrix` 实现多 OS、多版本、多架构的并行构建测试

### 运行环境：托管 + 自托管 Runner

| Runner 类型 | 说明 | 标签格式 |
|-----------|------|---------|
| **官方托管** | 开箱即用的云上资源池，预装主流语言工具链 | `{os},{arch},{flavor}` 三段式，如 `{ubuntu-24,x64,small}` |
| **自托管** | 自建基础设施，支持 GPU、内网、自定义工具链 | `self-hosted` + 自定义标签 |

官方资源池提供从 1 核 4G（slim）到 32 核 128G（2xlarge）共 6 档规格，默认使用 `[ubuntu-latest, x64, small]`（2核8G）。支持通过 `container` 字段指定自定义 Docker 镜像运行环境。

### 变量与密钥：四级配置体系

| 类型 | 作用域 | 引用方式 | 适用场景 |
|------|--------|---------|---------|
| `env` | workflow / job / step 三级 | `$VAR_NAME` 或 `${{ env.VAR }}` | 临时环境变量 |
| `vars` | 组织 / 项目级 | `${{ vars.VAR }}` | 跨流水线共享配置 |
| `secrets` | 组织 / 项目 | `${{ secrets.NAME }}` | 密码、Token 等敏感信息（日志自动脱敏） |
| `inputs` | workflow_dispatch / workflow_call | `${{ inputs.NAME }}` | 工作流输入参数（仅支持 string 类型） |

### 上下文与表达式

AtomGit Action 提供 12 种上下文，通过 `${{ context.property }}` 表达式语法在工作流中动态访问运行信息：

| 上下文 | 说明 | 典型用途 |
|--------|------|---------|
| `atomgit` | 平台与事件核心信息 | 分支判断 `atomgit.ref`、事件类型 `atomgit.event_name` |
| `env` | 自定义环境变量 | 变量引用 `env.APP_NAME` |
| `vars` | 配置变量 | 部署目标 `vars.DEPLOY_ENV` |
| `secrets` | 加密密钥 | 凭证引用 `secrets.DEPLOY_TOKEN` |
| `inputs` | 输入参数 | 手动触发参数 `inputs.environment` |
| `job` / `jobs` | 当前/被调用 Job 信息 | 状态判断 `job.status` |
| `steps` | 步骤信息与输出 | 跨步骤传值 `steps.id.outputs.result` |
| `runner` | Runner 环境信息 | 系统 `runner.os`、临时目录 `runner.temp` |
| `matrix` / `strategy` | 矩阵变量与策略信息 | 矩阵参数 `matrix.version` |

表达式支持比较运算、逻辑运算、状态函数（`success`/`failed`/`always`/`cancelled`）和字符串函数（`contains`/`startsWith`/`format`/`hashFiles` 等）。

### 安全与权限

| 安全能力 | 说明 |
|---------|------|
| **Secret 加密存储** | 密钥在界面加密创建，日志自动脱敏为 `***`，Fork PR 默认不可访问项目 Secret |
| **Token 最小权限** | `ATOMGIT_TOKEN` 的权限范围由 `permissions` 字段精确控制（read/write/none），支持 `permissions: {}` 最小权限模式 |
| **PR 安全隔离** | `pull_request` 事件下 Fork 仓库的 workflow 仅拥有 read 权限且无法访问 Secret；`pull_request_target` 使用目标分支的 workflow 文件，防止恶意 PR 篡改执行逻辑 |
| **并发控制** | 通过 `concurrency` 限制同一工作流的并行运行数，支持 IGNORE（忽略）和 QUEUE（排队）策略 |

### 制品与缓存

| 能力 | 说明 |
|------|------|
| **制品（Artifacts）** | 跨 Job 传递构建产物，支持上传/下载，可设定保留天数 |
| **缓存（Cache）** | 基于文件的依赖缓存机制，通过 `key` + `restore-keys` 前缀匹配加速 npm、Maven、pip、Gradle 等依赖安装 |

## 工作流文件结构一览

一个完整的 AtomGit Action 工作流文件包含以下核心字段：

```yaml
name: 示例流水线                   # 工作流名称
on:                                # 触发事件
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        type: string
env:                               # 工作流级环境变量
  APP_NAME: my-app
defaults:                          # 默认设置
  run:
    shell: bash
concurrency:                       # 并发控制
  enable: true
  max: 3
  exceed-action: QUEUE
permissions:                       # 权限声明
  repository: read
  pr: write
stages:                            # 阶段定义（可缺省）
  - name: build-stage
    fail_fast: true
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - uses: checkout
          - run: make build
  - name: deploy-stage
    jobs:
      deploy:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - run: make deploy
post:                              # 后处理阶段
  run_always: true
  steps:
    - run: echo "notification"
```
