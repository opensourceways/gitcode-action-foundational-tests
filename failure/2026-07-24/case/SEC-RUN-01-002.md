## 失败分诊 · SEC-RUN-01-002 · Runner 环境变量与共享目录必须跨 job 隔离

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "isolation broken"` — **PASS**: 未出现
  - 正向 `run_logs` `equals: "isolated_as_expected"` — **PASS**: 日志显示 "isolated as expected"

**根因初判**: 与 SEC-RUN-01-001 相同 — 测试表面通过但可能因容器隔离而非环境隔离生效
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Set env and tmp (status=COMPLETED) ===
  [2026/07/23 22:09:43.134 GMT+08:00] [INFO] Job(1529973812697632768_1529973812668272647) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/ae32645c-6c03-4c98-8e96-718cf793d193.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/ae32645c-6c03-4c98-8e96-718cf793d193.sh


  === JOB: Check env isolation (status=COMPLETED) ===
  [2026/07/23 22:09:43.135 GMT+08:00] [INFO] Job(1529973812697632768_1529973812668272649) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/f649cccc-4a31-4695-af37-c62095ab268d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/f649cccc-4a31-4695-af37-c62095ab268d.sh
  isolated as expected
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库支持多 job workflow
  - 操作步骤: 1. job A 设置环境变量和 /tmp 文件；2. job B 检查环境变量和 /tmp 是否被污染
  - 预期结果: job B 的环境变量和共享目录为干净状态，不继承 job A 的设置

- **实际行为**:
  - job A: 通过 `$ATOMGIT_ENV` 设置 `MY_SECRET_ENV=leaked`，写入 `/tmp/env-test.txt`
  - job B: `$MY_SECRET_ENV` 为空且 `/tmp/env-test.txt` 不存在 → 输出 "isolated as expected"
  - 两个 job 几乎同时启动（时间戳差 0.001s），说明是并行执行
  - 若两个 job 在不同容器/Pod，环境隔离是容器层面而非 runner 清理
  - **失败传导链**: 并行 job 在不同容器 → 天然隔离 → "isolated as expected" 可能不是清理的效果

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `job-a-env` 和 `job-b-env`:
    ```yaml
    jobs:
      job-a-env:
        name: Set env and tmp
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Set env
            run: |
              echo MY_SECRET_ENV=leaked >> $ATOMGIT_ENV
              echo leaked-data > /tmp/env-test.txt
      job-b-env:
        name: Check env isolation
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Check env clean
            run: |
              if [ -n "$MY_SECRET_ENV" ] || [ -f /tmp/env-test.txt ]; then
                echo "isolation broken"
                exit 1
              else
                echo "isolated as expected"
              fi
    ```
  - **GitCode 规格** `runner-management/selecting-runner-labels.md`:
    ```
    自托管 runner 上应执行与官方 runner 同等级别的清理
    ```
  - **逐项映射**:
    - `$ATOMGIT_ENV`: 测试 YAML 写入此文件传递环境变量 — 此为 job 级环境变量文件
    - 两个 job 无 `needs` 声明，默认并行执行 — 并行 job 可能在不同容器实例
    - 规格未说明 `$ATOMGIT_ENV` 的隔离语义（per-job 还是共享文件）

- **环境前置条件验证**: 未发现异常；两个 job 均正常完成

**置信度**: 低（与 SEC-RUN-01-001 相同问题 — 容器级隔离混淆了清理验证）

**影响**:
- **阻塞性**: 中 — 无法区分容器隔离和清理隔离
- **静默性**: 极高 — 测试的"通过"可能是假阳性
- **影响面**: 中 — 影响 RUN 系列隔离测试
- **综合**: 并行 job 可能在不同容器中运行，环境变量和 /tmp 天然隔离；"isolated as expected" 无法证明是 runner 清理的结果
- **是否有规避手段**: 是 — 使用 `needs: job-a-env` 确保串行执行+同一 runner；或使用 workspace 目录

**建议**:
- Phase 01/02: 修改测试 YAML：(1) job-b-env 添加 `needs: job-a-env` 确保串行且同 runner；(2) 增加对照：若 `needs` 后仍隔离，说明清理生效
