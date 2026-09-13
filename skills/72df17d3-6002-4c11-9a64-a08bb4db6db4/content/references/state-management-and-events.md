# 微信小程序状态管理与跨页面通信架构 (State Management & Events)

## 一、跨页面通信方案横向对比

| 方案 | 适用场景 | 优点 | 缺点 / 架构陷阱 |
| :--- | :--- | :--- | :--- |
| **`EventChannel`** (推荐) | 父子页面跳转传参 & 回退反向通知 | 原生支持、生命周期与页面完全绑定、自动销毁 | 仅支持由 `wx.navigateTo` 产生的上下游页面 |
| **响应式 Store** (推荐) | 用户信息、购物车、全局配置、多端联动 | 状态单一可信源、支持计算属性与视图自动同步 | 需要构建工具支持（如 MobX / Pinia） |
| **全局 `EventBus`** | 跨分包长距离解耦广播通知 | 简单灵活，跨越任意组件与页面层级 | **极易造成内存泄漏**，页面卸载未注销会导致监听器多次触发 |
| **`app.globalData`** (慎用) | 静态配置数据读取 | 最原生最简单 | 无法响应式触发视图更新，易发生数据竞态与脏读 |

---

## 二、原生 `EventChannel` 高效数据回传

```typescript
// 1. 列表页点击编辑，跳转并建立监听通道
// pages/address-list/index.ts
Page({
  onEditAddress(e: any) {
    const addressId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/address-edit/index?id=${addressId}`,
      events: {
        // 监听来自编辑页保存成功后的反向事件
        addressSaved: (updatedData: AddressItem) => {
          this.updateLocalItem(updatedData);
        }
      }
    });
  }
});

// 2. 编辑页保存成功，触发通道事件并返回
// pages/address-edit/index.ts
Page({
  async onSave(formData: AddressItem) {
    await saveAddressApi(formData);
    const eventChannel = this.getOpenerEventChannel();
    if (eventChannel) {
      eventChannel.emit('addressSaved', formData);
    }
    wx.navigateBack();
  }
});
```

---

## 三、安全防内存泄漏的 `SafeEventBus`

```typescript
// infrastructure/events/safe-event-bus.ts
type EventHandler = (...args: any[]) => void;

class SafeEventBus {
  private events = new Map<string, Set<EventHandler>>();

  on(event: string, handler: EventHandler, pageCtx?: any): () => void {
    if (!this.events.has(event)) {
      this.events.set(event, new Set());
    }
    this.events.get(event)!.add(handler);

    const unbind = () => this.off(event, handler);

    // 架构师防呆设计：如果传入了 Page 实例，自动拦截 onUnload 进行注销
    if (pageCtx && typeof pageCtx.onUnload === 'function') {
      const originalUnload = pageCtx.onUnload;
      pageCtx.onUnload = function () {
        unbind();
        originalUnload.apply(this);
      };
    }

    return unbind;
  }

  off(event: string, handler: EventHandler) {
    const set = this.events.get(event);
    if (set) {
      set.delete(handler);
      if (set.size === 0) this.events.delete(event);
    }
  }

  emit(event: string, ...args: any[]) {
    const handlers = this.events.get(event);
    if (handlers) {
      handlers.forEach(fn => fn(...args));
    }
  }
}

export const eventBus = new SafeEventBus();
```
