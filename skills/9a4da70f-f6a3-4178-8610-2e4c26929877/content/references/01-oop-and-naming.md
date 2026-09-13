# 01 - 命名与面向对象规约 (Naming & OOP Standards)

## 1. 命名风格与契约 (Naming Conventions)

### 1.1 基础命名规则
- **代码中的命名严禁使用拼音与英文混合，更不允许直接使用中文。** 国际通用的专有名词（如 alibaba、taobao、rmb 等）可视为英文。
- **类名**：使用 `UpperCamelCase` 风格，必须遵从驼峰形式。
  - 抽象类命名使用 `Abstract` 或 `Base` 开头。
  - 异常类命名使用 `Exception` 结尾。
  - 测试类命名以它要测试的类的名称开始，以 `Test` 结尾。
- **方法名、参数名、成员变量、局部变量**：统一使用 `lowerCamelCase` 风格。
- **常量命名**：全部大写，单词间用下划线隔开，力求语义完整，不要嫌名字长。
  - `long` 或 `Long` 初始赋值时，必须使用大写的 `L`，不能是小写的 `l`（小写容易与数字 `1` 混淆）。

```java
// ❌ 错误示范
long count = 100l; // 容易看成 1001
String is_deleted_flag;
public void GetUserInfo();

// ✅ 正确示范
long count = 100L;
String deletedFlag;
public void getUserInfo();
public static final int MAX_RETRY_TIMES = 3;
```

### 1.2 POJO 布尔属性命名铁律 (The Boolean Getter Pitfall)
> [!CAUTION]
> **POJO 类中的任何布尔类型的变量，都不要加 `is` 前缀，否则部分框架解析会引起序列化错误。**

- **根本原因**：定义为 `Boolean isSuccess` 的属性，其 getter 方法会被自动生成为 `isSuccess()` 或 `getIsSuccess()`。部分 RPC 框架（如 Dubbo / Hessian）或 JSON 序列化工具（如 Jackson / Fastjson）在通过反射推断属性名时，会将 `isSuccess()` 对应的属性反推为 `success`，导致服务端与客户端属性名不一致，反序列化后值为 `null`。
- **正确规约**：POJO 属性统一命名为 `Boolean success`。

```java
// ❌ 错误示范
public class UserDTO implements Serializable {
    private Boolean isDeleted; // 反序列化时可能丢失属性
    private Boolean isVip;
}

// ✅ 正确示范
public class UserDTO implements Serializable {
    private Boolean deleted;
    private Boolean vip;
}
```

---

## 2. 数据类型与包装类规约 (Primitives vs Wrappers)

### 2.1 包装类型使用准则
1. **所有的 POJO 类属性必须使用包装数据类型**（如 `Integer`, `Long`, `Boolean` 等）。
   - *原因*：数据库查询结果可能是 `null`，如果 POJO 使用基本数据类型，ORM 框架在自动拆箱时会直接抛出 `NullPointerException`；且基本类型的默认值（如 `0`、`false`）会掩盖数据库真实的 `null` 语义。
2. **RPC 方法的返回值和参数必须使用包装数据类型**。
3. **所有的局部变量推荐使用基本数据类型**（减少堆内存开销与垃圾回收压力）。

```java
// ❌ 错误示范：实体类使用基本类型
public class OrderDO {
    private long id;
    private int status; // 如果数据库为 null，ORM 映射直接 NPE
}

// ✅ 正确示范
public class OrderDO {
    private Long id;
    private Integer status;
}
```

---

## 3. 金额与浮点数精确计算 (BigDecimal Calculation)

> [!IMPORTANT]
> **涉及金额、计费、费率等精确数值计算时，严禁使用 `float` 或 `double`，必须使用 `BigDecimal`。**

### 3.1 BigDecimal 构造规约
- **禁止使用 `new BigDecimal(double)` 构造方法**。`double` 的二进制表示存在精度偏差，`new BigDecimal(0.1)` 实际为 `0.1000000000000000055511151231257827021181583404541015625`。
- **必须使用 `BigDecimal(String)` 或 `BigDecimal.valueOf(double)`**。

```java
// ❌ 错误示范
BigDecimal amount1 = new BigDecimal(0.1); // 精度已丢失
double total = amount1.doubleValue() + 0.2;

// ✅ 正确示范
BigDecimal amount1 = new BigDecimal("0.1");
BigDecimal amount2 = BigDecimal.valueOf(0.2);
BigDecimal totalAmount = amount1.add(amount2);
```

### 3.2 BigDecimal 比较与四舍五入
- **禁止使用 `equals()` 比较大小**：`new BigDecimal("1.0").equals(new BigDecimal("1.00"))` 返回 `false`（`equals` 会同时比较精度 scale）。
- **必须使用 `compareTo()` 进行数值大小比较**：`amount1.compareTo(amount2) == 0`。
- **除法运算必须指定保留小数位数及舍入模式 (RoundingMode)**，防止因除不尽抛出 `ArithmeticException`（如 `1/3`）。

```java
// ❌ 错误示范：除法不指定舍入模式，除不尽时抛 ArithmeticException
BigDecimal result = amount.divide(divisor);

// ✅ 正确示范
BigDecimal result = amount.divide(divisor, 2, RoundingMode.HALF_UP);
```

---

## 4. 对象比较与 equals 契约 (Equals & HashCode Contract)

1. **重写 `equals` 必须同时重写 `hashCode`**。
   - *原因*：`Set`、`HashMap` 等哈希集合依赖 `hashCode` 定位桶，依赖 `equals` 确认元素唯一性。只重写 `equals` 会导致相同的对象在 `HashSet` 中重复存在。
2. **字符串/常量比较时，字面量在前面**，防止调用对象为 `null` 触发 NPE：
   ```java
   // ✅ 正确示范
   if ("SUCCESS".equals(status)) { ... }
   // 或使用 Objects.equals
   if (Objects.equals(status, targetStatus)) { ... }
   ```
3. **基本类型包装类的比较必须使用 `equals()`**，不能使用 `==`。
   - *原因*：`Integer` 等包装类在 `-128` 到 `127` 之间会使用常量池缓存，超出该范围 `==` 比较的是对象内存地址，返回 `false`。

```java
// ❌ 错误示范
Integer a = 200;
Integer b = 200;
if (a == b) { ... } // 结果为 false！

// ✅ 正确示范
if (a.equals(b)) { ... }
```

---

## 5. 集合与数组转换规约 (Array & Collection Conversion)

1. **集合转数组**：必须使用集合的 `toArray(T[] a)`，传入的是类型完全一致、大小为 0 的数组。
   ```java
   List<String> list = new ArrayList<>(2);
   list.add("ali");
   list.add("java");
   // ✅ 正确示范：传入 new String[0]（JVM 高效分配空间）
   String[] array = list.toArray(new String[0]);
   ```
2. **禁止将 `toArray()` 无参返回的 `Object[]` 强制向下转型为具体类型数组**（会抛出 `ClassCastException`）。
