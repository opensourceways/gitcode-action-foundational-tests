## 校验失败 · REL-LOG-01-040 · 超长日志——单 job 输出 100 MB 日志应完整保留且可下载查看

**判定结果**: ERROR

**根因**: API 调用失败 (WAF 拦截 / 网络错误)
**响应**: {"status_code": 418, "text": "<!DOCTYPE html><html style=\"height:100%;width:100%\"><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /><meta http-equiv=\"Server\" content=\"CloudWAF\" /><title id=\"title\">访问被拦截！</title></head><body onload=\"bindall()\" style=\"height:100

- 维度: reliability | 优先级: P1
- intent_ref: INTENT-REL-040 | trigger: workflow_dispatch
