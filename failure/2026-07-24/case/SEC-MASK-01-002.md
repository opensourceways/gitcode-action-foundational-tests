## 失败分诊 · SEC-MASK-01-002 · Secret 值在 step summary 和错误堆栈中必须被脱敏

**判定结果**: FAIL
**失败断言**:
  - 负向 `step_summary` `must_not_contain_secret: "API_KEY"` — 无法验证: step summary 未产生可验证的明文泄露
  - 负向 `error_stack` `must_not_contain_secret: "API_KEY"` — 无法判定: 错误输出 "Failing with key " 后为空

**根因初判**: 环境问题（secret API_KEY 可能为空或未注入，且断言器无法检查 error_stack 目标）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test summary masking (status=FAILED) ===
  [2026/07/23 22:06:57.709 GMT+08:00] [INFO] Job(1529973118867476480_1529973118842310663) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/11ffd625-7ee1-4a2b-8f49-3b4fddc20001.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/11ffd625-7ee1-4a2b-8f49-3b4fddc20001.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9cb3636a-c161-490a-95cb-ab53c2167329.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9cb3636a-c161-490a-95cb-ab53c2167329.sh
  Failing with key 
  ::error::Process exited with code 1
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库配置了 secret API_KEY
  - 操作步骤: 1. 提交 workflow，将 secrets.API_KEY 写入 ATOMGIT_STEP_SUMMARY；2. 查看 step summary 与日志
  - 预期结果: step summary 中 API_KEY 原值被替换为 `***`；错误堆栈中亦不应出现原值

- **实际行为**:
  - Step 1（Write secret to summary）: 无输出（日志为空行），secret 写入 ATOMGIT_STEP_SUMMARY 结果不可见
  - Step 2（Intentionally fail）: 输出 "Failing with key " 后为空，API_KEY 值未显示
  - Job 最终 status=FAILED（因 exit 1），但两个步骤中的 API_KEY 值均为空
  - **失败传导链**: `${{ secrets.API_KEY }}` 求值为空 → step summary 与 error stack 中均无明文泄露 → 无法验证脱敏是否生效

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `summary-mask` 的 `Write secret to summary` 和 `Intentionally fail`:
    ```yaml
    jobs:
      summary-mask:
        name: Test summary masking
        steps:
          - name: Write secret to summary
            run: |
              echo "Key: ${{ secrets.API_KEY }}" >> $ATOMGIT_STEP_SUMMARY
          - name: Intentionally fail
            run: |
              echo "Failing with key ${{ secrets.API_KEY }}"
              exit 1
    ```
  - **GitCode 规格** `core-concepts/variables-secrets-context-expressions.md` 第 10-16 行:
    ```
    | `secrets` | Passwords, tokens, private keys | Yes | `${{ secrets.NAME }}` |
    ```
  - **逐项映射**:
    - `${{ secrets.API_KEY }}`: 测试 YAML 在两个步骤中引用 secret — 匹配规格
    - `$ATOMGIT_STEP_SUMMARY`: 测试 YAML 写入 step summary 环境变量 — 此为平台提供的变量，规格未明确说明其脱敏行为
    - 测试 YAML 通过 `exit 1` 人为制造失败，触发错误堆栈

- **环境前置条件验证**: **FAIL** — `${{ secrets.API_KEY }}` 求值为空，所有输出中 secret 值均为空白。符合"Secret/token empty in logs + no config_probe → 环境问题 (Phase 02)"规则

**置信度**: 高（secret 值为空，与 SEC-MASK-01-001 相同的根因）

**影响**:
- **阻塞性**: 中 — 与 SEC-MASK-01-001 相同，依赖 secret 注入前置
- **静默性**: 高 — 无法验证脱敏效果
- **影响面**: 中 — 影响 MASKS 系列用例
- **综合**: secret API_KEY 未注入，两个步骤中 secret 值均为空，无法验证 step summary 和 error stack 的脱敏行为
- **是否有规避手段**: 是 — 修复 secret 注入后重新测试

**建议**:
- Phase 02: 与 SEC-MASK-01-001 共享根因修复 — 验证 secret 注入配置
- Phase 01: 在 step summary 写入后增加 `cat $ATOMGIT_STEP_SUMMARY` 步骤以读取并验证 summary 内容
