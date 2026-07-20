<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/running-pipelines/manually-trigger-pipeline | fetched: 2026-07-20 -->

# 手动触发流水线

**适用场景**：当需要在非自动触发场景下主动执行流水线——例如调试某分支、验证临时参数、发布特定版本——可通过 `workflow_dispatch` 事件手动触发。

## 配置说明

### 定义 workflow_dispatch workflow

在 `.gitcode/workflows/` 目录下创建或编辑 workflow 文件，添加 `workflow_dispatch` 触发事件：

```yaml
# 手动触发流水线
name: Manual Deploy
on:
  workflow_dispatch:
    inputs:
      environment:
        description: '部署目标环境'
        required: true
        default: 'staging'
        type: string
      version:
        description: '部署版本号'
        required: true
        type: string
      dry-run:
        description: '仅模拟，不实际部署'
        required: false
        type: string
        default: "false"
      tags:
        description: '测试标签（逗号分隔）'
        required: false
        type: string

stages:
  - name: validate
    jobs:
      - name: check-version
        runs-on: {ubuntu-24,x64,small}
        steps:
          - run: echo "Deploy version ${{ inputs.version }} to ${{ inputs.environment }}"
          - run: echo "Dry run mode = ${{ inputs.dry-run }}"
  - name: deploy
    jobs:
      - name: push-to-env
        runs-on: {ubuntu-24,x64,medium}
        steps:
          - run: make deploy ENV=${{ inputs.environment }} VERSION=${{ inputs.version }}
```

### inputs 字段类型详解

AtomGit Action 的 `inputs` 仅支持 `string` 类型参数。所有输入值均为字符串。

| type | 说明 | 示例 |
|------|------|------|
| `string` | 文本输入 | 版本号、镜像名、环境名 |

每个 input 字段属性：

- `description`：输入项说明文字，展示在触发表单中
- `required`：是否必填（`true`/`false`）
- `default`：默认值
- `type`：输入类型，当前仅支持 `string`

### 触发操作

1. 进入项目 **Actions** 标签页。
2. 左侧选择目标 workflow 名称。
3. 右侧点击 **Run workflow** 按钮。
4. 弹出表单，选择或填写各 `inputs` 参数，并选择目标分支。
5. 点击 **Run** 提交触发。

> **注意**：只有 `on` 中包含 `workflow_dispatch` 的 workflow 才会显示 **Run workflow** 按钮。

### 在 workflow 中引用 inputs

```yaml
steps:
  - run: echo "Environment = ${{ inputs.environment }}"
  - run: echo "Version = ${{ inputs.version }}"
  - if: ${{ inputs.dry-run == 'true' }}
    run: echo "This is a dry run"
```

`inputs` 上下文仅在 `workflow_dispatch` 触发的运行中可用，其他触发事件下引用 `inputs` 会报错。

## 常见问题

**Q：点击 Run workflow 后提示"此 workflow 不支持手动触发"？**

A：workflow 的 `on` 字段未包含 `workflow_dispatch` 事件，请修改 `.gitcode/workflows/{file}.yml` 添加该触发类型。

**Q：workflow_dispatch 能否与其他触发事件共存？**

A：可以。`on` 字段支持多事件并列：

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        type: string
```

**Q：手动触发时如何指定分支？**

A：触发表单中有分支选择下拉框，默认为仓库默认分支，可切换为任意分支。workflow 将使用该分支上的 `.gitcode/workflows/` 文件版本执行。
