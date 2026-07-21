#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_batch.py — Phase 02 批量执行器（确定性；slash 命令与 CI 共用入口）

读 queue.json，逐条调 run_case.py 真跑。**每条前后更新 state.json**，使 status.py
可在执行中途读到进度（done/total/current）。编译产物（compiled/）由上游 yaml-compiler
产出——本脚本不编译；缺编译产物的用例 run_case 会判 NOT_CONFIGURED。

用法:
  python run_batch.py <phase02-run-id> [--no-logs] [--only c1,c2]
  例: python run_batch.py 2026-07-21-10

CI 友好：不依赖 Claude，消费已入库的 compiled/ 产物即可 headless 运行。
"""
import os
import sys
import json
import time
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PHASE02 = os.path.dirname(HERE)
ROOT = os.path.dirname(PHASE02)


def _load(path, default=None):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else default


def _write_state(run_dir, state):
    json.dump(state, open(os.path.join(run_dir, "state.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def _update_run_md(run_dir, run_id, state):
    with open(os.path.join(run_dir, "run.md"), "w", encoding="utf-8") as f:
        f.write(f"# Phase 02 Run {run_id}\n\n")
        f.write(f"- 状态: {state['status']}\n")
        f.write(f"- 进度: {state['done']}/{state['total']}"
                + (f"（当前: {state['current']}）" if state.get("current") else "") + "\n")
        v = state.get("verdicts", {})
        if v:
            f.write("- 判定累计: " + " · ".join(f"{k}={n}" for k, n in v.items()) + "\n")


def main():
    if len(sys.argv) < 2:
        print("usage: run_batch.py <phase02-run-id> [--no-logs] [--only c1,c2]")
        sys.exit(2)
    run_id = sys.argv[1]
    args = sys.argv[2:]
    no_logs = "--no-logs" in args
    only = None
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))

    run_dir = os.path.join(PHASE02, "runs", run_id)
    queue = _load(os.path.join(run_dir, "queue.json"))
    if not queue:
        print(f"缺 queue.json（先跑 schema_check.py）: runs/{run_id}/")
        sys.exit(1)
    cases = [c for c in queue["cases"] if not only or c["case_id"] in only]

    state = {"status": "running", "total": len(cases), "done": 0,
             "current": None, "verdicts": {}, "started": time.strftime("%H:%M:%S")}
    _write_state(run_dir, state)
    _update_run_md(run_dir, run_id, state)
    print(f"=== 批量执行 {run_id} · {len(cases)} 条 ===")

    for i, c in enumerate(cases, 1):
        cid, contract = c["case_id"], os.path.join(ROOT, c["contract_path"])
        state["current"] = f"{cid} ({i}/{len(cases)})"
        _write_state(run_dir, state)
        _update_run_md(run_dir, run_id, state)
        print(f"[{i}/{len(cases)}] {cid} ...")

        cmd = [sys.executable, os.path.join(HERE, "run_case.py"), contract, run_id]
        if no_logs:
            cmd.append("--no-logs")
        env = dict(os.environ, PYTHONUTF8="1")
        subprocess.run(cmd, env=env)

        # run_case 已把结果并入 summary.json；从中读回本条判定
        summ = _load(os.path.join(run_dir, "summary.json"), {"records": []})
        rec = next((r for r in summ["records"] if r["case_id"] == cid), None)
        v = rec["verdict"] if rec else "NO_RESULT"
        state["verdicts"][v] = state["verdicts"].get(v, 0) + 1
        state["done"] = i
        state["current"] = None
        _write_state(run_dir, state)
        _update_run_md(run_dir, run_id, state)

    state["status"] = "completed"
    _write_state(run_dir, state)
    _update_run_md(run_dir, run_id, state)
    print(f"=== 完成 · " + " · ".join(f"{k}={n}" for k, n in state["verdicts"].items()) + " ===")


if __name__ == "__main__":
    main()
