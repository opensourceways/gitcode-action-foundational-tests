import os, re, json

BASE = r"D:/业务/action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases"

text_files = sorted([f for f in os.listdir(os.path.join(BASE, "text")) if f.startswith("SEC-") and f.endswith(".md")])
yaml_files = sorted([f for f in os.listdir(os.path.join(BASE, "yaml")) if f.startswith("SEC-") and f.endswith(".yaml")])

manifest = []
p0 = p1 = p2 = 0
negative_count = 0
total_assertions = 0
intent_map = {}

for tf in text_files:
    cid = tf.replace(".md", "")
    with open(os.path.join(BASE, "text", tf), "r", encoding="utf-8") as f:
        content = f.read()
    pri = "P0"
    if "优先级:    P1" in content:
        pri = "P1"
    elif "优先级:    P2" in content:
        pri = "P2"
    intent_match = re.search(r'溯源意图:\s+(INTENT-SEC-\d+)', content)
    intent = intent_match.group(1) if intent_match else "UNKNOWN"
    title_match = re.search(r'标题:\s+(.+)', content)
    title = title_match.group(1).strip() if title_match else ""
    manifest.append({"id": cid, "intent": intent, "priority": pri, "title": title})
    intent_map.setdefault(intent, []).append(cid)
    if pri == "P0":
        p0 += 1
    elif pri == "P1":
        p1 += 1
    elif pri == "P2":
        p2 += 1

for yf in yaml_files:
    with open(os.path.join(BASE, "yaml", yf), "r", encoding="utf-8") as f:
        content = f.read()
    assertions = re.findall(r'type:\s+(negative|positive|nonfunctional)', content)
    total_assertions += len(assertions)
    negative_count += assertions.count("negative")

# Check intent coverage
all_intents = [f"INTENT-SEC-{i:03d}" for i in range(1, 37)]
covered = set(intent_map.keys())
uncovered = [i for i in all_intents if i not in covered]

with open(os.path.join(BASE, "..", "case-manifest-security.md"), "w", encoding="utf-8") as f:
    f.write("# Security 维度用例清单 (Run 2026-07-23-01)\n\n")
    f.write(f"生成用例总数: {len(manifest)}\n")
    f.write(f"P0: {p0} | P1: {p1} | P2: {p2}\n")
    f.write(f"Negative 断言数: {negative_count}/{total_assertions}\n")
    f.write(f"覆盖 intent 数: {len(covered)}/36\n\n")
    if uncovered:
        f.write(f"未覆盖 intent: {', '.join(uncovered)}\n\n")
    else:
        f.write("所有 36 条准入 intent 均已覆盖。\n\n")
    f.write("| 用例 ID | 溯源意图 | 优先级 | 标题 |\n")
    f.write("|---|---|---|---|\n")
    for item in manifest:
        f.write(f"| {item['id']} | {item['intent']} | {item['priority']} | {item['title']} |\n")

print(f"Total cases: {len(manifest)}")
print(f"P0: {p0}, P1: {p1}, P2: {p2}")
print(f"Negative assertions: {negative_count}/{total_assertions}")
print(f"Intents covered: {len(covered)}/36")
if uncovered:
    print(f"Uncovered: {uncovered}")
