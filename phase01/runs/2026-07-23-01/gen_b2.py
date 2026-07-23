import os, json

BASE = r"D:/业务/action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases"

def write_text(cid, body):
    with open(os.path.join(BASE, "text", cid + ".md"), "w", encoding="utf-8") as f:
        f.write(body)

def write_yaml(cid, body):
    with open(os.path.join(BASE, "yaml", cid + ".yaml"), "w", encoding="utf-8") as f:
        f.write(body)

def build_yaml(cid, dims, dim, pri, title, intent, setup, trigger, wf, assertions, teardown, fault=None):
    lines = []
    lines.append("id: " + cid)
    lines.append("dimensions: " + json.dumps(dims))
    lines.append("dimension: " + dim)
    lines.append("priority: " + pri)
    lines.append('title: "' + title + '"')
    lines.append("intent_ref: " + intent)
    lines.append("setup:")
    lines.append("  repo_fixture: " + setup.get("repo_fixture", "default"))
    if setup.get("secrets"):
        lines.append("  secrets: " + json.dumps(setup["secrets"]))
    lines.append("workflow: |")
    for wl in wf.split("\n"):
        lines.append("  " + wl)
    lines.append("trigger:")
    lines.append("  event: " + trigger["event"])
    lines.append("  as: " + trigger["as"])
    lines.append("  params: " + json.dumps(trigger.get("params", {})))
    lines.append("fault_injection: null")
    lines.append("assertions:")
    for a in assertions:
        lines.append("  - type: " + a["type"])
        lines.append("    target: " + a["target"])
        for k, v in a.items():
            if k in ("type", "target"):
                continue
            lines.append("    " + k + ": " + json.dumps(v))
    lines.append("teardown:")
    lines.append("  reset: " + teardown)
    return "\n".join(lines) + "\n"

# SEC-004-a mask log
write_text("SEC-MASK-01-001",
"""用例 ID:   SEC-MASK-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-004
母意图:    —
标题:      Secret 值在运行日志中必须被自动脱敏为 ***

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN

操作步骤:
  1. 提交一个 workflow，在 run 步骤中直接 echo secrets.DEPLOY_TOKEN
  2. 触发 workflow 并查看运行日志

预期结果:
  - 日志中 DEPLOY_TOKEN 的原值被替换为 ***
  - 日志全文搜索 DEPLOY_TOKEN 原值命中数为 0

验证点:
  - [负向] 日志中绝不应出现 DEPLOY_TOKEN 原值
  - [正向] 脱敏标记 *** 出现在对应位置

清理:      重置 fixture 仓库
""")

