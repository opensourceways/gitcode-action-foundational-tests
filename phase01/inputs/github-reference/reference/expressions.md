<!-- source: https://docs.github.com/en/actions/reference/workflows-and-actions/expressions | fetched: 2026-07-20 -->

# Evaluate expressions in workflows and actions

Find information for expressions in GitHub Actions.

## Literals

As part of an expression, you can use `boolean`, `null`, `number`, or `string` data types.

| Data type | Literal value |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `boolean` | `true` or `false` |
| `null` | `null` |
| `number` | Any number format supported by JSON. |
| `string` | You don't need to enclose strings in `${{` and `}}`. However, if you do, you must use single quotes (`'`) around the string. To use a literal single quote, escape the literal single quote using an additional single quote (`''`). Wrapping with double quotes (`"`) will throw an error. |

Note that in conditionals, falsy values (`false`, `0`, `-0`, `""`, `''`, `null`) are coerced to `false` and truthy (`true` and other non-falsy values) are coerced to `true`.

### Example of literals

```yaml
env:
  myNull: ${{ null }}
  myBoolean: ${{ false }}
  myIntegerNumber: ${{ 711 }}
  myFloatNumber: ${{ -9.2 }}
  myHexNumber: ${{ 0xff }}
  myExponentialNumber: ${{ -2.99e-2 }}
  myString: Mona the Octocat
  myStringInBraces: ${{ 'It''s open source!' }}
```

## Operators

| Operator | Description |
| ----------------- | --------------------- |
| `( )` | Logical grouping |
| `[ ]` | Index |
| `.` | Property de-reference |
| `!` | Not |
| `<` | Less than |
| `<=` | Less than or equal |
| `>` | Greater than |
| `>=` | Greater than or equal |
| `==` | Equal |
| `!=` | Not equal |
| `&&` | And |
| <code>\|\|</code> | Or |

> **Note**
>
> * GitHub ignores case when comparing strings.
> * `steps.<step_id>.outputs.<output_name>` evaluates as a string. You need to use specific syntax to tell GitHub to evaluate an expression rather than treat it as a string.
> * For numerical comparison, the `fromJSON()` function can be used to convert a string to a number.

GitHub performs loose equality comparisons. If the types do not match, GitHub coerces the type to a number. GitHub casts data types to a number using these conversions:

| Type | Result |
| ------- | ------------------------------------------------------------------------------------------------- |
| Null | `0` |
| Boolean | `true` returns `1` / `false` returns `0` |
| String | Parsed from any legal JSON number format, otherwise `NaN`. Note: empty string returns `0`. |
| Array | `NaN` |
| Object | `NaN` |

* When `NaN` is one of the operands of any relational comparison (`>`, `<`, `>=`, `<=`), the result is always `false`.
* GitHub ignores case when comparing strings.
* Objects and arrays are only considered equal when they are the same instance.

## Functions

GitHub offers a set of built-in functions that you can use in expressions. Some functions cast values to a string to perform comparisons. GitHub casts data types to a string using these conversions:

| Type | Result |
| ------- | --------------------------------------------- |
| Null | `''` |
| Boolean | `'true'` or `'false'` |
| Number | Decimal format, exponential for large numbers |
| Array | Arrays are not converted to a string |
| Object | Objects are not converted to a string |

### contains

`contains( search, item )` — Returns `true` if `search` contains `item`. If `search` is an array, this function returns `true` if the `item` is an element in the array. If `search` is a string, this function returns `true` if the `item` is a substring of `search`. This function is not case sensitive. Casts values to a string.

Example using a string: `contains('Hello world', 'llo')` returns `true`.

Example using an object filter: `contains(github.event.issue.labels.*.name, 'bug')` returns `true` if the issue related to the event has a label "bug".

Example matching an array of strings: `contains(fromJSON('["push", "pull_request"]'), github.event_name)` returns `true` if `github.event_name` is "push" or "pull_request".

### startsWith

`startsWith( searchString, searchValue )` — Returns `true` when `searchString` starts with `searchValue`. This function is not case sensitive. Casts values to a string.

Example: `startsWith('Hello world', 'He')` returns `true`.

