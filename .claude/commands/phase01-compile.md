---
description: 由文本用例重新编译可执行 YAML（GitCode 规范变更 / 差异澄清时用）
---

仅**重新编译**某 run 的可执行 YAML——文本用例（source of truth）基本不动。用于 GitCode 规范调整、或那「少量不一致」被澄清后，刷新交接给第二部分的 YAML。

## 参数
`$ARGUMENTS`：`<run-id> [ID或维度]`，可选限定重编译范围；空=该 run 全部文本用例。

## 执行
1. 定位 `phase01/runs/<run-id>/cases/text/`。
2. 用 Task 拉起 **case-writer**（读 `phase01/agents/case-writer/CLAUDE.md`），指令：**只做编译，不改文本用例**——依据当前 `phase01/inputs/gitcode-spec/` 规范，把文本用例重新编译为 `cases/yaml/<ID>.yaml`。
3. 每条 YAML 过 `phase01/schema/executable-case.schema.yaml` 校验。
4. 在 `run.md` 时间线追加：本次重编译的触发原因（规范变更点）、影响的用例 ID、schema 校验结果。
5. 若某文本用例因规范变更已不适用，**不擅自改文本用例**——列出来提示用户，建议走 `/phase01-update` 修订意图/文本。

## 纪律
- 只动 `cases/yaml/`，不动 `cases/text/`（保持文本层稳定）。
- 校验失败的 YAML 必须列出并说明原因，不静默交付。

---

## YAML 校验常见问题及修复

### 1. Step name 包含非法字符

`name` 字段仅允许：中文、A-Z a-z 0-9、`-` `_` `,` `;` `:` `.` `/` `(` `)` `（` `）` 及空格；长度1-128；不能为空。

**非法字符**：`[` `]` `|` `!` `>` `&` `#` `?` `*` `=` `<` `'` `"`

**修复方式**：将 `[TC-xxx]` 替换为 `(TC-xxx)`，删除其余非法字符。

### 2. Bare `- uses:` steps 缺少 `name:`

`steps` 中的每一项必须包含 `run` 或 `uses`，且不可同时存在。但每个 step 也必须有 `name`。

**修复方式**：在裸 `- uses: checkout` 前加一行 `- name: (TC-000) checkout source`，并将 `uses: checkout` 缩进对齐作为同一步的二级属性：

```yaml
# 错误
- name: (TC-000) checkout source
- uses: checkout

# 正确
- name: (TC-000) checkout source
  uses: checkout
```

### 3. `if:` 表达式必须使用 `${{ }}`

`if:` 中的表达式必须使用 `${{ expr }}` 而非 `$${ expr }`。注意 `run:` 块内的 `$${ }` 是合法的 shell 转义语法，**不要**修改。

### 4. Job steps 数量限制

每个 job 的 steps 数不能超过 16 条。超过时必须拆分：
- 按 ≤16 个 step 一组拆分
- 新 job 命名：原 job 名加 `-b`、`-c`、`-d` 后缀
- 新 job 保留原 job 的 `runs-on`、`env`、`strategy` 等全部属性

### 5. `on.push` 不能同时存在 `paths` 和 `paths-ignore`

若同时存在，保留 `paths`，删除 `paths-ignore` 及其列表项。

### 6. 文件再生后需重新应用所有修复

当使用 `gen_yamls_v4.py` 重新生成 YAML 文件后，上述所有修复需要重新应用。建议一次性完成所有修复，不要分批执行，以免中间状态导致文件内容异常。

注意：`gen_yamls_v4.py` 中的 `ES()` 函数已修复为生成 `${{ }}` 而非 `$${ }`，且 `always` 已改为 `always()`。若使用旧版生成器，需先更新该函数。

### 7. PowerShell 脚本注意事项

- 修改 YAML 文件时，使用 `[System.IO.File]::ReadAllText/ReadAllLines` 和 `WriteAllLines` 操作 UTF-8 文件
- `-replace` 的 pattern 参数中，若包含 `?` 等正则元字符，需使用 `[regex]::Escape()`
- 字符串中的 `${i}:` 会被 PowerShell 解释为 drive 变量引用，应改用 `${i}:` 或避免该模式
- 单引号字符串中的 `$` 是字面量，双引号字符串中的 `$` 会被展开
- 不要在 `for` 循环的 `Write-Host` 中使用 `"$i: $($lines[$i])"`，应使用 `"${i}: $($lines[$i])"`

### 8. `defaults.run` 下不能包含 `name`

`defaults.run` 仅支持 `shell:` 和 `working-directory:` 两个属性。若自动修复脚本错误地在 `defaults.run` 下插入了 `name:`，会导致 `defaults.run.name: unknown property` 错误。

**修复方式**：检查 `defaults:` → `run:` 区域，删除其中的 `name:` 行。

### 9. `if:` 中的裸关键字（不含 `${{ }}`）

某些 `if:` 表达式可能写成裸关键字（如 `if: always`）而非合法格式 `if: ${{ always() }}`。平台校验会报 `if表达式无法解析`。

需要包裹的常见裸关键字：
- `always` → `${{ always() }}`（注意 `always` 需写作函数调用 `always()`，否则平台报"不支持的关键字"）
- `success()` → `${{ success() }}`
- `failure()` → `${{ failure() }}`
- `cancelled()` → `${{ cancelled() }}`

