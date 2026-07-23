#!/usr/bin/env python3
"""
dump_actions_md.py — 拉取项目的全部 Action 插件并导出为 Markdown。

用法:
    python3 dump_actions_md.py                    # 输出到 stdout
    python3 dump_actions_md.py > actions.md       # 保存到文件
"""

import os, sys, json, time
import requests

API_HOST = "web-api.gitcode.com"
PROJECT = "ComputingActionTest/foundational-tests"


def _load_env():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_paths = [
        os.path.join(script_dir, ".env"),
        os.path.join(script_dir, "..", "..", ".env"),
    ]
    for p in env_paths:
        if os.path.exists(p):
            env_vars = {}
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env_vars[k.strip()] = v.strip()
            if "GITCODE_COOKIE" in env_vars:
                return env_vars
    return {}


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


def _enc(project_path):
    return project_path.replace("/", "%2F")


def fetch_plugins(host, project, cookie):
    """分页拉取全部插件列表，返回 [{name, creator, display_name, refer, ...}]。"""
    all_plugins = []
    page = 1
    headers = build_headers(cookie)
    while True:
        url = f"https://{host}/api/v2/projects/{_enc(project)}/actions/plugins/all?page={page}&per_page=50"
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        content = data.get("content", [])
        all_plugins.extend(content)
        sys.stderr.write(f"  page {page}/{data.get('page_count', '?')} — {len(content)} plugins\n")
        if page >= data.get("page_count", 1):
            break
        page += 1
        time.sleep(0.3)
    return all_plugins


def fetch_detail(host, project, name, version, cookie):
    """拉取单个插件的详情（readme 文本）。"""
    headers = build_headers(cookie)
    url = f"https://{host}/api/v2/projects/{_enc(project)}/actions/plugins/detail?name={name}&version={version or ''}"
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


def main():
    env = _load_env()
    cookie = env.get("GITCODE_COOKIE")
    if not cookie:
        sys.exit("未找到 GITCODE_COOKIE——请确认项目根 .env 已配置")

    print("[*] 拉取插件列表...", file=sys.stderr)
    plugins = fetch_plugins(API_HOST, PROJECT, cookie)
    print(f"[+] 共 {len(plugins)} 个插件\n", file=sys.stderr)

    # ── 输出 Markdown ──
    print(f"# GitCode Actions 插件目录\n")
    print(f"> 项目: `{PROJECT}` | 插件总数: {len(plugins)}\n")
    print("---\n")

    for i, p in enumerate(plugins, 1):
        name = p.get("name", "?")
        display = p.get("display_name", name)
        creator = p.get("creator", "—")
        refer = p.get("refer", 0)

        sys.stderr.write(f"  [{i}/{len(plugins)}] fetching {name}...\n")
        try:
            detail = fetch_detail(API_HOST, PROJECT, name, "", cookie)
        except Exception as e:
            print(f"## {i}. {display}\n")
            print(f"- **name**: `{name}`")
            print(f"- **creator**: {creator}")
            print(f"- **被引用**: {refer}")
            print(f"- **详情**: 拉取失败 ({e})\n")
            sys.stderr.write(f"    FAIL {e}\n")
            continue

        versions = detail.get("vision_list", [])
        vision_content = detail.get("vision_content", [])
        readme = ""
        for vc in vision_content:
            if vc.get("readme"):
                readme = vc["readme"]
                break

        print(f"## {i}. {display}\n")
        print(f"- **name**: `{name}`")
        print(f"- **creator**: {creator}")
        print(f"- **被引用**: {refer}")
        print(f"- **版本**: {', '.join(versions) if versions else '—'}\n")

        if readme:
            print(readme)
            print()
        else:
            print("*（无 README）*\n")

        print("---\n")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
