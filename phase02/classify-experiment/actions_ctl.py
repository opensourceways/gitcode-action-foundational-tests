#!/usr/bin/env python3
"""
actions_ctl.py — GitCode Actions 写操作 CLI（dispatch / stop / list）

认证方式（与 validate_workflow.py 一致）：
  1. --cookie       直接传 GITCODE_COOKIE（推荐，从浏览器 F12 抓包）
  2. 环境变量        GITCODE_COOKIE
  3. 项目根目录 .env  GITCODE_COOKIE=xxx

用法：
  # 列出项目的所有 workflow
  python3 actions_ctl.py list -p ComputingActionTest/foundational-tests

  # 手动触发一个 workflow
  python3 actions_ctl.py dispatch -p ComputingActionTest/foundational-tests -w PILOT-BASIC

  # 用 workflow_id 精确触发
  python3 actions_ctl.py dispatch -p ComputingActionTest/foundational-tests --id 9e72bed83e4d406cb7929f09a297aedc

  # 触发并传入 inputs
  python3 actions_ctl.py dispatch -p ComputingActionTest/foundational-tests -w PILOT-BASIC -i '{"node_version":"20"}'

  # 停止一个运行中的 run
  python3 actions_ctl.py stop -p ComputingActionTest/foundational-tests -r ad4bf34694cb4277b2c11943914ec88f
"""

import argparse
import json
import os
import sys
import time

import requests

API_HOST = "web-api.gitcode.com"
API_V8_HOST = "api.gitcode.com"


# ── 认证 ──────────────────────────────────────────────────────────

def _load_env_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for _ in range(4):
        candidate = os.path.join(script_dir, ".env")
        if os.path.exists(candidate):
            env_vars = {}
            with open(candidate) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, _, v = line.partition("=")
                        env_vars[k.strip()] = v.strip().strip('"').strip("'")
            return env_vars
        script_dir = os.path.dirname(script_dir)
    return {}


def resolve_cookie(cookie_arg=None):
    cookie = cookie_arg or os.environ.get("GITCODE_COOKIE")
    if not cookie:
        cookie = _load_env_file().get("GITCODE_COOKIE", "")
    return cookie


def build_headers(cookie):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cookie}",
        "Origin": "https://gitcode.com",
        "Referer": "https://gitcode.com/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "X-App-Channel": "gitcode-fe",
        "X-App-Version": "0",
        "X-Device-ID": "unknown",
        "X-Device-Type": "Linux",
        "X-Platform": "web",
        "Cookie": f"GITCODE_ACCESS_TOKEN={cookie}; GitCodeUserName=ccijunk",
    }


# ── API 封装 ──────────────────────────────────────────────────────

def _enc(project_path):
    return project_path.replace("/", "%2F")


def list_workflows(project_path, cookie, host=API_HOST):
    """列出项目的所有 workflow。"""
    headers = build_headers(cookie)
    url = f"https://{host}/api/v2/projects/{_enc(project_path)}/actions/workflows/list"
    resp = requests.post(url, headers=headers, json={}, timeout=10)
    resp.raise_for_status()
    return resp.json().get("content", [])


