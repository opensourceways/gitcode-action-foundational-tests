<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/running-pipelines/view-run-results | fetched: 2026-07-20 -->

# 查看流水线运行结果

## 配置说明

流水线运行结果可在项目多个入口查看：

### 入口一：项目主页 → Actions 标签页

1. 进入目标项目页面，点击顶部导航栏的 **Actions** 标签。
2. 左侧边栏列出所有 workflow 名称，点击目标 workflow。
3. 右侧展示该 workflow 的运行列表，每条记录包含：
   - **触发事件**：如 `push`、`pull_request`、`workflow_dispatch` 等
   - **触发分支/标签**：显示触发来源
   - **状态徽标**：✅ 成功 / ❌ 失败 / 🟡 运行中 / ⏸ 取消 / 🔶 跳过
   - **运行编号**：唯一标识，如 `#42`
   - **触发人**与**耗时**

### 入口二：提交记录页

在代码仓库的 Commits 页面，每条提交记录右侧显示一个精简状态徽标，点击可跳转到对应运行详情。

### 入口三：Pull Request 页

PR 页面的 Checks 标签页汇总该 PR 触发的所有流水线运行结果，便于评审人快速判断代码质量。

### 运行详情页面

点击某次运行后进入详情页，展示内容取决于 workflow 定义中的 **stages** 结构：

```yaml
# 查看运行结果
stages:
  compile:
    name: build
    jobs:
      - name: compile
        runs-on: {ubuntu-24,x64,small}
        steps:
          - run: make build
  test:
    name: test
    fail_fast: true          # 本阶段任一 job 失败即跳过后续 stage
    jobs:
      - name: unit-test
        runs-on: {ubuntu-24,x64,medium}
        steps:
          - run: make test
  deploy:
    name: deploy
    jobs:
      - name: push-image
        runs-on: {ubuntu-24,x64,large}
        steps:
          - run: make deploy
```

详情页按 stages 顺序纵向排列：

| 展示区域 | 说明 |
|---------|------|
| **Stage 侧栏** | 按 `stages` 定义顺序列出各阶段，标注状态 |
| **Job 卡片** | 每个 job 展示名称、Runner 标签、耗时、状态 |
| **Step 时间线** | 展开 job 后逐 step 显示执行耗时与结果 |
| **Post 后处理** | 若 workflow 定义了 `post` 阶段，在主流程后单独展示 |

> **注意**：AtomGit Action 的 `stages` 机制默认串行执行——前一 stage 全部 job 成功后，下一 stage 才开始。若某 stage 设置了 `fail_fast: true`，则该 stage 中任意 job 失败会立即中断当前 stage 并跳过所有后续 stage。

### 状态徽标嵌入

可将运行状态徽标嵌入 README：

```
![Build Status](https://atomgit.com/{owner}/{repo}/badges/{workflow_name}/pipeline.svg)
```

## 常见问题

**Q：为什么详情页中某个 stage 显示为"跳过"？**

A：前置 stage 中有 job 失败，且后续 stage 被串行机制跳过；或前置 stage 配置了 `fail_fast: true`，任一 job 失败即终止整个 workflow。

**Q：运行详情页出现"post"阶段是什么含义？**

A：AtomGit Action 支持 `post` 后处理阶段，默认 `run_always: true`，即使主流程失败也会执行 post stage，常用于资源清理、通知推送等场景。

**Q：如何只查看失败运行？**

A：在 Actions 标签页左侧筛选栏，选择状态过滤为"Failed"即可。
