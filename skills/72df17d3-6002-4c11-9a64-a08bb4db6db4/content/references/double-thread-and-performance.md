# 微信小程序双线程模型与极致性能调优 (Double-Thread & Performance)

## 一、双线程模型架构本质

微信小程序的运行环境分为**渲染层（View / WebView 或 Skyline）**与**逻辑层（AppService / JSCore 或 V8）**：

```
+-------------------------------------------------------------+
|                      渲染层 (WebView / Skyline)             |
|   - 解析 WXML 结构与 WXSS 样式                               |
|   - 维护虚拟 DOM 树 (Virtual DOM)                            |
|   - 捕获用户手势与触摸事件                                   |
+-------------------------------------------------------------+
                              ▲
                              │ 1. 序列化通信 (JSON.stringify / Native Bridge)
                              │ 2. 线程切换与数据反序列化
                              ▼
+-------------------------------------------------------------+
|                      逻辑层 (AppService / JSCore)           |
|   - 运行 JavaScript / TypeScript 业务逻辑                   |
|   - 处理网络请求、本地存储与定时器                          |
|   - 维护 Page 实例数据与触发 this.setData                   |
+-------------------------------------------------------------+
```

### 核心性能结论
1. **通信成本是首要瓶颈**：每次 `setData` 都会将数据从逻辑层序列化为 JSON 字符串，经由微信底层 Native 桥接，传递给渲染层反序列化并对比 DOM diff。
2. **频次与体积直接决定卡顿度**：高频调用 `setData` 或单次传输超大对象会导致通信队列拥塞，引起页面掉帧、点击无响应和输入延迟。

---

## 二、`setData` 五大架构级优化军规

### 1. 纯渲染数据与业务内部状态严格分离
* ❌ **错误做法**：将网络请求返回的整个大字典（含不需要展示的后端内部标识、临时分页游标、定时器 ID）一股脑塞入 `this.setData(res.data)`。
* ✅ **正确做法**：只有 WXML 模板中绑定的字段才放入 `setData`，其余纯业务数据直接挂在 `this` 实例上（如 `this._timer = setInterval(...)`、`this._rawMeta = res.meta`）。

### 2. 路径化精确更新 (Path-based Fine-grained Updates)
针对数组元素修改，严禁深拷贝整个数组后重新 `setData`：

```typescript
// ❌ 错误：传输全量 100 条数据到渲染层
const list = [...this.data.articles];
list[5].liked = true;
this.setData({ articles: list });

// ✅ 正确：仅传输发生变化的单个字段
this.setData({
  [`articles[5].liked`]: true,
  [`articles[5].likeCount`]: this.data.articles[5].likeCount + 1
});
```

### 3. 分页列表增量追加 (Append-only Paging)

```typescript
// 分页加载下一页数据
async loadNextPage() {
  const newItems = await fetchApi(this.page + 1);
  const startIndex = this.data.list.length;

  const updateMap: Record<string, any> = {};
  newItems.forEach((item, index) => {
    updateMap[`list[${startIndex + index}]`] = item;
  });

  this.setData(updateMap);
}
```

### 4. 数据节流与批量归并 (Debounce / Throttle)
在长列表连续滚动或快速点赞场景下，将毫秒内的多次 `setData` 归并为一次：

```typescript
class BatchDataUpdater {
  private queue: Record<string, any> = {};
  private timer: number | null = null;

  constructor(private pageCtx: any) {}

  update(key: string, value: any) {
    this.queue[key] = value;
    if (this.timer) return;

    this.timer = setTimeout(() => {
      this.pageCtx.setData(this.queue);
      this.queue = {};
      this.timer = null;
    }, 16); // 约 1 帧 (60fps) 间隔内归并
  }
}
```

---

## 三、WXS (WeiXin Script) 视图层直连渲染

针对拖拽、滑动吸顶、视差滚动等需要高频监听 touch 事件的场景，逻辑层处理会有严重延迟。**WXS 直接运行在渲染层，零线程通信延迟**：

```html
<!-- index.wxml -->
<wxs module="touchHandler">
  var startX = 0;
  function handleTouchStart(e, ownerInstance) {
    startX = e.touches[0].pageX;
  }
  function handleTouchMove(e, ownerInstance) {
    var moveX = e.touches[0].pageX;
    var deltaX = moveX - startX;
    // 直接在渲染层修改 DOM 样式，完全不经过逻辑层
    var ins = ownerInstance.selectComponent('.movable-box');
    ins.setStyle({
      transform: 'translateX(' + deltaX + 'px)'
    });
  }
  module.exports = {
    handleTouchStart: handleTouchStart,
    handleTouchMove: handleTouchMove
  };
</wxs>

<view
  class="movable-box"
  bindtouchstart="{{touchHandler.handleTouchStart}}"
  bindtouchmove="{{touchHandler.handleTouchMove}}">
  可流畅拖拽的卡片
</view>
```
