# GitCode Action ↔ GitHub Actions 差异速记（抓取副产物）

> 抓取官方文档过程中直接观察到的、与 GitHub Actions 不一致或需重点验证的点。**这是给 compat-diff agent 的高价值线索种子**，非穷举；正式差异确认仍需对照 `inputs/github-reference/` 与真实运行。
> 每条标注：GitCode 侧事实 / GitHub 侧对照 / 风险类别。

## 1. 目录与文件
- **工作流目录**：GitCode 用 `.gitcode/workflows/`，GitHub 用 `.github/workflows/`。→ 迁移第一摩擦点（迁移摩擦/完备性）。仅识别 `.yml`/`.yaml`。

## 2. 上下文与变量命名（高发差异）
- **上下文对象**：GitCode 核心上下文是 `atomgit.*`（如 `atomgit.ref`/`atomgit.sha`/`atomgit.event_name`），GitHub 是 `github.*`。→ 直接搬 GitHub workflow 会全线失效（兼容性/迁移）。
- **系统环境变量前缀**：GitCode 为 `ATOMGIT_*`（`ATOMGIT_TOKEN`/`ATOMGIT_OUTPUT`/`ATOMGIT_ENV`/`ATOMGIT_PATH`/`ATOMGIT_STEP_SUMMARY`…），GitHub 为 `GITHUB_*`。
- **自动令牌**：GitCode `ATOMGIT_TOKEN` / `secrets.ATOMGIT_TOKEN`，GitHub `GITHUB_TOKEN`。
- 注：`runtime-environment-variables.md` 里部分描述文案仍夹带 `GITHUB_ACTION_PATH` 等 GitHub 残留措辞——文档一致性问题，值得单独出易用性 intent。

## 3. 表达式与函数（重点差异区）
- **状态函数不带括号**：GitCode 写 `success`/`always`/`failed`/`cancelled`（如 `if: ${{ success }}`）；GitHub 是函数调用 `success()`/`always()`/`failure()`/`cancelled()`。→ 语义等价但语法不同，易踩坑（兼容性）。
- **函数集差异**：GitCode 额外有 `substring(str,start,len)`、`replace(str,old,new)`；GitHub 无这两个内置。GitCode 的失败函数名为 `failed`，GitHub 为 `failure()`。
- 需验证 `contains`/`startsWith`/`endsWith`/`format`/`hashFiles`/`toJson` 边界行为是否与 GitHub 完全一致。

## 4. 执行编排模型（GitCode 特有）
- **stages 阶段机制**：GitCode 特有的顶层 `stages`（阶段间串行、阶段内 job 并行、`fail_fast`）。GitHub 无 stages 概念，只有 job 级 `needs` DAG。
- **post 后处理阶段**：GitCode 顶层 `post`（默认 `run_always: true`）。GitHub 无等价顶层字段（仅 action 内 `post`）。
- **两种 fail_fast**：`stages.fail_fast`（阶段级）与 `strategy.fail-fast`（矩阵级）语义不同，注意混淆。

## 5. 触发器差异
- **事件集**：GitCode 有 `pull_request_comment`（带 `comments` 正则过滤）这一 GitHub 没有的事件；`issue_comment` 都有。
- **pull_request types 取值**：GitCode 为 `[merge, open, reopen, update]`，默认 `[open, reopen, update]`；GitHub types 取值不同（`opened`/`synchronize`/`reopened`/…命名也不同）。→ 命名+取值双重差异。
- **paths 匹配上限**：GitCode 声明「匹配前 300 个变更文件」，超出不参与判断。→ 边界/稳定性可测点。
- **schedule**：GitCode 声明最短间隔 5 分钟、UTC、仅默认分支生效。
- **workflow_call 嵌套**：GitCode 最多 2 层（不能再套一层）。

## 6. 权限模型差异
- **permissions 权限域命名**：GitCode 用 `project`/`pr`/`issue`/`note`/`repository`/`hook`（值 read/write/none）；GitHub 用 `contents`/`pull-requests`/`issues`/`actions`… 命名完全不同。→ 迁移必改（兼容性/安全）。
- 快捷语法 `read-all`/`write-all`/`{}` 与 GitHub 类似。

## 7. Runner 标签体系
- **三段式标签**：GitCode `{os-version},{arch},{flavor}`（如 `{ubuntu-24,x64,small}`）与 `default`；GitHub 用 `ubuntu-latest` 等单标签 + `runs-on` 数组。→ `runs-on` 写法差异（兼容性/迁移）。
- 托管规格默认仅 slim/small/medium，large 及以上需申请。

## 8. 安全隔离（与 GitHub 理念一致，需实测确认）
- `pull_request`（fork）→ TOKEN 仅 read、不可访问 Secret；`pull_request_target` → base 上下文、可写、可访问 Secret。语义与 GitHub 一致，**但 GitCode「大部分兼容」，隔离强度需逐条实测**（安全命脉）。
- secret 日志脱敏 `***`；文档自承 `echo "${{ secrets.X }}"` 可能绕过脱敏 → 直接的 negative 断言点。
- `pull_request_target` 若 checkout PR `head.sha` 再执行其脚本 = 高权限跑不可信代码，注入风险点。

## 9. inputs 类型限制
- GitCode `workflow_dispatch`/`workflow_call` 的 `inputs` **仅支持 string 类型**；GitHub 支持 `boolean`/`choice`/`number`/`environment`。→ 迁移摩擦 + 类型转换需求。

## 10. 内置 action 名称
- GitCode 用无 owner 短名：`checkout`/`setup-node`/`setup-java`/`setup-go`/`setup-python`/`cache`/`upload-artifact`/`download-artifact`。GitHub 为 `actions/checkout@v4` 等带 owner+版本。→ 引用写法差异，等价实现行为需验证。
- Action 运行时 `runs.using` 文档仅列 `node16`（GitHub 支持 node20/docker/composite）。

## 11. 废弃命令
- GitCode 明确废弃 `::set-output`/`::set-env`/`::add-path`，改用 `>> $ATOMGIT_OUTPUT` 等——与 GitHub 演进一致；但 `::add-mask::` 仍在用。

---
**给 compat-diff 的用法**：以上每条都可展开成一条「一致性用例」或「差异确认用例」，注意在 intent 里写清 oracle 对齐方向（见 `phase01/rules.md` §4）。
