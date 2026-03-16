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

# 查看django_migrations表中的记录
print("django_migrations表中的记录：")
cursor.execute("SELECT * FROM django_migrations WHERE app='tasks'")
migrations = cursor.fetchall()
for migration in migrations:
    print(migration)

# 关闭连接
cursor.close()
db.close()