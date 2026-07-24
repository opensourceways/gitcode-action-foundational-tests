## 失败分诊 · USE-CONC-01-001 · concurrency.max 配置 10 时报错应提示有效范围 1-5

**判定结果**: FAIL
**失败断言**:
- negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝 max: 10）
- nonfunctional/error_message: rubric "报错信息必须包含有效范围 1-5 或 1 到 5" — 无任何报错产生

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: concurrency max out of range (status=COMPLETED) ===
  [2026/07/23 22:41:02.663 GMT+08:00] [INFO] Job(1529981696067907584_1529981696046936071) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/ce4cdef8-2756-4284-bf72-91077196f349.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/ce4cdef8-2756-4284-bf72-91077196f349.sh
  hello
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: workflow 文件位于 .gitcode/workflows/
  - 操作步骤: 在 workflow 中配置 concurrency: max: 10
  - 预期结果: YAML 校验报错，明确说明 max 取值范围应为 1-5

- **实际行为**:
  - 平台**未进行 YAML 校验**，job 成功执行（status=COMPLETED），step 正常输出 "hello"
  - **失败传导链**: 平台 → 跳过 concurrency.max 范围校验 → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `<workflow>` 的 `concurrency` 段:
    ```yaml
    concurrency:
      max: 10
      exceed-action: QUEUE
    on:
      workflow_dispatch:
    jobs:
      bad:
        name: concurrency max out of range
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: step
            run: |
              echo "hello"
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第152-166行:
    ```yaml
    concurrency:
      enable: true
      max: 1
      exceed-action: IGNORE
    ```
  - **逐项映射**:
    - 测试 `max: 10` → 规格示例仅写 `max: 1`，但**未在规格中显式声明取值范围 1-5**；文档缺漏
    - 测试 `exceed-action: QUEUE` → 规格 `exceed-action: IGNORE`；QUEUE 是有效选项（其他文档页提及），参数值匹配
    - 平台对 `max: 10` 采取静默放行策略，未对超范围值报错

- **环境前置条件验证**: workflow 在 .gitcode/workflows/ 下，触发为 workflow_dispatch，Runner 标签 [dedicate-hosted, x64, large]

**置信度**: 高（日志明确显示 job 成功完成但预期应被拒绝；规格中确实未声明 max 范围约束）

**影响**:
- **阻塞性**: 🔴 用户配置 concurrency.max 超出平台内部限制后完全无反馈，后续重试/并发行为不可预期
- **静默性**: 🔴 完全静默 — 无 WARNING、无 ERROR、无 INFO 提示
- **影响面**: 🟡 所有配置了 concurrency 的 workflow（尤其是从 GitHub Actions 迁移用户，GitHub 无 max 概念）
- **综合**: 用户配置超范围 concurrency.max 值会被静默接受但运行时行为不确定
- **是否有规避手段**: 否

**建议**:
- 平台方应在 YAML 校验层增加 concurrency.max 范围校验 [1, 5]
- 建议同时补全 configure-jobs.md 文档，显式声明 max 取值范围 1-5 及超出策略
- 短期可在 CI/CD 模版中附加注释提示 max 有效范围为 1-5
