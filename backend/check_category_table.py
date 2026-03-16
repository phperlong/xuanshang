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

# 查看是否存在tasks_category表
print("检查是否存在tasks_category表...")
cursor.execute("SHOW TABLES LIKE 'tasks_category'")
result = cursor.fetchone()

if result:
    print("tasks_category表存在")
    # 查看表结构
    print("表结构：")
    cursor.execute("DESCRIBE tasks_category")
    structure = cursor.fetchall()
    for field in structure:
        print(field)
else:
    print("tasks_category表不存在")

# 关闭连接
cursor.close()
db.close()