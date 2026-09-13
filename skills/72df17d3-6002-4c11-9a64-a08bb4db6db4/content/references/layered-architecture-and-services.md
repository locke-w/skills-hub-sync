# 微信小程序整洁分层架构与网络服务 (Layered Architecture & Services)

## 一、标准四层架构分层规范

```
+-------------------------------------------------------------+
|                     1. 表现层 (Presentation)                |
|   - WXML 骨架、WXSS 响应式样式、Page/Component 视图配置     |
|   - 职责：只处理 UI 交互反馈、事件派发与骨架展示             |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
|                     2. 控制/状态层 (Presenter / Store)       |
|   - 响应式 Store (Pinia/MobX)、视图状态模型 (ViewModel)     |
|   - 职责：数据校验、局部状态响应式同步、计算派生属性         |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
|                     3. 领域服务层 (Domain Services)         |
|   - 纯业务用例 (Use Cases)、业务规则与计算公式              |
|   - 职责：纯 TypeScript 编写，无微信 API 强耦合，易于单测    |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
|                     4. 基础设施层 (Infrastructure)           |
|   - 网络请求客户端 (HttpClient)、本地双层缓存 (Storage)      |
|   - 微信 Native SDK 桥接封装 (wx.* API Promisify)           |
+-------------------------------------------------------------+
```

---

## 二、目录结构工程规范

```
src/
├── app.ts
├── app.json
├── app.wxss
├── components/             # 全局通用 UI 组件
│   └── skeleton/
├── pages/                  # 主包页面
│   └── home/
│       ├── index.ts
│       ├── index.wxml
│       ├── index.wxss
│       └── index.json
├── subpackages/            # 业务分包
│   └── trade/
├── domain/                 # 领域业务服务 (纯逻辑)
│   ├── services/
│   │   └── order-calculator.service.ts
│   └── models/
│       └── order.model.ts
├── store/                  # 全局状态管理
│   ├── user.store.ts
│   └── cart.store.ts
└── infrastructure/         # 基础设施
    ├── http/
    │   ├── client.ts       # 具备重试与 Token 刷新的客户端
    │   └── interceptor.ts
    ├── storage/
    │   └── cache-manager.ts# 内存+微信本地二级缓存
    └── logger/
        └── reporter.ts     # 微信实时日志上报
```

---

## 三、网络请求防并发重复提交与缓存

```typescript
// infrastructure/http/dedupe.ts
export class RequestDeduplicator {
  private activeMap = new Map<string, Promise<any>>();

  generateKey(url: string, method: string, data: any): string {
    return `${method}:${url}:${JSON.stringify(data || {})}`;
  }

  async run<T>(key: string, requestFn: () => Promise<T>): Promise<T> {
    if (this.activeMap.has(key)) {
      // 存在相同且尚未完成的请求，复用同一个 Promise 避免重复发送
      return this.activeMap.get(key)!;
    }

    const promise = requestFn().finally(() => {
      this.activeMap.delete(key);
    });

    this.activeMap.set(key, promise);
    return promise;
  }
}
```
