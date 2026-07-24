## 失败分诊 · USE-LOG-01-001 · 多 step 日志按时间线组织且边界清晰

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_logs) — 期望日志含 `"step one prepare"`（YAML 中 step 的 name 字段），实际日志含 `"prepare done"`（step 内 shell echo 的输出内容），两者的字符串内容不匹配

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（26 行）:
  ```
  === JOB: multi step log clarity (status=COMPLETED) ===
  [2026/07/23 22:43:59.466 GMT+08:00] [INFO] Job(1529982437490958336_1529982437461598215) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/094b1d2f-6eda-40d5-ae7f-7e1d27197e8c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/094b1d2f-6eda-40d5-ae7f-7e1d27197e8c.sh
  prepare done

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/bfaddf8f-5d2a-492b-bca1-e16a551ee496.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/bfaddf8f-5d2a-492b-bca1-e16a551ee496.sh
  build done

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/d9c3725c-5b35-464a-a324-54d4823ef44f.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/d9c3725c-5b35-464a-a324-54d4823ef44f.sh
  test done

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/625bd794-2d31-4d11-ab4a-4bdc7dd27ec6.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/625bd794-2d31-4d11-ab4a-4bdc7dd27ec6.sh
  package done

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4b2214c4-1be7-4ac9-bd8b-8c7acae4c313.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4b2214c4-1be7-4ac9-bd8b-8c7acae4c313.sh
  summary done
  ```
  5 个 step 按定义顺序成功执行，各自产出了日志输出（`prepare done`, `build done`, `test done`, `package done`, `summary done`）。每个 step 之间有明确的日志段分隔（新脚本创建和执行行）。Job 状态为 COMPLETED。

- **预期行为**（Phase 01 文本用例 `USE-LOG-01-001`，优先级 P1，维度 usability）:
  - 操作步骤 1: "触发一个含 5 个以上 steps 的 workflow"
  - 操作步骤 2: "在日志面板查看组织方式"
  - 预期结果: "step 按定义顺序排列，含时间戳前缀，长输出可折叠"
  - 验证点: "[正向] 日志面板中 step 按定义顺序排列，step 名称与 workflow 中 name 一致"

- **实际行为**:
  - 5 个 step 按定义顺序执行，时间线组织正确，平台行为符合预期。但断言关键词 `"step one prepare"` 是测试 YAML 中 step 的 `name` 字段值（metadata），而实际 runner 日志输出的是 step 内 `run` 的 shell 标准输出内容（`"prepare done"`）。断言错误地期望 YAML 元数据字段出现在 shell stdout 中，导致假失败。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `multi-step` job 的步骤定义:
    ```yaml
    steps:
      - name: step one prepare
        run: |
          echo "prepare done"
      - name: step two build
        run: |
          echo "build done"
      ...
    ```
    断言 assertions[0] 检查 `run_logs contains "step one prepare"`，但 runner 日志仅包含 shell stdout（`"prepare done"`），不包含 YAML 字段 `name` 的字符串值。
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/running-pipelines/view-job-logs.md` 第 17-27 行的日志结构说明:
    ```
    ── Job: compile ({ubuntu-24,x64,small})
    ├── Step 1: Checkout repository        ← run: git checkout
    ├── Step 2: Set up toolchain           ← uses: action-setup-toolchain
    ```
    文档展示的日志结构以 step 编号和名称标识边界，step name 在运行日志中有显示，但断言检查的目标是 `run_logs`（shell stdout 文本），而非 UI 渲染层级的 step 标签。

**置信度**: 高（日志 26 行全量证实 5 个 step 全部成功执行且按序排列，断言关键词 `"step one prepare"` 与 shell stdout 输出 `"prepare done"` 的字符串不匹配是典型的标记词汇错误）

**建议**:
- 修改断言关键词为 shell 输出内容：将 `"step one prepare"` 改为 `"prepare done"`（对应 step 1）、`"step two build"` 改为 `"build done"`（对应 step 2），逐一覆盖所有 5 个 step
- 若需验证 step name 在日志中可见，应使用 `nonfunctional: ui_layout` 的 LLM 评估（已存在于 assertions[1]），而非在 `run_logs` 文本中搜索
- 相关用例: 无直接 sibling（唯一的多 step 日志用例）
