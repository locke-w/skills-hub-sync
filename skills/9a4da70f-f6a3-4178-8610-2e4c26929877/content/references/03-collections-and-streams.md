# 03 - 集合与流操作规约 (Collections & Streams)

## 1. 集合初始化容量计算 (Initial Capacity)

> [!IMPORTANT]
> **创建 `HashMap` / `HashSet` 时，必须显式指定初始容量。**
> 初始容量计算公式为：`initialCapacity = (int) (expectedSize / 0.75F + 1)`，或使用 Guava 的 `Maps.newHashMapWithExpectedSize(expectedSize)`。

### 1.1 规约原因
`HashMap` 默认初始容量为 16，负载因子为 0.75。当元素数量超过 `capacity * 0.75` 时会触发扩容（rehash），扩容操作涉及创建新数组与所有链表/红黑树节点的重新哈希，开销极大。

```java
// ❌ 错误示范：预知要存 1000 个元素却使用默认容量
Map<String, String> map = new HashMap<>(); // 将触发多次扩容，损耗性能

// ✅ 正确示范：预知存储 1000 个元素
// 计算方式：1000 / 0.75 + 1 = 1335 -> 实际 HashMap 会自动对齐至 2048
Map<String, String> map = new HashMap<>((int) (1000 / 0.75F + 1));
```

---

## 2. 集合常用操作避坑指南 (Collection Traps)

### 2.1 Arrays.asList() 不可修改与强转陷阱
`Arrays.asList()` 返回的是 `java.util.Arrays$ArrayList`（适配器内部类），并非 `java.util.ArrayList`。
- **陷阱 1**：不支持增删操作，调用 `add()` / `remove()` / `clear()` 会抛出 `UnsupportedOperationException`。
- **陷阱 2**：修改底层原始数组，会直接影响 `List` 的数据。

```java
// ❌ 错误示范
String[] array = new String[]{"a", "b"};
List<String> list = Arrays.asList(array);
list.add("c"); // 抛出 UnsupportedOperationException！

// ✅ 正确示范：使用真正可变的 ArrayList
List<String> safeList = new ArrayList<>(Arrays.asList(array));
safeList.add("c");
```

### 2.2 List.subList() 视图与并发修改陷阱
`list.subList(fromIndex, toIndex)` 返回的是原列表的内部视图（`SubList`），**绝不可向下强转为 `ArrayList`**（抛 `ClassCastException`）。
- 对 `subList` 子列表的修改会直接反映到原列表上。
- **致命陷阱**：在生成 `subList` 之后，**若对原列表进行了任何增删操作**，所有对子列表的访问都会直接抛出 `ConcurrentModificationException`。

```java
// ❌ 错误示范
List<String> original = new ArrayList<>(List.of("1", "2", "3", "4"));
List<String> sub = original.subList(0, 2);
original.add("5"); // 修改原列表
System.out.println(sub.get(0)); // 抛出 ConcurrentModificationException！

// ✅ 正确示范：如需独立使用，进行防御性复制
List<String> independentSub = new ArrayList<>(original.subList(0, 2));
```

### 2.3 Collectors.toMap 的 Key 冲突与 Null Value 崩溃
使用 Java Stream 的 `Collectors.toMap()` 时必须注意两大崩溃点：
1. **Key 重复**：默认抛出 `IllegalStateException: Duplicate key`。必须显式传入合并策略函数 `(v1, v2) -> v1`。
2. **Value 为 null**：JDK 8 底层 `Map.merge()` 遇到 value 为 `null` 时直接抛出 `NullPointerException`。

```java
// ❌ 错误示范：有重复 key 时直接崩溃；有 null value 时直接 NPE
Map<Long, String> userMap = userList.stream()
    .collect(Collectors.toMap(User::getId, User::getName));

// ✅ 正确示范：显式解决 Key 冲突，并过滤 null 值
Map<Long, String> safeUserMap = userList.stream()
    .filter(u -> u.getName() != null) // 过滤 null value
    .collect(Collectors.toMap(
        User::getId,
        User::getName,
        (existingVal, newVal) -> newVal // 出现重复 Key 时保留新值
    ));
```

---

## 3. 集合遍历与元素删除规约 (Iteration & Removal)

> [!CAUTION]
> **严禁在 foreach / for-in 循环里进行元素的 `remove` / `add` 操作。**
> `foreach` 语法糖本质使用 `Iterator`，但在循环体中直接调用 `list.remove()` 会导致 `modCount` 与 `expectedModCount` 不一致，抛出 `ConcurrentModificationException`。

```java
// ❌ 错误示范
List<String> list = new ArrayList<>();
list.add("1");
list.add("2");
for (String item : list) {
    if ("1".equals(item)) {
        list.remove(item); // 抛出 ConcurrentModificationException
    }
}

// ✅ 正确示范 1：使用 Iterator 显式删除
Iterator<String> iterator = list.iterator();
while (iterator.hasNext()) {
    String item = iterator.next();
    if ("1".equals(item)) {
        iterator.remove(); // 安全删除
    }
}

// ✅ 正确示范 2：Java 8+ 推荐 removeIf
list.removeIf("1"::equals);
```

---

## 4. 并行流 (Parallel Stream) 使用限制

1. `list.parallelStream()` 默认使用全局公共线程池 `ForkJoinPool.commonPool()`。
2. **严禁在并行流中执行阻塞 I/O（如数据库查询、RPC 调用、网络请求）**，否则会耗尽整个 JVM 共享的 ForkJoin 线程池，拖垮应用中所有依赖并行流或异步 CompletableFuture 的任务。
3. 并行流收集器必须使用线程安全的归约操作，严禁在外部共享非常量集合（如 `parallelStream().forEach(list::add)` 会导致数据丢失或越界）。
