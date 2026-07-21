# 日志抓取凭据 —— 用户需提供什么

> **好消息（2026-07-21 更新）**：日志正文抓取**只需 OAuth token**，
> 不再需要浏览器会话 / cookie / 过 WAF。本文档已大幅简化。

---

## 需要什么

**只需一样**：`GITCODE_ACCESS_TOKEN`（你已经在用的那个 OAuth token）。

- 放环境变量 `GITCODE_ACCESS_TOKEN`，或仓库外文件 `~/.gitcode-token`。
- 这跟 git push / 状态类 API 用的是**同一个 token**——所以跑日志类用例**不需要额外提供任何东西**。

就这样。

---

## 原理（为什么现在这么简单）

日志走官方 v8 端点（用 OAuth token 即可）：

```
GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs/:job_id/download_log?access_token=<TOKEN>
→ 302 重定向 → raw.gitcode.com → 200 application/zip
→ 解压：每个 step 一个 .log 文件（完整 runner 输出，含掩码后的 ***）
```

harness 的 `log_fetcher.py` 已封装全过程（下载→跟随302→解压→拼接）。

---

## ⚠️ 已废弃：浏览器会话方案

早期一版用 `web-api.gitcode.com` + 浏览器 `Bearer JWT` + cookie + 过 WAF 来取日志
（对应旧文件 `~/.gitcode-web-curl.txt`）。**现已废弃**，因为：

- 那套依赖浏览器登录态，**JWT 数天就过期**，要反复重抓 curl。
- 要带全套浏览器头绕过 CloudWAF，脆弱。

zip 方案只用 OAuth token，稳定且无过期烦恼，已取代它。
`~/.gitcode-web-curl.txt` 不再需要，可删除。

---

## 踩过的坑（供排查）

| 现象 | 原因 / 解法 |
|---|---|
| download 返回 404 | 端点名用成了 `download-log`（连字符）；正确是 **`download_log`（下划线）** |
| 只拿到 302 空响应 | 没跟随重定向；需 `curl -L` / urllib（默认跟随） |
| job id 为空串 | `/jobs` 接口的 `jobs[].id` 某些场景为空；改从 **run detail `stages.jobs[].id`** 取 |
| 解压失败/空 zip | 该 job 无日志（失败于 job 创建前）；harness 有假绿守卫，判 FAIL |

---

## 自检

```bash
# 列出某 run 的 jobs + 日志
python phase02/scripts/log_fetcher.py <owner> <repo> <run_id>
# 单个 job 的日志
python phase02/scripts/log_fetcher.py <owner> <repo> <run_id> <job_id>
```

打印出日志正文 → OK。报"未找到 OAuth token" → 配置 `GITCODE_ACCESS_TOKEN`。

---

*相关：[`scripts/log_fetcher.py`](../scripts/log_fetcher.py) · [`scripts/api-client.md`](../scripts/api-client.md)*
