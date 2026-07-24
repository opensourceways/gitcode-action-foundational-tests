## 校验失败 · USE-MASK-01-001 · secret 脱敏文档描述与实际行为一致并给出缓解建议

**判定结果**: ERROR

**根因**: API 调用失败 (WAF 拦截 / 网络错误)
**响应**: {"status_code": 418, "text": "<!DOCTYPE html><html style=\"height:100%;width:100%\"><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /><meta http-equiv=\"Server\" content=\"CloudWAF\" /><title id=\"title\">访问被拦截！</title></head><body onload=\"bindall()\" style=\"height:100

- 维度: usability | 优先级: P0
- intent_ref: INTENT-USE-016 | trigger: workflow_dispatch
