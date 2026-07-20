<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/pass-output-between-jobs | fetched: 2026-07-20 -->
<!-- 勘误提示：本页 WebFetch 返回为摘要（未保留完整代码块），下述为要点提炼，建议重抓补全。 -->

# 任务间传递输出参数

## 概述

介绍在 AtomGit 流水线中如何在不同级别间传递输出参数：当你需要在 step 之间、job 之间、甚至 workflow 之间传递输出参数时可参考。

## 前提条件

- 理解 `id`、`outputs`、`needs` 的作用
- 理解 `ATOMGIT_OUTPUT` 环境变量的用法

## 三级传递模型

```
Step 输出（ATOMGIT_OUTPUT） → 映射到 Job 输出（jobs.<job_id>.outputs） → 映射到 workflow_call job 输出
```

## 核心配置方式

- **Step 输出**：在步骤中使用 `ATOMGIT_OUTPUT` 环境变量写入键值对。每个参数最大 1MB。
  ```yaml
  steps:
    - id: version
      run: echo "version=1.0.0" >> "$ATOMGIT_OUTPUT"
  ```
- **Job 输出**：通过映射 step 的输出使其他 job 可引用，下游 job 通过 `needs.<job_id>.outputs.<key>` 访问。
  ```yaml
  jobs:
    prepare:
      runs-on: [ubuntu-latest, x64, small]
      outputs:
        version: ${{ steps.version.outputs.version }}
      steps:
        - id: version
          run: echo "version=1.0.0" >> "$ATOMGIT_OUTPUT"
    build:
      needs: prepare
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - run: echo "build version ${{ needs.prepare.outputs.version }}"
  ```
- **Workflow 输出**：在可重用工作流中，将 job 输出映射至 workflow 级别输出（`on.workflow_call.outputs`）。

## 多行输出

使用分隔符语法处理多行内容，通过生成随机分隔符确保值准确传递（参见「使用脚本命令」§多行输出）。
