#!/usr/bin/env python3
"""Generate Security P1 cases batch 1 (masking) for Run 2026-07-21-01."""
import os

BASE = "/Users/husheng/codes/meta-projects/gitcode-action/phase01/runs/2026-07-21-01/cases"

def write_text(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def write_yaml(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# SEC-MASK-03-001: Secret echo masking
write_text(f"{BASE}/text/SEC-MASK-03-001.md", """用例 ID:   SEC-MASK-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-005
母意图:    —
标题:      Secret 值直接 echo 到日志时应被脱敏为 ***

前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 push 触发的基础 workflow

操作步骤:
  1. 在 workflow step 中通过 ${{ secrets.TEST_SECRET }} 引用 secret 并 echo 到日志
  2. 将 secret 值赋给 env 中间变量后 echo 该变量
  3. 在同一 job 内多次引用同一 secret
  4. 通过 API 拉取 job 日志全文搜索已知 secret 明文

预期结果:
  - 日志中所有出现 secret 值的位置均应被替换为 ***
  - 搜索已知 secret 明文值在日志全文中的命中数 = 0
  - env 中间变量引用的 secret 值同样被遮蔽
  - 非 secret 文本的 echo 应正常显示

验证点:
  - [负向] job 日志全文搜索 TEST_SECRET 已知明文值，命中数 = 0
  - [负向] 同一 job 内多次引用同一 secret，每次出现均应被遮蔽
  - [正向] echo 非 secret 文本时日志正常显示

清理:      none
""")

write_yaml(f"{BASE}/yaml/SEC-MASK-03-001.yaml", """id: SEC-MASK-03-001
dimensions: [security]
dimension: security
priority: P0
title: "Secret 值直接 echo 到日志时应被脱敏为 ***"
intent_ref: INTENT-SEC-005

setup:
  repo_fixture: with-secrets
  secrets: [TEST_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    mask-basic:
      name: (SEC-MASK-03-001) 验证 secret 基础脱敏
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-001) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-001) 通过表达式 echo secret
          run: echo "MASK_CHECK: ${{ secrets.TEST_SECRET }}"
        - name: (SEC-MASK-03-001) 通过 env 中间变量 echo secret
          run: echo "ENV_MASK: ${MY_SECRET}"
          env:
            MY_SECRET: ${{ secrets.TEST_SECRET }}
        - name: (SEC-MASK-03-001) 多次引用同一 secret
          run: |
            echo "REF1: ${MY_SECRET}"
            echo "REF2: ${MY_SECRET}"
            echo "REF3: ${MY_SECRET}"
          env:
            MY_SECRET: ${{ secrets.TEST_SECRET }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "job 日志全文搜索 TEST_SECRET 已知明文值，命中数 = 0"
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "多次引用同一 secret，每次出现均被遮蔽为 ***"
  - type: positive
    target: run_logs
    eval: deterministic
    rubric: "echo 非 secret 文本时日志正常显示"

teardown:
  reset: none
""")

print("SEC-MASK-03-001 done")

# SEC-MASK-03-002: base64 encoding bypass
write_text(f"{BASE}/text/SEC-MASK-03-002.md", """用例 ID:   SEC-MASK-03-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-006
母意图:    —
标题:      Secret 经过 base64 编码后 echo 到日志仍应被脱敏

前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow 中将 secret 值通过 base64 编码后 echo 到日志
  2. 将 base64 解码后的值再次 echo
  3. 通过 API 拉取 job 日志搜索原始 secret 明文和 base64 编码值

预期结果:
  - 日志中不出现未经遮蔽的 secret 原始值
  - base64 编码后的 secret 输出中，原始值不应以明文出现
  - base64 解码后的值应被遮蔽

验证点:
  - [负向] 日志全文搜索 TEST_SECRET 原始明文值，命中数 = 0
  - [负向] base64 编码后的值若直接 echo，不应泄露 secret 原始值
  - [负向] base64 解码后 echo 原始值不应在日志中以明文出现

清理:      none
""")

write_yaml(f"{BASE}/yaml/SEC-MASK-03-002.yaml", """id: SEC-MASK-03-002
dimensions: [security]
dimension: security
priority: P1
title: "Secret 经过 base64 编码后 echo 到日志仍应被脱敏"
intent_ref: INTENT-SEC-006

setup:
  repo_fixture: with-secrets
  secrets: [TEST_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    mask-b64:
      name: (SEC-MASK-03-002) 验证 base64 编码后脱敏
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-002) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-002) base64 编码后 echo
          run: |
            ENCODED=$(echo -n "${MYSEC}" | base64)
            echo "B64: ${ENCODED}"
            DECODED=$(echo -n "${ENCODED}" | base64 -d)
            echo "DECODED: ${DECODED}"
          env:
            MYSEC: ${{ secrets.TEST_SECRET }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "job 日志全文搜索 TEST_SECRET 原始明文值，命中数 = 0"
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "base64 编码和解码后的值在日志中均不泄露原始 secret"

teardown:
  reset: none
""")

print("SEC-MASK-03-002 done")

# SEC-MASK-03-003: substring concatenation bypass
write_text(f"{BASE}/text/SEC-MASK-03-003.md", """用例 ID:   SEC-MASK-03-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-007
母意图:    —
标题:      Secret 通过子字符串拼接后 echo 到日志应仍被脱敏

前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow 中将 secret 拆分为两半
  2. 通过 shell 拼接两个半段后 echo 到日志
  3. 逐字符循环拼接 secret 后 echo 到日志
  4. 通过 API 拉取 job 日志搜索原始 secret 完整值

预期结果:
  - 拼接后的完整 secret 值不应以明文出现在日志中
  - 逐字符拼接的完整值同样应被遮蔽

验证点:
  - [负向] 日志全文搜索 TEST_SECRET 完整明文值，命中数 = 0
  - [负向] 两半拼接 echo 的输出中不出现完整 secret 值
  - [负向] 逐字符拼接后 echo 的输出中不出现完整 secret 值

清理:      none
""")

write_yaml(f"{BASE}/yaml/SEC-MASK-03-003.yaml", """id: SEC-MASK-03-003
dimensions: [security]
dimension: security
priority: P1
title: "Secret 通过子字符串拼接后 echo 到日志应仍被脱敏"
intent_ref: INTENT-SEC-007

setup:
  repo_fixture: with-secrets
  secrets: [TEST_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    mask-substr:
      name: (SEC-MASK-03-003) 验证子字符串拼接后脱敏
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-003) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-003) 两半拼接 echo
          run: |
            LEN=${#MYSEC}
            HALF=$(( LEN / 2 ))
            P1="${MYSEC:0:$HALF}"
            P2="${MYSEC:$HALF}"
            echo "CONCAT: ${P1}${P2}"
          env:
            MYSEC: ${{ secrets.TEST_SECRET }}
        - name: (SEC-MASK-03-003) 逐字符拼接 echo
          run: |
            R=""
            for ((i=0; i<${#MYSEC}; i++)); do
              R="${R}${MYSEC:$i:1}"
            done
            echo "CHAR: ${R}"
          env:
            MYSEC: ${{ secrets.TEST_SECRET }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "job 日志全文搜索 TEST_SECRET 完整明文值，命中数 = 0"
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "两半拼接和逐字符拼接 echo 的输出中不出现完整 secret 值"

teardown:
  reset: none
""")

print("SEC-MASK-03-003 done")

# SEC-MASK-03-004: multiline secret masking
write_text(f"{BASE}/text/SEC-MASK-03-004.md", """用例 ID:   SEC-MASK-03-004
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-008
母意图:    —
标题:      Secret 包含多行文本时应整体被脱敏

前置条件:
  - 仓库配置了多行 secret MULTILINE_SECRET
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow 中逐行 echo 多行 secret 的各行内容
  2. 将多行 secret 整体 echo 到日志
  3. 通过 API 拉取 job 日志，逐行搜索 secret 各行内容

预期结果:
  - 多行 secret 的每一行在日志中出现时均应被遮蔽为 ***
  - 整体 echo 时各行均不应以明文出现

验证点:
  - [负向] 日志全文逐行搜索 MULTILINE_SECRET 各行值，命中数 = 0
  - [负向] 整体 echo 多行 secret 时各行的明文均不出现
  - [负向] 包含换行转义符的 secret 不应被还原为实际换行后的明文

清理:      none
""")

write_yaml(f"{BASE}/yaml/SEC-MASK-03-004.yaml", """id: SEC-MASK-03-004
dimensions: [security]
dimension: security
priority: P1
title: "Secret 包含多行文本时应整体被脱敏"
intent_ref: INTENT-SEC-008

setup:
  repo_fixture: with-secrets
  secrets: [MULTILINE_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    mask-multi:
      name: (SEC-MASK-03-004) 验证多行 secret 脱敏
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-004) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-004) 逐行 echo 多行 secret
          run: |
            echo "${MYSEC}" | while IFS= read -r L; do
              echo "LINE: ${L}"
            done
          env:
            MYSEC: ${{ secrets.MULTILINE_SECRET }}
        - name: (SEC-MASK-03-004) 整体 echo 多行 secret
          run: |
            echo "FULL_BEGIN"
            echo "${MYSEC}"
            echo "FULL_END"
          env:
            MYSEC: ${{ secrets.MULTILINE_SECRET }}

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "job 日志全文逐行搜索 MULTILINE_SECRET 各行值，命中数 = 0"
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "整体 echo 多行 secret 时各行的明文均不出现"

teardown:
  reset: none
""")

print("SEC-MASK-03-004 done")

# SEC-MASK-03-005: add-mask command safety
write_text(f"{BASE}/text/SEC-MASK-03-005.md", """用例 ID:   SEC-MASK-03-005
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-027
母意图:    —
标题:      ::add-mask:: workflow 命令的正确性与安全性

前置条件:
  - 存在 push 触发的 workflow
  - 不存在预置 secret

操作步骤:
  1. 在 workflow step 中使用 echo '::add-mask::MY_DYNAMIC_SECRET' 注册动态脱敏值
  2. 随后 echo 该动态值，观察日志中是否被遮蔽
  3. 尝试使用 ::stop-commands:: 后再 echo 该值

预期结果:
  - ::add-mask:: 注册的值在后续日志中被遮蔽为 ***
  - ::stop-commands:: 不应恢复被 mask 的值
  - add-mask 命令本身的返回值不应泄露被遮蔽前的值

验证点:
  - [正向] echo '::add-mask::VALUE' 后 echo VALUE，日志显示 ***
  - [负向] ::stop-commands:: 后 echo VALUE，仍应被遮蔽
  - [负向] add-mask 命令返回值不含要遮蔽的原始值

清理:      none
""")

write_yaml(f"{BASE}/yaml/SEC-MASK-03-005.yaml", """id: SEC-MASK-03-005
dimensions: [security]
dimension: security
priority: P1
title: "::add-mask:: workflow 命令的正确性与安全性"
intent_ref: INTENT-SEC-027

setup:
  repo_fixture: default
  secrets: []
  variables: {}
  branch_protection: default

workflow: |
  on: [push]
  jobs:
    addmask:
      name: (SEC-MASK-03-005) 验证 add-mask 命令安全性
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-005) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-005) 注册动态 mask 值
          run: |
            echo "::add-mask::DYN_SECRET_VAL_42"
            echo "MASK_REG_OK"
        - name: (SEC-MASK-03-005) echo 被 mask 的值
          run: |
            echo "DYN_SECRET_VAL_42"
            echo "AFTER_MASK"
        - name: (SEC-MASK-03-005) stop-commands 后 echo
          run: |
            echo "::stop-commands::"
            echo "DYN_SECRET_VAL_42"
            echo "AFTER_STOP"

trigger:
  event: push
  as: maintainer
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "::add-mask:: 注册后 echo 该值应被遮蔽为 ***"
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "::stop-commands:: 后 echo 该值仍应被遮蔽"
  - type: negative
    target: step_logs
    eval: deterministic
    rubric: "add-mask 命令行本身不泄露被遮蔽前的值"

teardown:
  reset: none
""")

print("SEC-MASK-03-005 done")

# SEC-MASK-03-006: mask job isolation
write_text(f"{BASE}/text/SEC-MASK-03-006.md", """用例 ID:   SEC-MASK-03-006
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-028
母意图:    —
标题:      fork PR 下 ::add-mask:: 命令注册新 mask 不应影响主分支 job

前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 fork 仓库可提交 PR

操作步骤:
  1. fork PR 的 workflow 中通过 ::add-mask:: 注册大量干扰值
  2. fork PR job 完成后，在主分支触发内部 push workflow
  3. 在内部 job 中 echo 常规文本验证 mask 表独立

预期结果:
  - fork PR job 注册的 mask 值不影响后续内部 job
  - 后续内部 job 的 mask 表应独立

验证点:
  - [负向] fork PR job 注册的 mask 值在后续内部 job 中不生效
  - [负向] fork PR job 注册大量 mask 不影响后续 job 正常日志输出

清理:      fixture
""")

write_yaml(f"{BASE}/yaml/SEC-MASK-03-006.yaml", """id: SEC-MASK-03-006
dimensions: [security]
dimension: security
priority: P1
title: "fork PR 下 ::add-mask:: 命令注册新 mask 不应影响主分支 job"
intent_ref: INTENT-SEC-028

setup:
  repo_fixture: with-fork-and-secrets
  secrets: [TEST_SECRET]
  variables: {}
  branch_protection: default

workflow: |
  on: [pull_request]
  jobs:
    fork-mask:
      name: (SEC-MASK-03-006) fork PR 注册干扰 mask
      runs-on: [ubuntu-latest, x64, small]
      steps:
        - name: (SEC-MASK-03-006) 检出代码
          uses: checkout
        - name: (SEC-MASK-03-006) 注册干扰 mask 值
          run: |
            echo "::add-mask::FORK_MASKVAL_1"
            echo "::add-mask::FORK_MASKVAL_2"
            echo "::add-mask::FORK_MASKVAL_3"
            echo "FLOOD_DONE"
        - name: (SEC-MASK-03-006) echo 干扰值
          run: |
            echo "FORK_MASKVAL_1"
            echo "FORK_MASKVAL_2"

trigger:
  event: fork_pr
  as: untrusted_contributor
  params: {}

fault_injection: null

assertions:
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "fork PR 注册的干扰 mask 值在日志中以 *** 出现"
  - type: negative
    target: run_logs
    eval: deterministic
    rubric: "后续内部 job 不受 fork PR mask 注册影响"

teardown:
  reset: fixture
""")

print("SEC-MASK-03-006 done")

print(f"\n=== Security masking batch complete (6 cases) ===")
