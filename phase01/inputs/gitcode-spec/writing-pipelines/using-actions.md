<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/using-actions | fetched: 2026-07-20 -->

# 使用 Action 插件

**适用场景**：当你需要在 step 中调用可复用的 Action 插件来完成拉取代码、设置语言环境、缓存依赖、上传制品等操作时。

## 前提条件

*   已了解 `uses` 和 `with` 的用法。

## 快速示例

```yaml
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - name: Checkout source code
        uses: checkout
      - name: Setup Node.js
        uses: setup-node
        with:
          node-version: "20"
      - run: npm ci
      - run: npm test
```

## 配置说明

### 三种引用方式

AtomGit Action 支持三种 Action 插件引用方式：

| 方式 | 语法 | 说明 |
|------|------|------|
| 官方插件 | `uses: action-name@ref` | 直接写插件名称 |
| 开源插件 | `uses: owner/repo/path@ref` | AtomGit 公开仓库中的插件 |
| 本仓引用 | `uses: ./path/to/action` | 当前仓库中的插件 |

#### 1. 官方插件引用

直接写插件名称：

```yaml
steps:
  - uses: checkout
  - uses: setup-node
    with:
      node-version: "20"
```

#### 2. 开源插件引用

使用 `{owner}/{repo}/{path}@{ref}` 格式引用开源仓库中的 Action：

```yaml
steps:
  - uses: checkout
  - uses: docker/build-push-action@v6
    with:
      push: true
      tags: example.com/demo/app:latest
```

#### 3. 自定义插件引用（同仓相对路径）

引用当前仓库中的本地 Action：

```yaml
steps:
  - uses: ./.gitcode/actions/my-custom-action
```

本地 Action 需在仓库对应路径下有 `action.yml` 元数据文件：

```yaml
# 使用 Action 插件
name: "My Custom Action"
description: "Do something custom"
inputs:
  param1:
    description: "Parameter 1"
    required: false
    default: "default-value"
outputs:
  result:
    description: "Action result"
runs:
  using: 'node16'
  main: 'dist/main.js'
```

### Action 版本引用方式

| 引用方式 | 说明 | 推荐度 |
|---------|------|--------|
| `@v4`（Tag） | 使用主版本 Tag，可自动获取补丁更新 | 推荐 |
| `@v4.1.0`（完整版本） | 使用精确版本，行为稳定但不会自动更新 | 安全性最高 |
| `@main`（分支） | 使用分支最新提交，行为可能变化 | 不推荐 |
| `@a1b2c3d`（SHA） | 使用精确提交 SHA，行为完全确定 | 生产环境推荐 |

### with 传入参数

`with` 用于向 Action 传递输入参数，参数名需与 Action 的 `action.yml` 中 `inputs` 定义一致：

```yaml
steps:
  - uses: setup-node
    with:
      node-version: "20"
      registry-url: "https://registry.npmjs.org"
```
