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

write_text("SEC-WCMD-01-003",
"""用例 ID:   SEC-WCMD-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-030
母意图:    —
标题:      ATOMGIT_ENV 不被不可信输入污染提权

前置条件:
  - 仓库支持 workflow 环境变量注入

操作步骤:
  1. 提交一个 workflow，将含换行/协议控制字符的不可信值写入 ATOMGIT_ENV
  2. 触发 workflow 并检查后续 step 的环境变量

预期结果:
  - 不可信值写入 ATOMGIT_ENV 时不应注入额外环境变量
  - 多行/换行注入被安全处理

验证点:
  - [负向] 含换行/协议控制字符的不可信值写入 ATOMGIT_ENV 时，不应注入计划外的环境变量
  - [非功能] 多行值应经随机 delimiter 等机制安全写入

清理:      重置 fixture 仓库
""")

write_yaml("SEC-WCMD-01-003", build_yaml(
    "SEC-WCMD-01-003", ["security"], "security", "P0",
    "ATOMGIT_ENV 不被不可信输入污染提权", "INTENT-SEC-030",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  env-injection:\n    name: Test ATOMGIT_ENV injection\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Write malicious env\n        run: |\n          echo \"MY_VAR=good\nINJECTED_VAR=bad\" >> $ATOMGIT_ENV\n      - name: Check no injection\n        run: |\n          if [ -n \"$INJECTED_VAR\" ]; then\n            echo \"injection succeeded\"\n            exit 1\n          else\n            echo \"no injection\"\n          fi",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "injection succeeded"},
        {"type": "positive", "target": "run_logs", "equals": "no injection"}
    ],
    "fixture"
))

write_text("SEC-WCMD-01-004",
"""用例 ID:   SEC-WCMD-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-030
母意图:    SEC-WCMD-01-003
标题:      ATOMGIT_OUTPUT 不被不可信输入污染提权

前置条件:
  - 仓库支持 workflow output 传递

操作步骤:
  1. 提交一个 workflow，将含换行/协议控制字符的不可信值写入 ATOMGIT_OUTPUT
  2. 触发 workflow 并检查后续 step 的 output

预期结果:
  - 不可信值写入 ATOMGIT_OUTPUT 时不应注入额外 output 条目
  - 后续 step 不应读取到被劫持的 output

验证点:
  - [负向] 含换行/协议控制字符的不可信值写入 ATOMGIT_OUTPUT 时，不应注入计划外的 output 条目
  - [非功能] 多行值应经安全机制写入

清理:      重置 fixture 仓库
""")

write_yaml("SEC-WCMD-01-004", build_yaml(
    "SEC-WCMD-01-004", ["security"], "security", "P0",
    "ATOMGIT_OUTPUT 不被不可信输入污染提权", "INTENT-SEC-030",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  output-injection:\n    name: Test ATOMGIT_OUTPUT injection\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Write malicious output\n        id: bad\n        run: |\n          echo \"result=good\nhijacked=bad\" >> $ATOMGIT_OUTPUT\n      - name: Check no hijack\n        run: |\n          if [ \"${{ steps.bad.outputs.hijacked }}\" = \"bad\" ]; then\n            echo \"hijack succeeded\"\n            exit 1\n          else\n            echo \"no hijack\"\n          fi",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "hijack succeeded"},
        {"type": "positive", "target": "run_logs", "equals": "no hijack"}
    ],
    "fixture"
))

write_text("SEC-TOCTOU-01-001",
"""用例 ID:   SEC-TOCTOU-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-031
母意图:    —
标题:      审批后推送新 commit 不应被已授权特权运行执行

前置条件:
  - 仓库配置了审批触发 workflow

操作步骤:
  1. 管理员审批一个 workflow 运行
  2. 在审批后、执行前，攻击者推送恶意 commit
  3. 观察特权运行是否执行了新 commit

预期结果:
  - 特权运行应绑定审批时刻的具体 commit SHA
  - 审批后推送的新 commit 不应被已授权的特权运行自动采用

验证点:
  - [负向] 审批后推送的恶意代码绝不应被已授权特权运行执行
  - [正向] 特权运行执行的 commit 与审批时锁定的 SHA 一致

清理:      重置 fixture 仓库
""")

write_yaml("SEC-TOCTOU-01-001", build_yaml(
    "SEC-TOCTOU-01-001", ["security"], "security", "P0",
    "审批后推送新 commit 不应被已授权特权运行执行", "INTENT-SEC-031",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  toctou-test:\n    name: Test TOCTOU protection\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Check commit SHA\n        run: |\n          echo \"Running commit: ${{ atomgit.sha }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "unapproved_commit_executed"},
        {"type": "positive", "target": "run_logs", "equals": "approved_sha_matched"}
    ],
    "fixture"
))

print("b11 done")