write_yaml("SEC-MASK-01-001", build_yaml(
    "SEC-MASK-01-001", ["security"], "security", "P0",
    "Secret 值在运行日志中必须被自动脱敏为 ***", "INTENT-SEC-004",
    {"repo_fixture": "with-secrets", "secrets": ["DEPLOY_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  mask-test:\n    name: Test log masking\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Echo secret directly\n        run: |\n          echo \"The secret is ${{ secrets.DEPLOY_TOKEN }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "DEPLOY_TOKEN"},
        {"type": "positive", "target": "run_logs", "equals": "masked_with_asterisks"}
    ],
    "fixture"
))

# SEC-004-b mask summary
write_text("SEC-MASK-01-002",
"""用例 ID:   SEC-MASK-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-004
母意图:    SEC-MASK-01-001
标题:      Secret 值在 step summary 和错误堆栈中必须被脱敏

前置条件:
  - 仓库配置了 secret API_KEY

操作步骤:
  1. 提交一个 workflow，将 secrets.API_KEY 写入 ATOMGIT_STEP_SUMMARY
  2. 触发 workflow 并查看 step summary 与日志

预期结果:
  - step summary 中 API_KEY 的原值被替换为 ***
  - 若步骤失败产生堆栈，堆栈中亦不应出现原值

验证点:
  - [负向] step summary 不含 API_KEY 原值
  - [负向] 错误堆栈不含 API_KEY 原值

清理:      重置 fixture 仓库
""")

write_yaml("SEC-MASK-01-002", build_yaml(
    "SEC-MASK-01-002", ["security"], "security", "P0",
    "Secret 值在 step summary 和错误堆栈中必须被脱敏", "INTENT-SEC-004",
    {"repo_fixture": "with-secrets", "secrets": ["API_KEY"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  summary-mask:\n    name: Test summary masking\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Write secret to summary\n        run: |\n          echo \"Key: ${{ secrets.API_KEY }}\" >> $ATOMGIT_STEP_SUMMARY\n      - name: Intentionally fail\n        run: |\n          echo \"Failing with key ${{ secrets.API_KEY }}\"\n          exit 1",
    [
        {"type": "negative", "target": "step_summary", "must_not_contain_secret": "API_KEY"},
        {"type": "negative", "target": "error_stack", "must_not_contain_secret": "API_KEY"}
    ],
    "fixture"
))

# SEC-005 base64
write_text("SEC-MASK-01-003",
"""用例 ID:   SEC-MASK-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-005
母意图:    —
标题:      Secret 日志脱敏不可通过 base64 编码绕过

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN

操作步骤:
  1. 提交一个 workflow，在 job 中对 secret 做 base64 编码后再输出到日志
  2. 触发 workflow 并查看运行日志

预期结果:
  - base64 编码后的 secret 值不应以明文形式出现在日志中
  - 系统应能识别编码后的 secret 并执行脱敏

验证点:
  - [负向] 日志中绝不应出现 base64 编码后的 DEPLOY_TOKEN
  - [非功能] 脱敏机制应覆盖常见编码变换

清理:      重置 fixture 仓库
""")

write_yaml("SEC-MASK-01-003", build_yaml(
    "SEC-MASK-01-003", ["security"], "security", "P0",
    "Secret 日志脱敏不可通过 base64 编码绕过", "INTENT-SEC-005",
    {"repo_fixture": "with-secrets", "secrets": ["DEPLOY_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  b64-bypass:\n    name: Test base64 bypass\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Encode and echo secret\n        run: |\n          encoded=$(echo -n \"${{ secrets.DEPLOY_TOKEN }}\" | base64)\n          echo \"encoded=$encoded\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "DEPLOY_TOKEN"},
        {"type": "negative", "target": "run_logs", "eval": "llm_assisted", "rubric": "日志中 base64 编码后的字符串与 secret 原值存在一一对应关系时应被遮蔽"}
    ],
    "fixture"
))

# SEC-006 concat
write_text("SEC-MASK-01-004",
"""用例 ID:   SEC-MASK-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-006
母意图:    —
标题:      Secret 日志脱敏不可通过字符串拼接或插值绕过

前置条件:
  - 仓库配置了 secret API_KEY

操作步骤:
  1. 提交一个 workflow，将 secret 拆分为多段通过字符串拼接输出
  2. 触发 workflow 并查看运行日志

预期结果:
  - 拼接后的 secret 值不应以可还原形式出现在日志中
  - 即使分多行、多步骤输出，也应保持脱敏一致性

验证点:
  - [负向] 拼接后的 secret 值绝不应以可还原形式出现在日志中
  - [非功能] 即使分多行输出也应保持脱敏

清理:      重置 fixture 仓库
""")

write_yaml("SEC-MASK-01-004", build_yaml(
    "SEC-MASK-01-004", ["security"], "security", "P0",
    "Secret 日志脱敏不可通过字符串拼接或插值绕过", "INTENT-SEC-006",
    {"repo_fixture": "with-secrets", "secrets": ["API_KEY"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  concat-bypass:\n    name: Test concat bypass\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Echo secret in parts\n        run: |\n          part1=$(echo \"${{ secrets.API_KEY }}\" | cut -c1-4)\n          part2=$(echo \"${{ secrets.API_KEY }}\" | cut -c5-8)\n          echo \"part1=$part1 part2=$part2\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "API_KEY"},
        {"type": "negative", "target": "run_logs", "eval": "llm_assisted", "rubric": "日志全文搜索 secret 的任意连续子串（长度超过阈值）命中数为 0"}
    ],
    "fixture"
))

print("b2 done")
