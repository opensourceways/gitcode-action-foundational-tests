# inputs/business-context/ （建议 · 业务场景）

放 **业务场景、部署方式、历史问题与改造点**。这些是易用性/兼容性/安全 agent 设计贴合实际场景的关键输入——纯读规格造不出「用户真正会踩的坑」。

## 请补充

### 1. Runner 接入方式（必填）
```
# 示例
部署模型:
  - 官方托管 Runner（默认）
  - 自托管主机 Runner（内网环境，需预装特定工具链）
  - 自托管 K8s Runner（弹性伸缩场景）
组织/项目级 Runner 划分策略:
  - <描述>
跨仓库 Runner 复用规则:
  - <描述>
```

### 2. 典型业务工作流模板（建议）
```
# 示例
- 场景：PR 代码检查 → 构建 → 测试 → 部署（多环境）
- 场景：定时安全扫描 + 报告推送
- 场景：多架构 (x64 + arm64) 镜像构建
- 场景：Matrix 多版本 (JDK 8/11/17/21) 测试
```

### 3. 从 GitHub Actions 迁移的重点（建议）
```
# 示例
迁移规模:
  - 预计迁移仓库数: <N>
  - 预计迁移 workflow 数: <N>
迁移改造点:
  - <如：所有 `${{ github.* }}` 上下文全局替换为 `${{ atomgit.* }}`>
  - <如：permissions 字段从 GitHub 命名改为 GitCode 命名>
  - <如：`runs-on` 从 `ubuntu-latest` 改为三段式标签>
已知摩擦:
  - <如：`pull_request` types 命名差异导致 CI 不触发>
  - <如：workflow_dispatch inputs 仅支持 string>
```

### 4. 历史踩坑记录 / 已知问题（建议）
```
# 示例
- 问题: <描述> ｜ 影响: <维度> ｜ 状态: <已修复/仍存在/待确认>
- 问题: fork PR 下 secret 是否确实隔离 ｜ 影响: security ｜ 状态: 待确认
- 问题: 自托管 Runner 重启后注册状态丢失 ｜ 影响: reliability ｜ 状态: 已修复
```

### 格式

Markdown。

## 消费方

- **usability agent**：迁移摩擦 · 典型工作流是否开箱能跑 · 改造点是否文档化
- **compat-diff agent**：迁移改造点列表补足差异盲区（用户告诉你哪里改了，反向验证是否合理）
- **security agent**：部署模型（如自托管 Runner 内网环境）改变攻击面评估
- **reliability agent**：业务工作流模板提供真实负载模式的规模参数
- **orchestrator**：历史问题列表直接喂进风险登记册，调高历史高频风险项的优先级

## 刷新时的影响

更新本目录后，以下命令会触发相关 agent 重新审视：
- `/phase01-update <run-id> dim:usability` → 基于新业务场景重跑易用性 intent
- `/phase01-update <run-id> dim:compat` → 基于新迁移改造点补兼容性 intent
- `/phase01-update <run-id> dim:security` → 基于新部署模型重评估攻击面

> 补充完成后可在此文件末尾记：`已补充 / 日期`。
