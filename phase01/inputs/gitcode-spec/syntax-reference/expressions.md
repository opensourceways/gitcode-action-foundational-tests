<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/syntax-reference/expressions | fetched: 2026-07-20 -->

# 表达式

AtomGit Action 使用 `${{ expression }}` 语法在工作流中编写表达式。表达式可在 `if` 条件、变量赋值、步骤参数等位置使用。

## 3.1 字面量

| 类型 | 语法 | 示例 |
|------|------|------|
| 布尔值 | `true` / `false` | `${{ true }}` |
| null | `null` | `${{ null }}` |
| 数字 | 整数或浮点数 | `${{ 42 }}`, `${{ 3.14 }}` |
| 字符串 | 单引号包裹 | `${{ 'hello' }}` |

## 3.2 运算符

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `==` | 等于 | `${{ atomgit.ref == 'refs/heads/main' }}` |
| `!=` | 不等于 | `${{ atomgit.event_name != 'schedule' }}` |
| `!` | 逻辑非 | `${{ !success }}` |
| `&&` | 逻辑与 | `${{ success && atomgit.ref == 'refs/heads/main' }}` |
| `\|\|` | 逻辑或 | `${{ failed \|\| cancelled }}` |
| `>` | 大于 | `${{ matrix.version > 12 }}` |
| `<` | 小于 | `${{ matrix.version < 14 }}` |
| `>=` | 大于等于 | `${{ strategy.job-total >= 3 }}` |
| `<=` | 小于等于 | `${{ inputs.count <= 10 }}` |

> **运算符优先级（从高到低）：** `` → `!` → `<`, `>`, `<=`, `>=` → `==`, `!=` → `&&` → `||`

## 3.3 函数

| 函数 | 说明 | 示例 |
|------|------|------|
| `success` | 所有前置步骤成功时返回 `true` | `if: ${{ success }}` |
| `always` | 无论前置步骤结果如何始终返回 `true` | `if: ${{ always }}` |
| `cancelled` | 工作流被取消时返回 `true` | `if: ${{ cancelled }}` |
| `failed` | 任一前置步骤失败时返回 `true` | `if: ${{ failed }}` |
| `contains(search, item)` | 判断 search 是否包含 item | `${{ contains(atomgit.ref, 'release') }}` |
| `startsWith(search, prefix)` | 判断 search 是否以 prefix 开头 | `${{ startsWith(atomgit.ref, 'refs/tags/') }}` |
| `endsWith(search, suffix)` | 判断 search 是否以 suffix 结尾 | `${{ endsWith(atomgit.ref_name, '.rc') }}` |
| `format(template, args...)` | 格式化字符串，0/1... 为占位符 | `${{ format('Hello {0}, {1}!', name, role) }}` |
| `substring(str, start, len)` | 截取子字符串 | `${{ substring(atomgit.sha, 0, 7) }}` |
| `replace(str, old, new)` | 替换字符串 | `${{ replace(atomgit.ref, 'refs/heads/', '') }}` |
| `hashFiles(paths...))` | 计算文件哈希值 | `${{ hashFiles('src/**', 'package.json') }}` |
| `toJson(value)` | 将对象序列化为 JSON 字符串 | `${{ toJson(atomgit.event) }}` |

### 函数详细说明：

- **success**：当所有前置步骤的 conclusion 为 `success` 时返回 `true`。在 `if` 条件中，如未指定条件，默认为 `success`。
- **always**：在任何情况下返回 `true`，用于确保步骤始终执行（如清理步骤）。配合 `post` 或 `run_always` 使用。
- **cancelled**：工作流被取消时返回 `true`。
- **failed**：当任一前置步骤的 conclusion 为 `failure` 时返回 `true`。
- **contains(search, item)**：字符串搜索时为子串匹配；数组/对象搜索时判断是否存在该元素。
- **startsWith/endsWith**：纯字符串操作，区分大小写。
- **format**：使用 `{0}`, `{1}`, ... 作为占位符，参数依次替换。
- **hashFiles**：计算匹配路径文件的组合 SHA256 哈希，用于缓存 key 生成。

## 3.4 表达式示例

```yaml
steps:
  - name: 仅在 main 分支且成功时执行
    if: ${{ success && atomgit.ref == 'refs/heads/main' }}
    run: echo "Deploy to production"

  - name: 失败或取消时仍执行清理
    if: ${{ always }}
    run: echo "Cleanup resources"

  - name: 仅在失败时执行通知
    if: ${{ failed }}
    run: echo "Send failure notification"

  - name: 标签推送时构建
    if: ${{ startsWith(atomgit.ref, 'refs/tags/') }}
    run: echo "Build release"

  - name: 使用 format 拼接字符串
    env:
      IMAGE_TAG: ${{ format('{0}:{1}', 'myimage', atomgit.sha) }}
    run: echo $IMAGE_TAG
```
