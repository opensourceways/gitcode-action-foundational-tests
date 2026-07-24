#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compile_asserts.py — Phase 02 断言编译器：把 Phase01 契约 YAML 的 assertions 编译成
assertion_engine 可消费的 compiled/<case-id>.asserts.json。

定位：执行前准备（非判定）。把 rubric 里的语义翻译成引擎的确定性 kind，
最终 pass/fail 仍由 assertion_engine 确定性裁决（不违反判定铁律 §A）。

用法:
  python compile_asserts.py <phase01-run-id> <phase02-run-id> [--src-dir <path>]
  python compile_asserts.py 2026-07-23-01 2026-07-23-valid --src-dir path/to/yaml
"""

import os, sys, json, glob, re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PHASE02 = os.path.join(ROOT, "phase02")

# 从 rubric 文本提取确定性关键词（大写标识符、数字码如 403）
_KEYWORD_RE = re.compile(r'[A-Z][A-Z0-9_]{2,}(?:=\S*)?|\b[0-9]{3}\b')


def _extract_keyword(rubric_text):
    matches = _KEYWORD_RE.findall(rubric_text or "")
    return [m.strip().rstrip(",").rstrip(";") for m in matches if len(m.strip()) > 2]


def compile_one(assertion, case_id):
    """编译单条 assertion → 引擎断言 dict 或 None（needs_review）。"""
    atype = assertion.get("type", "")
    target = assertion.get("target", "")
    rubric_text = assertion.get("rubric", "")

    # ── 0) 明文值字段：不限 target，有明确值就编译 ──
    # contains / must_contain（positive）
    if atype == "positive":
        val = (assertion.get("contains") or assertion.get("must_contain"))
        if val is not None:
            return {"kind": "value", "expect": str(val)}
    # must_not_contain / must_not_equal（negative）
    if atype == "negative":
        val = (assertion.get("must_not_contain") or assertion.get("must_not_equal"))
        if val is not None:
            return {"kind": "leak", "forbidden": str(val)}
    # must_not_contain_secret / contains_masked → config_probe
    sn = (assertion.get("must_not_contain_secret") or assertion.get("contains_masked"))
    if sn is not None and sn:
        return {"kind": "config_probe"}

    # ── 1) status 家族：有 equals 字段且值为非HTTP码枚举 → run_status ──
    # ★ 近似局限：job/step 级 status 用 run 级 conclusion 近似判定（复用 run_status）。
    # 单 job / 全 job 同命运：正确。多 job 部分成功部分失败：run.conclusion 整体可能不精确。
    # 若后续发现多 job 用例判不准，需新增 job 级 kind，本期用近似换覆盖率。
    _STATUS_TARGETS = (
        "run_status", "job_status", "step_status", "step_conclusion",
        "parent_status", "api_status", "downstream_status",
        "job_a_status", "job_b_status", "rerun_result",
    )
    eq_val = assertion.get("equals")
    if target in _STATUS_TARGETS and eq_val is not None:
        eq_s = str(eq_val)
        if re.match(r"^\d{3}$", eq_s):
            return None  # HTTP 码不作为状态，留给明文值进入 needs_review
        if atype == "positive":
            return {"kind": "run_status", "equals": eq_s}
        if atype == "negative":
            not_eq = assertion.get("not_equals", eq_s)
            return {"kind": "run_status_not", "not_equals": str(not_eq)}

    # ── 1b) 原始 run_status（无 equals 时兜底）───
    if target == "run_status":
        if atype == "positive":
            val = assertion.get("equals", "COMPLETED")
            return {"kind": "run_status", "equals": str(val)}
        if atype == "negative":
            val = assertion.get("not_equals", assertion.get("equals") or "SUCCESS")
            return {"kind": "run_status_not", "not_equals": str(val)}

    # 2) run_logs（equals 字段 + 关键词提取，contains/must_not_contain 已在 §0 全局处理）
    if target == "run_logs":
        # 2a) equals（positive 用作日志内容匹配）
        if atype == "positive":
            val = assertion.get("equals")
            if val is not None:
                return {"kind": "value", "expect": str(val)}
        # 2b) eval=deterministic + rubric → extract keyword
        if assertion.get("eval") == "deterministic" and rubric_text:
            kws = _extract_keyword(rubric_text)
            if kws:
                kw = kws[0]
                if atype == "positive":
                    return {"kind": "value", "expect": kw}
                if atype == "negative":
                    return {"kind": "leak", "forbidden": kw}
        return None

    # 3) nonfunctional → 无法确定性编译
    if atype == "nonfunctional":
        return None

    return None


def main():
    if len(sys.argv) < 3:
        print("usage: compile_asserts.py <phase01-run-id> <phase02-run-id> [--src-dir <path>]")
        sys.exit(2)

    p1, p2 = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    src_dir_override = None
    if "--src-dir" in args:
        idx = args.index("--src-dir")
        src_dir_override = args[idx + 1]

    if src_dir_override:
        src_dir = src_dir_override
    else:
        src_dir = os.path.join(ROOT, "phase01", "runs", p1, "cases", "yaml")
    if not os.path.isdir(src_dir):
        print(f"找不到用例目录: {src_dir}")
        sys.exit(1)

    out_dir = os.path.join(PHASE02, "runs", p2, "compiled")
    os.makedirs(out_dir, exist_ok=True)

    compiled = 0
    compiled_asserts = 0
    needs_review = []

    for f in sorted(glob.glob(os.path.join(src_dir, "*.yaml")) +
                    glob.glob(os.path.join(src_dir, "*.yml"))):
        try:
            doc = yaml.safe_load(open(f, encoding="utf-8"))
        except yaml.YAMLError:
            continue
        cid = (doc or {}).get("id", os.path.splitext(os.path.basename(f))[0])
        asserts = doc.get("assertions", []) if isinstance(doc, dict) else []
        if not asserts:
            continue

        compiled_list = []
        for a in asserts:
            if not isinstance(a, dict):
                continue
            result = compile_one(a, cid)
            if result:
                compiled_list.append(result)
                compiled_asserts += 1
            else:
                needs_review.append({
                    "case_id": cid,
                    "assertion": {str(k): str(v) for k, v in a.items()},
                    "reason": "target 或 rubric 无确定性映射规则",
                })

        if compiled_list:
            out_path = os.path.join(out_dir, f"{cid}.asserts.json")
            json.dump({"assertions": compiled_list}, open(out_path, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=2)
            compiled += 1

    # ── compile-report ──
    print(f"compile_asserts 完成:")
    print(f"  成功编译: {compiled} 条用例（{compiled_asserts} 条断言）")
    print(f"  needs_review: {len(needs_review)} 条断言")

    if needs_review:
        review_path = os.path.join(out_dir, "_needs_review.json")
        json.dump(needs_review, open(review_path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"  needs_review 清单 → {review_path}")
        reasons = {}
        for item in needs_review:
            a = item["assertion"]
            r = f"type={a.get('type','?')} target={a.get('target','?')}"
            reasons[r] = reasons.get(r, 0) + 1
        print("  典型原因分布:")
        for r, c in sorted(reasons.items(), key=lambda x: -x[1])[:10]:
            print(f"    {c}x {r}")


if __name__ == "__main__":
    main()