### endsWith

`endsWith( searchString, searchValue )` — Returns `true` if `searchString` ends with `searchValue`. This function is not case sensitive. Casts values to a string.

Example: `endsWith('Hello world', 'ld')` returns `true`.

### format

`format( string, replaceValue0, replaceValue1, ..., replaceValueN)` — Replaces values in the `string`, with the variable `replaceValueN`. Variables in the `string` are specified using the `{N}` syntax, where `N` is an integer. You must specify at least one `replaceValue` and `string`. There is no maximum for the number of variables. Escape curly braces using double braces.

Example: `format('Hello {0} {1} {2}', 'Mona', 'the', 'Octocat')` returns 'Hello Mona the Octocat'.

Example escaping braces: `format('{{Hello {0} {1} {2}!}}', 'Mona', 'the', 'Octocat')` returns '{Hello Mona the Octocat!}'.

### join

`join( array, optionalSeparator )` — The value for `array` can be an array or a string. All values in `array` are concatenated into a string. If you provide `optionalSeparator`, it is inserted between the concatenated values. Otherwise, the default separator `,` is used. Casts values to a string.

Example: `join(github.event.issue.labels.*.name, ', ')` may return 'bug, help wanted'

### toJSON

`toJSON(value)` — Returns a pretty-print JSON representation of `value`. You can use this function to debug the information provided in contexts.

### fromJSON

`fromJSON(value)` — Returns a JSON object or JSON data type for `value`. You can use this function to provide a JSON object as an evaluated expression or to convert any data type that can be represented in JSON or JavaScript, such as strings, booleans, null values, arrays, and objects.

### hashFiles

`hashFiles(path)` — Returns a single hash for the set of files that matches the `path` pattern. You can provide a single `path` pattern or multiple `path` patterns separated by commas. The `path` is relative to the `GITHUB_WORKSPACE` directory and can only include files inside of the `GITHUB_WORKSPACE`. This function calculates an individual SHA-256 hash for each matched file, and then uses those hashes to calculate a final SHA-256 hash for the set of files. If the `path` pattern does not match any files, this returns an empty string.

Pattern matching for `hashFiles` follows glob pattern matching and is case-insensitive on Windows.

### case

`case( pred1, val1, pred2, val2, ..., default )` — Evaluates predicates in order and returns the value corresponding to the first predicate that evaluates to `true`. If no predicate matches, it returns the last argument as the default value.

## Status check functions

You can use the following status check functions as expressions in `if` conditionals. A default status check of `success()` is applied unless you include one of these functions.

> **Warning**: Avoid using `always()` for any task that could suffer from a critical failure. Use the recommended alternative: `if: ${{ !cancelled() }}`

### success()

Returns `true` when all previous steps have succeeded.

```yaml
steps:
  - name: The job has succeeded
    if: ${{ success() }}
```

### always()

Causes the step to always execute, and returns `true`, even when canceled. The `always` expression is best used at the step level or on tasks that you expect to run even when a job is canceled.

```yaml
if: ${{ always() }}
```

### cancelled()

Returns `true` if the workflow was canceled.

```yaml
if: ${{ cancelled() }}
```

### failure()

Returns `true` when any previous step of a job fails. If you have a chain of dependent jobs, `failure()` returns `true` if any ancestor job fails.

```yaml
steps:
  - name: The job has failed
    if: ${{ failure() }}
```

## Object filters

You can use the `*` syntax to apply a filter and select matching items in a collection.

For example, consider an array of objects named `fruits`:

```json
[
  { "name": "apple", "quantity": 1 },
  { "name": "orange", "quantity": 2 },
  { "name": "pear", "quantity": 1 }
]
```

The filter `fruits.*.name` returns the array `[ "apple", "orange", "pear" ]`.

---

> **关键差异提示（compat-diff）**: GitHub 状态函数带括号 `success()` / `failure()` / `always()` / `cancelled()`；GitCode 不带括号。GitHub 有 `join()` / `fromJSON()` / `case()` 函数而 GitCode 文档未列出。GitHub 有 loose equality + 类型强转规则，GitCode 需验证是否一致。
