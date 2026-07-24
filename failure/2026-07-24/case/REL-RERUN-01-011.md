## 失败分诊 · REL-RERUN-01-011 · rerun 边界值——单条运行连续重新运行 3 次应全部成功

**判定结果**: FAIL
**失败断言**: 正向/rerun_count expected=3 actual=N/A; 正向/run_status expected=completed(success) actual=COMPLETED (仅 1 run)

**根因初判**: 环境/Harness（log 仅包含原始 run，无 3 次 rerun 记录——rerun API 可能未成功触发）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: reliability test job (status=COMPLETED) ===
  [2026/07/23 22:35:44.236 GMT+08:00] [INFO] Job(1529980360316555264_1529980360291389447) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/63cb090b-59e5-4785-be0e-1f92475aae7e.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/63cb090b-59e5-4785-be0e-1f92475aae7e.sh
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库存在一次失败的 workflow 运行
  - 操作步骤: 对该运行依次执行 Re-run all jobs 共 3 次
  - 预期结果: 第 1-3 次 rerun 均创建新运行; 每次 rerun 的 sha/ref 与原始运行一致; 3 次新运行均 success

- **实际行为**:
  - 仅 1 个 job instance 有 log（status=COMPLETED），5 秒 sleep 正常
  - 无任何 rerun 记录——rerun_count 无法验证
  - test harness 可能未成功触发 rerun，或 rerun 的 log 未被收集
  - **失败传导链**: 原始 run 成功 → rerun 未触发或未被收集 → rerun_count 断言失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` step:
    ```yaml
    - name: sleep step
      run: |
        sleep 5
    ```
  - **GitCode 规格** `running-pipelines/rerun-failed-jobs.md` 第 11-13 行:
    1. 进入运行详情页，点击右上角 **Re-run all jobs** 按钮
    2. 系统创建一条新的运行记录，所有 job 重新执行，运行编号递增
  - **GitCode 规格** `running-pipelines/rerun-failed-jobs.md` 第 29-33 行:
    | 限制项 | 说明 |
    | 最大重试次数 | 单条运行最多重新运行 3 次 |
  - **逐项映射**: sleep 5 的快速 job 配置合理（快速完成便于验证 rerun）; 但断言期望 rerun_count=3 的前提是存在一次**失败**运行（`前置条件: 仓库存在一次失败的 workflow 运行`），而 test harness 触发的工作流是成功完成——可能需要先触发失败再 rerun。

- **环境前置条件验证**: runner 可用，job 成功完成；无 rerun 记录

**置信度**: 中（log 中无 rerun 记录，可能是 test harness 未触发 rerun 或 rerun 前置条件（失败 run）未满足）

**影响**:
- **阻塞性**: 🟡中等 — rerun 功能未被验证
- **静默性**: 🔴静默 — 无 rerun 记录或错误
- **影响面**: 🟡同用例 — 仅 rerun 用例
- **综合**: test harness 需要先创建失败 run，再对其执行 3 次 rerun——当前可能跳过了失败创建的步骤
- **是否有规避手段**: 是（手动验证 rerun 功能，或修复 test harness 的 rerun 触发逻辑）

**建议**:
- 检查 test harness 是否在触发原始 run 后正确检测 job 状态并触发 rerun
- 前置条件 "失败的 workflow 运行"——当前 log 显示 job COMPLETED（success），可能需要先触发一个会失败的 workflow 才能测试 rerun
- 考虑使用 fail step 创建初始失败运行，然后对失败运行触发 rerun
