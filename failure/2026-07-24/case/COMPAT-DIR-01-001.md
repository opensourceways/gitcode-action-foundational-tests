## 失败分诊 · COMPAT-DIR-01-001 · 工作流目录差异——.gitcode/workflows/ 正常识别

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `completed_success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 6 行）:
```
=== JOB: Verify .gitcode workflows dir (status=COMPLETED) ===
[2026/07/23 22:17:42.925 GMT+08:00] [INFO] Job(1529975825048813568_1529975825011064839) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/597789f8-f4eb-4c9d-b32d-5f1d73680286.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/597789f8-f4eb-4c9d-b32d-5f1d73680286.sh
GITCODE_DIR_RECOGNIZED_OK
```

  **日志分析**: "GITCODE_DIR_RECOGNIZED_OK" — .gitcode/workflows/ 正常识别

- **预期行为**（Phase 01 文本用例 `COMPAT-DIR-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在 .gitcode/workflows/ci.yml 中创建工作流定义"
  - 操作步骤 2: "提交并推送到仓库"
  - 操作步骤 3: "触发对应事件，验证工作流被正确识别和执行"

  预期结果:
  - .gitcode/workflows/ 下的 .yml 文件被平台识别为有效工作流
  - 对应事件触发时工作流正常执行
  - 此行为与 GitCode 官方文档一致

  验证点:
  - [正向] .gitcode/workflows/*.yml 被正确识别
  - [正向] 对应事件触发后工作流正常执行
  - [负向] 不应出现 .gitcode 目录下文件被忽略的情况

- **实际行为**:
  - "GITCODE_DIR_RECOGNIZED_OK" — .gitcode/workflows/ 正常识别


- **测试 YAML 与规格精确对照**:
  - 规格文件: `workflow-file-location-structure.md` (路径: `phase01/inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md`)
  - 规格节选:
```yaml
# .gitcode/workflows/<workflow-name>.yml 目录
# 仅 .yml 和 .yaml 后缀的文件会被识别
```
    该规格明确声明: 37-41行明确规定 `.gitcode/workflows/` 为 workflow 文件存放目录

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"GITCODE_DIR_RECOGNIZED_OK" — .gitcode/workflows/ 正常识别）

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-DIR-01-001 标记为「用例断言修复后应重新验跑」
- 相关用例: COMPAT-DIR-01-002
