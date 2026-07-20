<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/action-development/runtime-environment-variables | fetched: 2026-07-20 -->

# 运行时环境变量

## 流水线系统变量

当前支持如下内置的公共环境变量，可以直接引用，无需定义。

| 系统变量 | AtomGit定义 |
|---------|-----------|
| CI | 始终设置为 true。 |
| ATOMGIT_ACTION | 当前正在运行的操作名称。通常为 actions 名称。若在同一任务中多次使用相同脚本或操作，名称将包含下划线加序号后缀（如 actionscheckout、actionscheckout_2）。 |
| ATOMGIT_ACTION_PATH | Action 所在路径。复合操作指向包含 action.yml 的目录；Docker 容器操作指向容器内 Action 文件目录。与 ATOMGIT_WORKSPACE（代码检出根目录）不同。 |
| ATOMGIT_ACTION_REPOSITORY | 对于执行 action 的步骤，为 action 的所有者和存储库名称（如 actions/checkout）。 |
| ATOMGIT_ACTIONS | 运行工作流时默认设置为 true。可用于区分本地运行还是 AtomGit Actions 运行。 |
| ATOMGIT_ACTOR | 启动工作流的人员或应用程序名称 |
| ATOMGIT_ACTOR_ID | 触发初始工作流运行的用户或应用程序的账户ID（与用户名不同）。 |
| ATOMGIT_API_URL | 返回 API 网址。 |
| ATOMGIT_BASE_REF | 拉取请求的基准/目标分支名称。仅当事件为 `pull_request/merge_request` 或 `pull_request_target/merge_request_target` 时设置。 |
| ATOMGIT_ENV | 指向设置工作流命令变量的文件路径。当前步骤唯一，每个步骤会变化。 |
| ATOMGIT_EVENT_NAME | 触发工作流的事件名称（如 workflow_dispatch）。 |
| ATOMGIT_HEAD_REF | 拉取请求的头部/源分支。仅当事件为 `pull_request` 或 `pull_request_target` 时设置。 |
| ATOMGIT_JOB | 当前工作的 job_id（如 greeting_job）。 |
| ATOMGIT_OUTPUT | 指向设置当前步骤输出的文件路径。当前步骤唯一，每个步骤会变化。 |
| ATOMGIT_PATH | 指向设置系统路径变量的文件路径。当前步骤唯一，每个步骤会变化。 |
| ATOMGIT_REF | 触发工作流的分支或标签完整引用。push 为被推送 ref；未合并 pull_request 为合并分支；已合并为 head 分支。分支格式 `refs/heads/<分支名>`；未合并 PR（非 pull_request_target）为 `refs/pull/<pr_number>/merge`；pull_request_target 引用基准分支；标签为 `refs/tags/<tag_name>`。 |
| ATOMGIT_REF_NAME | 触发工作流的分支或标签简短名称。未合并 PR 格式为 `<pr_number>/merge`。 |
| ATOMGIT_REF_PROTECTED | 若为触发 ref 配置了分支保护或规则集，则为真。 |
| ATOMGIT_REF_TYPE | 引用类型，有效值为 branch 或 tag。 |
| ATOMGIT_REPOSITORY | 所有者和存储库名称（如 octocat/Hello-World）。 |
| ATOMGIT_REPOSITORY_ID | 存储库 ID（与名称不同）。 |
| ATOMGIT_REPOSITORY_OWNER | 仓库所有者名称（如 octocat）。 |
| ATOMGIT_REPOSITORY_OWNER_ID | 仓库所有者账户 ID（与姓名不同）。 |
| ATOMGIT_RETENTION_DAYS | 工作流运行日志和工件的保留天数（如 90）。 |
| ATOMGIT_RUN_ATTEMPT | 每次尝试的唯一编号，从 1 开始，每次重新运行递增。 |
| ATOMGIT_RUN_ID | 每个工作流运行的唯一编号，重新运行不变。 |
| ATOMGIT_RUN_NUMBER | 特定工作流每次运行的唯一编号，从 1 开始递增，重新运行不变。 |
| ATOMGIT_SERVER_URL | AtomGit 服务器 URL。 |
| ATOMGIT_SHA | 触发工作流的提交 SHA（具体值取决于事件类型）。 |
| ATOMGIT_STEP_SUMMARY | 指向包含任务摘要的文件路径。当前步骤唯一，每个步骤会变化。 |
| ATOMGIT_TRIGGERING_ACTOR | 发起工作流运行的用户名。重新运行时可能与 ATOMGIT_ACTOR 不同；重新运行使用 ATOMGIT_ACTOR 的权限。 |
| ATOMGIT_WORKFLOW | 工作流名称。若未指定名称，则为工作流文件完整路径。 |
| ATOMGIT_WORKFLOW_ID | 工作流唯一标识 ID |
| ATOMGIT_WORKFLOW_REF | 工作流引用路径。格式 `{owner}/{repo}/.gitcode/workflows/{filename}@{ref}`。 |
| ATOMGIT_WORKFLOW_SHA | 工作流文件的提交 SHA 值。 |
| ATOMGIT_WORKSPACE | 运行器上步骤的默认工作目录。 |
| RUNNER_ARCH | 运行器架构，可能值 X86、X64、ARM、ARM64。 |
| RUNNER_ENVIRONMENT | 运行器环境，可能值 gitcode-hosted（公共资源池）、self-hosted（自托管）。 |
| RUNNER_NAME | 执行任务的运行器名称（可能不唯一）。 |
| RUNNER_OS | 运行器操作系统，可能值 Linux、Windows、macOS。 |
| RUNNER_TEMP | 运行器临时目录路径，每个任务开始和结束时清空。 |
| RUNNER_TOOL_CACHE | 包含预装工具的目录路径。 |

