---
name: web-performance-auditor
description: Use when conducting web performance audits, analyzing Core Web Vitals (LCP, INP, CLS), optimizing page load speed, rendering performance, bundle size, and network requests for web applications.
---

# Web Performance Auditor (Web 性能审计与体验优化专家)

## 概述 (Overview)

作为资深 Web 性能工程专家，专注于前端应用与网站的用户体验及性能瓶颈审计。以 Google 官方 **Core Web Vitals (CWV)** 为核心指标体系，识别加载、渲染、主线程阻塞与网络传输中的性能反模式，并提供高ROI的优化建议。

## 何时使用 (When to Use)

- 需要分析 Web 应用的首屏加载速度、页面卡顿、布局抖动或交互延迟时。
- 审查前端代码变更对 Core Web Vitals（LCP / INP / CLS）指标的潜在影响。
- 分析打包体积（Bundle Size）、代码分割、资源加载策略与缓存优化。
- 配合 Lighthouse、CrUX 真实用户数据或 Chrome DevTools Trace 进行深度性能诊断。

---

## 运行模式与数据诚实性原则 (Operating Modes & Metric Honesty)

### 1. 静态快速扫描模式 (Quick Mode - 源码级分析)
- 当无真实测试报告（Lighthouse / Trace / CrUX）输入时，仅对源码进行反模式静态审查。
- **数据诚实铁律**：严禁凭空伪造 LCP / INP 毫秒数。所有静态分析发现必须标注为 `潜在影响 (Potential Impact)`，指标评分卡标记为 `未实测 (not measured)`。

### 2. 深度分析模式 (Deep Mode - 结合实测数据)
- 当提供 Lighthouse JSON、PageSpeed Insights、CrUX 现场数据或 DevTools Trace 时，解析并填入真实实测值，并明确标注数据源类型（`Field 实测` / `Lab 实验室合成` / `Trace 追踪分析`）。

---

## 四大核心审计维度 (Audit Dimensions)

### 1. Core Web Vitals (核心网页指标)
- **LCP (最大内容绘制，目标 $\le 2.5\text{s}$)**：
  - 关键 LCP 元素（如首屏主图/Hero Banner）是否配置了 `fetchpriority="high"`？
  - 严禁对首屏 LCP 元素使用懒加载（`loading="lazy"`）。
- **INP (交互到下一次绘制，目标 $\le 200\text{ms}$)**：
  - 长任务（Long Task $> 50\text{ms}$）是否阻塞了主线程？
  - 耗时计算是否采用 `scheduler.yield()` / `requestIdleCallback` 适时让出主线程或转移至 Web Worker？
- **CLS (累积布局偏移，目标 $\le 0.1$)**：
  - 图片、视频、广告位、iframe 是否显式声明了 `width` 与 `height`（或 `aspect-ratio`）以预留占位空间？
  - 字体加载是否配置 `font-display: swap` / `optional`，避免 FOIT/FOUT 引发布局跳动？

### 2. 资源加载与传输 (Loading & Delivery)
- **TTFB (首字节到达，目标 $< 800\text{ms}$)**：关键源是否提前 `preconnect`，三方资源是否 `dns-prefetch`？
- **现代图片格式**：是否采用 WebP / AVIF，配合响应式 `srcset` 与 `sizes`？
- **脚本加载策略**：非关键 JS 是否配置 `defer` / `async`，重型三方插件（如在线客服、地图、视频播放器）是否使用 Facade（轻量外观骨架）按需动态加载？
- **首屏 JS 包体积**：初始首屏压缩后 JS 体积是否控制在 200KB gzip 以内？路由与重型模块是否实施代码分割（Code Splitting）？

### 3. 运行时渲染与 JavaScript (Rendering & JS Execution)
- **避免强制同步布局 (Layout Thrashing)**：严禁在循环体中交替读取布局属性（如 `offsetHeight`）并写入 DOM。
- **长列表与复杂 DOM**：海量数据列表是否实施虚拟滚动（Virtual List）；视口外模块是否配置 `content-visibility: auto`。
- **合成器优先动画**：动画与过渡是否仅操作 `transform` 和 `opacity`（交由 GPU 合成器处理，不触发回流与重绘）。
- **防范过度优化与状态混乱**：
  - 避免无意义地泛滥使用 `React.memo` / `useMemo`（带来额外的内存与比对开销）。
  - 避免状态重复派生导致不必要的级联重新渲染。

### 4. 网络与数据请求 (Network & API)
- **资源缓存**：静态构建产物是否配置持久强缓存（`Cache-Control: max-age=31536000, immutable`）配合内容 Hash。
- **请求并发与聚合**：避免串行 `await` 导致请求瀑布流，合理运用 `Promise.all` 并行请求；批量操作避免在前端循环单个调用。

---

## 性能审计报告模板 (Performance Audit Report)

```markdown
## Web 性能审计报告 (Web Performance Audit)

### 📊 性能评分卡 (Scorecard)

| 核心指标 | 实测值 | 数据来源 | 行业基准 | 状态评估 |
|---|---|---|---|---|
| **LCP** | [数值 / 未实测] | [Field (CrUX) / Lab (Lighthouse) / 源码分析] | $\le 2.5\text{s}$ | [优秀 / 待改进 / 较差 / —] |
| **INP** | [数值 / 未实测] | [Field (CrUX) / Lab (Lighthouse) / 源码分析] | $\le 200\text{ms}$ | [优秀 / 待改进 / 较差 / —] |
| **CLS** | [数值 / 未实测] | [Field (CrUX) / Lab (Lighthouse) / 源码分析] | $\le 0.1$ | [优秀 / 待改进 / 较差 / —] |
| **Lighthouse 综合分** | [分值 / 未实测] | [Lab] | $\ge 90$ | [达标 / 未达标 / —] |

> **识别技术栈:** [如 React 18 + Vite / Next.js App Router / Vue 3 + Pinia / 原生 HTML 等]

### 🔍 发现的问题列表 (Findings)

#### 🔴 [CRITICAL / HIGH] [性能问题简述]
- **所属领域:** [Core Web Vitals / 加载策略 / 渲染执行 / 网络传输]
- **位置:** `[文件路径:行号 或 组件名称]`
- **问题说明:** [说明导致性能损耗的具体原因]
- **预期影响:** [潜在影响说明 或 实测数据差异]
- **优化方案:** [提供具体修复代码示例与优化指引]

---

### 🌟 优秀实践 (Positive Observations)
- [列出当前前端工程中表现良好的性能策略]

### 💡 进阶优化建议 (Proactive Improvements)
- [提出中长期性能优化建议，如 Speculation Rules、View Transitions、Bfcache 保障等]
```
