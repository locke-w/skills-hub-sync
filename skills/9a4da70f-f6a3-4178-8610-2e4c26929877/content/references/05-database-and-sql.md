# 05 - 数据库与 SQL 持久层规约 (MySQL & ORM)

## 1. 建表与 DDL 规约 (Table Design & DDL)

### 1.1 命名与字段基础规范
- **表名、字段名**：必须使用小写字母或数字，禁止出现数字开头，禁止两个下划线中间只出现数字。
- **表名禁止使用复数名词**：例如订单表命名为 `trade_order`，而非 `trade_orders`。
- **存储引擎与字符集**：必须使用 `InnoDB` 存储引擎与 `utf8mb4` 字符集（支持 Emoji 与全量 Unicode）。
- **主键设计**：必须是 `bigint unsigned NOT NULL AUTO_INCREMENT`，单机或分库分表场景使用雪花算法生成 64 位整型 ID。
- **必备三字段**：所有表必须包含 `id`、`gmt_create`、`gmt_modified`。

### 1.2 标准建表 DDL 模板
```sql
CREATE TABLE `tb_trade_order` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `order_sn` varchar(64) NOT NULL DEFAULT '' COMMENT '业务订单流水号',
  `user_id` bigint unsigned NOT NULL DEFAULT '0' COMMENT '买家用户ID',
  `total_amount` decimal(12,2) NOT NULL DEFAULT '0.00' COMMENT '订单总金额(元)',
  `order_status` tinyint NOT NULL DEFAULT '0' COMMENT '状态: 0-待支付, 1-已支付, 2-已发货, 3-已完成, 4-已取消',
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0' COMMENT '逻辑删除: 0-正常, 1-已删除',
  `gmt_create` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_sn` (`order_sn`),
  KEY `idx_user_status` (`user_id`, `order_status`),
  KEY `idx_gmt_create` (`gmt_create`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='交易订单主表';
```

---

## 2. 索引设计规约 (Index Guidelines)

1. **命名规范**：
   - 唯一索引：`uk_字段名` 或 `uk_字段1_字段2`
   - 普通索引：`idx_字段名` 或 `idx_字段1_字段2`
2. **索引数量控制**：单表索引数量建议控制在 6 个以内。索引虽加速查询，但会显著降低 `INSERT` / `UPDATE` 吞吐量并增加磁盘与 Buffer Pool 开销。
3. **最左前缀匹配**：建立联合索引 `idx_a_b_c` 时，查询条件必须包含最左侧字段 `a` 才能有效走索引；范围查询（`>`, `<`）会导致其右侧列索引失效。
4. **字符串索引前缀长度**：`varchar(255)` 等较长字段建立索引时，需评估区分度并指定前缀长度（如 `KEY idx_email (email(20))`），降低索引体积。

---

## 3. SQL 编写与查询性能规约 (SQL Performance)

<EXTREMELY-IMPORTANT>
1. **严禁在生产代码中使用 `SELECT *` 查询。**
2. **严禁在 SQL 中使用字符串拼接，防范 SQL 注入。**
3. **`count(*)` 优于 `count(1)` 与 `count(col)`。**
</EXTREMELY-IMPORTANT>

### 3.1 杜绝 SELECT *
- **原因 1**：无法命中覆盖索引（Covering Index），强制触发回表（Bookmark Lookup）。
- **原因 2**：消耗额外的网络带宽与 JVM 堆内存。
- **原因 3**：当数据表新增或修改列类型时，可能引发应用层反序列化异常。

```sql
-- ❌ 错误示范
SELECT * FROM tb_trade_order WHERE user_id = 1001;

-- ✅ 正确示范：按需查询字段
SELECT id, order_sn, total_amount, order_status FROM tb_trade_order WHERE user_id = 1001;
```

### 3.2 深度分页优化 (Deep Pagination)
当 `OFFSET` 过大时（如 `LIMIT 1000000, 20`），MySQL 需要扫描 1000020 行并丢弃前 100 万行，耗时极长。
- **优化方案：延迟关联（基于覆盖索引的子查询）**：

```sql
-- ❌ 低效分页：扫描 1000020 行数据回表
SELECT id, order_sn, total_amount FROM tb_trade_order 
ORDER BY id LIMIT 1000000, 20;

-- ✅ 高效优化：先在索引树快速定位 ID，再关联查询
SELECT t.id, t.order_sn, t.total_amount 
FROM tb_trade_order t
JOIN (
    SELECT id FROM tb_trade_order ORDER BY id LIMIT 1000000, 20
) AS tmp ON t.id = tmp.id;
```

---

## 4. MyBatis / ORM 防御性规约 (MyBatis Best Practices)

### 4.1 SQL 注入防范：#{} vs ${}
- **强制使用 `#{}`**：MyBatis 会将其编译为 PreparedStatement 的参数占位符 `?`，防止 SQL 注入。
- **慎用 `${}`**：`${}` 是纯文本字符串替换。仅在动态传入 ORDER BY 列名或表名时使用，且**必须在 Java 代码中做严格的白名单校验**。

```xml
<!-- ❌ 错误示范：存在 SQL 注入严重漏洞 -->
<select id="queryByName" resultType="OrderDO">
    SELECT id, order_sn FROM tb_trade_order WHERE user_name = '${userName}'
</select>

<!-- ✅ 正确示范：预编译占位符 -->
<select id="queryByName" resultType="OrderDO">
    SELECT id, order_sn FROM tb_trade_order WHERE user_name = #{userName}
</select>
```

### 4.2 批量操作大小限制
在 MyBatis XML 中使用 `<foreach>` 批量插入或 `IN` 查询时，**必须在应用层做分批处理（如每次最多 500 条）**，防止生成超大 SQL 导致 MySQL `max_allowed_packet` 报错或锁表超时。
