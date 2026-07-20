<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/configure-matrix-builds | fetched: 2026-07-20 -->

# 配置矩阵构建

**适用场景**：当需要在多个操作系统、多个语言版本、多种架构组合下并行执行测试或构建时。

## 前提条件

- 已确定需要测试的维度（OS、语言版本、架构等）
- 已确认 Runner 标签能覆盖所需的运行环境

## 快速示例

```yaml
name: matrix-test
on:
  push:
    branches:
      - main
jobs:
  test:
    runs-on: ${{ matrix.os }},${{ matrix.arch }},small
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        arch: [x64]
        node-version: [18, 20]
      exclude:
        - os: windows-latest
          node-version: 18
      fail-fast: false
      max-parallel: 4
    steps:
      - uses: checkout
      - uses: setup-node
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

## 配置说明

### matrix 变量定义

`matrix` 定义矩阵变量，每个变量值的组合会生成一个 job 实例。

**一维矩阵**：

```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
```

**二维矩阵**：

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node-version: [18, 20]
```

二维矩阵生成 2 × 2 = 4 个 job 实例。

**三维矩阵**：

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    arch: [x64, arm64]
    node-version: [18, 20]
```

### include 展开与追加配置

`include` 用于向现有矩阵追加特定组合或为特定组合添加额外变量：

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node-version: [18, 20]
    include:
      - os: macos-latest
        node-version: 20
        experimental: true
```

`include` 中未在基础矩阵定义的变量（如 `experimental`）会被添加到对应 job 实例中。

### exclude 排除特定组合

`exclude` 用于从矩阵中排除特定组合：

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node-version: [18, 20]
    exclude:
      - os: windows-latest
        node-version: 18
```

排除后实际生成 3 个 job 实例（而非 4 个）。

### fail-fast 快速失败策略

```yaml
strategy:
  fail-fast: true
```

- `fail-fast: true`：任意一个 job 实例失败后，立即取消其余尚未完成的 job 实例
- `fail-fast: false`：任意一个 job 实例失败后，其余 job 实例继续执行

> **注意**：`strategy.fail-fast` 和 `stages.fail_fast` 是不同层面的控制。`strategy.fail-fast` 控制矩阵内 job 实例的行为，`stages.fail_fast` 控制阶段间 job 的行为。

### max-parallel 最大并行数

```yaml
strategy:
  max-parallel: 4
```

限制同时运行的矩阵 job 实例数量。不设置时默认最大并行数取决于 Runner 可用数量。

### runs-on 动态选择

矩阵中 `runs-on` 可引用 `matrix` 变量动态选择 Runner：

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }},${{ matrix.arch }},small
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        arch: [x64, arm64]
```
