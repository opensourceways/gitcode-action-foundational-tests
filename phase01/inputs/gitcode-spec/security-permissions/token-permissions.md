<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/security-permissions/token-permissions | fetched: 2026-07-20 -->

# Token 权限与最小授权

## 概述

本文档介绍如何在 AtomGit 流水线中配置 `ATOMGIT_TOKEN` 的权限，遵循最小授权原则，确保每个 job 仅拥有必要的访问权限。

## 配置说明

### ATOMGIT_TOKEN 自动生成

每次流水线运行时，AtomGit Action 自动生成 `ATOMGIT_TOKEN`，用于：

- 克隆代码仓库
- 推送构建产物
- 创建 PR、Issue 评论
- 操作项目资源

`ATOMGIT_TOKEN` 的权限范围由 workflow 的 `permissions` 字段控制。

### permissions 字段详解

**顶层 permissions（workflow 级别默认）**：

```yaml
# Token 权限与最小授权
name: CI Pipeline
permissions:
  project: read           # 项目信息读取
  pr: write               # PR 写操作（创建、评论、合并）
  issue: read             # Issue 读取
  note: write             # 评论/Note 写操作
  repository: write       # 仓库写操作（推送）
  hook: none              # Webhook 无权限
```

### 权限类型对照

| 权限域 | `read` | `write` | `none` | 说明 |
|--------|--------|---------|---------|------|
| **project** | 读取项目信息 | 修改项目设置 | 无权限 | 项目元数据操作 |
| **pr** | 读取 PR | 创建/评论/合并 PR | 无权限 | Pull Request 操作 |
| **issue** | 读取 Issue | 创建/评论 Issue | 无权限 | Issue 操作 |
| **note** | 读取评论 | 创建评论 | 无权限 | 通用评论操作 |
| **repository** | 克隆/读取 | 推送/修改仓库 | 无权限 | 代码仓库操作 |
| **hook** | 读取 Webhook | 管理 Webhook | 无权限 | Webhook 管理 |

### 最小权限原则实践

**原则**：每个 job 仅声明其所需权限，不多给。

**示例一：仅读仓库的 lint job**

```yaml
permissions:
  repository: read         # 仅需克隆代码
  pr: none                 # 不操作 PR
  issue: none              # 不操作 Issue
  note: none               # 不评论
  project: none            # 不读取项目信息
  hook: none               # 不操作 Webhook

stages:
  - name: lint
    jobs:
      - name: code-lint
        runs-on: {ubuntu-24,x64,slim}
        steps:
          - run: npm run lint
```

**示例二：需要评论 PR 的测试 job**

```yaml
permissions:
  repository: read         # 克隆代码
  pr: write                # 在 PR 上评论测试结果
  issue: none
  note: none
  project: none
  hook: none

stages:
  - name: test
    jobs:
      - name: report-results
        runs-on: {ubuntu-24,x64,small}
        steps:
          - run: |
              pytest
              curl -X POST "https://atomgit.com/api/v5/repos/${{ atomgit.repository }}/pulls/${{ atomgit.event.pr.number }}/comments" \
                -H "Authorization: token $ATOMGIT_TOKEN" \
                -d '{"body": "All tests passed ✅"}'
```

### permissions 与 ATOMGIT_TOKEN 的关系

| permissions 配置 | ATOMGIT_TOKEN 实际权限 |
|------------------|----------------------|
| 未声明 permissions | 使用仓库设置中定义的权限 |
| 顶层声明 permissions | 所有 job 继承顶层权限，除非 job 级覆盖 |
| `permissions: {}`（空） | ATOMGIT_TOKEN 仅拥有最小默认权限（repository:read） |

> **关键安全提示**：`pull_request` 事件来自 fork 仓库时，ATOMGIT_TOKEN 仅拥有 read 权限，无论 permissions 如何声明。这是 AtomGit Action 的安全隔离机制。若需写权限，需使用 `pull_request_target` 事件。
