# 04 - 异常处理与日志规约 (Exceptions & Logs)

## 1. 异常处理铁律 (Exception Handling Iron Rules)

<EXTREMELY-IMPORTANT>
1. **严禁捕获异常后不作任何处理（静默吞掉异常）。**
2. **严禁使用 `e.printStackTrace()` 或 `System.out.println()` 输出异常。**
3. **`@Transactional` 事务注解必须显式指定 `rollbackFor = Exception.class`。**
</EXTREMELY-IMPORTANT>

### 1.1 异常捕获与抛出规范
- **禁止使用异常做流程控制**：异常的创建与堆栈抓取开销极大，条件分支应使用 `if-else`。
- **保留原始异常堆栈**：重新抛出自定义业务异常时，必须传入原始异常对象 `e` 作为 `cause`，否则会导致根因丢失。

```java
// ❌ 错误示范 1：吞掉异常
try {
    orderService.pay(orderId);
} catch (Exception e) {
    // 空代码块，生产故障时无任何线索
}

// ❌ 错误示范 2：丢失原始堆栈
try {
    orderService.pay(orderId);
} catch (SQLException e) {
    throw new BizException("PAYMENT_FAILED"); // 无法追踪原始 SQL 异常原因！
}

// ✅ 正确示范：记录关键入参并保留 cause
try {
    orderService.pay(orderId);
} catch (SQLException e) {
    log.error("Order payment db error, orderId: {}", orderId, e);
    throw new BizException(ErrorCode.DB_ERROR, "Order payment failed", e);
}
```

### 1.2 事务回滚注解规范
Spring 的 `@Transactional` 默认仅在遇到 `RuntimeException` 或 `Error` 时触发回滚。若发生受检异常（`Checked Exception` 如 `IOException`、`SQLException` 等），事务**不会**回滚，导致数据不一致。

```java
// ❌ 错误示范：受检异常发生时不回滚
@Transactional
public void processOrder(OrderDTO dto) throws IOException { ... }

// ✅ 正确示范：显式声明回滚范围为所有 Exception
@Transactional(rollbackFor = Exception.class)
public void processOrder(OrderDTO dto) { ... }
```

---

## 2. 日志规约与最佳实践 (Logging Standards)

### 2.1 日志门面与占位符
- **强制使用 SLF4J 门面**（通过 Lombok `@Slf4j` 或 `LoggerFactory.getLogger(X.class)`），不要绑定具体的日志实现类（如 Log4j、Logback）。
- **强制使用占位符 `{}` 输出日志**，禁止使用 `+` 操作符进行字符串拼接（字符串拼接即使在日志级别不满足时也会消耗 CPU 和内存创建 String 实例）。

```java
// ❌ 错误示范
log.info("Processing order: " + orderId + ", status: " + status);

// ✅ 正确示范
log.info("Processing order: {}, status: {}", orderId, status);
```

### 2.2 日志级别规范与性能防护
| 日志级别 | 适用场景 | 关键约束 |
| :--- | :--- | :--- |
| **ERROR** | 系统故障、无法恢复的错误、需要立即人工介入或告警 | 必须打印完整入参与堆栈信息 `log.error("...", param, e)` |
| **WARN** | 预期内的异常、非致命错误、降级处理、即将废弃的调用 | 避免产生告警风暴，清晰说明降级路径 |
| **INFO** | 核心业务里程碑、状态变更、系统启动参数、接口出入参摘要 | 控制输出频次，避免日志占满磁盘 |
| **DEBUG** | 研发排错细节数据 | 输出大对象序列化前必须加 `if (log.isDebugEnabled())` 判断 |

```java
// ✅ 正确示范：昂贵操作需进行级别判断保护
if (log.isDebugEnabled()) {
    log.debug("User complex payload: {}", JacksonUtil.toJson(hugeObject));
}
```

---

## 3. 敏感数据脱敏规范 (Sensitive Data Masking)

> [!CAUTION]
> **生产环境日志及对外 API 响应中，严禁明文打印用户隐私与敏感数据。**

- **手机号**：保留前 3 后 4 位，如 `138****1234`
- **身份证号**：保留前 6 后 4 位，如 `110101********1234`
- **银行卡号**：保留前 6 后 4 位，如 `622202******1234`
- **登录密码 / 秘钥 / Token**：完全禁止打印或用固定掩码 `******` 替换

```java
public final class DesensitizeUtil {
    private DesensitizeUtil() {}

    public static String maskMobile(String mobile) {
        if (mobile == null || mobile.length() != 11) {
            return mobile;
        }
        return mobile.replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2");
    }
}
```

---

## 4. MDC 全链路追踪 (TraceId Propagation)

在多服务调用与并发异步线程中，必须通过 `MDC (Mapped Diagnostic Context)` 注入并传递 `traceId`，使整条链路的日志可通过单一 ID 检索。

```java
public class TraceUtil {
    public static final String TRACE_ID = "traceId";

    public static void startTrace() {
        MDC.put(TRACE_ID, UUID.randomUUID().toString().replace("-", ""));
    }

    public static void endTrace() {
        MDC.remove(TRACE_ID);
    }
}
```
