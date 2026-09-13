# 02 - 并发编程与线程池规约 (Concurrency & Threads)

## 1. 线程池创建铁律 (Thread Pool Creation Iron Rule)

<EXTREMELY-IMPORTANT>
**线程资源必须通过线程池提供，不允许在应用中自行显式创建线程。**
**线程池严禁使用 `Executors` 去创建，必须通过 `ThreadPoolExecutor` 的方式显式创建，明确线程池运行规则。**
</EXTREMELY-IMPORTANT>

### 1.1 Executors 的 OOM 致命隐患
- `Executors.newFixedThreadPool(...)` 和 `Executors.newSingleThreadExecutor(...)`：
  - 允许的请求队列长度为 `Integer.MAX_VALUE`（内部采用无界 `LinkedBlockingQueue`），在并发积压时可能耗尽内存，导致 **OOM (OutOfMemoryError)**。
- `Executors.newCachedThreadPool(...)` 和 `Executors.newScheduledThreadPool(...)`：
  - 允许创建的最大线程数为 `Integer.MAX_VALUE`，瞬间高并发会导致创建过量线程，耗尽操作系统线程资源与内存，导致 **OOM / 系统假死**。

### 1.2 生产级 ThreadPoolExecutor 标准配置模板

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * 生产级通用线程池配置类
 */
public final class ThreadPoolFactory {

    private ThreadPoolFactory() {}

    /**
     * 创建业务专属线程池
     *
     * @param poolName 业务线程池名称前缀，便于排查定位日志
     * @param coreSize 核心线程数
     * @param maxSize  最大线程数
     * @param queueCap 有界阻塞队列容量
     * @return 线程池实例
     */
    public static ThreadPoolExecutor createCustomPool(String poolName, int coreSize, int maxSize, int queueCap) {
        return new ThreadPoolExecutor(
            coreSize,
            maxSize,
            60L,
            TimeUnit.SECONDS,
            new ArrayBlockingQueue<>(queueCap), // 强制指定有界队列
            new NamedThreadFactory(poolName),   // 强制自定义线程命名工厂
            new ThreadPoolExecutor.CallerRunsPolicy() // 推荐由调用方主线程退避兜底，或自定义拒绝报警
        );
    }

    /**
     * 自定义命名线程工厂
     */
    public static class NamedThreadFactory implements ThreadFactory {
        private final String namePrefix;
        private final AtomicInteger threadNumber = new AtomicInteger(1);
        private final ThreadGroup group;

        public NamedThreadFactory(String poolName) {
            SecurityManager s = System.getSecurityManager();
            this.group = (s != null) ? s.getThreadGroup() : Thread.currentThread().getThreadGroup();
            this.namePrefix = "pool-" + poolName + "-thread-";
        }

        @Override
        public Thread newThread(Runnable r) {
            Thread t = new Thread(group, r, namePrefix + threadNumber.getAndIncrement(), 0);
            if (t.isDaemon()) {
                t.setDaemon(false);
            }
            if (t.getPriority() != Thread.NORM_PRIORITY) {
                t.setPriority(Thread.NORM_PRIORITY);
            }
            return t;
        }
    }
}
```

---

## 2. ThreadLocal 防泄漏与串号铁律 (ThreadLocal Safety)

> [!CAUTION]
> **必须在 `finally` 块中回收自定义的 `ThreadLocal` 变量。尤其在线程池环境下，线程会被反复复用，未清除的 `ThreadLocal` 会导致业务数据串号污染与类加载器内存泄漏。**

### 2.1 泄漏与串号机理
`ThreadLocalMap` 的 `Entry` 弱引用 `key`（ThreadLocal 对象），但强引用 `value`（业务对象）。
1. 当外部无强引用时，`key` 被垃圾回收变为空，但只要线程不销毁，`value` 永远无法被回收，导致堆内存泄漏。
2. 线程池复用该线程处理下一个请求时，若读取旧的 `ThreadLocal`，将导致用户身份/租户上下文**数据串号严重事故**。

### 2.2 标准调用范式
```java
// ✅ 正确示范：try-finally 强制清理
public class UserContextHolder {
    private static final ThreadLocal<UserContext> CONTEXT = new ThreadLocal<>();

    public static void set(UserContext user) {
        CONTEXT.set(user);
    }

    public static UserContext get() {
        return CONTEXT.get();
    }

    public static void remove() {
        CONTEXT.remove();
    }
}

// 业务使用场景（如 Filter / AOP / 线程处理）
public void doBusiness(UserContext user) {
    try {
        UserContextHolder.set(user);
        // 执行核心业务逻辑
        processTask();
    } finally {
        UserContextHolder.remove(); // 强制在 finally 中清除
    }
}
```

---

## 3. 并发工具与锁机制规约 (Locks & Synchronization)

### 3.1 高并发计数器选型
- **高并发写场景**：优先使用 `LongAdder`，其通过分段累加（Cell 数组）降低 CAS 冲突，吞吐量远高于 `AtomicLong`。
- **低并发或需要绝对准确读取瞬间值场景**：可使用 `AtomicLong`。

```java
// ✅ 正确示范：高并发统计 QPS / 调用量
LongAdder requestCounter = new LongAdder();
requestCounter.increment();
long total = requestCounter.sum();
```

### 3.2 Lock 加锁与释放标准结构
- 获取锁必须在 `try` 代码块外，释放锁必须在 `finally` 块的第一行。

```java
// ✅ 正确示范
Lock lock = new ReentrantLock();
lock.lock();
try {
    // 临界区业务代码
    doSomething();
} finally {
    lock.unlock(); // 确保一定释放
}
```

### 3.3 双重检查锁 (DCL) 单例与 volatile
- 实现双重检查锁定单例模式时，单例引用变量必须声明为 `volatile`，防止指令重排导致对象未完全初始化时被提前暴露。

```java
// ✅ 正确示范
public class SingletonService {
    private static volatile SingletonService instance;

    private SingletonService() {}

    public static SingletonService getInstance() {
        if (instance == null) {
            synchronized (SingletonService.class) {
                if (instance == null) {
                    instance = new SingletonService();
                }
            }
        }
        return instance;
    }
}
```
