<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/action-development/plugin-development-guide | fetched: 2026-07-20 -->

# 插件开发指南

**语言：插件代码语言推荐为 TypeScript。**

## 编写核心代码

插件核心逻辑可用 JavaScript/TypeScript 编写。如需使用其他语言的脚本，请通过 JS/TS 调用执行。

**开发建议：** 先实现最核心的功能确保基本运行，然后逐步迭代。

### 示例：使用 Node.js 开发插件

```typescript
import core from '@actions/core';

try {
  const myInput = core.getInput('myInput');           // 获取插件输入
  const ref = process.env['ATOMGIT_REF'];             // 获取系统变量
  const result = `Hello ${pipelineId}, ${myInput}!`;  // 插件核心逻辑
} catch (error) {
  core.setFailed(`Action failed with error: ${error.message}`);
}
```

### 参数获取方式

| 方法 | 用途 |
|------|------|
| `process.env[]` | 获取环境变量参数 |
| `core.getInput()` | 获取插件输入参数 |

### 推荐工具包

[GitHub Actions Toolkit](https://github.com/actions/toolkit) 提供 `@actions/core`、`@actions/io`、`@actions/exec`、`@actions/glob`、`@actions/http-client` 等模块。

## 日志输出

```javascript
const core = require('@actions/core');
core.info('Starting action...');
core.warning('This is a warning message');
core.error('This is an error message');
```

| 方法 | 用途 |
|------|------|
| `core.info()` | 普通日志信息 |
| `core.warning()` | 警告信息 |
| `core.error()` | 错误信息 |

## 执行状态反馈

- 正常执行完成：任务 process 返回 `0`
- 异常或错误：通过 `core.setFailed()` 修改进程返回，调度框架捕获非 0 返回则判定任务失败

## 结果输出和收集

插件通过系统变量 `$ATOMGIT_OUTPUT` 定义 output 收集文件路径，输出至该文件的内容会被回收至流水线 step、job、pipeline 级 output 归档。

### 方式一：通过日志关键字实时输出

实时收集，相同 key 覆盖，不同 key 追加：

```
log.info(`::set-output var=${outputkey}:${outputvalue}`)
```

### 方式二：批量写入 output（推荐）

统一写入 `$ATOMGIT_OUTPUT` 官方路径，执行成功后统一上报：

```typescript
export async function writeOutputContext(data: string) {
  const filePath = core.getInputForEnv("ATOMGIT_OUTPUT");
  log.info("outputFilePath is " + filePath);
  if (!filePath) {
    log.error(ErrorCode.INVALID_PARAM, {
      cause: `Failed to get the upload report path: ATOMGIT_OUTPUT`,
      causeZh: `获取输出路径失败: ATOMGIT_OUTPUT`,
    });
    return;
  }
  fs.appendFile(filePath, data, async (err) => {
    if (err) {
      log.error(ErrorCode.LOCAL_ERROR, {
        cause: `Failed to write the report file.`,
        causeZh: `写入output上报文件失败`,
      });
      return;
    } else {
      log.info("File written successfully!");
    }
  });
}
```

## 插件 Summary 报告输出

可为每个 Job 输出自定义 Markdown，展示在 Workflow 运行摘要页面。将 Step 生成的 Markdown 追加写入 `ATOMGIT_STEP_SUMMARY` 指向的文件（每个 Step 独立且唯一）。Job 完成后所有 Step 摘要按顺序拼接为统一 Job 摘要；多个 Job 摘要按完成时间顺序展示。

```bash
echo "### Hello world! :rocket:" >> $ATOMGIT_STEP_SUMMARY
```

多行 Markdown（每次追加自动加换行）：

```bash
- name: Generate list using Markdown
  run: |
    echo "This is the lead in sentence for the list" >> $ATOMGIT_STEP_SUMMARY
    echo "" >> $ATOMGIT_STEP_SUMMARY # 空行
    echo "- Lets add a bullet point" >> $ATOMGIT_STEP_SUMMARY
    echo "- Lets add a second bullet point" >> $ATOMGIT_STEP_SUMMARY
    echo "- How about a third one?" >> $ATOMGIT_STEP_SUMMARY
```

## 插件执行后处理（post）

`post` 脚本（推荐 `post.js`）提供给调度服务 post 调用，用于清理现场、善后逻辑。

| 触发方式 | 说明 |
|---------|------|
| 主动停止流水线 | 用户点击停止，调度服务主动调用 |
| 插件完成后自然调用 | 需开发者在 `main` 中监听终止信号并调用 |

```typescript
import {post} from "./stop";

async function run() {
    process.on('SIGINT', () => {
        post();
        process.exit(0);
    });
    log.info("process has been started, press 'Ctrl C' to stop.");
    setInterval(() => { log.info("process running..."); }, 1000);
}
```
