<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/configure-dependencies-order | fetched: 2026-07-20 -->

# 配置任务依赖与执行顺序

## 概述

本文档介绍如何在 AtomGit 流水线中控制多个 job 的执行顺序，实现串行流程或复杂的 DAG 拓扑。

## 前提条件

- workflow 中包含多个 job
- 理解 `needs` 依赖和 `stages` 阶段机制

## 快速示例

### 方式一：使用 needs 配置依赖

```yaml
name: pipeline-with-needs
on:
  push:
    branches:
      - main
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
    needs: test
    steps:
      - run: echo "deploy"
```

### 方式二：使用 stages 阶段机制

```yaml
name: pipeline-with-stages
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

## 配置说明

### needs 依赖机制

`needs` 配置 job 间的依赖关系：

- 被依赖的 job 完成后才执行当前 job
- 多个依赖 job 并行完成后才执行当前 job
- 依赖的 job 失败时，当前 job 默认不执行（除非配置 `if: ${{ always }}`）

#### 串行依赖示例

```yaml
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "build"
  test:
    needs: build
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "test"
  deploy:
    needs: test
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "deploy"
```

#### 多依赖汇聚示例

```yaml
jobs:
  lint:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "lint"
  unit-test:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "unit test"
  integration-test:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "integration test"
  package:
    needs:
      - lint
      - unit-test
      - integration-test
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "package"
  release:
    needs: package
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "release"
```

对应拓扑图：

```
lint ──────────┐
               │
unit-test ─────├── package ── release
               │
int-test ──────┘
```

### stages 阶段机制

`stages` 是 AtomGit Action 特有的 workflow 层级结构：

- **阶段间串行执行**：按 stages 定义顺序，前一个 stage 所有 job 完成后进入下一个 stage
- **阶段内并行执行**：同一 stage 内的多个 job 并行执行
- **fail_fast**：当 stage 中某个 job 失败时：
  - `fail_fast: true`：立即终止当前 stage 中其他 job，跳过后续所有 stage
  - `fail_fast: false`：当前 stage 中其他 job 继续执行，但后续 stage 不会执行

```yaml
stages:
  stage1:
    name: PR SCA
    jobs:
      sca:
        name: codescan
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - name: sca
            run: |
              python3 codescan_gitcode.py
      static:
        name: static check
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - name: static_check
            run: |
              python3 static_gitcode.py
  stage2:
    name: Release SCA
    jobs:
      sca:
        name: codescan
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - name: sca
            run: |
              python3 codescan_gitcode.py
      static:
        name: static check
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - name: static_check
            run: |
              python3 static_gitcode.py
```

- **stages 可缺省**：当 workflow 仅有一个逻辑阶段时，`stages` 字段可省略

### needs 与 stages 的区别

| 对比项 | needs | stages |
|--------|-------|--------|
| 控制粒度 | job 级别 | stage 级别 |
| 执行模型 | DAG 拓扑 | 阶段串行 + 阶段内并行 |
| 失败策略 | 依赖 job 失败则下游默认不执行 | fail_fast 控制阶段内和跨阶段行为 |
| 适用场景 | 精细依赖编排 | 大阶段分组串行 |

两种方式可以组合使用：同一 stage 内的 job 仍可通过 `needs` 配置依赖关系。
