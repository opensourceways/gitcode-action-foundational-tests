<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/running-pipelines/view-job-logs | fetched: 2026-07-20 -->

# 查看任务日志

**适用场景**：当流水线任务执行失败或行为异常时，你需要逐 step 查看完整日志输出，定位具体错误行、命令返回码或环境问题。

## 配置说明

### 查看入口

1. 进入目标运行详情页（参见 1.1）。
2. 点击目标 job 卡片展开 step 时间线。
3. 点击某个 step 行，右侧面板展示该 step 的完整标准输出与标准错误。

### 日志结构

每个 job 的日志按 step 顺序组织：

```
── Job: compile ({ubuntu-24,x64,small})
├── Step 1: Checkout repository        ← run: git checkout
├── Step 2: Set up toolchain           ← uses: action-setup-toolchain
├── Step 3: Run build command          ← run: make build
└── Post: Clean up workspace           ← post 处理
```

每条日志行前缀包含时间戳和 step 编号，便于时间线追踪。

### 日志搜索与折叠

- **折叠**：长输出的 step 默认折叠关键区间，点击展开查看完整内容。
- **搜索**：在日志面板顶部输入关键词（如 `Error`、`fatal`、`FATAL`），系统高亮匹配行。
- **下载**：点击右上角"下载日志"按钮，获取该 job 的完整日志文件。

### 日志中的上下文变量

日志中可能包含 AtomGit Action 上下文变量的展开结果，例如：

```yaml
steps:
  - run: echo "Repo is ${{ atomgit.repository }}"
  - run: echo "Actor is ${{ atomgit.actor }}"
  - run: echo "Event is ${{ atomgit.event_name }}"
```

`atomgit` 上下文在日志中展开为实际值，便于确认触发信息是否正确。

### 系统变量 ATOMGIT_*

除 `${{ }}` 表达式外，Runner 环境中还注入了 `ATOMGIT_*` 系统环境变量，可在日志中直接查看：

| 变量名 | 说明 |
|--------|------|
| `ATOMGIT_REPOSITORY` | 仓库全名（owner/repo） |
| `ATOMGIT_EVENT_NAME` | 触发事件类型 |
| `ATOMGIT_REF` | 触发引用（分支/标签） |
| `ATOMGIT_SHA` | 触发提交 SHA |
| `ATOMGIT_ACTOR` | 触发人 |
| `ATOMGIT_TOKEN` | 自动生成的会话 Token |
| `ATOMGIT_RUN_ID` | 运行唯一 ID |
| `ATOMGIT_RUN_NUMBER` | 运行编号 |

```yaml
steps:
  - run: |
      echo "System vars:"
      echo "Repo = $ATOMGIT_REPOSITORY"
      echo "SHA  = $ATOMGIT_SHA"
```

## 常见问题

**Q：日志中出现 `***` 遮掩内容，如何查看原值？**

A：含 Secret 值的日志行会被自动遮掩为 `***`，这是安全机制，无法在界面中查看原值。请确认 Secret 是否正确配置于项目/组织 Settings → Secrets 页面。

**Q：部分 step 日志为空，原因是什么？**

A：可能原因包括：(1) step 使用了 `uses` 引用 Action，该 Action 内部无输出；(2) 命令被 `> /dev/null` 重定向；(3) step 在 setup 阶段超时被 Kill，日志未完整写入。

**Q：日志下载后文件编码异常？**

A：下载日志为 UTF-8 编码文本，若本地工具默认 GBK 打开可能出现乱码，请切换编辑器编码为 UTF-8。
