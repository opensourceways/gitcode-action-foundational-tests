<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/quick-start | fetched: 2026-07-20 -->

# 快速开始

可通过阅读本文档快速开始在平台上使用流水线功能。

## 前提条件

- 已拥有 AtomGit / GitCode 账号，并创建至少一个仓库
- 仓库已有基本代码内容（至少一个分支）
- 已了解 YAML 基础语法

## 创建 Workflow 文件

在仓库根目录下创建 `.gitcode/workflows/` 目录，并添加 YAML 文件：

```
mkdir -p .gitcode/workflows
touch .gitcode/workflows/first-pipeline.yml
```

> **注意**：AtomGit Action 的 Workflow 文件存放目录为 **`.gitcode/workflows/`**，而非 `./workflows/`。目录路径错误会导致流水线无法被识别和触发。

## 最小 YAML 示例

```yaml
name: First Pipeline
on:
  push:
    branches:
      - main
jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - name: Print hello message
        run: echo "Hello GitCode Action"
```

### 示例解析

| 字段 | 说明 |
|------|------|
| `name` | Workflow 名称，显示在流水线列表中 |
| `on` | 触发事件，此处为 `main` 分支的 `push` 事件 |
| `jobs` | 任务集合 |
| `runs-on` | Runner 标签，`default` 使用默认资源池 |
| `run` | 执行 shell 命令 |

### atomgit 上下文常用变量

| 变量 | 说明 |
|------|------|
| `ATOMGIT_REF` | 触发分支或标签引用（如 `refs/heads/main`） |
| `ATOMGIT_SHA` | 触发提交的 SHA 值 |
| `ATOMGIT_REPOSITORY` | 仓库全名（如 `owner/repo`） |
| `ATOMGIT_EVENT_NAME` | 触发事件类型（如 `push`、`pull_request`） |
| `ATOMGIT_WORKFLOW` | 当前 Workflow 名称 |

## 提交触发

将 Workflow 文件提交到仓库即可触发流水线：

```
git add .gitcode/workflows/first-pipeline.yml
git commit -m "Add first GitCode Action pipeline"
git push origin main
```

## 成功结果验证

1. 进入 AtomGit 仓库页面，点击 **"流水线"** 或 **"Actions"** Tab
2. 在流水线列表中找到 **"First Pipeline"** 条目
3. 点击进入详情页，查看执行状态
4. 确认 Job 状态为 ✅（成功）
