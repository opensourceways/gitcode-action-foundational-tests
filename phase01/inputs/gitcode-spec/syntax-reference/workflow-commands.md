<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/syntax-reference/workflow-commands | fetched: 2026-07-20 -->

# 工作流命令（语法参考）

工作流命令是通过 `echo` 向 Runner 发送特殊指令的机制，用于设置输出、环境变量、PATH 等信息。

## 5.1 设置步骤输出 — ATOMGIT_OUTPUT

将值写入步骤输出，供后续步骤通过 `steps.<step_id>.outputs.<name>` 访问。

```
echo "result=success" >> $ATOMGIT_OUTPUT
```

**多行输出：**

```
echo "multiline<<EOF" >> $ATOMGIT_OUTPUT
echo "第一行内容"
echo "第二行内容"
echo "EOF" >> $ATOMGIT_OUTPUT
```

## 5.2 设置环境变量 — ATOMGIT_ENV

将值写入后续步骤的环境变量，在当前 Job 的后续步骤中可用。

```
echo "MY_VAR=my_value" >> $ATOMGIT_ENV
```

**多行环境变量：**

```
echo "MULTILINE<<EOF" >> $ATOMGIT_ENV
echo "第一行"
echo "第二行"
echo "EOF" >> $ATOMGIT_ENV
```

## 5.3 设置系统 PATH — ATOMGIT_PATH

向 Runner 的 PATH 添加目录，在当前 Job 的后续步骤中生效。

```
echo "/custom/bin" >> $ATOMGIT_PATH
```

## 5.4 步骤摘要 — ATOMGIT_STEP_SUMMARY

将 Markdown 内容写入工作流运行摘要，显示在 AtomGit 工作流运行详情页面。

```
echo "## 构建结果" >> $ATOMGIT_STEP_SUMMARY
echo "| 项目 | 状态 |" >> $ATOMGIT_STEP_SUMMARY
echo "|------|------|" >> $ATOMGIT_STEP_SUMMARY
echo "| App | ✅ 成功 |" >> $ATOMGIT_STEP_SUMMARY
```

## 5.6 废弃的命令格式

以下旧版命令格式已废弃，建议不再使用：

| 废弃命令 | 替代方案 |
|--------|--------|
| `echo "::set-output name=result::success"` | `echo "result=success" >> $ATOMGIT_OUTPUT` |
| `echo "::set-env name=MY_VAR::my_value"` | `echo "MY_VAR=my_value" >> $ATOMGIT_ENV` |
| `echo "::add-path::/custom/bin"` | `echo "/custom/bin" >> $ATOMGIT_PATH` |

> 注：日志脱敏命令 `echo "::add-mask::$SECRET"` 见「使用脚本命令」页。
