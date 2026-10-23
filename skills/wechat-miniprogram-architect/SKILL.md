---
name: wechat-miniprogram-architect
description: Use when designing, building, refactoring, or reviewing WeChat Mini-Program (微信小程序) systems and enterprise applications. Invoke for double-thread performance optimization, setData fine-grained updates, subpackage architecture (independent packages, preload, async imports), clean layered architecture, global reactive state management, network interceptor with token refresh, Skyline engine adaptation, privacy compliance, and observability logging.
license: MIT
metadata:
  version: "1.1.0"
  domain: frontend-and-miniprogram-architecture
  triggers: 微信小程序架构, 小程序架构师, 微信小程序, 小程序性能优化, 小程序分包, 小程序状态管理, setData优化, Skyline渲染, wechat miniprogram, miniprogram architecture
  role: architect
  scope: architecture-and-engineering
  output-format: code-and-diagrams
  related-skills: frontend-ui-engineering, api-and-interface-design, performance-optimization, code-review-and-quality
---

# WeChat Mini-Program Architect (微信小程序架构师思想)

企业级微信小程序全栈架构专家，专注于**双线程模型底层优化、分包与体积治理、整洁分层架构、响应式状态管理、高可靠网络与全链路可观测性**。

---

## 微信小程序架构师六大核心心法

```
+-----------------------------------------------------------------------------------+
|                        1. 双线程模型认知 (Double-Thread Mindset)                    |
|   - 逻辑层 (JSCore) 与 渲染层 (WebView / Skyline) 物理隔离                         |
|   - 性能瓶颈永远在 JSBridge 通信开销，严控 setData 频次与体积                       |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        2. 分包与体积架构 (Subpackage & Bundle)                     |
|   - 主包极致瘦身 (≤ 1.5MB 黄金线)，仅留核心 TabBar + 基础骨架                      |
|   - 独立分包 (秒开裂变) + 分包预下载 (Preload) + 分包异步化 (Async Import)         |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        3. 整洁分层与领域抽象 (Clean Layered Architecture)          |
|   - 表现层 (WXML/WXSS/Page) -> Presenter/Store -> Domain Service -> Infrastructure|
|   - 核心业务逻辑下沉，不强依赖 wx.* 全局变量，保障单测与跨端复用能力             |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        4. 单一规范状态源 (Single Source of Truth)                 |
|   - 页面间通信优先 EventChannel 与 全局响应式 Store (MobX / Pinia)                |
|   - 严格避免使用全局 globalData 导致的数据流向失控与竞态问题                       |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        5. 基础设施韧性 (Resilient Infrastructure)                  |
|   - 请求拦截器：Token 无感自动刷新、防并发重复提交、全链路 TraceId 注入            |
|   - 本地缓存：内存 L1 + 微信 Storage L2 二级缓存策略，防高频同步 IO 阻塞            |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        6. 线上可观测性与合规 (Observability & Compliance)           |
|   - 微信实时日志 (RealtimeLogManager) + 页面生命周期链路埋点                      |
|   - 严格执行《用户隐私保护指引》按需授权 (Privacy Authorization) 与异常容灾降级    |
+-----------------------------------------------------------------------------------+
```

---

## 核心工作流 (Architecture Workflow)

1. **业务域拆分与分包规划**：
   - 识别高频核心路径与低频分支业务。
   - 制定主包、子业务分包、独立分包划分方案，配置 `preloadRule` 和 `subpackageAsyncloading`。
2. **状态模型与数据流设计**：
   - 确立规范数据源，区分服务端持久数据、客户端全局共享状态与页面级瞬态。
   - 页面回退时使用 `EventChannel` 或响应式 Store 监听，拒绝粗暴在 `onShow` 中全量重刷。
3. **渲染性能与通信契约设计**：
   - 页面初始化优先提供静态骨架（Skeleton），减少白屏感知时长（FCP）。
   - 涉及长列表必须采用虚拟滚动（Virtual List）或分页增量追加（`this.setData({ [`list[${index}]`]: newItem })`）。
   - 高频手势与复杂动画优先采用 WXS 脚本或 Skyline Worklet 线程直连渲染。
4. **统一网络与异常治理**：
   - 封装 `HttpClient`，实现请求排队、Token 过期重试队列、全链路错误映射与断网离线提示。
5. **发布前质量门禁审查**：
   - 检查主包体积是否超标、是否存在未解绑的全局 EventBus 监听器、是否通过 Audits 体验评分。

---

## 参考指南索引 (Reference Guides)

| 核心主题 | 参考文档 | 深度内容 |
| :--- | :--- | :--- |
| **双线程与渲染性能** | `references/double-thread-and-performance.md` | `setData` 原理、路径级增量更新、虚拟列表、WXS 动画 |
| **分包与体积治理** | `references/subpackage-and-bundle-architecture.md` | 主包瘦身、独立分包、预加载策略、分包异步化跨包调用 |
| **整洁分层架构与请求** | `references/layered-architecture-and-services.md` | 4 层架构规范、Token 无感刷新、防重复提交拦截器 |
| **状态管理与跨页通信** | `references/state-management-and-events.md` | EventChannel、响应式 Store、防内存泄露 EventBus 封装 |
| **安全合规与可观测性** | `references/security-observability-and-skyline.md` | 隐私按需授权、实时日志上报、全局错误捕获、Skyline 迁移 |

