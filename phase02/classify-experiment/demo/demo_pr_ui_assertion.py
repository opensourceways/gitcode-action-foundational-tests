#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_pr_ui_assertion.py — PR UI annotation 断言模式 (Playwright)

目标: USE-ANNOT-01-002 需要检查 PR 页面中 ::error:: / ::warning:: 的 annotation 展示。
由于 PR 触发不工作，这里演示 Playwright 检查 GitCode PR 页面的模式。

用法:
    cd phase02/classify-experiment/demo
    python3 demo_pr_ui_assertion.py

前置:
    pip install playwright && playwright install chromium
"""

import os, sys, json, re, time

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k, v = k.strip(), v.strip()
                v = re.sub(r'\s+#.*$', '', v).strip().strip('"').strip("'")
                if k not in os.environ:
                    os.environ[k] = v

load_env()


def main():
    print("=" * 60)
    print("PR UI ASSERTION — Playwright 模式演示")
    print("=" * 60)

    # PR #5 is still open: https://gitcode.com/ComputingActionTest/foundational-tests/merge_requests/5
    pr_url = "https://gitcode.com/ComputingActionTest/foundational-tests/merge_requests/5"

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print()
        print("⚠️  Playwright 未安装。安装方法:")
        print("   pip install playwright && playwright install chromium")
        print()
        print("── 替代方案：curl + grep 检查 PR API ──")
        print()
        TOKEN = os.environ.get("GITCODE_ACCESS_TOKEN", "")
        import urllib.request, json

        # 方案 1: 通过 PR comments API 查 annotation 是否以评论形式出现
        url = f"https://api.gitcode.com/api/v5/repos/ComputingActionTest/foundational-tests/pulls/5/comments?access_token={TOKEN}"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=15) as r:
                comments = json.loads(r.read().decode("utf-8"))
            print(f"   PR #5 comments: {len(comments) if isinstance(comments, list) else 'N/A'}")
            if isinstance(comments, list):
                for c in comments:
                    print(f"     - {json.dumps(c, ensure_ascii=False)[:200]}")
        except Exception as e:
            print(f"   Comments API error: {e}")

        # 方案 2: PR diff/files API
        url2 = f"https://api.gitcode.com/api/v5/repos/ComputingActionTest/foundational-tests/pulls/5/files?access_token={TOKEN}"
        try:
            req2 = urllib.request.Request(url2, method="GET")
            with urllib.request.urlopen(req2, timeout=15) as r:
                files = json.loads(r.read().decode("utf-8"))
            print(f"   PR #5 files: {len(files) if isinstance(files, list) else 'N/A'}")
        except Exception as e:
            print(f"   Files API error: {e}")

        print()
        print("=" * 60)
        print("PR UI assertion 判定模式 (待 PR 触发可用时):")
        print()
        print("  1. Create PR with annotation-producing workflow")
        print("  2. Wait for workflow run → job generates ::error::/::warning::")
        print("  3. Open PR page via Playwright:")
        print()
        print("  from playwright.sync_api import sync_playwright")
        print("  with sync_playwright() as p:")
        print("      browser = p.chromium.launch()")
        print("      page = browser.new_page()")
        print("      page.goto(pr_url)")
        print("      # Check for annotation elements")
        print("      annotations = page.locator('.annotation, .check-annotation, [data-annotation]')")
        print("      errors = page.locator('.error-annotation, [class*=\"error\"]')")
        print("      warnings = page.locator('.warning-annotation, [class*=\"warning\"]')")
        print("      # Assert file path, line number in annotation")
        print("      page.screenshot(path='pr_ui.png')")
        print()
        print("  4. LLM-assisted: 截图交 LLM 判定 annotation 颜色/路径/行号")
        print("  5. Fallback: PR 页面 HTML 交 LLM 判定")
        print("=" * 60)
        return 0

    # Playwright available — run actual check
    print(f"\n   PR URL: {pr_url}")
    print(f"   启动 Chromium...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(pr_url, wait_until="networkidle", timeout=30000)
        print(f"   页面标题: {page.title()}")

        # Take screenshot
        screenshot_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_path = os.path.join(screenshot_dir, "pr_ui_screenshot.png")
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"   截图: {screenshot_path}")

        # Check for annotations
        selectors = [
            ".check-annotation",
            ".ci-annotation",
            ".pipeline-annotation",
            "[data-testid='annotation']",
            ".merge-request-annotation",
            ".file-annotation",
        ]
        for sel in selectors:
            count = page.locator(sel).count()
            if count > 0:
                print(f"   找到 annotation: {sel} x{count}")

        # Check page content for error/warning
        content = page.content()
        if "error" in content.lower():
            print("   页面含 'error' 字样")
        if "annotation" in content.lower():
            print("   页面含 'annotation' 字样")

        print(f"   HTML 长度: {len(content)} chars")
        print(f"   HTML 预览: {content[:500]}")

        browser.close()

    print()
    print("=" * 60)
    print("Playwright PR UI 断言可行 — 截图/HTML 交 LLM 判定")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
