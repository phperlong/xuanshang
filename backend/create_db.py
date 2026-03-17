import MySQLdb

# 连接到 MySQL 服务器
conn = MySQLdb.connect(
    host='db',
    user='root',
    password='root'
)

# 创建游标
cursor = conn.cursor()

# 创建数据库
try:
    cursor.execute('CREATE DATABASE IF NOT EXISTS xuanshang CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
    print('数据库创建成功！')
except Exception as e:
    print(f'创建数据库时出错: {e}')
finally:
    # 关闭游标和连接
    cursor.close()
    conn.close()