---

## 上下文

### 可用上下文

| 上下文名称 | 类型 | 描述 |
|---------|------|------|
| atomgit | object | 关于工作流运行的信息。 |
| env | object | 包含在工作流、任务或步骤中设置的变量。 |
| vars | object | 包含在仓库、组织或环境级别设置的变量。 |
| job | object | 关于当前正在运行的任务的信息。 |
| jobs | object | 仅对于可重用工作流，包含来自可重用工作流的任务输出。 |
| steps | object | 关于当前任务中已运行的步骤的信息。 |
| runner | object | 关于正在运行当前任务的运行器的信息。 |
| secrets | object | 包含可用的工作流运行的密钥的名称和值。 |
| strategy | object | 关于当前任务的矩阵执行策略的信息。 |
| matrix | object | 包含在工作流中定义的、适用于当前任务的矩阵属性。 |
| inputs | object | 包含传递给操作、可重用工作流或手动触发工作流的输入属性。 |

如果引用不存在的属性，将计算为空字符串。

### 示例

```yaml
name: CI
on: push
jobs:
  prod-check:
    if: ${{ atomgit.ref == 'refs/heads/main' }}
    runs-on: default
    steps:
      - run: echo "Deploying to production server on branch $ATOMGIT_REF"
```

if 检查由 AtomGit Pipeline 处理，只有结果为 true 时任务才被发送到执行环境。

---

## 运行时过程文件说明

AtomGit Runner 运行流水线时会生成一组临时过程文件，并通过环境变量暴露路径给当前 step 或 action。`ATOMGIT_ENV`、`ATOMGIT_OUTPUT`、`ATOMGIT_PATH`、`ATOMGIT_STEP_SUMMARY` 的路径通常"当前 step 唯一"，不同 step 路径会变化；写入后一般从后续 step 或 runner 汇总阶段生效。

### 1. 全量过程文件总表

| 系统变量 | 文件类型 | 主要用途 | 生效范围 | 典型写入格式 |
|---------|---------|---------|---------|-------------|
| `ATOMGIT_ENV` | 环境变量文件 | 设置后续 step 可读取的环境变量 | 当前 job 的后续 step | `echo "NAME=value" >> "$ATOMGIT_ENV"` |
| `ATOMGIT_OUTPUT` | Step 输出文件 | 设置当前 step 的 output | 当前 step 输出，`steps.<id>.outputs` 引用 | `echo "name=value" >> "$ATOMGIT_OUTPUT"` |
| `ATOMGIT_PATH` | PATH 追加文件 | 将目录追加到系统 PATH | 当前 job 的后续 step/action | `echo "/path/to/bin" >> "$ATOMGIT_PATH"` |
| `ATOMGIT_STEP_SUMMARY` | Step/Job 摘要文件 | 生成 Markdown Job Summary | 当前 step 写入，job 结束后汇总 | `echo "### Summary" >> "$ATOMGIT_STEP_SUMMARY"` |

