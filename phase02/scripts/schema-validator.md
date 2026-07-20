# Schema Validator（schema-validator）

## 类型
确定性脚本（Bash + yq / Python + jsonschema）

## 职责
对 Phase 01 产出的可执行 YAML 用例逐条做 schema 校验——这是 Phase 02 的**第一道闸门**。不合规用例直接拒收并生成拒收清单回报 Phase 01。

## 输入
- Phase 01 YAML 用例目录：`phase01/runs/<run-id>/cases/yaml/*.yaml`
- Schema 文件：`phase01/schema/executable-case.schema.yaml`

## 处理逻辑

### 1. 扫描输入
```bash
find phase01/runs/<run-id>/cases/yaml/ -name "*.yaml" -o -name "*.yml" | sort
```

### 2. 逐条校验
对每条 YAML 文件：
- 解析 YAML 结构
- 对照 schema 校验必填字段：`id`, `dimensions`, `dimension`, `priority`, `title`, `intent_ref`, `setup`, `trigger`, `assertions`, `teardown`
- 校验每个字段的类型/枚举/正则：
  - `id` 格式：`^(COMP|COMPAT|REL|SEC|USE)-[A-Z0-9]+-\d{2}-\d{3}(-V\d+)?$`
  - `dimension` 枚举：`[completeness, compatibility, reliability, security, usability]`
  - `priority` 枚举：`[P0, P1, P2]`
  - `intent_ref` 格式：`^INTENT-(COMP|COMPAT|REL|SEC|USE)-[0-9]+$`
  - `trigger.event` 枚举：`[push, pr, fork_pr, manual, schedule, tag]`
  - `trigger.as` 枚举：`[maintainer, untrusted_contributor]`
  - `assertions[].type` 枚举：`[positive, negative, nonfunctional]`
  - `teardown.reset` 枚举：`[fixture, full_instance, none]`
- 额外业务校验：
  - `dimension=security` 的用例，`assertions` 中至少一条 `type=negative`
  - `fault_injection != null` 的用例，`teardown.reset` 不得为 `none`（除非确无副作用）

### 3. 输出结果
- 通过校验：列入执行队列（写入 `queue.md`）
- 不通过校验：列入拒收清单（格式见 `contract.md` §4.2）

## 输出
- `runs/<run-id>/queue.md`：通过校验的用例清单（按 priority 排序）
- stdout：拒收清单（如有）
- 退出码：0 = 全部通过 / 1 = 存在拒收项

## 实现示意（bash + python）

```bash
#!/bin/bash
# schema-validator.sh
# Usage: ./schema-validator.sh <phase01-run-id> <phase02-run-id>

SCHEMA="phase01/schema/executable-case.schema.yaml"
INPUT_DIR="phase01/runs/$1/cases/yaml"
QUEUE_FILE="phase02/runs/$2/queue.md"
REJECT_FILE="phase02/runs/$2/rejected.md"

PASSED=0
REJECTED=0

echo "# 执行队列 · $(date +%Y-%m-%d)" > "$QUEUE_FILE"
echo "| 用例 ID | 维度 | 优先级 | 标题 |" >> "$QUEUE_FILE"
echo "|---|---|---|---|" >> "$QUEUE_FILE"

echo "# 拒收清单 · $(date +%Y-%m-%d)" > "$REJECT_FILE"
echo "| 文件 | 错误字段 | 错误类型 | 说明 |" >> "$REJECT_FILE"
echo "|---|---|---|---|" >> "$REJECT_FILE"

for f in "$INPUT_DIR"/*.yaml "$INPUT_DIR"/*.yml; do
  [ -f "$f" ] || continue
  # TODO: 实际校验逻辑——用 python jsonschema 或 yq 逐字段检查
  # 这里描述意图，具体实现在 Phase 02 落地时补全
  RESULT=$(python3 phase02/scripts/schema_validator.py "$f" "$SCHEMA")
  if [ "$RESULT" = "PASS" ]; then
    PASSED=$((PASSED + 1))
    # 从 YAML 提取 id/dimension/priority/title 写入 queue.md
  else
    REJECTED=$((REJECTED + 1))
    echo "$RESULT" >> "$REJECT_FILE"
  fi
done

echo "---"
echo "校验完成: $PASSED 通过, $REJECTED 拒收"

[ $REJECTED -eq 0 ] && exit 0 || exit 1
```

## 质量要求
- 校验结果可复核：每条拒收记录必须给出具体字段和违反的规则
- 幂等：同一批 YAML 多次校验结果一致
- 与 Phase 01 schema 保持同步：schema 变更时本脚本自动适配（因从同一份 schema 文件读取）
