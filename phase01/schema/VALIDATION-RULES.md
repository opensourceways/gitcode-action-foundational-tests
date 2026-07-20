# Case Writer 编译校验规则

> case-writer agent 生成 YAML 时必须逐条遵守。本文件整合了 schema 校验 + GitCode 平台实测验证规则（来源：demo 仓库 `AGENTS.md`）。
> 遵守此规则可一次通过 `/phase02-schema-check` 和平台 YAML 校验。

---

## 1. Runner 标签格式 ★ [平台实测]

**只用数组格式，禁止 `{}` 对象格式。**

```yaml
# ✅ 正确 — 数组格式（demo 仓库实测可用）
runs-on: [ubuntu-latest, x64, small]
runs-on: [self-hosted, arch=arm]
runs-on: ['codearts-hosted', 'ubuntu-latest', 'x64', 'large']

# ❌ 错误 — 对象格式被平台拒绝
runs-on: {ubuntu-24, x64, small}       # unknown property
runs-on: default                        # 不明确的标签
```

**匹配逻辑**：`runs-on` 中列出的所有标签必须同时存在于 Runner 的标签集合中。

---

## 2. Job name 必填 ★ [平台实测]

每个 job 必须显式声明 `name`，平台报 `jobs[id].name: The value cannot be empty`。

```yaml
# ✅ 正确
jobs:
  hello:
    name: Print hello message       # ← 必填
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - name: Say hello
        run: echo "hello"

# ❌ 错误
jobs:
  hello:
    runs-on: [ubuntu-latest, x64, small]   # 缺 name
```

---

## 3. Step name 必填 + 非法字符清理 ★ [平台实测]

### 3a. 每个 step 必须有 `name`

包括 bare `uses:` step：

```yaml
# ❌ 错误
- uses: checkout

# ✅ 正确
- name: (TC) checkout source
  uses: checkout
```

### 3b. Step name 仅允许以下字符 [平台校验]

允许：中文、A-Z a-z 0-9、`-` `_` `,` `;` `:` `.` `/` `(` `)` `（` `）` 及空格；长度 1-128。

**禁止**：`[` `]` `|` `!` `>` `&` `#` `?` `*` `=` `<` `'` `"` `@` `$` `{` `}` `+`

```yaml
# ❌ 含 [ ] — 替换为 ( )
- name: "[TC-001] env(workflow级)"

# ✅
- name: "(TC-001) env workflow 级"
```

### 3c. `defaults.run` 下不能包含 `name`

`defaults.run` 仅支持 `shell:` 和 `working-directory:`。

---

## 4. `if:` 表达式必须使用 `${{ }}` [平台实测]

```yaml
# ❌ 裸关键字
if: always

# ✅ 函数调用格式
if: ${{ always() }}
```

常见转换：
- `always` → `${{ always() }}`
- `success()` → `${{ success() }}`
- `failure()` → `${{ failure() }}`
- `cancelled()` → `${{ cancelled() }}`

---

## 5. Job steps 数量限制 ≤ 16 [平台限制]

超出 16 个 step 必须拆分 job（加 `-b`、`-c` 后缀）。

---

## 6. `on.push` 不能同时有 `paths` 和 `paths-ignore` [平台限制]

若同时存在，保留 `paths`，删除 `paths-ignore`。

---

## 7. `vars` 上下文不支持 [平台限制]

GitCode 平台不支持 `vars.*` 上下文。引用 `vars` 的用例标注 SKIP 或改用 `atomgit.*`。

---

## 8. YAML 写入注意事项 ★

### 8a. `on:` 关键字保护

YAML 1.1 将 `on` 解析为 boolean `true`。写入 workflow YAML 时必须使用 block scalar `|` 格式，**禁止**用 `yaml.dump()` 重新序列化 workflow 字段。

```yaml
# ✅ 正确 — workflow 使用 block scalar
workflow: |
  on:
  - push
  jobs:
    ...

# ❌ 错误 — 会被 yaml.dump 转为 true: 
workflow: "on:\n- push\n..."
```

### 8b. 标题引号

标题含 `:` `{` `}` `[` `]` `$` `#` `&` `*` `!` `|` `>` `%` `@` `` ` `` 时必须双引号包裹。

---

## 9. 标题（title）引号规则

### 10. ID 格式规则

```
<维度前缀>-<主题>-\d{2}-\d{3}(-V\d+)?
```

- 维度前缀：`COMP` | `COMPAT` | `REL` | `SEC` | `USE`
- 主题：`[A-Z0-9]+(?:-[A-Z0-9]+)*`
- run 序列：2 位数字，序号：3 位数字

### 11. 触发事件枚举

`push | pr | pull_request | fork_pr | pull_request_target | pull_request_comment | manual | schedule | tag | workflow_dispatch | issue_comment`

### 12. 必填字段 + 断言纪律

| 检查项 | 规则 |
|---|---|
| `dimension=security` | 至少 1 条 `type: negative` |
| `fault_injection` 非空 | `teardown.reset` 不得为 `none` |
| 所有维度 | `assertions` 非空数组 |
| `setup` | 必含 `repo_fixture` |

---

## 生成时自检清单

case-writer 在写入每个 YAML 前执行：

- [ ] `runs-on` 用数组格式 `[ubuntu-latest, x64, small]`
- [ ] 每个 job 有 `name:`
- [ ] 每个 step 有 `name:`，无 `[` `]` `$` `{` `}` 等非法字符
- [ ] `if:` 表达式用 `${{ }}` 包裹，函数带 `()`
- [ ] workflow 字段用 block scalar `|`，不用 `yaml.dump()`
- [ ] 每个 job steps ≤ 16
- [ ] `dimension=security` → 含 `type: negative`
- [ ] 所有必填字段非空

---

*最后更新: 2026-07-21 · 来源: Run 2026-07-20-02 128 条校验 + demo 仓库 AGENTS.md 12 条平台规则*
