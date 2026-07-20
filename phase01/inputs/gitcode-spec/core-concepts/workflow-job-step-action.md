<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/core-concepts/workflow-job-step-action | fetched: 2026-07-20 -->

# 工作流、任务、步骤和 Action

AtomGit Action 的执行模型遵循清晰的层级链：

```
Event → Workflow → Stages → Jobs → Runner → Steps → Scripts / Actions
```

当特定 **Event（事件）** 触发后，系统加载对应的 **Workflow（工作流）** 定义文件，按 **Stages（阶段）** 顺序串行推进，每个 Stage 内的 **Jobs（任务）** 默认并行执行，每个 Job 被分配到一台 **Runner（运行器）** 上，Job 内的 **Steps（步骤）** 串行依次运行。

## Workflow（工作流）

Workflow 是自动化流程的顶层定义，存储在仓库的 `.gitcode/workflows/` 目录下，以 YAML 格式描述。

```yaml
name: Build and Deploy
on:
  push:
    branches: [main]
stages:
  - build
    jobs:
      build-job:
        runs-on: ubuntu-latest
        steps:
          - run: echo "Building..."
  - test
    jobs:
      test-job:
        runs-on: ubuntu-latest
        steps:
          - run: echo "Testing..."
  - deploy
    jobs:
      deploy-job:
        runs-on: ubuntu-latest
        steps:
          - run: echo "Deploying..."
```

## Stages（阶段）

Stage 是 AtomGit Action 特有的编排机制：

- **阶段间串行执行**：前一 Stage 内所有 Job 完成后才进入下一个 Stage
- **阶段内 Job 默认并行**：同一 Stage 中的多个 Job 默认同时启动
- **fail_fast 机制**：当 Stage 设置 `fail_fast: true` 时，任一 Job 失败立即终止同阶段其他 Job

```yaml
stages:
  build_stage:
    name: 构建
    fail_fast: true
    jobs:
      runs-on: ...
  test_stage:
    name: 测试
    jobs:
      runs-on: ...
```

**Post 后处理阶段**是 AtomGit Action 的特殊 Stage 类型：

- 在流水线达到终态后执行，默认 `run_always: true`
- 适合用于通知、清理、报告等收尾操作

## Job（任务）

Job 是 Stage 内的可执行单元，被调度到一台 Runner 上运行。核心属性：

| 字段 | 说明 |
|------|------|
| `stage` | 声明 Job 所属的 Stage |
| `runs-on` | 指定运行器标签 |
| `needs` | 声明依赖的其他 Job |
| `if` | 条件表达式 |
| `env` | Job 级环境变量 |
| `steps` | 步骤列表，串行执行 |
| `timeout-minutes` | 超时时间 |
| `continue-on-error` | Job 失败不阻断后续 |
| `strategy` | 矩阵策略配置 |

## Step（步骤）

Step 是 Job 内的最小执行单元，按定义顺序串行运行：

| 类型 | 关键字 | 说明 |
|------|--------|------|
| **Script** | `run` | 执行 Shell 命令 |
| **Action** | `uses` | 调用可复用动作组件 |

```yaml
steps:
  - name: Checkout code
    uses: checkout
  - name: Install dependencies
    run: npm install
  - name: Run tests
    run: npm test
    env:
      NODE_ENV: test
```

## Action（动作）

Action 是可复用的原子操作组件，被 Step 通过 `uses` 字段调用：

```yaml
steps:
  - uses: checkout
  - uses: setup-node
    with:
      node-version: '20'
```

## Runner（运行器）

Runner 是执行 Job 的计算节点，分为官方资源池 Runner 和自托管 Runner：

```yaml
jobs:
  build:
    runs-on: ubuntu-latest    # 官方资源池
  deploy:
    runs-on: [self-hosted, linux, x64]   # 自托管
```
