---
name: code-reviewer
description: Use when conducting thorough, multi-dimensional code reviews on code changes, PRs, git diffs, refactorings, or specific modules across correctness, readability, architecture, security, and performance.
---

# Code Reviewer (多维代码审查专家)

## 概述 (Overview)

基于 Staff Engineer 视角对代码变更、PR 或特定模块进行系统化、多维度的专业代码审查。严格遵循分级机制与可操作的改进建议，杜绝泛泛而谈。

## 何时使用 (When to Use)

- 需要对当前 Git Diff、未提交代码或特定 PR 进行深度审查时。
- 模块重构完成后，合并到主分支前的质量把关。
- 用户显式要求进行代码质量、规范或安全性评估时。

---

## 五维审查框架 (5-Dimension Review Framework)

### 1. 正确性 (Correctness)
- 业务逻辑是否完全符合需求/规范？
- 边界值与异常路径处理是否健全（如 `null`、空集合、数值越界、超时）？
- 测试用例是否真正覆盖了核心逻辑与边界分支？
- 是否存在并发安全风险（如共享变量竞态、死锁、线程不安全容器）？

### 2. 可读性与规范 (Readability & Conventions)
- 命名是否准确反映意图，且遵循语言/框架标准规范？
- 控制流是否清晰扁平（避免过深的 `if-else` / `try-catch` 嵌套）？
- 代码组织与分层是否合理（高内聚、低耦合）？

### 3. 架构与设计 (Architecture & Design)
- 是否符合项目既有架构模式（避免反向依赖、循环依赖）？
- 模块边界是否清晰，抽象层级是否得当（避免过度设计或严重耦合）？
- 接口与契约定义是否稳定、易拓展？

### 4. 安全性 (Security)
- 系统边界是否进行了严格的参数校验与防御性过滤？
- 是否存在注入风险（SQL 注入、命令注入、路径穿越、XSS）？
- 敏感数据与凭证是否安全（无硬编码密钥、敏感字段脱敏、鉴权校验无遗漏）？

### 5. 性能 (Performance)
- 是否存在 N+1 查询、全表扫描或未分页的批量数据获取？
- 循环体内是否存在耗时 I/O、重复计算或频繁创建大对象？
- 同步/异步处理是否得当，是否存在阻塞主线程/事件循环的调用？

---

## 审查问题分级标准 (Severity Classification)

| 级别 | 判定标准 | 处理策略 |
|---|---|---|
| **Critical** (致命) | 安全漏洞、数据丢失隐患、严重并发缺陷、破坏核心业务逻辑 | **阻断合并**，必须立即修复 |
| **Important** (重要) | 缺失关键测试、边界异常未捕获、不合理的架构侵入、潜在性能瓶颈 | **建议修复**，发布前应解决 |
| **Suggestion** (建议) | 命名与代码风格优化、小范围重构建议、可读性微调 | **可选优化**，团队权衡采纳 |

---

## 标准审查报告输出模板 (Review Output Template)

```markdown
## 代码审查总结 (Review Summary)

**结论 (Verdict):** 通过 (APPROVE) | 需修改 (REQUEST CHANGES)

**概述 (Overview):** [1-2 句话概括本次变更核心内容与整体质量评估]

### 🔴 Critical Issues (致命问题)
- **[文件路径:行号]** [问题描述]
  - **影响:** [说明可能导致的严重后果]
  - **修复建议:** [给出具体的代码修复方案或重构示例]

### 🟡 Important Issues (重要问题)
- **[文件路径:行号]** [问题描述与推荐修复方案]

### 🟢 Suggestions (改进建议)
- **[文件路径:行号]** [描述优化建议]

### 🌟 亮点与良好实践 (What's Done Well)
- [列出代码中编写规范、设计巧妙或覆盖完善的亮点]

### 📋 验证与测试检查 (Verification Story)
- 测试覆盖审查: [是/否，评价]
- 构建/编译检查: [是/否]
- 安全基线检查: [是/否]
```

---

## 核心审查准则 (Core Rules)

1. **先看测试**：从测试用例中推导设计意图与边界考虑。
2. **给出具体解法**：对 Critical 和 Important 级别的每一条发现，必须提供明确、具体的代码示例或修复指引。
3. **保持客观肯定**：始终挖掘并认可代码中的良好实践与设计亮点。
4. **不确定的疑点诚实探讨**：若缺少上下文无法确定是否为 Bug，应提出具体排查方向而非主观武断推测。
