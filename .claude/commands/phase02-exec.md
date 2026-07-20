# /phase02-exec — 执行测试用例

## 用途
Phase 02 的核心命令。将 `/phase02-schema-check` 通过的用例，按完整执行链路（环境准备 → YAML 编译 → 部署触发 → 采集 → 断言 → 落库 → 清理）逐条执行，产出一批结构化结果。

## 何时使用
- `/phase02-schema-check` 全部通过后
- 需要增量执行（只跑某维度/某优先级的用例）时
- 上次执行中断后继续时

## 前置条件
- Schema 校验通过（`queue.md` 已就绪）
- 环境变量 `GITCODE_ACCESS_TOKEN` 已配置
- 测试实例可达
- API token 有效
- Runner 在线

## 执行步骤

1. **启动检查**（参照 `phase02/agents/harness-orchestrator/CLAUDE.md`）：
   - 验证 API token 有效性（发送一个简单 API 请求确认 200）
   - 验证测试实例可达
   - 确认所需脚本/agent 就绪

2. **构建执行队列**：
   - 读取 `queue.md`，按 priority 排序（P0 → P1 → P2）
   - `full_instance` 级重置的用例排在队列末尾（独占执行窗口）

3. **逐用例执行**（参照 `phase02/process.md` §2.2）：
   对每条用例，按以下链路串行：
   ```
   ① env-manager     → 创建/重置测试仓库，配置 secrets/variables
   ② yaml-compiler   → 编译 workflow 为 GitCode YAML
   ③ workflow-runner → 部署 YAML、触发、等待、采集
   ④ assertion-engine → 判定 PASS/FAIL/FLAKY/TIMEOUT/ENV_ERROR
   ⑤ report-builder  → 落库单条结果
   ⑥ env-manager     → 按 teardown.reset 清理
   ⑦ failure-analyst → (条件) 若 FAIL，做 LLM 根因初判
   ```

4. **执行控制**：
   - 同维度用例串行，不同维度可并行（默认 4 并发）
   - 每 30 秒更新 `timeline.md`
   - 安全事件（secret 泄露）→ 立即中止，标记 `aborted`
   - 失败率超过 50% → 暂停，等用户判断
   - `ENV_ERROR` 连续 3 条 → 暂停

5. **收尾**：
   - 更新 `summary.json`（分维度统计）
   - 标记 run 状态为 `completed`

## 参数
- `<phase01-run-id>`：Phase 01 用例来源（必需）
- `--dims <dim1,dim2>`：只执行指定维度（可选，默认全部）
- `--priority <P0|P1|P2>`：只执行指定优先级（可选）
- `--concurrency <N>`：最大并发数（可选，默认 4）
- `--timeout <seconds>`：每条用例超时（可选，默认 1800）

## 输出
- `phase02/runs/<run-id>/results/<case-id>.json` — 每条用例的完整执行结果
- `phase02/runs/<run-id>/summary.json` — 结构化汇总
- `phase02/runs/<run-id>/timeline.md` — 执行时间线
- 终端输出：实时进度 + 每条用例的判定

## 示例
```
/phase02-exec 2026-07-20-01                                    # 执行全部用例
/phase02-exec 2026-07-20-01 --dims security,reliability        # 只跑安全+稳定性
/phase02-exec 2026-07-20-01 --priority P0                      # 只跑 P0
/phase02-exec 2026-07-20-01 --concurrency 2 --timeout 600      # 慢速执行
```
