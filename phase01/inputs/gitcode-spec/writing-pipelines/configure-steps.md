<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/configure-steps | fetched: 2026-07-20 -->

# 配置步骤 Steps

**适用场景**：当你需要在 job 内定义具体的执行步骤，包括运行脚本、调用 Action 插件、设置环境变量、条件执行等时。

## 前提条件

*   已定义 job 并指定 `runs-on`。
*   了解需要执行的具体操作（脚本或 Action 插件）。

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
      - name: Install and test
        run: |
          npm ci
          npm test
      - name: Print version
        env:
          APP_VERSION: "1.0.0"
        run: echo "version=$APP_VERSION"
```

## 配置说明

### id 步骤标识

`id` 用于唯一标识 step，后续可通过 `${{ steps.<id>.outputs.<key> }}` 引用该步骤的输出：

```yaml
steps:
  - id: version
    run: echo "version=1.0.0" >> "$ATOMGIT_OUTPUT"
  - name: Print version
    run: echo "${{ steps.version.outputs.version }}"
```

### name 步骤显示名称

`name` 是 step 在日志和界面中的展示名称：

```yaml
steps:
  - name: Install dependencies
    run: npm install
```

### uses 调用 Action 插件

`uses` 指定要调用的 Action 插件，格式为 `{owner}/{repo}@{ref}`：

```yaml
steps:
  - name: Checkout source code
    uses: checkout
```

详见[使用 Action 插件](/docs/help/home/org_project/pipeline/writing-pipelines/using-actions)。

### with 传入参数

`with` 用于向 Action 插件传递输入参数：

```yaml
steps:
  - uses: setup-node
    with:
      node-version: "20"
      registry-url: "https://registry.npmjs.org"
```

### run 执行命令

`run` 用于执行 shell 命令，支持单行和多行：

单行命令：

```yaml
steps:
  - name: Single command
    run: echo "hello"
```

多行命令：

```yaml
steps:
  - name: Multi-line commands
    run: |
      npm install
      npm run build
      npm test
```

### shell 选择 Shell 类型

`shell` 指定命令的执行 Shell，支持 `bash`、`sh`、`pwsh`、`python`：

```yaml
steps:
  - name: Run bash
    shell: bash
    run: Write-Host "Hello from bash"
```

```yaml
steps:
  - name: Run Python
    shell: python
    run: echo "Hello from python"
```

### working-directory 工作目录

`working-directory` 指定 step 的执行工作目录（相对于仓库根目录）：

```yaml
steps:
  - uses: checkout
  - name: Build frontend
    working-directory: frontend
    run: npm run build
```

AtomGit Action 支持 working-directory 的三级优先级规则：

**Workflow级 → Job级 → Step级**（优先级从低到高）

```yaml
defaults:
  run:
    shell: bash
    working-directory: project
jobs:
  build:
    defaults:
      run:
        shell: sh
        working-directory: src
    steps:
      - run: echo "uses sh in src"
      - shell: bash
        run: echo "overrides to bash"
```

### env 环境变量

step 级 `env` 仅在该 step 内生效：

```yaml
steps:
  - name: Print env
    env:
      APP_ENV: staging
      DEBUG: true
    run: |
      echo "APP_ENV=$APP_ENV"
      echo "DEBUG=$DEBUG"
```

### if 条件执行

step 级 `if` 控制该步骤是否执行，支持表达式和状态函数：

```yaml
steps:
  - name: Deploy only on main
    if: ${{ atomgit.ref == 'refs/heads/main' }}
    run: echo "deploy to production"
```

```yaml
steps:
  - name: Run on failure
    if: ${{ failed }}
    run: echo "previous step failed"
```

### continue-on-error 步骤容错

```yaml
steps:
  - name: Maybe-fail step
    continue-on-error: true
    run: ./flaky-script.sh
```

设置后，该 step 失败不会导致 job 失败，后续 step 仍会继续执行。

### timeout-minutes 步骤超时

```yaml
steps:
  - name: Long running step
    timeout-minutes: 10
    run: ./slow-build.sh
```

默认 step 无独立超时限制（受 job 的 `timeout-minutes` 控制）。

## 常见问题

**Q：step 的 env 和 job 的 env 有什么区别？**

A：job 的 `env` 对该 job 内所有 step 可见；step 的 `env` 仅在该 step 内生效。同名的 step 级变量会覆盖 job 级变量。

**Q：run 命令中如何引用上下文变量？**

A：在 YAML 中使用 `${{ }}` 表达式引用，如 `${{ atomgit.sha }}`；在 shell 命令中直接使用环境变量，如 `$ATOMGIT_SHA`。
