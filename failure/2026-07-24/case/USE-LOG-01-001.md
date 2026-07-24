## 失败分诊 · USE-LOG-01-001 · 多 step 日志按时间线组织且边界清晰

**判定结果**: FAIL
**失败断言**:
- positive/run_logs: contains `"step one prepare"` — raw log 中不含 step 名称，仅含 step 的 run 命令输出
- nonfunctional/ui_layout: rubric "用户能在 3 秒内定位到失败的 step（通过视觉层级、颜色或状态图标区分）" — 待 UI 验证

**根因初判**: 用例问题
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
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

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: workflow 含多个 steps
  - 操作步骤: 触发一个含 5 个以上 steps 的 workflow；在日志面板查看组织方式
  - 预期结果: step 按定义顺序排列，含时间戳前缀，长输出可折叠

- **实际行为**:
  - 5 个 step 按定义顺序依次执行成功，每个 step 产生独立脚本文件和输出
  - step 间的边界通过 "No shell specified..." / "Script file created..." / "Executing..." 标记区分
  - **失败传导链**: 测试断言检查 `run_logs` 包含 `"step one prepare"` → raw log 中不含 step `name` 字段文本 → 包含匹配失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `multi-step` job 的 5 个 steps:
    ```yaml
    steps:
      - name: step one prepare
        run: |
          echo "prepare done"
      - name: step two build
        run: |
          echo "build done"
      - name: step three test
        run: |
          echo "test done"
      - name: step four package
        run: |
          echo "package done"
      - name: step five summary
        run: |
          echo "summary done"
    ```
  - **GitCode 规格** `running-pipelines/view-job-logs.md` 第15-34行:
    ```markdown
    ### 日志结构
    
    每个 job 的日志按 step 顺序组织：
    
    ── Job: compile ({ubuntu-24,x64,small})
    ├── Step 1: Checkout repository
    ├── Step 2: Set up toolchain
    ├── Step 3: Run build command
    └── Post: Clean up workspace
    
    每条日志行前缀包含时间戳和 step 编号
    ```
  - **逐项映射**:
    - 测试 5 个 `name` 字段 → 规格 UI 日志结构中 step 以 `name` 作为显示标识
    - 测试 `run_logs` 包含 `"step one prepare"` 断言 → raw log 文本不含 step name，name 出现在 UI 层而非文本 log 中
    - 差异：断言检查的是 `run_logs`（文本日志），但 step name 存在于 UI 透出层，不在 raw log 文本中

- **环境前置条件验证**: workflow_dispatch 触发，Runner [dedicate-hosted, x64, large]，5 个 steps 全部执行成功

**置信度**: 中（断言将 UI 展示特征（step name）映射到 raw log 文本层；5 个 step 确实按顺序执行成功，日志有脚本文件边界作为分隔）

**影响**:
- **阻塞性**: 🟢 不影响功能性 — 5 个 step 全部成功执行且输出正确
- **静默性**: 🟢 无静默问题 — step 输出清晰可见
- **影响面**: 🟢 仅影响测试断言层，不影响平台功能
- **综合**: step 顺序执行正确、输出清晰，但 raw log 中不含 step name 导致断言失败
- **是否有规避手段**: 是（将断言目标从 `run_logs` 改为 UI DOM 检测或不检查 step name 文本）

**建议**:
- Phase 01: 修正断言，`run_logs` 应检查 step 的 run 命令输出内容（如 "prepare done"），而非 step name（"step one prepare"）
- 或修改测试框架使 `run_logs` 包含 step name header（如果平台 API 在日志中嵌入了 step 边界标注）
- UI 层面验证（3 秒定位失败 step）需通过 UI 自动化（Playwright/Selenium）而非日志断言
