# MySQL 内容笔记

资料来源：`E:\生成式AI\Mysql数据库-牛子` 目录下的 10 份课程 PDF。  
整理日期：2026-07-13  
定位：面向 MySQL 入门学习、SQL 基础查询、表管理、数据处理和进阶数据库对象的复习笔记。

## 目录

- [1. SQL 与基本 SELECT](#1-sql-与基本-select)
- [2. MySQL 运算符](#2-mysql-运算符)
- [3. 多表查询](#3-多表查询)
- [4. 单行函数](#4-单行函数)
- [5. 聚合函数、GROUP BY 与 HAVING](#5-聚合函数group-by-与-having)
- [6. 子查询](#6-子查询)
- [7. 创建和管理数据库与表](#7-创建和管理数据库与表)
- [8. 数据处理与视图](#8-数据处理与视图)
- [9. 触发器、存储过程和存储函数](#9-触发器存储过程和存储函数)
- [10. 评价问题基础入门](#10-评价问题基础入门)
- [11. 学习路线建议](#11-学习路线建议)

## 1. SQL 与基本 SELECT

对应资料：`1.MySQL_基本SELECT的语句.pdf`

### 1.1 SQL 分类

SQL 是关系型数据库的通用查询语言，MySQL 支持标准 SQL，同时也有自己的语法扩展。

常见分类：

- DDL：数据定义语言，用于创建、修改、删除数据库对象，例如 `CREATE`、`ALTER`、`DROP`。
- DML：数据操作语言，用于增删改查数据，例如 `INSERT`、`DELETE`、`UPDATE`、`SELECT`。
- DCL：数据控制语言，用于管理权限和安全级别，例如授权、撤销权限等。

学习重点：`SELECT` 是查询基础，也是后续多表查询、函数、分组、子查询的前提。

### 1.2 SELECT 基本结构

常见写法：

```sql
SELECT 字段1, 字段2
FROM 表名;
```

查询所有字段：

```sql
SELECT *
FROM 表名;
```

给字段或表达式起别名：

```sql
SELECT last_name AS name, salary * 12 AS annual_salary
FROM employees;
```

### 1.3 表结构与过滤

查看表结构通常是写查询前的第一步，目的是确认字段名、字段类型和可用数据。

过滤数据使用 `WHERE`：

```sql
SELECT employee_id, last_name, salary
FROM employees
WHERE salary > 10000;
```

常见过滤条件：

- 数值比较：`>`、`>=`、`<`、`<=`、`=`、`<>`
- 范围：`BETWEEN ... AND ...`
- 集合：`IN (...)`
- 模糊匹配：`LIKE`
- 空值判断：`IS NULL`、`IS NOT NULL`

注意：判断空值不要写 `= NULL`，应使用 `IS NULL`。

### 1.4 排序与分页

排序使用 `ORDER BY`：

```sql
SELECT last_name, salary
FROM employees
ORDER BY salary DESC;
```

分页常用 `LIMIT`：

```sql
SELECT employee_id, last_name
FROM employees
LIMIT 0, 10;
```

学习建议：

- 先能写出基础 `SELECT ... FROM ... WHERE ...`。
- 再练习排序、分页、别名和去重。
- 查询结果不符合预期时，优先检查字段名、过滤条件和空值判断。

## 2. MySQL 运算符

对应资料：`2.MySQL运算符.pdf`

### 2.1 算术运算符

常见算术运算：

- `+`：加法
- `-`：减法
- `*`：乘法
- `/` 或 `DIV`：除法
- `%` 或 `MOD`：取模

示例：

```sql
SELECT salary, salary * 12 AS annual_salary
FROM employees;
```

注意：

- MySQL 中 `+` 表示数值相加，不表示字符串拼接。
- 字符串拼接通常使用 `CONCAT()`。
- 非数值参与数值运算时，MySQL 可能尝试类型转换，转换失败时容易得到非预期结果。

### 2.2 比较运算符

常见比较：

```sql
SELECT *
FROM employees
WHERE salary >= 8000;
```

常用条件：

- `=`、`<>` 或 `!=`
- `<`、`<=`、`>`、`>=`
- `BETWEEN ... AND ...`
- `IN (...)`
- `LIKE`
- `IS NULL`

### 2.3 逻辑运算符

常见逻辑：

- `AND`：多个条件同时成立
- `OR`：多个条件任一成立
- `NOT`：取反
- `XOR`：异或

示例：

```sql
SELECT last_name, salary, department_id
FROM employees
WHERE salary > 8000 AND department_id = 60;
```

注意：多个逻辑条件组合时建议使用括号明确优先级。

### 2.4 位运算符与优先级

位运算通常用于底层标记、权限位等场景，入门阶段只需了解。

学习重点：

- 写复杂条件时，用括号表达意图。
- 不要依赖自己记忆运算符优先级，SQL 可读性更重要。

## 3. 多表查询

对应资料：`3.MySQL-多表查询.pdf`

### 3.1 为什么需要多表查询

实际业务通常会把不同实体拆到不同表中，例如员工表、部门表、职位表。要得到完整信息，就需要按关联字段连接多张表。

示例目标：查询员工姓名和部门名称。

### 3.2 笛卡尔积

如果多表查询没有写连接条件，会产生笛卡尔积，即两张表的每一行互相组合，结果数量会急剧变大。

错误倾向：

```sql
SELECT last_name, department_name
FROM employees, departments;
```

应该补充连接条件：

```sql
SELECT e.last_name, d.department_name
FROM employees e
JOIN departments d
  ON e.department_id = d.department_id;
```

### 3.3 常见连接

- 内连接：只返回两边匹配的数据。
- 左外连接：保留左表全部数据，右表没有匹配则为 `NULL`。
- 右外连接：保留右表全部数据，左表没有匹配则为 `NULL`。
- 交叉连接：产生笛卡尔积，通常需要谨慎使用。

常用写法：

```sql
SELECT e.last_name, d.department_name
FROM employees e
LEFT JOIN departments d
  ON e.department_id = d.department_id;
```

### 3.4 UNION

`UNION` 用于合并多个查询结果。

```sql
SELECT employee_id, last_name FROM employees
UNION
SELECT employee_id, last_name FROM retired_employees;
```

注意：

- 多个查询的列数应一致。
- 对应列的数据类型要兼容。
- `UNION` 会去重；如果不需要去重，可考虑 `UNION ALL`。

学习建议：

- 多表查询先找“表与表之间的关联字段”。
- 优先使用显式 `JOIN ... ON ...`，可读性更好。
- 遇到结果数量异常变多，优先检查是否漏了连接条件。

## 4. 单行函数

对应资料：`4.MySQL-单行函数.pdf`

单行函数对每一行输入返回一个结果，可以嵌套使用，参数可以是字段、表达式或固定值。

### 4.1 数值函数

常见用途：

- 四舍五入
- 取绝对值
- 向上/向下取整
- 随机数
- 取模

示例：

```sql
SELECT salary, ROUND(salary / 30, 2) AS daily_salary
FROM employees;
```

### 4.2 字符串函数

常见用途：

- 拼接字符串：`CONCAT`
- 大小写转换
- 截取字符串
- 获取长度
- 替换内容
- 去除空格

示例：

```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name
FROM employees;
```

### 4.3 日期和时间函数

常见用途：

- 获取当前日期或时间
- 提取年月日
- 日期加减
- 计算日期差
- 格式化日期

示例：

```sql
SELECT CURDATE() AS today, NOW() AS current_time;
```

### 4.4 流程控制函数

用于在查询结果中写条件判断。

示例：

```sql
SELECT last_name,
       salary,
       CASE
         WHEN salary >= 10000 THEN 'high'
         WHEN salary >= 6000 THEN 'middle'
         ELSE 'low'
       END AS salary_level
FROM employees;
```

### 4.5 加密、解密与信息函数

这类函数可用于获取数据库信息、用户信息或进行简单加密处理。入门阶段重点是知道它们存在，实际项目中涉及密码、密钥、安全时应更谨慎，不能把数据库函数当作完整安全方案。

## 5. 聚合函数、GROUP BY 与 HAVING

对应资料：`5.MySQL-聚合函数.pdf`

### 5.1 常见聚合函数

聚合函数作用于一组数据，并返回一个统计结果。

常见函数：

- `AVG()`：平均值
- `SUM()`：求和
- `MAX()`：最大值
- `MIN()`：最小值
- `COUNT()`：计数

示例：

```sql
SELECT MAX(salary), MIN(salary), AVG(salary), SUM(salary)
FROM employees;
```

注意：聚合函数不能直接嵌套调用，例如不应写成 `AVG(SUM(...))`。

### 5.2 GROUP BY

`GROUP BY` 用于分组统计。

```sql
SELECT department_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY department_id;
```

学习重点：

- `SELECT` 中非聚合字段通常要出现在 `GROUP BY` 中。
- 分组字段决定了统计粒度。

### 5.3 HAVING

`WHERE` 过滤分组前的数据，`HAVING` 过滤分组后的结果。

```sql
SELECT department_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY department_id
HAVING AVG(salary) > 8000;
```

### 5.4 SELECT 执行理解

写 SQL 时通常按：

```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
HAVING ...
ORDER BY ...
LIMIT ...
```

理解执行逻辑时可以按：

1. 先确定数据来源 `FROM`
2. 再按行过滤 `WHERE`
3. 然后分组 `GROUP BY`
4. 再做分组过滤 `HAVING`
5. 再选择输出字段 `SELECT`
6. 最后排序和分页

## 6. 子查询

对应资料：`6.MySQL_子查询.pdf`

子查询是嵌套在另一个查询中的查询，通常用于把一个查询结果作为另一个查询的条件。

### 6.1 基本形式

示例：查询工资高于 Abel 的员工。

```sql
SELECT last_name, salary
FROM employees
WHERE salary > (
  SELECT salary
  FROM employees
  WHERE last_name = 'Abel'
);
```

注意：

- 子查询应放在括号中。
- 子查询一般放在比较条件右侧，可读性更好。
- 单行子查询对应单行操作符，多行子查询对应多行操作符。

### 6.2 单行子查询

返回一行结果，常配合：

- `=`
- `>`
- `>=`
- `<`
- `<=`
- `<>`

### 6.3 多行子查询

返回多行结果，常配合：

- `IN`
- `ANY`
- `ALL`

示例：

```sql
SELECT employee_id, last_name
FROM employees
WHERE department_id IN (
  SELECT department_id
  FROM departments
  WHERE location_id = 1700
);
```

### 6.4 相关子查询

相关子查询会引用外层查询的数据，通常每处理外层一行，就需要结合内层查询判断。

适用场景：

- 查询每个部门中工资高于本部门平均工资的员工。
- 检查某条记录是否存在关联数据。

学习建议：

- 先能读懂单行子查询。
- 再练习 `IN` 型多行子查询。
- 最后理解相关子查询和 `EXISTS`。

## 7. 创建和管理数据库与表

对应资料：`7.MySQL-创建和管理表.pdf`

### 7.1 数据存储层级

MySQL 中常见层级：

数据库服务器 -> 数据库 -> 数据表 -> 行与列。

完整存储过程通常包括：

1. 创建数据库
2. 确认字段
3. 创建数据表
4. 插入数据

### 7.2 命名规则

建议：

- 数据库名、表名、字段名语义清楚。
- 避免空格和特殊字符。
- 不要和保留字冲突；如果必须使用，需要用反引号包裹。
- 同一类字段的数据类型要保持一致。

### 7.3 创建数据库

```sql
CREATE DATABASE db_name;
```

指定字符集：

```sql
CREATE DATABASE db_name
DEFAULT CHARACTER SET utf8mb4;
```

### 7.4 创建表

```sql
CREATE TABLE students (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  age INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

常见约束：

- `PRIMARY KEY`：主键
- `NOT NULL`：不能为空
- `UNIQUE`：唯一
- `DEFAULT`：默认值
- `AUTO_INCREMENT`：自增
- `FOREIGN KEY`：外键

### 7.5 修改、重命名和删除

修改表结构：

```sql
ALTER TABLE students ADD email VARCHAR(100);
```

重命名表：

```sql
RENAME TABLE old_name TO new_name;
```

删除表：

```sql
DROP TABLE students;
```

注意：`DROP` 属于高风险操作，执行前要确认环境和备份。

## 8. 数据处理与视图

对应资料：`8.MySQL-数据处理与展示.pdf`

### 8.1 插入数据

插入完整字段：

```sql
INSERT INTO departments
VALUES (70, 'Pub', 100, 1700);
```

插入指定字段：

```sql
INSERT INTO departments(department_id, department_name)
VALUES (100, 'Finance');
```

建议：实际项目中优先写明字段名，避免表结构变化后插入顺序出错。

### 8.2 更新数据

```sql
UPDATE employees
SET salary = salary * 1.1
WHERE department_id = 60;
```

注意：更新必须认真写 `WHERE`。没有 `WHERE` 可能会更新整张表。

### 8.3 删除数据

```sql
DELETE FROM employees
WHERE employee_id = 100;
```

注意：删除前先用同样的 `WHERE` 写 `SELECT` 检查影响范围。

### 8.4 视图

视图可以理解为保存好的查询结果结构，本身通常不直接存储数据，而是基于基础表查询。

创建视图：

```sql
CREATE VIEW employee_department_view AS
SELECT e.employee_id, e.last_name, d.department_name
FROM employees e
JOIN departments d
  ON e.department_id = d.department_id;
```

使用视图：

```sql
SELECT *
FROM employee_department_view;
```

适用场景：

- 简化复杂查询
- 隐藏部分字段
- 提供稳定的数据访问层

注意：视图依赖基础表，基础表结构变化可能影响视图。

## 9. 触发器、存储过程和存储函数

对应资料：`9.MySQL-触发器、存储过程和函数.pdf`

### 9.1 触发器

触发器是在特定事件发生时自动执行的数据库逻辑。常见事件包括：

- `INSERT`
- `UPDATE`
- `DELETE`

触发时间：

- `BEFORE`
- `AFTER`

基本结构：

```sql
CREATE TRIGGER trigger_name
BEFORE INSERT ON table_name
FOR EACH ROW
BEGIN
  -- 触发器逻辑
END;
```

适用场景：

- 插入商品时自动创建库存记录
- 修改数据时记录审计日志
- 删除数据时同步清理关联记录

注意：

- 触发器会自动执行，调试成本较高。
- 过度使用会让业务逻辑隐藏在数据库中，不利于排查。

### 9.2 存储过程

存储过程是一组预先保存的 SQL 逻辑，可以被调用执行。

适用场景：

- 重复执行的复杂数据库操作
- 批处理任务
- 封装多步 SQL

优点：

- 减少重复 SQL
- 逻辑靠近数据库，执行效率可能更稳定
- 可封装复杂操作

风险：

- 业务逻辑分散到数据库中，代码层不容易发现。
- 调试、版本管理和迁移需要额外规范。

### 9.3 存储函数

存储函数通常有返回值，适合封装计算逻辑。

与存储过程的区别：

- 存储函数强调返回一个结果。
- 存储过程更强调执行一组动作。

## 10. 评价问题基础入门

对应资料：`10.评价问题基础入门.pdf`

这部分不是 MySQL 基础语法，而是数据分析中的评价建模入门，适合放在数据库学习后的扩展内容中理解。

### 10.1 评价问题的基本思路

评价问题通常要把多个指标合成为一个综合评分。

基本流程：

1. 确定评价对象
2. 确定评价指标
3. 收集和整理数据
4. 对数据进行标准化
5. 确定指标权重
6. 计算综合得分
7. 可视化或排序解释结果

### 10.2 数据处理

常见预处理：

- 指标同向化：让所有指标方向一致，例如越大越好或越小越好。
- 标准化：消除量纲影响。
- 缺失值处理：删除、填充或单独标记。
- 异常值处理：检查极端值是否合理。

### 10.3 权重计算

课程中提到的方向包括：

- 层次分析法：偏主观，适合专家打分确定权重。
- 熵权法：偏客观，利用数据离散程度确定权重。
- TOPSIS：通过与理想最优解、最劣解的距离计算综合评价。

与 MySQL 的关系：

- MySQL 可用于存储、清洗和初步汇总指标数据。
- 更复杂的评价算法通常会在 Python、R 或专门的数据分析工具中完成。

## 11. 学习路线建议

### 11.1 入门顺序

建议按课程顺序学习：

1. 基本 `SELECT`
2. 运算符和过滤条件
3. 多表查询
4. 单行函数
5. 聚合函数、分组和 `HAVING`
6. 子查询
7. 创建和管理数据库、表
8. 插入、更新、删除、视图
9. 触发器、存储过程、存储函数
10. 数据评价问题扩展

### 11.2 每章练习重点

| 章节 | 必会目标 |
| --- | --- |
| SELECT | 能写基本查询、过滤、排序、分页 |
| 运算符 | 能组合多个条件，正确处理空值和范围 |
| 多表查询 | 能用 `JOIN ... ON ...` 避免笛卡尔积 |
| 单行函数 | 能处理字符串、日期、条件分支 |
| 聚合函数 | 能按组统计，并区分 `WHERE` 与 `HAVING` |
| 子查询 | 能写单行、多行和简单相关子查询 |
| 建表 | 能设计字段、类型和约束 |
| 数据处理 | 能安全插入、更新、删除，并理解视图 |
| 触发器/过程/函数 | 能理解用途、语法和风险 |
| 评价问题 | 能理解指标、权重、综合评分的流程 |

### 11.3 易错点清单

- 忘记 `WHERE`，导致更新或删除全表。
- 多表查询漏写连接条件，产生笛卡尔积。
- 用 `= NULL` 判断空值，应改为 `IS NULL`。
- 把 `WHERE` 和 `HAVING` 混用。
- `SELECT` 中混用普通字段和聚合函数时忘记 `GROUP BY`。
- 依赖字段顺序插入数据，表结构变化后容易出错。
- 随意使用 `DROP`、`DELETE`、`UPDATE`，没有先查询影响范围。
- 触发器和存储过程写太多，导致业务逻辑隐藏在数据库里。

### 11.4 推荐复习方式

1. 每学一章，自己写 5 条 SQL。
2. 每条 SQL 先解释“我要查什么”，再执行。
3. 查询结果不对时，先检查条件、连接、分组和空值。
4. 对 `UPDATE` / `DELETE`，先把条件写成 `SELECT` 验证。
5. 把常用 SQL 模板单独整理，后续写 FastAPI 数据库接口时复用。

