<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/using-variables-secrets | fetched: 2026-07-20 -->

# 使用变量和密钥

**适用场景**：当你需要在 workflow 中使用环境变量、配置变量、密钥或输入参数，并理解它们的作用域和优先级规则时。

## 前提条件

* 已在 AtomGit 界面创建所需的 vars 和 secrets（路径：项目设置 → Action秘钥与变量）。
* 理解 env、vars、secrets、inputs 的区别。

## 快速示例

```yaml
name: ci-with-vars
on:
  push:
    branches:
      - main
  workflow_dispatch:
    inputs:
      environment:
        description: "部署环境"
        type: string
        default: test

env:
  APP_NAME: demo-app

jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    env:
      BUILD_MODE: release
    steps:
      - uses: checkout
      - name: Print variables
        env:
          STEP_VAR: step-level
        run: |
          echo "APP_NAME=$APP_NAME"
          echo "BUILD_MODE=$BUILD_MODE"
          echo "STEP_VAR=$STEP_VAR"
          echo "CONFIG_VAR=${{ vars.DEPLOY_TARGET }}"
          echo "SHA=${{ atomgit.sha }}"
      - name: Use secret
        env:
          REGISTRY_PASSWORD: ${{ secrets.REGISTRY_PASSWORD }}
        run: echo "password is masked"
```

## 配置说明

### 四种变量类型

| 类型 | 适合存储 | 是否敏感 | 定义位置 | 引用方式 |
|------|--------|--------|--------|--------|
| `env` | workflow 内部临时环境变量 | 否 | YAML 文件 | `$APP_NAME` 或 `${{ env.APP_NAME }}` |
| `vars` | 仓库/组织级普通配置 | 否 | AtomGit 界面 | `${{ vars.DEPLOY_TARGET }}` |
| `secrets` | 密码、token、私钥 | 是 | AtomGit 界面 | `${{ secrets.REGISTRY_PASSWORD }}` |
| `inputs` | workflow_dispatch / workflow_call 输入 | 否 | YAML 文件 | `${{ inputs.environment }}` |

### env 环境变量

`env` 支持三级作用域：Workflow级 → Job级 → Step级

```yaml
env:
  APP_NAME: demo-app        # Workflow级，所有 job 和 step 可见

jobs:
  build:
    env:
      BUILD_MODE: release    # Job级，该 job 内所有 step 可见
    steps:
      - env:
          STEP_VAR: step-level   # Step级，仅该 step 可见
        run: echo "$STEP_VAR"
```

**优先级规则**：Step级 > Job级 > Workflow级。同名的 step 级变量会覆盖 job 级和 workflow 级变量。

**YAML 中引用 vs Runner 中引用**：

| 引用方式 | 语法 | 适用场景 |
|--------|------|--------|
| YAML 中引用（表达式） | `${{ env.APP_NAME }}` | 在 YAML 字段中使用，在 Runner 执行前替换 |
| Runner 中引用（环境变量） | `$APP_NAME` | 在 `run` 命令中使用，由 Shell 解释 |

### vars 配置变量

`vars` 在 AtomGit 界面创建，支持仓库级和组织级作用域：

```yaml
steps:
  - name: Use config variable
    run: echo "deploy to ${{ vars.DEPLOY_TARGET }}"
```

创建路径：仓库设置 → 变量 → 新建变量

### secrets 密钥

`secrets` 在 AtomGit 界面加密创建，日志中自动脱敏显示为 `***`：

```yaml
steps:
  - name: Login registry
    env:
      REGISTRY_USERNAME: ${{ secrets.REGISTRY_USERNAME }}
      REGISTRY_PASSWORD: ${{ secrets.REGISTRY_PASSWORD }}
    run: |
      echo "$REGISTRY_PASSWORD" | docker login example.com -u "$REGISTRY_USERNAME" --password-stdin
```

> **安全提示**：
>
> * 不要在日志中打印 secret（`echo "$SECRET"` 日志中会脱敏，但 `echo "${{ secrets.MY_SECRET }}"` 可能绕过脱敏）。
> * 不要把 secret 写入制品或缓存。
> * 外部贡献者的 PR/MR 默认不应暴露高权限 secret。

### 系统变量

AtomGit Action 的系统变量使用 `ATOMGIT_*` 前缀：

| 系统变量 | 说明 |
|---------|------|
| `ATOMGIT_TOKEN` | 自动生成的 workflow token |
| `ATOMGIT_SHA` | 当前提交 SHA |
| `ATOMGIT_REF` | 当前分支或 Tag 引用 |
| `ATOMGIT_EVENT_NAME` | 触发事件名称 |
| `ATOMGIT_REPOSITORY` | 仓库标识（owner/repo） |
| `ATOMGIT_WORKSPACE` | Runner 上的工作目录 |
| `ATOMGIT_OUTPUT` | step 输出写入文件路径 |
| `ATOMGIT_ENV` | 环境变量写入文件路径 |
| `ATOMGIT_PATH` | PATH 写入文件路径 |
| `ATOMGIT_RUNNER_OS` | Runner 操作系统 |
| `ATOMGIT_RUNNER_ARCH` | Runner 架构 |

### 优先级规则总览

从高到低：

1. Step级 `env`
2. Job级 `env`
3. Workflow级 `env`
4. `vars`（配置变量）
5. 系统变量（`ATOMGIT_*`）
