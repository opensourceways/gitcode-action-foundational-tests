#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pool_scheduler.py — Phase 02 多仓队列并发调度器（确定性）

读 queue.json → 按 pool-config.yaml 分发到 N 仓并发执行 → batch_end teardown。
不改变任何现有组件的对外契约。落库格式 100% 复用 run_case.write_result/update_summary。

用法:
  python pool_scheduler.py <phase02-run-id> [--only c1,c2] [--no-logs]
  例: python pool_scheduler.py 2026-07-22-t1

设计原则（施工契约第0节）:
  1. 判定铁律：pass/fail 只由 assertion_engine.evaluate() 裁决。
  2. 不改现有组件对外契约。
  3. 参数化正解 = 每仓一个 RunnerConfig，现有函数零改动。
  4. 配置驱动：仓数/容量/命名/轮询参数全来自 pool-config.yaml。
"""

import os
import sys
import json
import time
from contextlib import ExitStack
from concurrent.futures import ThreadPoolExecutor

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
PHASE02 = os.path.dirname(HERE)
ROOT = os.path.dirname(PHASE02)

sys.path.insert(0, HERE)
import workflow_runner as wr
import assertion_engine as ae
import run_case as rc


# ── 配置加载 ────────────────────────────────────────────────────────
def load_pool_config(path=None):
    """读 pool-config.yaml → 返回 {count, repo_names, per_repo_capacity, ...}。"""
    if path is None:
        path = os.path.join(PHASE02, "inputs", "pool-config.yaml")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"pool-config.yaml 不存在: {path}\n"
            "请先创建 phase02/inputs/pool-config.yaml（参考施工契约 §2）")
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    rp = raw["repo_pool"]
    count = rp["count"]
    naming = rp["naming"]
    repo_names = [naming.replace("{n}", str(i)) for i in range(count)]
    return {
        "owner": rp["owner"],
        "repo_names": repo_names,
        "count": count,
        "branch": rp.get("branch", "main"),
        "per_repo_capacity": raw["queue"]["per_repo_capacity"],
        "poll_interval": raw["polling"]["interval_seconds"],
        "case_timeout": raw["polling"]["case_timeout_seconds"],
        "teardown_mode": raw["execution"]["teardown"],
    }


def _build_configs(pool_cfg):
    """为每个仓创建 RunnerConfig。"""
    cfgs = []
    for name in pool_cfg["repo_names"]:
        cfgs.append(wr.RunnerConfig(
            owner=pool_cfg["owner"],
            repo=name,
            branch=pool_cfg["branch"],
            poll_interval=pool_cfg["poll_interval"],
            timeout=pool_cfg["case_timeout"],
        ))
    return cfgs


# ── state.json 管理 ────────────────────────────────────────────────
def _load_state(run_dir):
    sp = os.path.join(run_dir, "state.json")
    return json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}


def _write_state(run_dir, state):
    json.dump(state, open(os.path.join(run_dir, "state.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


# ── 主循环 ──────────────────────────────────────────────────────────
def run_pool(run_id, only=None, no_logs=False):
    """多仓并发调度主入口。返回状态字典。"""
    run_dir = os.path.join(PHASE02, "runs", run_id)

    # 加载输入
    pool_cfg = load_pool_config()
    cfgs = _build_configs(pool_cfg)

    queue = json.load(open(os.path.join(run_dir, "queue.json"), encoding="utf-8"))
    cases = [c for c in queue["cases"] if not only or c["case_id"] in only]
    if not cases:
        print("无可执行用例（检查 --only 过滤或 queue.json 是否为空）")
        return {"status": "empty"}

    total = len(cases)
    pool = list(cases)  # 待派发队列
    per_repo_capacity = pool_cfg["per_repo_capacity"]
    poll_interval = pool_cfg["poll_interval"]
    case_timeout = pool_cfg["case_timeout"]

    # 每个仓独立数据结构
    repo_names = pool_cfg["repo_names"]
    in_flight = []  # [{cid, repo_cfg, ws, trigger_event, sha/run_id, wf_filename, contract_doc, asserts, t0}]
    repo_deployed = {rn: [] for rn in repo_names}   # 记录本批每仓 push 的文件名 (for batch teardown)

    # state 初始化
    state = {"status": "running", "total": total, "done": 0,
             "current": None, "verdicts": {},
             "in_flight_count": 0, "started": time.strftime("%H:%M:%S")}
    _write_state(run_dir, state)

    print(f"=== 多仓并发调度 {run_id} · {total} 条用例 · "
          f"{pool_cfg['count']} 仓 × 容量 {per_repo_capacity} ===")
    print(f"  仓库: {', '.join(repo_names)}")

    with ExitStack() as stack:
        # 每仓一个 Workspace（各自 clone 一次，全程复用）
        ws_of = {}
        for cfg in cfgs:
            try:
                ws_of[cfg.repo] = stack.enter_context(wr.Workspace(cfg))
            except wr.ApiError as e:
                print(f"  !! clone 失败 {cfg.repo}: {e}")
                # 仓库不可用——标记该仓已满容量，后续不用它
                ws_of[cfg.repo] = None

        # 启动时孤儿清理（每仓扫一遍 .gitcode/workflows/，删除残留）
        for cfg in cfgs:
            ws = ws_of.get(cfg.repo)
            if ws is not None:
                try:
                    wr.sweep_orphans(ws, cfg, keep=[])
                except Exception as e:
                    wr.log(f"  sweep_orphans({cfg.repo}) 异常（忽略）: {e}")

        # 主循环
        while pool or in_flight:
            # ── ① 补位：给未满的仓派用例 ──
            for cfg in cfgs:
                ws = ws_of.get(cfg.repo)
                if ws is None:
                    continue
                # 计算该仓当前在途数
                repo_in_flight = [it for it in in_flight if it["repo_cfg"].repo == cfg.repo]
                while len(repo_in_flight) < per_repo_capacity and pool:
                    c = pool.pop(0)
                    cid = c["case_id"]
                    contract_path = os.path.join(ROOT, c["contract_path"])
                    contract_doc = rc.load_contract(contract_path)
                    wf, asserts = rc.load_execution_inputs(contract_doc, run_dir, cid)

                    # 预检/无 workflow → 直接落库（不 push，不占在途）
                    if not wf:
                        verdict = {"verdict": "NOT_CONFIGURED", "verdict_flags": [],
                                   "reason": "Phase 01 契约无 workflow 字段", "assertion_results": []}
                        rec = rc.write_result(run_dir, contract_doc, verdict,
                                              {"status": "NOT_CONFIGURED", "case_id": cid})
                        rc.update_summary(run_dir, rec)
                        _bump_state(state, "NOT_CONFIGURED", run_dir)
                        _print_verdict(cid, "NOT_CONFIGURED")
                        continue

                    ok, verr = wr.preflight_validate(contract_doc, cfg=cfg)
                    if not ok:
                        wr.log(f"  {cid}: 预检不通过（{len(verr)} 项）→ COMPILE_ERROR，不 push")
                        verdict = {"verdict": "COMPILE_ERROR", "verdict_flags": [],
                                   "reason": "; ".join(verr), "assertion_results": []}
                        rec = rc.write_result(run_dir, contract_doc, verdict,
                                              {"status": "COMPILE_ERROR", "case_id": cid})
                        rc.update_summary(run_dir, rec)
                        _bump_state(state, "COMPILE_ERROR", run_dir)
                        _print_verdict(cid, "COMPILE_ERROR")
                        continue

                    ev = (contract_doc.get("trigger") or {}).get("event", "push")
                    ok2, reason = wr.trigger_supported(ev)
                    if not ok2:
                        verdict = {"verdict": "INCONCLUSIVE", "verdict_flags": [],
                                   "reason": reason, "assertion_results": []}
                        rec = rc.write_result(run_dir, contract_doc, verdict,
                                              {"status": "INCONCLUSIVE", "case_id": cid})
                        rc.update_summary(run_dir, rec)
                        _bump_state(state, "INCONCLUSIVE", run_dir)
                        _print_verdict(cid, f"INCONCLUSIVE({reason})")
                        continue

                    if ev in ("workflow_dispatch", "manual"):
                        if not cfg.cookie:
                            _record_direct(run_dir, state, contract_doc, cid, "INCONCLUSIVE",
                                           "GITCODE_COOKIE 未配置，dispatch 触发不可用")
                            _print_verdict(cid, "INCONCLUSIVE(GITCODE_COOKIE 未配置)")
                            continue

                        wr.log(f"  [{cfg.repo}] deploy+dispatch {cid}")
                        t0 = time.time()
                        sha, wf_filename = wr.deploy(ws, cfg, cid, wf)
                        if not sha:
                            _record_direct(run_dir, state, contract_doc, cid, "ENV_ERROR",
                                           "git push 失败", t0=t0)
                            _print_verdict(cid, "ENV_ERROR")
                            continue

                        repo_deployed[cfg.repo].append(wf_filename)
                        run_id, reason = _start_dispatch(cfg, wf_filename, contract_doc)
                        if not run_id:
                            _record_direct(run_dir, state, contract_doc, cid, "ENV_ERROR",
                                           reason, t0=t0)
                            _print_verdict(cid, f"ENV_ERROR({reason})")
                            continue

                        in_flight.append({"cid": cid, "repo_cfg": cfg, "ws": ws,
                                          "trigger_event": ev, "sha": sha,
                                          "wf_filename": wf_filename, "run_id": run_id,
                                          "contract_doc": contract_doc, "asserts": asserts,
                                          "t0": t0})
                        repo_in_flight = [it for it in in_flight if it["repo_cfg"].repo == cfg.repo]
                        continue

                    # push（同仓串行——一次只 push 一条）
                    wr.log(f"  [{cfg.repo}] deploy {cid}")
                    sha, wf_filename = wr.deploy(ws, cfg, cid, wf)
                    if not sha:
                        verdict = {"verdict": "ENV_ERROR", "verdict_flags": [],
                                   "reason": "git push 失败", "assertion_results": []}
                        rec = rc.write_result(run_dir, contract_doc, verdict,
                                              {"status": "ENV_ERROR", "case_id": cid})
                        rc.update_summary(run_dir, rec)
                        _bump_state(state, "ENV_ERROR", run_dir)
                        _print_verdict(cid, "ENV_ERROR")
                        continue

                    repo_deployed[cfg.repo].append(wf_filename)
                    if ev == "tag":
                        tag = f"test-{cid.lower().replace('_','-')}"
                        rc_t, out_t = wr._sh(f"git tag {tag} && git push origin {tag}", cwd=ws.repo_dir)
                        if rc_t != 0:
                            wr.log(f"  tag push 失败: {out_t[-150:]}")
                    in_flight.append({"cid": cid, "repo_cfg": cfg, "ws": ws,
                                      "trigger_event": ev,
                                      "sha": sha, "wf_filename": wf_filename,
                                      "contract_doc": contract_doc, "asserts": asserts,
                                      "t0": time.time()})
                    repo_in_flight = [it for it in in_flight if it["repo_cfg"].repo == cfg.repo]

                # 更新 in_flight_count
                state["in_flight_count"] = len(in_flight)
                _write_state(run_dir, state)

            # ── ② 批量轮询：每仓拉一次 run 列表 ──
            for cfg in cfgs:
                repo_items = [it for it in in_flight if it["repo_cfg"].repo == cfg.repo]
                if not repo_items:
                    continue
                runs = None
                for item in list(repo_items):  # 遍历副本，允许 remove
                    if item.get("trigger_event") in ("workflow_dispatch", "manual"):
                        r = _get_dispatch_run(item)
                    else:
                        if runs is None:
                            try:
                                runs = wr.list_runs(cfg, per_page=30)
                            except wr.ApiError:
                                runs = []
                        r = wr.match_run(runs, item["sha"], item["wf_filename"])
                    if r is None:
                        # 还没出现
                        if time.time() - item["t0"] > case_timeout:
                            _resolve_timeout(run_dir, state, item)
                            in_flight.remove(item)
                        continue
                    if r.get("status") in wr._TERMINAL:
                        _resolve_terminal(run_dir, state, item, r, no_logs)
                        in_flight.remove(item)
                    elif time.time() - item["t0"] > case_timeout:
                        _resolve_timeout(run_dir, state, item)
                        in_flight.remove(item)

            # ③ 等一轮再轮询（若还有在途）
            if pool or in_flight:
                time.sleep(poll_interval)

        # ── batch_end teardown（各仓互不依赖 → 并行清理）──
        if pool_cfg["teardown_mode"] == "batch_end":
            def _teardown_one(cfg):
                ws = ws_of.get(cfg.repo)
                if ws is None or not repo_deployed.get(cfg.repo):
                    return
                wr.log(f"  batch_end teardown: {cfg.repo} ({len(repo_deployed[cfg.repo])} 文件)")
                try:
                    wr.teardown_batch(ws, cfg, repo_deployed[cfg.repo])
                except Exception as e:
                    wr.log(f"  teardown_batch({cfg.repo}) 异常: {e}")

            targets = [cfg for cfg in cfgs
                       if ws_of.get(cfg.repo) is not None and repo_deployed.get(cfg.repo)]
            if targets:
                with ThreadPoolExecutor(max_workers=len(targets)) as ex:
                    list(ex.map(_teardown_one, targets))

    state["status"] = "completed"
    state["in_flight_count"] = 0
    _write_state(run_dir, state)

    print(f"=== 完成 · " + " · ".join(
        f"{k}={n}" for k, n in state["verdicts"].items()) + " ===")
    return state


# ── 辅助函数 ────────────────────────────────────────────────────────
def _bump_state(state, verdict, run_dir):
    state["verdicts"][verdict] = state["verdicts"].get(verdict, 0) + 1
    state["done"] += 1
    _write_state(run_dir, state)


def _print_verdict(cid, v):
    print(f"    {cid} → {v}")


def _record_direct(run_dir, state, contract_doc, cid, status, reason="", t0=None):
    verdict = {"verdict": status, "verdict_flags": [],
               "reason": reason, "assertion_results": []}
    rec = rc.write_result(run_dir, contract_doc, verdict,
                          wr._exec_result(status, cid, reason=reason, t0=t0))
    rc.update_summary(run_dir, rec)
    _bump_state(state, status, run_dir)
    return rec


def _dispatch_inputs(contract_doc):
    """Return explicit workflow_dispatch inputs from trigger.params, if present."""
    params = ((contract_doc.get("trigger") or {}).get("params") or {})
    if not isinstance(params, dict):
        return {}
    nested = params.get("inputs")
    if isinstance(nested, dict):
        return nested
    return params


def _start_dispatch(cfg, wf_filename, contract_doc):
    """Start a workflow_dispatch run and return (run_id, error_reason)."""
    time.sleep(5)  # Give GitCode time to register the freshly pushed workflow file.
    project_path = f"{cfg.owner}/{cfg.repo}"
    try:
        workflows = wr.list_workflows(cfg.cookie, project_path)
    except Exception as e:
        return None, f"list_workflows 失败: {e}"

    wf_id = None
    wf_file_path = None
    for workflow in workflows:
        fp = workflow.get("file_path") or ""
        if fp.endswith(wf_filename):
            wf_id = workflow.get("workflow_id")
            wf_file_path = fp
            break
    if not wf_id:
        return None, f"list_workflows 未找到匹配 {wf_filename} 的 workflow_id"

    repo_https_url = f"https://gitcode.com/{cfg.owner}/{cfg.repo}.git"
    code, run_id = wr.dispatch_workflow(cfg.cookie, project_path, wf_id, wf_file_path,
                                        cfg.branch, cfg.branch, repo_https_url,
                                        inputs=_dispatch_inputs(contract_doc))
    if code != 200 or not run_id:
        return None, f"dispatch_workflow 返回 HTTP {code}, run_id={run_id}"
    wr.log(f"  dispatch: workflow_run_id={run_id}")
    return run_id, ""


def _get_dispatch_run(item):
    cfg = item["repo_cfg"]
    try:
        run = wr.api_get(cfg, f"/actions/runs/{item['run_id']}")
    except wr.ApiError:
        return None
    return run


def _resolve_terminal(run_dir, state, item, run, no_logs):
    cid = item["cid"]
    cfg = item["repo_cfg"]
    try:
        rr = wr.collect(cfg, run, fetch_logs=not no_logs)
    except wr.ApiError as e:
        verdict = {"verdict": "ENV_ERROR", "verdict_flags": [],
                   "reason": f"collect 失败: {e}", "assertion_results": []}
        rec = rc.write_result(run_dir, item["contract_doc"], verdict,
                              {"status": "ENV_ERROR", "case_id": cid,
                               "duration_seconds": round(time.time() - item["t0"])})
        rc.update_summary(run_dir, rec)
        _bump_state(state, "ENV_ERROR", run_dir)
        _print_verdict(cid, "ENV_ERROR")
        return

    rr["case_id"] = cid
    rr["duration_seconds"] = round(time.time() - item["t0"])
    # 平台终态 FAILED + 0 job → workflow 被平台拒绝
    if rr.get("status") == "FAILED" and not rr.get("jobs"):
        rr["workflow_rejected"] = True
        rr["reason"] = "run FAILED 且 0 job：workflow 可能被平台拒绝"

    engine_asserts = item["asserts"] if item["asserts"] else [{"kind": "status"}]
    verdict = ae.evaluate(rr, engine_asserts)

    rec = rc.write_result(run_dir, item["contract_doc"], verdict, rr)
    rc.update_summary(run_dir, rec)
    _bump_state(state, rec["verdict"], run_dir)
    wr.log(f"  {cid} → {rec['verdict']} run={rec['gitcode_run_id'][:10]} "
           f"({rec['duration_seconds']}s) [repo={cfg.repo}]")


def _resolve_timeout(run_dir, state, item):
    cid = item["cid"]
    verdict = {"verdict": "TIMEOUT", "verdict_flags": [],
               "reason": f"超时 {int(time.time() - item['t0'])}s", "assertion_results": []}
    rec = rc.write_result(run_dir, item["contract_doc"], verdict,
                          {"status": "TIMEOUT", "case_id": cid,
                           "duration_seconds": round(time.time() - item["t0"])})
    rc.update_summary(run_dir, rec)
    _bump_state(state, "TIMEOUT", run_dir)
    _print_verdict(cid, "TIMEOUT")


# ── CLI ─────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("usage: pool_scheduler.py <phase02-run-id> [--only c1,c2] [--no-logs]")
        sys.exit(2)
    run_id = sys.argv[1]
    args = sys.argv[2:]
    no_logs = "--no-logs" in args
    only = None
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))

    run_pool(run_id, only=only, no_logs=no_logs)


if __name__ == "__main__":
    main()
