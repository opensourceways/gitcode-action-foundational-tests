## 失败分诊 · COMPAT-ENV-01-001 · ATOMGIT_SHA 环境变量应正确返回触发提交 SHA

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 7 行）:
```
=== JOB: Test ATOMGIT_SHA env var (status=COMPLETED) ===
[2026/07/23 22:17:55.420 GMT+08:00] [INFO] Job(1529975877301706752_1529975877263958023) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/fa86e9e0-7aba-4669-8c7a-9d3ea2710a12.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/fa86e9e0-7aba-4669-8c7a-9d3ea2710a12.sh
atomgit_sha=
done
```

  **日志分析**: run=COMPLETED, 断言词汇不匹配

- **预期行为**（Phase 01 文本用例 `COMPAT-ENV-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在 workflow 的 run 步骤中输出 $ATOMGIT_SHA"
  - 操作步骤 2: "触发 workflow 运行"

  预期结果:
  - $ATOMGIT_SHA 应返回当前触发事件的提交 SHA（40 位十六进制字符串）

  验证点:
  - [正向] 日志中 ATOMGIT_SHA 的值不为空且为有效 SHA 格式

- **实际行为**:
  - run=COMPLETED, 断言词汇不匹配


- **测试 YAML 与规格精确对照**:
  - 规格文件: `context.md / expressions.md` (路径: `phase01/inputs/gitcode-spec/syntax-reference/context.md`)
  - 规格节选:
```yaml
# context.md 第29-31行: atomgit.ref 为完整引用名
# 如 refs/heads/main
# expressions.md 第36-39行: success/failed 状态函数定义
```
    该规格明确声明: context.md 27-33行 atomgit 上下文属性 + expressions.md 36-39行状态函数

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（run=COMPLETED, 断言词汇不匹配）

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-ENV-01-001 标记为「用例断言修复后应重新验跑」
