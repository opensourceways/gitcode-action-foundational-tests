<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/configure-triggers | fetched: 2026-07-20 -->

# 配置触发条件

**适用场景**：当你需要控制 workflow 在什么事件、什么分支、什么路径或什么 Tag 下触发时。

## 前提条件

- workflow 文件已放在 `.gitcode/workflows/` 目录下。
- 熟悉 YAML 基本语法。

## 快速示例

```yaml
name: ci
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
jobs:
  test:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - uses: checkout
      - run: npm ci && npm test
```

## 配置说明

### push 触发

push 事件在代码推送到仓库时触发：

```yaml
on:
  push:
    branches:
      - main
      - develop
```

### pull_request 触发

pull_request 事件在创建、更新或合并 Pull Request 时触发。`branches` 过滤的是目标分支（base branch），而非源分支：

```yaml
on:
  pull_request:
    branches:
      - main
```

> **重要**：branches 过滤的是 PR 的目标分支（base branch），即 PR 合入的目标分支。如果 PR 的目标分支不在 branches 列表中，则不会触发。

pull_request 支持配置活动类型：

```yaml
on:
  pull_request:
    types:
      - open
      - update
      - reopen
    branches:
      - main
```

> **types 取值范围**：`pull_request` 的 `types` 取值范围为 `[merge, open, reopen, update]`。不填时默认为 `[open, reopen, update]`。

### workflow_dispatch 手动触发

workflow_dispatch 支持在 AtomGit 界面手动触发 workflow，可定义输入参数：

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: '部署目标环境'
        required: true
        default: 'staging'
        type: string
      version:
        description: "发布版本号"
        type: string
        required: false
        default: "1.0.0"
      deploy_count:
        description: '并行部署数量'
        type: string
        required: false
        default: "1"
      dry_run:
        description: '是否仅验证不部署'
        type: string
        required: false
        default: "false"
```

AtomGit Action 的 `workflow_dispatch.inputs` 仅支持 `string` 类型参数。所有输入值均为字符串，如需数字或布尔语义，可在工作流中通过表达式进行类型转换。

### workflow_call 可重用工作流触发

workflow_call 用于定义可被其他 workflow 调用的可重用工作流：

```yaml
on:
  workflow_call:
    inputs:
      config-path:
        description: "配置文件路径"
        type: string
        required: false
        default: "config/default.json"
    secrets:
      deploy-token:
        description: "部署 token"
        required: true
```

嵌套调用最多支持 2 层，即可重用工作流不能再调用另一个可重用工作流。

### schedule 定时触发

schedule 使用 POSIX cron 语法：

```yaml
on:
  schedule:
    - cron: "0 2 * * *"
```

> **注意**：
> - cron 使用 UTC 时区。
> - 定时任务可能存在数分钟的调度延迟。
> - schedule 仅在仓库的默认分支生效。
> - cron 的五段式含义：`分钟 小时 日 月 星期`。

### 多事件组合

同一 workflow 可同时响应多个事件：

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:
  schedule:
    - cron: "0 2 * * *"
```

### branches / branches-ignore 过滤

- `branches`：白名单模式，仅匹配的分支触发。
- `branches-ignore`：黑名单模式，不匹配的分支触发。
- 两者不能同时使用。

```yaml
on:
  push:
    branches:
      - main
      - develop
      - 'feature/**'
```

```yaml
on:
  push:
    branches-ignore:
      - experimental
```

### paths / paths-ignore 过滤

- `paths`：仅当匹配的路径发生变更时触发。
- `paths-ignore`：仅当不匹配的路径发生变更时触发。
- 两者不能同时使用。
- **paths 匹配前 300 个变更文件**，超出部分不参与匹配判断。

```yaml
on:
  push:
    branches:
      - main
    paths:
      - "src/**"
      - "package.json"
      - "!src/docs/**"
```

```yaml
on:
  push:
    branches:
      - main
    paths-ignore:
      - "docs/**"
      - "**.md"
```

### tags / tags-ignore 过滤

```yaml
on:
  push:
    tags:
      - "v*"
      - "release-*"
```

```yaml
on:
  push:
    tags-ignore:
      - "v*-alpha"
```

### 否定模式（!）

在 `branches`、`paths`、`tags` 中可以使用 `!` 前缀表示否定匹配：

```yaml
on:
  push:
    branches:
      - "feature/**"
      - "!feature/experimental"
    paths:
      - "src/**"
      - "!src/docs/**"
```

> **注意**：否定模式必须与肯定模式组合使用。如果仅有否定模式（如 `branches: ["!main"]`），workflow 将不会触发。
