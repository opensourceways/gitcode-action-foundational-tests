# inputs/workflow-samples/

真实开源项目的 GitCode Actions workflow 样本，作为兼容性测试与易用性分析的真实负载。

消费方：compat-diff · usability · L0 冒烟

---

## 当前样本

### cann/（7 个文件，共 817 行）

来源：CANN（昇腾 AI 异构计算架构）项目，华为开源，GitCode 内部试点项目。

| 文件 | 触发方式 | 核心 Action | 说明 |
|------|---------|------------|------|
| `arm_compile_action.yml` | `workflow_dispatch`（手动，含 task_name / image_version 入参） | checkout · obs-download · build-accelerate · obs-upload · 自定义 verify-package | ARM 编译流水线，`runs-on: [dedicate-hosted, arm64, xlarge]` |
| `x86_compile_action.yml` | `workflow_dispatch`（手动，含 task_name / image_version 入参） | checkout · obs-download · build-accelerate · obs-upload · 自定义 verify-package | x86 编译流水线，`runs-on: [dedicate-hosted, x64, large]` |
| `llt_action.yml` | `workflow_dispatch`（手动，含 image_version 入参） | checkout · obs-download · 自定义 ut-cov-report · obs-upload | 单元测试 + 覆盖率，`runs-on: [dedicate-hosted, x64, xlarge]` |
| `codecheck_action.yml` | `workflow_dispatch`（手动，含 precommit_image_version / codecheck_image_version 入参） | checkout · obs-download · 自定义 precommit / codecheck · obs-upload | 代码检查（precommit + codecheck 两个 job），`runs-on: [dedicate-hosted, x64, small]` |
| `staticcheck_action.yml` | `workflow_dispatch`（手动，含 image_version 入参） | checkout · obs-download · 自定义 staticcheck · obs-upload | 静态检查，`runs-on: [dedicate-hosted, x64, small]` |
| `ops-nn_action.yml` | `pull_request_comment` / `pr_comment`（评论触发，keyword 正则匹配） | checkout · obs-upload · obs-download · 自定义 revise-img / get-pr · build-accelerate | 多 stage 多 job 流水线，含 `stages:` 结构、`vars` 上下文（已知不支持 #11）、自定义 composite action 引用 |
| `sub_pipline_support.yaml` | `pr_comment`（评论触发，keyword 正则匹配） | — | 子流水线触发配置示例（仅含 `on:` 定义，无 jobs） |

**覆盖场景**：手动触发含入参、评论触发、OBS 上传/下载、构建加速、自定义 composite action 引用、多 stage 多 job、ARM / x86 双架构、`dedicate-hosted` 资源池。

---

### op-plugin/（1 个文件，424 行）

来源：op-plugin（昇腾算子插件）项目，华为开源，GitCode 内部试点项目。

| 文件 | 触发方式 | 核心 Action | 说明 |
|------|---------|------------|------|
| `PR-pipeline_op-plugin.yml` | `pull_request_comment`（评论触发）| checkout · sca-pr-scan · setup-python · antipoison · openlibing-pre-commit-action · reusable workflow（`.gitcode/workflows/build_job.yml`） | 完整 PR 流水线，含 3 个 stage：stage_1（SCA / Antipoison / CodeCheck / doc-only 判断）、stage_2（x86 + ARM 双架构 × 6 个 pytorch 版本共 12 个并行构建 job，全部调用可复用 workflow）、stage_3（UT）；含 `concurrency`（最大并发 5、抢占式）、workflow-level `inputs` 定义、多镜像版本矩阵（env 变量管理）、`runs-on: [dedicate-hosted, x64/arm64, 2xlarge/large]` |

**覆盖场景**：大规模并行构建（12 个构建 job）、可复用 workflow 调用（`workflow_call`）、并发控制与抢占、workflow-level inputs、多版本镜像矩阵、SCA 安全扫描、PR 评论触发、混合 x86/ARM 架构。

---

## 样本覆盖度分析

| 场景维度 | 覆盖情况 |
|---------|---------|
| 触发方式 | `workflow_dispatch`（手动）、`pull_request_comment`/`pr_comment`（评论触发）；**缺**：`push`、`pull_request`/`merge_request`、`schedule`、`workflow_call` 入口 |
| 资源池 | `dedicate-hosted`（自定义资源池）；**缺**：`ubuntu-latest`（官方资源池）样本 |
| 架构 | ARM（arm64）、x86（x64）均有覆盖 |
| 核心 Action | checkout · obs-upload/download · build-accelerate · setup-python · sca-pr-scan；**缺**：setup-node/go/jdk、cache、upload-artifact/download-artifact、docker 系列 |
| Workflow 模型 | 单 job、多 job、多 stage、可复用 workflow 调用（`uses: .gitcode/workflows/`）均有覆盖 |
| 并发控制 | `concurrency` + 抢占式配置已覆盖 |
| 安全场景 | SCA 扫描、antipoison 反投毒检查已覆盖；**缺**：fork PR 触发、secrets 隔离场景 |

---

已补充 / 2 个项目 / 8 个样本文件 / 2026-07-21
