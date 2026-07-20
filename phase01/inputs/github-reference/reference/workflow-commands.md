<!-- source: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands | fetched: 2026-07-20 -->

# Workflow commands for GitHub Actions

You can use workflow commands when running shell commands in a workflow or in an action's code.

## About workflow commands

Actions can communicate with the runner machine to set environment variables, output values used by other actions, add debug messages to the output logs, and other tasks.

Most workflow commands use the `echo` command in a specific format, while others are invoked by writing to a file.

### Example of a workflow command

**bash:**
```bash
echo "::workflow-command parameter1={data},parameter2={data}::{command value}"
```

> **NOTE:** Workflow command and parameter names are case insensitive.

## Using workflow commands to access toolkit functions

The [actions/toolkit](https://github.com/actions/toolkit) includes functions that can be executed as workflow commands. Use the `::` syntax to run the workflow commands within your YAML file; these commands are then sent to the runner over `stdout`.

| Toolkit function | Equivalent workflow command |
| ---------------- | --------------------------- |
| `core.addPath` | Accessible using environment file `GITHUB_PATH` |
| `core.debug` | `debug` |
| `core.notice` | `notice` |
| `core.error` | `error` |
| `core.endGroup` | `endgroup` |
| `core.exportVariable` | Accessible using environment file `GITHUB_ENV` |
| `core.getInput` | Accessible using environment variable `INPUT_{NAME}` |
| `core.getState` | Accessible using environment variable `STATE_{NAME}` |
| `core.isDebug` | Accessible using environment variable `RUNNER_DEBUG` |
| `core.summary` | Accessible using environment file `GITHUB_STEP_SUMMARY` |
| `core.saveState` | Accessible using environment file `GITHUB_STATE` |
| `core.setCommandEcho` | `echo` |
| `core.setFailed` | Used as a shortcut for `::error` and `exit 1` |
| `core.setOutput` | Accessible using environment file `GITHUB_OUTPUT` |
| `core.setSecret` | `add-mask` |
| `core.startGroup` | `group` |
| `core.warning` | `warning` |

## Setting messages

- **Debug**: `::debug::{message}` — must create secret `ACTIONS_STEP_DEBUG=true` to see debug messages.
- **Notice**: `::notice file={name},line={line},endLine={endLine},title={title}::{message}` — creates an annotation.
- **Warning**: `::warning file={name},line={line},endLine={endLine},title={title}::{message}` — creates a warning annotation.
- **Error**: `::error file={name},line={line},endLine={endLine},title={title}::{message}` — creates an error annotation.

## Grouping log lines

```text
::group::{title}
::endgroup::
```

## Masking a value in a log

```text
::add-mask::{value}
```

Masking a value prevents a string or variable from being printed in the log. Each masked word separated by whitespace is replaced with the `*` character. When you mask a value, it is treated as a secret and will be redacted on the runner. For example, after you mask a value, you won't be able to set that value as an output.

> **WARNING:** Make sure you register the secret with 'add-mask' before outputting it in the build logs or using it in any other workflow commands.

Masks are not passed between jobs.

## Stopping and starting workflow commands

```text
::stop-commands::{endtoken}
```

To stop the processing of workflow commands, pass a unique token to `stop-commands`. To resume processing workflow commands, pass the same token.

> **WARNING:** Make sure the token you're using is randomly generated and unique for each run.

```text
::{endtoken}::
```

## Sending values to the pre and post actions

You can create environment variables for sharing with your workflow's `pre:` or `post:` actions by writing to the file located at `GITHUB_STATE`.

## Environment files

During the execution of a workflow, the runner generates temporary files that can be used to perform certain actions. The path to these files can be accessed and edited using GitHub's default environment variables. You will need to use UTF-8 encoding when writing to these files.

### Setting an environment variable (`GITHUB_ENV`)

**bash:** `echo "{environment_variable_name}={value}" >> "$GITHUB_ENV"`

The step that creates or updates the environment variable does not have access to the new value, but all subsequent steps in a job will have access.

You can't overwrite the value of the default environment variables named `GITHUB_*` and `RUNNER_*`.

Multiline strings use a delimiter:

```text
{name}<<{delimiter}
{value}
{delimiter}
```

### Setting an output parameter (`GITHUB_OUTPUT`)

**bash:** `echo "{name}={value}" >> "$GITHUB_OUTPUT"`

Sets a step's output parameter. Note that the step will need an `id` to be defined to later retrieve the output value.

```yaml
      - name: Set color
        id: color-selector
        run: echo "SELECTED_COLOR=green" >> "$GITHUB_OUTPUT"
      - name: Get color
        env:
          SELECTED_COLOR: ${{ steps.color-selector.outputs.SELECTED_COLOR }}
        run: echo "The selected color is $SELECTED_COLOR"
```

### Adding a job summary (`GITHUB_STEP_SUMMARY`)

**bash:** `echo "{markdown content}" >> $GITHUB_STEP_SUMMARY`

Job summaries support GitHub flavored Markdown. `GITHUB_STEP_SUMMARY` is unique for each step in a job. When a job finishes, the summaries for all steps in a job are grouped together into a single job summary and are shown on the workflow run summary page.

### Adding a system path (`GITHUB_PATH`)

**bash:** `echo "$HOME/.local/bin" >> "$GITHUB_PATH"`

Prepends a directory to the system `PATH` variable and automatically makes it available to all subsequent actions in the current job; the currently running action cannot access the updated path variable.

---

> **关键差异提示（compat-diff）**: GitHub 环境文件变量为 `GITHUB_ENV`/`GITHUB_OUTPUT`/`GITHUB_PATH`/`GITHUB_STEP_SUMMARY`/`GITHUB_STATE`；GitCode 为 `ATOMGIT_ENV`/`ATOMGIT_OUTPUT`/`ATOMGIT_PATH`/`ATOMGIT_STEP_SUMMARY`。GitCode 明确废弃 `::set-output`/`::set-env`/`::add-path`（与 GitHub 演进一致）。`::add-mask::` 两边语义一致但需验证 GitCode 侧隔离强度。
