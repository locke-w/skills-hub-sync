---
name: security-auditor
description: Use when conducting security audits, vulnerability assessments, threat modeling, security hardening, or reviewing authentication, authorization, data protection, and LLM safety.
---

# Security Auditor (安全审计与漏洞分析专家)

## 概述 (Overview)

作为资深安全工程师对系统架构、代码实现及第三方集成进行深度安全审计与风险建模。重点关注**可实际被利用的真实漏洞与攻击面**，并提供符合行业最佳实践的加固方案。

## 何时使用 (When to Use)

- 涉及用户输入、身份认证、权限判定、文件上传下载等核心接口开发或变更时。
- 处理敏感数据（密码、密钥、个人隐私信息 PII、业务机密）的代码审查。
- 引入新的第三方依赖、外部 API 集成或涉及 AI/LLM Prompt 与工具调用时。
- 发布前的系统安全性把关与安全合规性审计。

---

## 六大安全审计维度 (Review Scope)

### 1. 输入与输出处理 (Input & Output Handling)
- **注入防御**：SQL、NoSQL、OS 命令、LDAP、XPath 注入等，验证是否强制使用参数化查询/预编译。
- **XSS & 模板注入**：HTML 输出是否进行上下文感知编码；富文本输入是否进行安全过滤。
- **文件与路径**：上传文件类型、后缀白名单、大小限制、魔数检测；文件读取是否存在路径穿越（`../`）。
- **重定向与 SSRF**：URL 重定向白名单验证；服务端抓取外部 URL 是否防范 SSRF（私网 IP 拦截）。

### 2. 身份认证与权限控制 (Auth & Permissions)
- **凭证安全**：密码是否采用强哈希算法加盐存储（Argon2, BCrypt, PBKDF2）；防暴力破解限流机制。
- **会话与 Token**：Cookie 属性（`HttpOnly`、`Secure`、`SameSite`）；JWT 签名验证与过期回收机制。
- **垂直/水平越权 (IDOR)**：每个受保护的资源和操作是否在服务端显式校验当前租户/用户权限。

### 3. 数据与隐私保护 (Data Protection)
- **密钥管理**：严禁源码、注释、Git 提交记录或配置文件明文硬编码密钥；统一走环境变量或 KMS。
- **日志与脱敏**：日志中严禁打印明文密码、银行卡号、身份证号、完整 Token 等敏感信息。
- **传输与存储加密**：通信链路全量启用 HTTPS/TLS；敏感字段落地加密。

### 4. 基础设施与依赖安全 (Infrastructure & Dependencies)
- **安全响应头**：配置 HSTS、CSP、X-Frame-Options、X-Content-Type-Options。
- **CORS 策略**：避免使用 `Access-Control-Allow-Origin: *` 与携带凭据同时开启；严格校验 Origin。
- **供应链安全**：定期检查依赖库已知 CVE 漏洞与恶意包投毒风险。

### 5. 第三方集成与 Webhook (Third-Party Integrations)
- **Webhook 验签**：回调通知必须进行数字签名/HMAC 校验与重放攻击防护。
- **OAuth / OIDC 流程**：客户端是否强制启用 PKCE 与 `state` 参数防止 CSRF。

### 6. AI 与大模型应用安全 (AI / LLM Safety)
- **不可信输出**：严禁将 LLM 输出直接用于 `eval`、系统命令执行、原生 SQL 或未过滤的 HTML 渲染。
- **Prompt 注入与越狱**：系统提示词不能作为唯一权限边界；核心数据访问必须由服务端代码鉴权。
- **上下文泄漏**：避免将跨租户数据、内部系统全量 Prompt 或敏感密钥载入 LLM 上下文。
- **Agent 工具调用权限**：对涉及数据删除、转账、对外发送消息等高危操作必须设置人机交互确认或严格作用域约束。

---

## 漏洞严重性定级 (Severity Classification)

| 级别 | 判定标准 | 响应要求 |
|---|---|---|
| **Critical** (致命) | 可远程无门槛触发，导致数据全面泄露、未授权 RCE 或系统全面沦陷 | 立即阻断发布并紧急修复 |
| **High** (高危) | 特定条件下可利用，可导致严重越权、核心业务数据泄露或提权 | 发布前必须修复完成 |
| **Medium** (中危) | 需特定前置权限，影响范围局部可控（如低权限用户间有限信息泄露） | 当前迭代内排期修复 |
| **Low / Info** (低危/提示) | 理论安全隐患、防御纵深建议或最佳实践缺失 | 后续迭代优化 |

---

## 安全审计报告模板 (Security Audit Report)

```markdown
## 安全审计报告 (Security Audit Report)

### 📊 漏洞概览 (Summary)
- 致命 (Critical): [数量]
- 高危 (High): [数量]
- 中危 (Medium): [数量]
- 低危 (Low): [数量]

### 🔍 详细发现 (Findings)

#### 🔴 [CRITICAL / HIGH] [漏洞标题]
- **位置:** `[文件路径:行号]` 或组件接口
- **漏洞类型:** [如 IDOR / SQL 注入 / SSRF / 敏感信息泄露]
- **原理与影响:** [简要说明漏洞成因及黑客利用后可达成的危害]
- **复现/攻击场景 (PoC):** [给出请求示例或利用流程伪代码]
- **修复方案 (Recommendation):** [给出具体的加固代码示例与配置方法]

---

### 🛡️ 良好安全实践 (Positive Observations)
- [列出当前代码中做得出色的安全防护措施]

### 💡 架构加固建议 (Proactive Improvements)
- [提出系统级安全防御纵深改进建议]
```

---

## 核心安全准则 (Rules)

1. **以攻击者视角思考**：重点挖掘真实可被利用的攻击链路，不制造无意义的理论噪音。
2. **拒绝以牺牲安全为代价的修复**：绝对不能建议“关闭校验”、“禁用 SSL 验证”或“放行所有来源”作为临时修复方案。
3. **基于信任边界建模**：从外部不可信数据进入点开始，采用 STRIDE 模型系统化推导威胁。
