# 微信小程序安全合规、全链路可观测性与 Skyline 架构 (Security & Observability)

## 一、微信用户隐私合规治理（按需授权拦截）

微信要求必须先向用户明确提示《用户隐私保护指引》，同意后方可调用敏感 API（如剪贴板、相册、地理位置、手机号）。

```typescript
// infrastructure/privacy/privacy-guard.ts
export class PrivacyGuard {
  static async checkAndAuthorize(): Promise<boolean> {
    return new Promise((resolve) => {
      if (!wx.requirePrivacyAuthorize) {
        return resolve(true); // 低版本基础库向下兼容
      }

      wx.requirePrivacyAuthorize({
        success: () => resolve(true),
        fail: () => resolve(false)
      });
    });
  }

  // 包装敏感操作
  static async withPrivacyAuth<T>(action: () => Promise<T>): Promise<T | null> {
    const granted = await this.checkAndAuthorize();
    if (!granted) {
      wx.showToast({ title: '需要您的授权才能继续使用', icon: 'none' });
      return null;
    }
    return await action();
  }
}
```

---

## 二、微信实时日志（RealtimeLogManager）与全链路错误捕获

```typescript
// infrastructure/logger/logger.ts
const log = wx.getRealtimeLogManager ? wx.getRealtimeLogManager() : null;

export const logger = {
  info(msg: string, ...args: any[]) {
    if (log) log.info(msg, ...args);
    console.log(`[INFO] ${msg}`, ...args);
  },
  warn(msg: string, ...args: any[]) {
    if (log) log.warn(msg, ...args);
    console.warn(`[WARN] ${msg}`, ...args);
  },
  error(msg: string, ...args: any[]) {
    if (log) log.error(msg, ...args);
    console.error(`[ERROR] ${msg}`, ...args);
  }
};

// app.ts 全局未捕获异常埋点
App({
  onLaunch() {
    // 监听未处理的 JavaScript 脚本异常
    wx.onError((error) => {
      logger.error('Uncaught_JS_Error', { error });
    });

    // 监听未处理的 Promise Rejection
    wx.onUnhandledRejection((res) => {
      logger.error('Unhandled_Promise_Rejection', { reason: res.reason });
    });

    // 内存告警监听
    wx.onMemoryWarning((res) => {
      logger.warn('Memory_Warning_Triggered', { level: res.level });
    });
  }
});
```

---

## 三、Skyline 新一代渲染架构演进

Skyline 是微信自研的新一代渲染引擎，基于 C++ 重写，彻底摆脱 WebView 限制，达到 Native 级别的流畅度。

### 1. 架构师核心优势
* **单线程直连渲染模式**：支持 Worklet 动画，手势与动效在同一线程即时响应，FPS 稳定在 60+。
* **物理级页面栈**：真正的页面推入与返回原生动画，支持手势右滑返回与自定义转场。
* **原生组件同层渲染**：彻底解决 Video/Map/Canvas 在 WebView 时代的层级穿透与重影 Bug。

### 2. Skyline 页面级开启配置
```json
// page.json
{
  "renderer": "skyline",
  "componentFramework": "glass-easel",
  "navigationStyle": "custom"
}
```