---

## 架构师硬性约束 (MUST DO / MUST NOT DO)

### MUST DO
- **路径化更新原则**：数组/对象局部变动必须使用精确路径键（如 `this.setData({ [`items[${idx}].status`]: 'DONE' })`），禁止全量重置大数组。
- **页面注销清理**：在 Page `onUnload` / Component `detached` 生命周期中必须显式解绑所有全局事件监听器和定时器。
- **异步接口 Promise 化**：所有 `wx.*` 异步 API 统一封装为 async/await 规范，并在最外层提供全局未捕获 Promise 拒绝监听。
- **冷启动轻量化**：`App.onLaunch` 中严禁执行耗时同步阻塞代码（如大量 `wx.getStorageSync`），复杂初始化必须异步延迟触发。
- **隐私授权前置拦截**：调用涉及用户信息、剪贴板、位置等敏感 API 前，必须经由统一合规组件触发 `wx.requirePrivacyAuthorize`。

### MUST NOT DO
- **严禁向 `setData` 传递与视图渲染无关的数据**：纯业务状态、定时器 ID、缓存数据严禁挂载在 Page `data` 中，直接挂在 `this` 实例上。
- **严禁高频调用 `setData`**：在 `onPageScroll` 或手势触摸事件中严禁高频直接执行 `setData`（必须防抖/节流或改用 WXS）。
- **严禁超大单次传输**：单次 `setData` 的数据包严禁超过 1024KB（微信官方红线），建议单次控制在 256KB 以内。
- **严禁滥用 `getCurrentPages()` 修改兄弟页面私有数据**：必须通过 `EventChannel` 或统一状态流同步。

---

## 经典架构代码模板 (Enterprise Code Templates)

### 1. 高性能路径增量更新 (Fine-Grained setData)

```typescript
// pages/order-list/index.ts
Page({
  data: {
    orders: [] as OrderItem[],
    isLoading: false
  },

  // 架构师规范：局部更新某个订单的状态，绝不重新 setData 整个 orders 数组
  updateOrderStatus(orderId: string, newStatus: string) {
    const index = this.data.orders.findIndex(item => item.id === orderId);
    if (index === -1) return;

    // 精确路径更新：仅传递发生变化的单个属性到渲染层
    this.setData({
      [`orders[${index}].status`]: newStatus,
      [`orders[${index}].updatedAt`]: Date.now()
    });
  }
});
```

### 2. 具备 Token 无感刷新的企业级 Http Client

```typescript
// infrastructure/http/client.ts
interface RequestConfig extends WechatMiniprogram.RequestOption {
  retryCount?: number;
  skipAuth?: boolean;
}

class HttpClient {
  private isRefreshing = false;
  private pendingRequests: Array<() => void> = [];

  async request<T>(config: RequestConfig): Promise<T> {
    const token = wx.getStorageSync('ACCESS_TOKEN');
    const headers = {
      'Content-Type': 'application/json',
      ...(token && !config.skipAuth ? { Authorization: `Bearer ${token}` } : {}),
      ...config.header
    };

    return new Promise((resolve, reject) => {
      wx.request({
        ...config,
        header: headers,
        success: async (res) => {
          if (res.statusCode === 200) {
            resolve(res.data as T);
          } else if (res.statusCode === 401 && !config.skipAuth) {
            // 401: Token 失效，进入排队无感刷新队列
            this.handleTokenExpired(config, resolve, reject);
          } else {
            reject(new Error(res.data?.['message'] || `HTTP Error ${res.statusCode}`));
          }
        },
        fail: (err) => reject(err)
      });
    });
  }

  private handleTokenExpired(config: RequestConfig, resolve: Function, reject: Function) {
    this.pendingRequests.push(() => {
      this.request(config).then(resolve).catch(reject);
    });

    if (!this.isRefreshing) {
      this.isRefreshing = true;
      this.refreshToken()
        .then((newToken) => {
          wx.setStorageSync('ACCESS_TOKEN', newToken);
          this.pendingRequests.forEach(cb => cb());
          this.pendingRequests = [];
        })
        .catch((err) => {
          wx.removeStorageSync('ACCESS_TOKEN');
          wx.reLaunch({ url: '/pages/login/index' });
        })
        .finally(() => {
          this.isRefreshing = false;
        });
    }
  }

  private async refreshToken(): Promise<string> {
    const refreshToken = wx.getStorageSync('REFRESH_TOKEN');
    // 调用刷新接口
    const res = await this.request<{ token: string }>({
      url: 'https://api.example.com/auth/refresh',
      method: 'POST',
      data: { refreshToken },
      skipAuth: true
    });
    return res.token;
  }
}

export const http = new HttpClient();
```