def dispatch_workflow(project_path, workflow_id, ref, branch, file_path,
                      repo_https_url, inputs, cookie, host=API_HOST):
    """手动触发一次 workflow 运行。返回 dispatch 响应（含 workflow_run_id）。"""
    headers = build_headers(cookie)
    url = f"https://{host}/api/v2/projects/{_enc(project_path)}/actions/workflows/{workflow_id}/dispatch"
    payload = {
        "ref": ref,
        "branch": branch,
        "branch_commit_id": "",
        "repo_https_url": repo_https_url,
        "file_path": file_path,
        "inputs": inputs or {},
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp.status_code, resp.json() if resp.headers.get("Content-Type", "").startswith("application/json") else resp.text


def stop_run(project_path, run_id, cookie, host=API_HOST):
    """停止一个运行中的 workflow run。"""
    headers = build_headers(cookie)
    url = f"https://{host}/api/v2/projects/{_enc(project_path)}/actions/workflow-runs/{run_id}/stop"
    resp = requests.post(url, headers=headers, json={}, timeout=10)
    return resp.status_code, resp.json() if resp.headers.get("Content-Type", "").startswith("application/json") else resp.text


def poll_run(project_path, run_id, access_token, timeout_sec=300, interval=10):
    """轮询等待 run 到达终态。返回最终 run 对象。"""
    owner, repo = project_path.split("/", 1)
    url = f"https://{API_V8_HOST}/api/v8/repos/{owner}/{repo}/actions/runs/{run_id}"
    elapsed = 0
    while elapsed < timeout_sec:
        resp = requests.get(url, params={"access_token": access_token}, timeout=10)
        if resp.status_code != 200:
            return None
        run = resp.json()
        status = run.get("status", "")
        if status in ("COMPLETED", "FAILED", "CANCELED"):
            return run
        time.sleep(interval)
        elapsed += interval
        print(f"  [{status}] {elapsed}s", file=sys.stderr)
    return None


# ── resolve workflow_id by name ───────────────────────────────────

def resolve_workflow_id(project_path, name_or_id, cookie):
    """如果传入的是 workflow 名称，从列表中查找对应的 id。"""
    # 直接传了 UUID
    if len(name_or_id) == 32 and all(c in "0123456789abcdef" for c in name_or_id):
        return name_or_id
    # 按名称匹配
    wfs = list_workflows(project_path, cookie)
    for w in wfs:
        if w.get("name") == name_or_id or w.get("file_path", "").endswith(name_or_id):
            return w["workflow_id"]
    print(f"[!] 未找到名为 '{name_or_id}' 的 workflow", file=sys.stderr)
    print(f"    可用: {[w['name'] for w in wfs]}", file=sys.stderr)
    sys.exit(1)


# ── CLI ───────────────────────────────────────────────────────────

def cmd_list(args):
    cookie = resolve_cookie(args.cookie)
    if not cookie:
        sys.exit("请设置 GITCODE_COOKIE（--cookie / 环境变量 / .env）")
    wfs = list_workflows(args.project, cookie)
    print(f"{'NAME':<50s} {'WORKFLOW_ID':<35s} FILE_PATH")
    print("-" * 120)
    for w in wfs:
        print(f"{w['name']:<50s} {w['workflow_id']:<35s} {w.get('file_path', '')}")


def cmd_dispatch(args):
    cookie = resolve_cookie(args.cookie)
    if not cookie:
        sys.exit("请设置 GITCODE_COOKIE（--cookie / 环境变量 / .env）")

    wf_id = resolve_workflow_id(args.project, args.workflow, cookie)

    # Build repo_https_url
    owner_repo = args.project
    repo_https_url = f"https://gitcode.com/{owner_repo}.git"

    # Get file_path
    wfs = list_workflows(args.project, cookie)
    file_path = ""
    for w in wfs:
        if w["workflow_id"] == wf_id:
            file_path = w.get("file_path", "")
            break

    branch = args.branch or "main"
    ref = args.ref or branch

    inputs = {}
    if args.inputs:
        inputs = json.loads(args.inputs)

    print(f"Dispatching: {args.project} workflow_id={wf_id} ref={ref}", file=sys.stderr)
    code, resp = dispatch_workflow(
        args.project, wf_id, ref, branch, file_path, repo_https_url, inputs, cookie
    )
    print(json.dumps(resp, ensure_ascii=False, indent=2))

    if code == 200 and resp.get("workflow_run_id") and args.wait:
        rid = resp["workflow_run_id"]
        access_token = os.environ.get("GITCODE_ACCESS_TOKEN", "")
        print(f"\nPolling run {rid} ...", file=sys.stderr)
        run = poll_run(args.project, rid, access_token, args.timeout, args.interval)
        if run:
            print(json.dumps(run, ensure_ascii=False, indent=2))
        else:
            print(f"Timeout / no response for run {rid}", file=sys.stderr)


def cmd_stop(args):
    cookie = resolve_cookie(args.cookie)
    if not cookie:
        sys.exit("请设置 GITCODE_COOKIE（--cookie / 环境变量 / .env）")

    code, resp = stop_run(args.project, args.run_id, cookie)
    print(json.dumps(resp, ensure_ascii=False, indent=2))
    sys.exit(0 if code == 200 else 1)


def main():
    parser = argparse.ArgumentParser(description="GitCode Actions 操作 CLI（dispatch / stop / list）")
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="列出项目的 workflow")
    p_list.add_argument("-p", "--project", default="ComputingActionTest/foundational-tests")
    p_list.add_argument("--cookie")

    # dispatch
    p_disp = sub.add_parser("dispatch", help="手动触发 workflow")
    p_disp.add_argument("-p", "--project", default="ComputingActionTest/foundational-tests")
    p_disp.add_argument("-w", "--workflow", required=True, help="workflow 名称 或 UUID")
    p_disp.add_argument("-r", "--ref", help="git ref（默认 main）")
    p_disp.add_argument("-b", "--branch", help="branch（默认 main）")
    p_disp.add_argument("-i", "--inputs", help='inputs JSON 字符串，如 \'{"key":"val"}\'')
    p_disp.add_argument("--wait", action="store_true", help="等待 run 完成")
    p_disp.add_argument("--timeout", type=int, default=300, help="轮询超时秒数")
    p_disp.add_argument("--interval", type=int, default=10, help="轮询间隔秒数")
    p_disp.add_argument("--cookie")

    # stop
    p_stop = sub.add_parser("stop", help="停止运行中的 workflow run")
    p_stop.add_argument("-p", "--project", default="ComputingActionTest/foundational-tests")
    p_stop.add_argument("-r", "--run-id", required=True, help="workflow_run_id")
    p_stop.add_argument("--cookie")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "dispatch":
        cmd_dispatch(args)
    elif args.command == "stop":
        cmd_stop(args)


if __name__ == "__main__":
    main()
