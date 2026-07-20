# 已知安全风险与历史问题

> 来源：测试过程中发现的问题与安全关注点，作为安全维度 agent 和 case-writer 生成 intent/用例的**实证输入**。
> 更新日期：2026-07-20

## 1. 多项目环境隔离

**问题描述**：多个开源项目共享同一批 runner 资源，一个项目的 workflow 执行不应影响另一个项目。

**测试关注点**：
- Runner workspace 跨项目残留（上一项目的文件/环境变量被下一项目继承）
- 共享缓存/artifact 的命名空间隔离
- 并发项目之间的资源争抢与优先级
- 项目 A 的 secret 不应在项目 B 的 workflow 中可访问

**关联 intent**：INTENT-SEC-025（runner 残留数据清理）、INTENT-SEC-033（runner 并发 job 隔离）

---

## 2. 敏感信息管理

**问题描述**：secret、token、API key 等敏感信息的全生命周期安全问题。

**测试关注点**：
- Secret 创建/更新/删除的权限控制（谁能管理 secret）
- Secret 在 workflow YAML 中的引用安全性（`${{ secrets.XXX }}`）
- Secret 在环境变量传递过程中的泄露风险
- Token 过期/轮换机制——过期 token 是否仍能通过缓存访问
- 组织级 secret vs 仓库级 secret 的可见性边界

**关联 intent**：INTENT-SEC-001/002（fork PR secret 隔离）、INTENT-SEC-015~017（permissions 模型）、INTENT-SEC-021（secret 命名规则）、INTENT-SEC-023（ATOMGIT_TOKEN 过期/轮换）、INTENT-SEC-036（内置 token 权限范围）

---

## 3. 日志脱敏、日志扫描、日志过期

**问题描述**：workflow 运行日志中可能包含敏感信息，需要自动脱敏、可审计、有生命周期管理。

**测试关注点**：
- Secret 值在日志中的自动遮蔽（`***`）——包括 echo 输出、环境变量打印、错误消息中的意外泄露
- 脱敏绕过场景：base64 编码、字符串拼接/插值、多行值、二进制混淆
- 日志扫描能力：是否提供工具/API 对历史日志做敏感信息扫描
- 日志保留期：默认保留多久、能否配置、过期后是否彻底删除（不可恢复）
- 日志下载/导出权限控制

**关联 intent**：INTENT-SEC-005（基础脱敏）、INTENT-SEC-006（base64 绕过）、INTENT-SEC-007（拼接绕过）、INTENT-SEC-008（多行值脱敏）、INTENT-USE-020（re-run 缓存日志保留）

**已知缺陷参考**：GitHub Actions 历史上 secret 脱敏在 workflow command echo 场景下有绕过案例——`::add-mask::` 命令本身的返回值可能包含被遮蔽前的值。

---

## 4. 共享盘敏感信息

**问题描述**：Runner 的共享文件系统（如 `/tmp`、`/home/runner`、`$GITHUB_WORKSPACE` 等）可能在不同 job/run 之间残留敏感文件或凭据。

**测试关注点**：
- Job 结束后 workspace 是否彻底清理
- `/tmp` 等共享目录是否跨 job 可见
- 缓存/artifact 是否可能包含意外的敏感文件（如 `.env`、`.git-credentials`）
- Self-hosted runner 上的磁盘残留——尤其是 runner 非 ephemeral 时

**关联 intent**：INTENT-REL-014（跨 job workspace 隔离）、INTENT-SEC-025（runner 残留数据清理）、INTENT-SEC-019（fork PR cache 投毒）

---

## 5. 网络隔离

**问题描述**：Workflow 运行时的网络出站/入站策略，防止 SSRF、数据外传、内部服务暴露。

**测试关注点**：
- Runner 是否可以访问内部网络/非公开服务（SSRF 攻击面）
- Runner 的出站网络是否有限制（防止数据外传到外部服务器）
- Fork PR 的 workflow 是否与 main repo 的 runner 共享网络命名空间
- Self-hosted runner 在内网部署时的网络边界——runner 是否成为内网跳板
- 网络隔离在容器/VM runner 和裸机 runner 上的差异

**关联 intent**：INTENT-SEC-025（runner 隔离——含网络层面）、测试关注点 §4（Runner 环境隔离——缺网络出站策略验证，已标记为覆盖盲区）

---

## 总结：安全测试优先级

基于以上5个已知关注点，安全测试应优先覆盖：

1. **P0**：fork PR 隔离（secret + token + cache）——问题 1/2/4/5 均与此相关
2. **P0**：日志脱敏与绕过——问题 3
3. **P1**：Runner 残留清理——问题 1/4
4. **P1**：网络隔离——问题 5
5. **P1**：敏感信息管理——问题 2

---

*本文件作为 `security-knowledge/` 的核心输入，在 `/phase01-gen` 时由 security agent 和 case-writer 消费。*
