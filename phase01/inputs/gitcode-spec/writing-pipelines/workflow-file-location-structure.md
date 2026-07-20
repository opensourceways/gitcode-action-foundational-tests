<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/workflow-file-location-structure | fetched: 2026-07-20 -->

# 工作流文件位置与基本结构

**适用场景** ：当你需要在仓库中创建第一个 AtomGit Action 流水线，或者需要了解 workflow 文件应该放在哪里、怎么命名、基本 YAML 结构怎么写时。

## 前提条件

- 已有 AtomGit 仓库且对仓库拥有写权限。
- AtomGit Action 功能已开启。
- 仓库可使用托管 Runner 或已配置自托管 Runner。

## 快速示例

```yaml
name: CI
on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - name: Checkout source code
        uses: checkout
      - name: Run build
        run: echo "build success"
```

## 配置说明

### 文件存放目录

AtomGit Action 的 workflow 文件存放目录为：

```
.gitcode/workflows/<workflow-name>.yml
```

仅 `.yml` 和 `.yaml` 后缀的文件会被识别为 workflow 文件，其他后缀将被忽略。

### 命名建议

| 场景 | 推荐文件名 | 说明 |
|------|----------|------|
| 持续集成 | `ci.yml` | push 或 PR 时构建和测试 |
| 合并请求检查 | `pr-check.yml` | PR 提交时自动检查 |
| 发布 | `release.yml` | Tag 触发发布流程 |
| Docker 镜像构建 | `docker-build.yml` | 构建并推送镜像 |
| 定时任务 | `nightly.yml` | 每日定时构建 |
| 手动部署 | `deploy.yml` | 手动触发部署 |

### 基本结构字段

| 字段 | 必填 | 说明 |
|------|-----|------|
| `name` | 否 | workflow 展示名称，缺省时使用文件名 |
| `on` | 是 | 触发条件，定义哪些事件触发 workflow |
| `env` | 否 | workflow 级环境变量，所有 job 和 step 可见 |
| `defaults` | 否 | 默认设置，如默认 shell 和 working-directory |
| `concurrency` | 否 | 并发控制，限制同一 workflow 的并行运行数 |
| `permissions` | 否 | 权限声明，控制 ATOMGIT_TOKEN 的权限范围 |
| `stages` | 否 | 阶段定义，仅在需要阶段串行控制时配置 |
| `jobs` | 是 | 任务集合（无stages时为顶层字段，有stages时嵌套在stages内） |
| `post` | 否 | 后处理阶段，用于通知、清理、回写等操作 |

### 完整基本结构示例

```yaml
name: 示例流水线
on:
  push:
    branches:
      - main
env:
  APP_NAME: my-app
defaults:
  run:
    shell: bash
concurrency:
  enable: true
  max: 3
  exceed-action: QUEUE
permissions:
  repository: read
  pr: write
stages:
  build_stage:
    name: 构建
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - uses: checkout
          - run: echo "build"
post:
  run_always: true
  steps:
    - run: echo "notification"
```

### stages 阶段机制

- **阶段间串行执行**：多个 stage 按定义顺序依次执行，前一个 stage 的所有 job 完成后才进入下一个 stage。
- **fail_fast**：当某个 stage 中的 job 失败时，可配置是否立即终止后续 stage 的执行。
- **可缺省**：当 workflow 仅有一个 stage 时，`stages` 字段可省略，此时所有 job 默认并行执行。

```yaml
name: staged-pipeline
on:
  push:
    branches:
      - main
stages:
  - name: build-stage
    fail_fast: true
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - run: echo "build"
  - name: test-stage
    fail_fast: false
    jobs:
      unit-test:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - run: echo "unit test"
      integration-test:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - run: echo "integration test"
  - name: deploy-stage
    jobs:
      deploy:
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - run: echo "deploy"
```

### post 后处理阶段

`post` 是 AtomGit Action 特有的后处理阶段，用于在 workflow 执行结束后进行通知、资源清理、状态回写等操作：

- `run_always` 默认为 `true`，即无论 workflow 是否成功都会执行。
- 适合放置通知推送（如邮件、IM 消息）、临时文件清理、运行结果回写等逻辑。

```yaml
name: ci-with-post
on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "build"
post:
  run_always: true
  steps:
    - name: Send notification
      run: echo "workflow finished, send notification"
```

### concurrency 并发控制

AtomGit Action 的并发控制配置：

```yaml
concurrency:
  enable: true
  max: 3
  exceed-action: QUEUE
  preemption:
    enable: true
    events: [mr_id]
```

| 字段 | 说明 |
|------|------|
| `enable` | 是否启用并发控制 |
| `max` | 最大并发数，范围 1-5 |
| `exceed-action` | 超出并发限制时的策略：`IGNORE`（忽略新请求）或 `QUEUE`（排队等待） |
| `preemption.enable` | 是否启用抢占策略，默认为true |
| `preemption.events` | 抢占事件，限制只能配置不超过10个 |

### permissions 权限

AtomGit Action 的权限体系，使用 `atomgit` 上下文对应的权限项：

```yaml
permissions:
  project: read
  pr: write
  issue: read
  note: write
  repository: read
  hook: none
```

| 权限项 | 说明 | 可选级别 |
|--------|------|---------|
| `project` | 项目访问权限 | read / write / none |
| `pr` | Pull Request 权限 | read / write / none |
| `issue` | Issue 权限 | read / write / none |
| `note` | 评论/备注权限 | read / write / none |
| `repository` | 仓库权限 | read / write / none |
| `hook` | Webhook 权限 | read / write / none |

快捷语法：

- `read-all`：所有权限设为 read
- `write-all`：所有权限设为 write
- `permissions: {}`：所有权限设为 none（最小权限原则）

```yaml
permissions: read-all
```

```yaml
permissions: {}
```

## 常见问题

**Q：stages 字段什么时候可以省略？**

A：当 workflow 仅有一个逻辑阶段（或不需要阶段串行控制）时，`stages` 可省略。省略后所有 job 默认并行执行，可通过 `needs` 配置依赖关系。

**Q：post 阶段的 run_always 能设为 false 吗？**

A：可以，但默认为 `true`。设为 `false` 后，post 阶段仅在 workflow 成功时执行。
