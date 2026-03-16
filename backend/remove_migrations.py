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

# 删除tasks应用的所有迁移记录
print("删除tasks应用的迁移记录...")
cursor.execute("DELETE FROM django_migrations WHERE app='tasks'")
db.commit()
print(f"删除了 {cursor.rowcount} 条记录")

# 关闭连接
cursor.close()
db.close()