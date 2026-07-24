# USABILITY 9条 FAIL · leader 复核定稿归因

> run: 2026-07-24-valid297-final | 复核人: leader | 日期: 2026-07-24
> 方法: 逐条拉 results/*.log.txt 实际日志 + 对照 gitcode-spec 精确行号，对 customer 初判做对抗性复核
> 结论: customer 笼统列的 "USE-CONC/CTX/EXPR/INPT/SECNAME 等产品缺陷" 经核对，**真硬缺陷仅 2 条**，其余为建议级/用例问题。

---

## 最终分类（9条）

### A. 真产品缺陷（文档承诺未兑现 / 明确校验缺失）— 2条

| 用例 | workflow 实际 | spec 依据 | 平台实际行为 | 定性 |
|---|---|---|---|---|
| **USE-CTX-01-001** | `echo "ref=${{ atomgit.ref }}"` | context.md L31：`atomgit.ref` = 完整全名 `refs/heads/main`；L32：`atomgit.ref_name` = 短名 `main` | 日志 `ref=main`（返回了短名） | **P1 真缺陷**：文档明确承诺 atomgit.ref 为全名 refs/heads/main，平台却返回短名 main（=ref_name 的值），文档承诺未兑现。断言为 positive/run_logs（判定干净，非 run_status_not 代理）|
| **USE-INPT-01-002** | dispatch input `type: boolean` | trigger-events.md L200-202：inputs type 表**仅列 `string`**，"如需布尔语义可用表达式转换" | 日志 `dry_run=false`，静默接受、run COMPLETED、零警告 | **P1 真缺陷**：文档明确 inputs 仅支持 string，平台对非法 type:boolean 不校验不警告（输入校验缺失）|

### B. usability 建议级（错误引导缺失，但未违反文档明确承诺）— 2条

| 用例 | workflow 实际 | spec 情况 | 平台行为 | 定性 |
|---|---|---|---|---|
| **USE-CTX-01-002** | `echo "ref=${{ github.ref }}"` | context.md 只定义 `atomgit.*`，无 `github.*`；但**未承诺 github.* 必须报错** | 解析成 `ref=placeholder_ref`、不报错、run COMPLETED | 建议级：用户误用 GitHub 习惯的 github.*，平台给占位符而非报错引导→错误诊断能力不足。非硬缺陷（无明确"必报错"承诺）|
| **USE-EXPR-01-001** | `echo "val=${{ atomgit.nonexistent_property }}"` | 无"访问不存在属性必须报错"的承诺；GitHub Actions 同为求值空 | 日志 `val=`（空串）、不报错 | 建议级：不报错让拼写错误无感知；但求值空是表达式语言常见设计，非硬缺陷 |

### C. 用例问题 / 我方假失败（非平台问题）— 5条

| 用例 | 断言现象 | 实际日志 | 定性 |
|---|---|---|---|
| **USE-CONC-01-001** | negative/run_status 期望非COMPLETED + error含"有效范围1-5" | `concurrency.max:10` 被接受、run COMPLETED、`hello` | 用例问题：configure-jobs.md L152-164 有 max 字段但**未规定范围 1-5**，用例假设的范围限制 spec 无依据，平台接受 max:10 合理 |
| **USE-LOG-01-001** | value 期望 `step one prepare`→absent | 日志有 `build done/test done/...` 但无 step name | 断言设计缺陷：log_fetcher 抓执行正文不含 step name，断言拿 step name（YAML元数据）当日志内容扫，必然 absent |
| **USE-MD-01-001** | value 期望 `Test Report`→absent | 日志 404 字节几乎空 | 编译缺口：step_summary 内容不在 run 日志（是单独 summary 文件），step_summary target 退化为 run_logs value 扫不到 |
| **USE-OS-01-001** | value 期望 `os=Linux`→absent | 日志 `os=linux`（小写） | 大小写假失败：断言大写 Linux、平台输出小写 linux |
| **USE-ENV-01-002** | status 期望全绿→job FAILED | `GITHUB_SHA: unbound variable` + exit 1 | 用例问题：GITHUB_SHA 是 GitHub 语法、GitCode 不支持，平台**正确报错**；status 断言退化，job 失败即判 FAIL（实为用例误用 GitHub 变量）|

---

## 核查结论

- customer 初判的 usability 产品缺陷清单需**大幅收敛**：真硬缺陷仅 2 条（USE-CTX-01-001、USE-INPT-01-002）。
- customer 突出提的 **USE-CONC-01-001 实为用例问题**（假设了 spec 不存在的 max 范围）；**USE-SECNAME 根本不在这 9 条 FAIL 内**（PASS 或在别处）。
- 5 条是我方假失败/用例问题（断言设计、编译缺口、大小写、误用 GitHub 语法），不应计入平台缺陷。

## 两个待定夺的保留项

1. **USE-CONC-01-001**：仅在 configure-jobs.md 一处未见 max 范围规定。若 spec 别处（如 syntax-reference）定义了 max 合法范围，则本条可翻为真缺陷（平台未校验超范围值）。
2. **USE-CTX-01-002 / USE-EXPR-01-001**：归"建议级"因文档无"必须报错"的明确承诺。若将"错误引导质量"视为 usability 硬指标，此 2 条可升级为缺陷。

## 方法论备注

这 4 条 negative 用例（CONC/CTX-02/EXPR/INPT）本质是测"平台对错误输入的防御性 + 错误引导质量"（核心是 nonfunctional/error_message 断言），run_status_not 只是"平台该不该拒绝"的代理。平台普遍表现为"静默接受、不报错、无引导"——是否算缺陷严格取决于 spec 是否承诺该输入应被校验/拒绝。这是防止把"平台宽松容错"误报成"平台缺陷"的关键判据（同 SEC-INJ/SEC-DOS 的假阳性教训）。