### 2. ATOMGIT_ENV：设置后续步骤环境变量

当前 step 写入后，当前 step 自身不能读取新值，后续 step 可读取。不建议覆盖 `ATOMGIT_*`、`RUNNER_*` 等系统变量（可能不生效或行为不可预期）。

```yaml
steps:
  - name: Generate build version
    run: |
      VERSION="1.0.${ATOMGIT_RUN_NUMBER}"
      echo "BUILD_VERSION=$VERSION" >> "$ATOMGIT_ENV"
  - name: Use build version
    run: echo "Current build version is $BUILD_VERSION"
```

多行环境变量使用 delimiter 语法：

```yaml
steps:
  - name: Set multiline env
    run: |
      {
        echo 'CHANGELOG<<EOF'
        echo '- add login feature'
        echo '- fix build script'
        echo EOF
      } >> "$ATOMGIT_ENV"
```

### 3. ATOMGIT_OUTPUT：设置 step 输出

设置输出的 step 必须配置 `id`，否则后续 step 无法通过 `steps.<id>.outputs` 引用。

```yaml
steps:
  - name: Generate image tag
    id: meta
    run: |
      IMAGE_TAG="app-${ATOMGIT_SHA::7}"
      echo "image_tag=$IMAGE_TAG" >> "$ATOMGIT_OUTPUT"
  - name: Use image tag
    run: echo "Image tag is ${{ steps.meta.outputs.image_tag }}"
```

job 之间传递输出：先设 step output，再通过 `jobs.<job_id>.outputs` 映射为 job output，下游 job 用 `needs.<job_id>.outputs.<name>` 获取。

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.meta.outputs.image_tag }}
    steps:
      - id: meta
        run: echo "image_tag=app-${ATOMGIT_SHA}" >> "$ATOMGIT_OUTPUT"
  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - run: echo "Deploy image tag: ${{ needs.build.outputs.image_tag }}"
```

### 4. ATOMGIT_PATH：向 PATH 追加命令目录

写入后当前 step 不能立即访问更新后的 PATH，后续 step 才能访问。

```yaml
steps:
  - name: Install custom cli
    run: |
      mkdir -p "$HOME/.local/bin"
      cat > "$HOME/.local/bin/hello-cli" <<'EOF'
      #!/usr/bin/env bash
      echo "hello from custom cli"
      EOF
      chmod +x "$HOME/.local/bin/hello-cli"
      echo "$HOME/.local/bin" >> "$ATOMGIT_PATH"
  - name: Use custom cli
    run: hello-cli
```

### 5. ATOMGIT_STEP_SUMMARY：生成 Job Summary

`>>` 追加，`>` 覆盖当前 step 已写入内容；删除 `ATOMGIT_STEP_SUMMARY` 指向的文件可清空当前 step summary。Step 完成后 summary 上传，后续 step 不能修改已上传的 summary。

```yaml
steps:
  - name: Generate test summary
    run: |
      echo "## Test Summary" >> "$ATOMGIT_STEP_SUMMARY"
      echo "| Metric | Value |" >> "$ATOMGIT_STEP_SUMMARY"
      echo "|---|---:|" >> "$ATOMGIT_STEP_SUMMARY"
      echo "| Total | 128 |" >> "$ATOMGIT_STEP_SUMMARY"
      echo "| Passed | 126 |" >> "$ATOMGIT_STEP_SUMMARY"
      echo "| Failed | 2 |" >> "$ATOMGIT_STEP_SUMMARY"
```

### 7. 常见注意事项

- **7.1** 当前 step 写入 `ATOMGIT_ENV`/`ATOMGIT_PATH`，通常后续 step 才生效——把"写入"和"使用"拆成两个 step。
- **7.2** 必须追加到文件（`>>`），只 `echo` 不重定向只会打印日志，不被解析为环境文件命令。
- **7.3** 多行内容用 delimiter；内容可能含独立 `EOF` 行时换更随机的 delimiter 或写普通文件传路径。
- **7.4** 不要覆盖平台默认变量（`ATOMGIT_*`/`RUNNER_*`）。
- **7.5** 不要把敏感信息写入 summary 或日志——summary 比日志更易被看到；不要依赖脱敏机制作为安全边界。
