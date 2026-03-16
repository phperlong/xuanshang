import MySQLdb

# 连接数据库
db = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="root",
    db="xuanshang",
    charset="utf8mb4"
)

# 创建游标
cursor = db.cursor()

# 查看所有表
print("数据库中的表：")
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
for table in tables:
    print(table[0])

# 检查tasks_task表是否存在
table_exists = False
for table in tables:
    if table[0] == 'tasks_task':
        table_exists = True
        break

if table_exists:
    print("\ntasks_task表存在，查看表结构：")
    cursor.execute("DESCRIBE tasks_task")
    structure = cursor.fetchall()
    for field in structure:
        print(field)
else:
    print("\ntasks_task表不存在！")

# 关闭连接
cursor.close()
db.close()