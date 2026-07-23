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

write_text("SEC-CACHE-01-001",
"""用例 ID:   SEC-CACHE-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-018
母意图:    —
标题:      fork PR 写入的 cache 必须不可被主仓后续 workflow 读取

前置条件:
  - 仓库配置了 cache

操作步骤:
  1. 以 fork 贡献者身份提交一个写入 cache 的 workflow
  2. 在主仓提交一个读取相同 cache key 的 workflow

预期结果:
  - 主仓 workflow 的 cache restore 不应命中 fork PR 写入的缓存
  - 缓存键应带仓库级隔离前缀

验证点:
  - [负向] 主仓 workflow 在 fork PR 写入 cache 后，绝不应命中到该缓存
  - [非功能] 缓存命中率监控应显示跨仓库命中为 0

清理:      重置 fixture 仓库
""")

write_yaml("SEC-CACHE-01-001", build_yaml(
    "SEC-CACHE-01-001", ["security"], "security", "P0",
    "fork PR 写入的 cache 必须不可被主仓后续 workflow 读取", "INTENT-SEC-018",
    {"repo_fixture": "with-cache", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request", "as": "untrusted_contributor", "params": {}},
    "on:\n  pull_request:\n    branches: [main]\njobs:\n  cache-write:\n    name: Write cache from fork\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Write cache\n        uses: cache\n        with:\n          path: ./node_modules\n          key: test-cache-key",
    [
        {"type": "negative", "target": "cache_restore", "must_not_hit": "fork_cache_key"},
        {"type": "positive", "target": "run_status", "equals": "completed"}
    ],
    "fixture"
))

write_text("SEC-CACHE-01-002",
"""用例 ID:   SEC-CACHE-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-018
母意图:    SEC-CACHE-01-001
标题:      主仓 cache restore 对 fork cache miss

前置条件:
  - fork PR 已写入 cache

操作步骤:
  1. 在主仓触发 workflow，使用与 fork PR 相同的 cache key 尝试 restore
  2. 查看 restore 结果

预期结果:
  - cache restore 结果为 miss
  - 日志中显示未找到对应缓存

验证点:
  - [负向] 主仓绝不应命中 fork PR 的缓存
  - [正向] cache restore 返回 miss

清理:      重置 fixture 仓库
""")

write_yaml("SEC-CACHE-01-002", build_yaml(
    "SEC-CACHE-01-002", ["security"], "security", "P0",
    "主仓 cache restore 对 fork cache miss", "INTENT-SEC-018",
    {"repo_fixture": "with-cache", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  cache-restore:\n    name: Restore cache from main repo\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Restore cache\n        uses: cache\n        with:\n          path: ./node_modules\n          key: test-cache-key",
    [
        {"type": "negative", "target": "cache_restore", "must_not_hit": "fork_cache_key"},
        {"type": "positive", "target": "run_logs", "equals": "cache_miss"}
    ],
    "fixture"
))

write_text("SEC-ARTF-01-001",
"""用例 ID:   SEC-ARTF-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-019
母意图:    —
标题:      fork PR 上传的 artifact 必须不可被主仓 workflow 下载或执行

前置条件:
  - 仓库支持 artifact 上传下载

操作步骤:
  1. 以 fork 贡献者身份提交一个上传 artifact 的 workflow
  2. 在主仓尝试下载该 artifact

预期结果:
  - 主仓不可通过 artifact ID 下载 fork PR 的 artifact
  - 跨仓库 artifact 下载应返回 404 或权限拒绝

验证点:
  - [负向] 主仓 workflow 绝不应能下载到 fork PR 上传的 artifact
  - [非功能] 跨仓库 artifact 下载应返回 404 或权限拒绝，不应静默返回空包

清理:      重置 fixture 仓库
""")

write_yaml("SEC-ARTF-01-001", build_yaml(
    "SEC-ARTF-01-001", ["security"], "security", "P0",
    "fork PR 上传的 artifact 必须不可被主仓 workflow 下载或执行", "INTENT-SEC-019",
    {"repo_fixture": "with-artifacts", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request", "as": "untrusted_contributor", "params": {}},
    "on:\n  pull_request:\n    branches: [main]\njobs:\n  artifact-upload:\n    name: Upload artifact from fork\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Create file\n        run: |\n          echo fork content > fork-artifact.txt\n      - name: Upload artifact\n        uses: upload-artifact\n        with:\n          name: fork-artifact\n          path: fork-artifact.txt",
    [
        {"type": "negative", "target": "artifact_download", "must_not_equal": "success"},
        {"type": "positive", "target": "artifact_download", "equals": "404_or_permission_denied"}
    ],
    "fixture"
))

print("b6b done")
