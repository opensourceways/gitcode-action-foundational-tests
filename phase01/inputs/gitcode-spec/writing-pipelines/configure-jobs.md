<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/configure-jobs | fetched: 2026-07-20 -->

# 配置任务 Jobs

**适用场景**：当你需要在 workflow 中定义一个或多个任务，指定运行环境、超时时间、环境变量、并发控制、矩阵策略等时。

## 前提条件

- 已理解 workflow 的基本结构。
- 已确定 job 需要的运行环境（Runner 标签）。

## 快速示例

```yaml
name: ci
on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    timeout-minutes: 30
    env:
      APP_ENV: production
    steps:
      - uses: checkout
      - run: ./build.sh
```

## 配置说明

### runs-on 运行环境

`runs-on` 指定 job 运行的 Runner 环境。AtomGit Action 的官方资源池标签采用**三段式格式**：`{os}-{version},{arch},{flavor}`。

| 段位 | 说明 | 示例 |
|------|------|------|
| `{os}-{version}` | 操作系统及版本 | `ubuntu-latest` |
| `{arch}` | CPU 架构 | `x64`、`arm64` |
| `{flavor}` | 资源规格 | `small`、`medium`、`large` |

完整标签示例：

```yaml
runs-on: [ubuntu-latest, x64, small]
```

默认标签 `default` 对应 `[ubuntu-latest, x64, small]`，即：

```yaml
runs-on: default
```

自托管资源池配置：

```yaml
runs-on:
  type: self-hosted
  group: my-runner-group
  labels:
    - linux
    - x64
    - gpu
```

| 字段 | 说明 |
|------|------|
| `type` | Runner 类型，`self-hosted` 表示自托管 |
| `group` | Runner 所属组 |
| `labels` | Runner 标签列表，用于匹配 |

### needs 依赖

通过 `needs` 配置 job 间的依赖关系，被依赖的 job 完成后才执行当前 job：

```yaml
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "build"
  test:
    runs-on: [ubuntu-latest, x64, small]
    needs: build
    steps:
      - run: echo "test"
  deploy:
    runs-on: [ubuntu-latest, x64, small]
    needs:
      - test
      - lint
    steps:
      - run: echo "deploy"
```

### if 条件执行

job 级别的 `if` 推迟整个 job 的执行：

```yaml
jobs:
  deploy:
    if: ${{ atomgit.ref == 'refs/heads/main' }}
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "deploy only on main"
```

### timeout-minutes 超时时间

```yaml
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    timeout-minutes: 30
    steps:
      - run: ./build.sh
```

默认超时时间为 360 分钟（6 小时）。超时后 job 将被强制终止。

### env 环境变量

job 级别的 `env` 对该 job 内所有 step 可见：

```yaml
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    env:
      APP_ENV: production
      BUILD_MODE: release
    steps:
      - run: echo "$APP_ENV"
      - run: echo "$BUILD_MODE"
```

### outputs 输出参数

job 可以声明输出参数，从 step 输出中映射：

```yaml
jobs:
  prepare:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - id: version
        run: echo "version=1.0.0" >> "$ATOMGIT_OUTPUT"
```

### concurrency 并发控制

job 级别也可配置并发控制：

```yaml
jobs:
  deploy:
    runs-on: [ubuntu-latest, x64, small]
    concurrency:
      enable: true
      max: 1
      exceed-action: IGNORE
    steps:
      - run: echo "deploy"
```

### strategy 矩阵策略

详见[配置矩阵构建](/docs/help/home/org_project/pipeline/writing-pipelines/configure-matrix-builds)。

### continue-on-error 容错

```yaml
jobs:
  flaky-test:
    runs-on: [ubuntu-latest, x64, small]
    continue-on-error: true
    steps:
      - run: ./run-flaky-test.sh
```

设置 `continue-on-error: true` 后，即使 job 失败，workflow 也不会因此终止（后续依赖该 job 的 job 需通过 `if` 条件判断是否继续）。

## 常见问题

**Q：runs-on 标签格式为什么是三段式？**

A：AtomGit Action 官方资源池标签采用 `{os}-{version},{arch},{flavor}` 三段式格式，提供了更精确的环境选择能力。

**Q：job 默认是并行还是串行？**

A：无 `needs` 配置时，多个 job 默认并行执行。配置 `needs` 后按依赖顺序执行。也可使用 `stages` 阶段机制实现阶段间串行。

**Q：continue-on-error 对后续 job 有什么影响？**

A：设置 `continue-on-error: true` 的 job 即使失败，也不会阻止后续 job 运行。但后续依赖该 job 的 job 中，`if: ${{ success }}` 条件将不满足，需要用 `if: ${{ always }}` 来确保执行。
