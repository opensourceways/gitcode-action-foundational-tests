<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/using-script-commands | fetched: 2026-07-20 -->

# 使用脚本命令

**适用场景**：当你需要在 step 中通过 `run` 执行 shell 命令、调用仓库内脚本、设置环境变量或写入输出参数时。

## 前提条件

* 已配置 `runs-on` 并了解 Runner 的预装工具。
* 如果执行仓库内脚本，需要先 checkout 代码。

## 快速示例

```yaml
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - uses: checkout
      - name: Run build script
        run: bash ./scripts/build.sh
```

## 配置说明

### 执行仓库内脚本

执行仓库中已有的脚本文件：

```yaml
steps:
  - uses: checkout
  - name: Run build script
    run: bash ./scripts/build.sh
```

> **注意**：脚本文件可能没有执行权限，建议使用 `bash script.sh` 或先 `chmod +x script.sh`。

### 设置执行权限

```yaml
steps:
  - uses: checkout
  - run: chmod +x ./scripts/build.sh
  - run: ./scripts/build.sh
```

### 写入 step 输出

使用 `ATOMGIT_OUTPUT` 环境变量写入 step 输出参数：

```yaml
steps:
  - id: version
    run: echo "version=1.0.0" >> "$ATOMGIT_OUTPUT"
  - name: Use output
    run: echo "${{ steps.version.outputs.version }}"
```

### 设置环境变量

使用 `ATOMGIT_ENV` 环境变量在 step 中设置后续 step 可见的环境变量：

```yaml
steps:
  - name: Set env
    run: echo "APP_VERSION=1.0.0" >> "$ATOMGIT_ENV"
  - name: Use env
    run: echo "version=$APP_VERSION"
```

### 添加 PATH

使用 `ATOMGIT_PATH` 向系统 PATH 添加路径：

```yaml
steps:
  - name: Add custom tool to PATH
    run: echo "/opt/custom-tools" >> "$ATOMGIT_PATH"
  - name: Use custom tool
    run: custom-tool --version
```

### 脱敏命令

使用 `::add-mask::` 对日志中的敏感信息进行掩藏：

```yaml
steps:
  - name: Mask secret
    run: |
      echo "::add-mask::$MY_SECRET"
      echo "The secret value is $MY_SECRET"
```

日志中 `$MY_SECRET` 的值将被显示为 `***`。

### 多行输出

写入多行值到输出或环境变量时，使用分隔符：

```yaml
steps:
  - id: multiline
    run: |
      EOF=$(dd if=/dev/urandom bs=15 count=1 status=none | base64)
      echo "content<<$EOF" >> "$ATOMGIT_OUTPUT"
      echo "line1" >> "$ATOMGIT_OUTPUT"
      echo "line2" >> "$ATOMGIT_OUTPUT"
      echo "$EOF" >> "$ATOMGIT_OUTPUT"
```
