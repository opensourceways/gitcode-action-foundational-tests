<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/action-development/top-level-fields | fetched: 2026-07-20 -->

# 顶级字段

本文档定义了插件开发中顶级字段的配置规范，包括插件的元信息、输入输出参数的声明方式，以及执行方式的配置。

## `name`

**必需** 插件的名称。AtomGit Pipeline 在流水线编排界面中显示 `name`，帮助用户直观识别每个步骤中的插件。

```
name: 'codecheck'
```

## `version`

**必需** 插件的版本号，采用语义化版本格式 `X.Y.Z`。

```
version: '1.0.0'
```

## `author`

**必需** 插件作者的标识，例如员工工号。

```
author: 'XXX'
```

## `description`

**必需** 对插件功能用途的一句话描述。

```
description: '样例插件'
```

## `inputs`

**必需** 输入参数。可通过输入参数指定插件在运行时使用的数据。AtomGit Pipeline 将输入参数存储为环境变量。建议使用小写输入 ID。

当指定输入时，系统将为输入创建名为 `INPUT_<VARIABLE_NAME>` 的环境变量。输入名称将转换为大写字母并将空格替换为 `_` 字符。

```
inputs:
  key_input:
    description: '单行输入测试'
    required: true
    default: test
```

> **注意** 如果未指定输入，则使用 `required: true` 的操作不会自动返回错误，需在代码中主动校验。

### `inputs.<input_id>`

**必需** 与输入关联的 `string` 标识符。`<input_id>` 的值为输入元数据的映射。必须是 `inputs` 对象中的唯一标识符，必须以字母或 `_` 开头，并且只能包含字母数字字符、`-` 或 `_`。

### `inputs.<input_id>.description`

**必需** 输入参数的 `string` 说明。

### `inputs.<input_id>.required`

**可选** 一个 `boolean`，用于指示操作是否需要输入参数。如果需要参数，则将其设置为 `true`。

### `inputs.<input_id>.default`

**可选** 一个表示默认值的 `string`。当流水线编排文件中未指定输入参数时使用默认值。

## `outputs`

**必需** 输出参数。可通过输出参数声明插件设置的数据，后续工作流中运行的操作可以使用之前运行操作中的输出数据。

```
outputs:
  record_id:
    description: "recordId"
```

### `outputs.<output_id>`

**必需** 与输出关联的 `string` 标识符。必须是 `outputs` 对象中的唯一标识符，必须以字母或 `_` 开头，并且只能包含字母数字字符、`-` 或 `_`。

### `outputs.<output_id>.description`

**必需** 输出参数的说明。

## `runs`

**必需** 指定当前 Action 的执行方式和运行时。

### `runs.using`

**必需** Action 的执行方式：

| 执行方式 | 说明 |
|---------|------|
| `node16` | Node.js 对应版本，执行 JavaScript/TypeScript 编译后的代码 |

### `runs.main`

**必需** Action 执行时对应的 JavaScript 代码入口文件。

```
runs:
  using: 'node16'
  main: 'dist/main.js'
```

### `runs.post`

**可选** Action 终止时对应的 JavaScript 代码入口文件，用于清理现场、执行善后逻辑等。

```
runs:
  using: 'node16'
  main: 'dist/main.js'
  post: 'dist/stop.js'
```

`post` 的触发机制：

| 触发方式 | 说明 |
|---------|------|
| 主动停止 | 用户点击停止流水线，由调度服务主动调用 |
| 自然调用 | 插件运行完成后自动调用（需插件开发者主动在 `main` 中监听终止信号并调用 `post` 逻辑） |

示例 - 在 `main` 中监听终止信号：

```javascript
// 引入相关的 post 方法
import {post} from "./stop";

async function run() {
    // 捕获 SIGINT 信号
    process.on('SIGINT', () => {
        // 调用 post 逻辑
        post();
        process.exit(0);
    });
    // 插件主逻辑...
}
```
