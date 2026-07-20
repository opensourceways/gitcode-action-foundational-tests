<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/configure-conditional-execution | fetched: 2026-07-20 -->

# 配置条件执行

**适用场景**：当你需要根据分支、Tag、事件类型、前置步骤状态等条件控制 job 或 step 是否执行时。

## 前提条件

*   理解 `atomgit` 上下文。
*   理解表达式语法 `${{ }}`。

## 快速示例

```yaml
name: conditional-workflow
on:
  push:
    branches:
      - main
      - develop
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - uses: checkout
      - name: Run only on main
        if: ${{ atomgit.ref == 'refs/heads/main' }}
        run: echo "main branch"
      - name: Run always
        if: ${{ always }}
        run: echo "always runs"
  deploy:
    if: ${{ atomgit.ref == 'refs/heads/main' }}
    runs-on: [ubuntu-latest, x64, small]
    needs: build
    steps:
      - run: echo "deploy to production"
```

## 配置说明

### if 表达式

`if` 条件使用 `${{ }}` 表达式语法：

```yaml
# job 级 if
jobs:
  deploy:
    if: ${{ atomgit.ref == 'refs/heads/main' }}
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - run: echo "deploy"

# step 级 if
steps:
  - name: Run on main
    if: ${{ atomgit.ref == 'refs/heads/main' }}
    run: echo "main branch"
```

### 状态函数

状态函数用于判断前置步骤或 job 的执行状态：

| 函数 | 含义 | 返回 true 的条件 |
|------|------|-----------------|
| `success` | 所有前置步骤成功 | 前置步骤全部成功（默认行为） |
| `failed` | 有前置步骤失败 | 至少一个前置步骤失败 |
| `cancelled` | workflow 被取消 | workflow 被取消 |
| `always` | 无论什么状态 | 任何状态都返回 true |

使用示例：

```yaml
steps:
  - name: Build
    run: ./build.sh
  - name: Notify on success
    if: ${{ success }}
    run: echo "build succeeded"
  - name: Notify on failure
    if: ${{ failed }}
    run: echo "build failed"
  - name: Cleanup
    if: ${{ always }}
    run: ./cleanup.sh
```

> **重要**：`if: ${{ always }}` 会强制 step 执行，即使前置步骤失败或 workflow 被取消。适合用于清理资源、发送通知等场景。

### 条件表达式运算符

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `==` | 等于 | `${{ atomgit.ref == 'refs/heads/main' }}` |
| `!=` | 不等于 | `${{ atomgit.event_name != 'schedule' }}` |
| `>` / `>=` / `<` / `<=` | 比较 | `${{ inputs.count > 10 }}` |
| `!` | 逻辑非 | `${{ !cancelled }}` |
| `&&` | 逻辑与 | `${{ success && atomgit.ref == 'refs/heads/main' }}` |
| `\|\|` | 逻辑或 | `${{ failed \|\| cancelled }}` |

### 字符串函数

| 函数 | 说明 | 示例 |
|------|------|------|
| `contains(str, substr)` | 包含子串 | `${{ contains(atomgit.ref, 'main') }}` |
| `startsWith(str, prefix)` | 以前缀开头 | `${{ startsWith(atomgit.ref, 'refs/tags/') }}` |
| `endsWith(str, suffix)` | 以后缀结尾 | `${{ endsWith(atomgit.ref, '.0') }}` |
| `format(template, ...)` | 格式化 | `${{ format('Hello {0}', atomgit.actor) }}` |
