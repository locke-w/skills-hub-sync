# 微信小程序分包与体积治理架构 (Subpackage & Bundle Architecture)

## 一、分包体系设计原则

微信小程序总包上限为 20MB（部分类目可申请更高），单分包/主包上限为 2MB。
**架构师原则**：主包体积必须控制在 **1.5MB 黄金安全线** 以内，首屏耗时（FCP）压至 800ms 以内。

```
+-------------------------------------------------------------+
|                     主包 (Main Package)                     |
|  - 仅包含 TabBar 页面 (首页、分类、我的)                     |
|  - 公共全局样式 (app.wxss)、基础网络库、轻量 Store           |
|  - 全局骨架屏组件与核心拦截器                               |
+-------------------------------------------------------------+
         │                      │                      │
         ▼                      ▼                      ▼
+------------------+   +------------------+   +------------------+
| 业务分包 A (Trade)|   | 业务分包 B (User)|   | 独立分包 (Activity)
|  - 购物车 / 结算 |   |  - 个人中心 / 设置 |   |  - 秒开活动 / 裂变 |
|  - 订单详情 / 售后|   |  - 地址管理 / 积分 |   |  - 无需下载主包！  |
+------------------+   +------------------+   +------------------+
```

---

## 二、`app.json` 企业级分包配置方案

```json
{
  "pages": [
    "pages/home/index",
    "pages/category/index",
    "pages/profile/index"
  ],
  "subpackages": [
    {
      "root": "subpackages/trade",
      "name": "trade",
      "pages": [
        "pages/cart/index",
        "pages/checkout/index",
        "pages/order-detail/index"
      ]
    },
    {
      "root": "subpackages/activity",
      "name": "activity",
      "pages": [
        "pages/lucky-draw/index"
      ],
      "independent": true // 独立分包：分享卡片直接打开，不下载主包
    }
  ],
  "preloadRule": {
    "pages/home/index": {
      "network": "all",
      "packages": ["trade"] // 用户进入首页后，后台静默预下载交易分包
    }
  }
}
```

---

## 三、分包异步化 (Subpackage Asynchronous Import)

解决**跨分包组件复用与跨分包代码引入**的技术方案，彻底避免由于抽取公共代码导致主包体积膨胀。

### 1. 跨分包自定义组件异步加载

```json
// pages/home/index.json
{
  "usingComponents": {
    "trade-coupon-card": "/subpackages/trade/components/coupon-card/index"
  },
  "componentPlaceholder": {
    "trade-coupon-card": "view" // 占位标签，在分包未下载完成前先用 view 占位
  }
}
```

### 2. 跨分包 JS 代码异步动态导入

```typescript
// pages/home/index.ts
async onShareClick() {
  // 异步加载 trade 分包中的工具类函数
  const { generateTradePoster } = await import('../../subpackages/trade/utils/poster');
  const posterUrl = await generateTradePoster(this.data.goodsId);
  wx.previewImage({ urls: [posterUrl] });
}
```

---

## 四、静态资源与体积瘦身清单

1. **图片资源 100% 走 CDN**：小程序源码中严禁放置超过 10KB 的静态大图，全部上传对象存储（COS/OSS），本地仅保留极其关键的 TabBar 小图标。
2. **Icon 矢量化**：使用 SVG Data-URI 或 Mini-IconFont 代替 png 图片。
3. **Tree-Shaking 与依赖审查**：严禁全量引入大型 NPM 库（如全量 Lodash），使用 `lodash-es` 按需导出。
