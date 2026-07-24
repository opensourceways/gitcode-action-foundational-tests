## 失败分诊 · SEC-RUN-01-001 · Job 结束后 workspace 与临时文件必须被彻底清理

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "residual found"` — **PASS**: 未出现 "residual found"
  - 正向 `run_logs` `equals: "cleaned_as_expected"` — **PASS**: 日志显示 "cleaned as expected"

**根因初判**: 测试通过（两个 job 均 COMPLETED，job B 未发现残留文件）— 但断言器在判定阶段标记为 FAIL，可能因 runner 标签 `dedicate-hosted` 导致 job 调度不在同一 runner 上，清理隔离结果不具说服力
**责任人**: Phase 01（测试设计需改进，同一 runner 上验证更可靠）

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Write sensitive file (status=COMPLETED) ===
  [2026/07/23 22:09:32.440 GMT+08:00] [INFO] Job(1529973767860523008_1529973767831162887) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/2be5f0a1-d517-487d-b657-77309a59054d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/2be5f0a1-d517-487d-b657-77309a59054d.sh


  === JOB: Check cleanup (status=COMPLETED) ===
  [2026/07/23 22:09:32.455 GMT+08:00] [INFO] Job(1529973767860523008_1529973767835357185) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0a3ef073-dbb1-4a4c-834c-628811a1ed80.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0a3ef073-dbb1-4a4c-834c-628811a1ed80.sh
  cleaned as expected
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库支持多 job workflow
  - 操作步骤: 1. job A 写入敏感临时文件；2. job B 检查是否存在 job A 的残留文件
  - 预期结果: job B 绝不应读取到 job A 残留的敏感文件

- **实际行为**:
  - job A (Write sensitive file): 创建 `/tmp/sensitive-temp.txt`，执行无错误
  - job B (Check cleanup): 检查 `/tmp/sensitive-temp.txt` 不存在，输出 "cleaned as expected"
  - 两个 job 运行在同一主机 `slave1`，但未确认是否在同一运行时容器/pod 内
  - runner 标签 `dedicate-hosted` 可能导致两个 job 被分配到不同容器
  - **失败传导链**: 两个 job 可能不在同一文件系统空间 → job B 检测不到 job A 的文件 → "cleaned as expected" 可能是隔离而非清理的结果

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `job-a` 和 `job-b`:
    ```yaml
    jobs:
      job-a:
        name: Write sensitive file
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Write temp secret
            run: |
              echo sensitive-data > /tmp/sensitive-temp.txt
      job-b:
        name: Check cleanup
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Check no residual
            run: |
              if [ -f /tmp/sensitive-temp.txt ]; then
                echo "residual found"
                exit 1
              else
                echo "cleaned as expected"
              fi
    ```
  - **GitCode 规格** `core-concepts/workflow-job-step-action.md` 第 69-83 行:
    ```
    Job 是 Stage 内的可执行单元，被调度到一台 Runner 上运行
    ```
  - **逐项映射**:
    - `runs-on`: 两个 job 使用相同的 `[dedicate-hosted, x64, large]` 标签 — 但规格未保证两个 job 在同一文件系统实例上
    - 测试 YAML 写入 `/tmp/sensitive-temp.txt` — 若容器隔离，不同容器无法共享 /tmp
    - 规格中未明确 job 间文件系统清理的语义（是 same-container 清理还是 cross-container 隔离）

- **环境前置条件验证**: 两个 job 均正常完成；job B 确未发现残留文件

**置信度**: 低（测试表面通过但设计存在缺陷：若两个 job 在不同容器/Pod 上运行，/tmp 天然隔离，"cleaned as expected" 是隔离效果而非清理效果）

**影响**:
- **阻塞性**: 中 — 无法区分 "清理生效" 和 "容器隔离"，安全评估无说服力
- **静默性**: 极高 — 测试结果是"好的假阳性"：若清理未生效但容器隔离掩盖了问题，将造成安全隐患
- **影响面**: 中 — 影响所有 job 间隔离清理类测试
- **综合**: 两个 job 在同一 runner group 但可能在不同容器，`/tmp` 天然隔离而非事后清理；"cleaned as expected" 无法区分清理和隔离
- **是否有规避手段**: 是 — 修改测试 YAML 使用 `workspace` 目录（`$ATOMGIT_WORKSPACE`）替代 `/tmp`；或使用 `needs` 确保两个 job 在同一 runner 实例上按依赖顺序执行

**建议**:
- Phase 01: (1) 将文件写入 `$ATOMGIT_WORKSPACE` 而非 `/tmp`；(2) 使用 `needs: job-a` 确保 job B 在 job A 之后且在同一 runner 上
- 平台方: 明确文档中 job 间的文件系统语义（workspace 保留 vs 清理 vs 隔离）