**修复方式**：将 `if: always` 等替换为 `if: ${{ always() }}`，跳过已含 `${{ }}` 的行。

### 10. 自动修复脚本的注意事项

- **`name:` 插入脚本需跳过 `defaults:` 区域**：在 `jobs:` 之前出现的 2-space indent key（如 `on:` 中的 trigger、`defaults.run` 等）不应被添加 `name:` 行。
- **脚本执行顺序**：建议按以下顺序执行修复：
  1. 清理 step name 非法字符
  2. 修复 bare `- uses:` 添加 `name:`
  3. 修复 `if:` 表达式（包含裸关键字和 `$${}`）
  4. 添加 job `name:`（需排除 `defaults:`/`on:` 等区域）
  5. 拆分超过 16 steps 的 job
- **验证**：每次修改后运行 `final_check_all.py` 确认无残留问题。

### 11. `vars` 上下文不被 GitCode 支持

GitCode 平台不支持 `vars` 上下文（`vars.XXX`），引用 `vars` 会导致 `不支持的关键字` 错误。

**修复方式**：删除引用 `vars` 的 `if:` 条件，或改用 `atomgit` 上下文。

### 12. `workflow_call.inputs` key 命名规则

`workflow_call.inputs` 下的 key 仅允许：大小写英文字母、数字、`_`（下划线），不支持连字符。同理 `workflow_call.secrets` 下的 key 也适用此规则。

**非法**：`config-path`、`deploy-token`
**合法**：`config_path`、`deploy_token`

### 13. `merge_requests` 也适用 paths/paths-ignore 互斥规则

`on.push` 的 `paths` 和 `paths-ignore` 互斥规则同样适用于 `merge_requests`（原 `pull_request`）。两者同时存在时，保留 `paths`，删除 `paths-ignore`。

### 14. `permissions` 范围列表

GitCode 支持的 `permissions` 范围：
- `repository`、`pr`、`issue`、`note`、`project`

不支持：`hook`、`actions`、`checks`、`contents`、`deployments`、`packages` 等 GitHub Actions 中的范围。

### 15. `post` 不作为顶层 workflow 属性

GitCode 不支持顶层 `post:` 属性块（含 `run_always` 和 `steps`）。`post` 是岗位生命周期概念，仅通过 job 内的步骤实现。

**修复方式**：删除整个顶层 `post:` 块。

### 16. `runs-on` 的 YAML 格式选择

- 静态标签用 flow sequence：`runs-on: [ubuntu-latest, x64, small]`
- 含 `${{ }}` 表达式时**必须**用单引号包裹 + flow sequence，避免 curly braces 与 flow sequence 冲突：
  ```yaml
  # ❌ 错误 - 花括号被解释为 flow mapping
  runs-on: [${{ matrix.os }}]

  # ❌ 错误 - 表达式作为裸值
  runs-on:
    - ${{ matrix.os }}

  # ✅ 正确 - 单引号包裹，花括号变为字面量
  runs-on: ['${{ matrix.os }}']
  ```

注意：即使 YAML 语法正确，GitCode 平台也**不支持**在 `runs-on` 中使用 `${{ }}` 表达式。表达式不会被解析，建议始终使用硬编码的 flow sequence 数组。

### 17. `env` key 命名规则

job/step 的 `env` 下 key 仅允许：大小写英文字母、数字、`_`（下划线），不支持连字符。

**非法**：`timeout-minutes`、`continue-on-error`
**合法**：`timeout_minutes`、`continue_on_error`

### 18. `runs-on` 单字符串限制

当 `runs-on` 以单个字符串（非数组）定义时，值必须为以下三者之一：`default`、`ubuntu-latest`、`euler-latest`。不能使用 `${{ matrix.os }}` 等表达式作为单字符串值。

**修复方式**：使用 flow sequence 数组 `runs-on: [ubuntu-latest, x64, small]`。注意 GitCode 平台**不支持**在 `runs-on` 中使用 `${{ }}` 表达式（无论是否引用包裹），表达式不会被执行解析。

### 19. 汇总：完整的步骤顺序检查清单

生成/修复 YAML 后，逐一检查：

| # | 检查项 | 触发词 |
|---|--------|--------|
| 1 | Step name 非法字符 | `[` `]` `\|` `!` `>` `&` `#` `?` `*` `=` `<` `'` `"` |
| 2 | Bare `uses:` 缺少 `name:` | `- uses:` 前无 `- name:` |
| 3 | `if:` 使用 `$${ }` 而非 `${{ }}` | `$${` |
| 4 | `if:` 表达式缺少 `${{ }}` | 裸 `always` / `success()` 等 |
| 5 | `if:` 中 `always` 写为 `always()` | `${{ always }}` |
| 6 | `vars` 上下文 | `vars.` |
| 7 | Job steps > 16 | 计数 |
| 8 | `paths` + `paths-ignore` 共存 (push/merge_requests) | `paths-ignore` |
| 9 | `workflow_call.inputs` key 含连字符 | `-` in input key |
| 10 | `permissions` 含不支持的范围 | `hook` 等 |
| 11 | 顶层 `post:` 块 | `post:` at indent 0 |
| 12 | `runs-on` 含 `${{ }}` 用了 flow sequence | `[${{` |
| 13 | `env` key 含连字符 | `-` in env key |
| 14 | `runs-on` 单字符串非白名单值 | `runs-on: ${{` |
