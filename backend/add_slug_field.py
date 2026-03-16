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

# 为Category表添加slug字段
print("为Category表添加slug字段...")
try:
    cursor.execute("ALTER TABLE tasks_category ADD COLUMN slug VARCHAR(50) UNIQUE")
    db.commit()
    print("slug字段添加成功")
except Exception as e:
    print(f"错误: {e}")

# 关闭连接
cursor.close()
db.close()