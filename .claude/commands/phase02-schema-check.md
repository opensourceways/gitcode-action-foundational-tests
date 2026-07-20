# /phase02-schema-check — 校验 Phase 01 输入的 YAML 用例

## 用途
Phase 02 的第一道闸门。对 Phase 01 产出的可执行 YAML 用例逐条做 schema 校验，通过的进入执行队列，不通过的生成拒收清单回报 Phase 01。

## 何时使用
- Phase 01 完成一批用例产出后（`/phase01-gen` DoD），准备执行前
- Phase 01 重新编译 YAML 后（`/phase01-compile`），重新校验
- 怀疑某些 YAML 可能不符合 schema 时

## 前置条件
- Phase 01 的 `runs/<run-id>/cases/yaml/` 目录下有 `.yaml` 文件
- `phase01/schema/executable-case.schema.yaml` 可用
- 已确认目标 Phase 01 run-id

## 执行步骤

1. **确认输入源**：询问用户目标 Phase 01 run-id（如 `2026-07-20-01`）。若用户未指定，扫描 `phase01/runs/` 下最新的 delivered run。

2. **读取 schema**：读 `phase01/schema/executable-case.schema.yaml`，解析所有 required 字段、类型约束、枚举值、正则 pattern。

3. **逐条校验**（参照 `phase02/scripts/schema-validator.md` 规格）：
   - 扫描 `phase01/runs/<run-id>/cases/yaml/*.yaml`
   - 逐条检查：
     - 文件可解析为合法 YAML
     - 必填字段齐全：`id`, `dimensions`, `dimension`, `priority`, `title`, `intent_ref`, `setup`, `trigger`, `assertions`, `teardown`
     - `id` 符合格式 `^(COMP|COMPAT|REL|SEC|USE)-[A-Z0-9]+-\d{2}-\d{3}(-V\d+)?$`
     - `dimension` 在枚举值内
     - `priority` 在 `[P0, P1, P2]` 内
     - `trigger.event` 在 `[push, pr, fork_pr, manual, schedule, tag]` 内
     - `assertions[].type` 在 `[positive, negative, nonfunctional]` 内
     - `teardown.reset` 在 `[fixture, full_instance, none]` 内
   - 业务校验：
     - `dimension=security` 的用例，`assertions` 中至少一条 `type=negative`
     - `fault_injection != null` 且 `teardown.reset=none` → 警告（破坏性用例应声明清理级别）

4. **输出结果**：
   - 通过的用例：写入 `phase02/runs/<run-id>/queue.md`
   - 不通过的用例：写入 `phase02/runs/<run-id>/rejected.md`（格式见 `contract.md` §4.2）
   - 终端输出：通过/拒收数量统计

5. **门禁判断**：
   - 全部通过 → 可以执行 `/phase02-exec`
   - 有拒收 → **阻止执行**，将拒收清单抄送用户，等待 Phase 01 修复后重校验

## 输出
- `phase02/runs/<run-id>/queue.md` — 执行队列
- `phase02/runs/<run-id>/rejected.md` — 拒收清单
- `phase02/runs/<run-id>/run.md` — 初始化元信息

## 示例
```
/phase02-schema-check                    # 自动选最新 Phase 01 run
/phase02-schema-check 2026-07-20-01      # 指定 Phase 01 run-id
```
