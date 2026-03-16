import MySQLdb

# 连接到 MySQL 服务器
conn = MySQLdb.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    db='xuanshang'
)

# 创建游标
cursor = conn.cursor()

# 删除任务表
try:
    cursor.execute('DROP TABLE IF EXISTS tasks_task;')
    print('任务表删除成功！')
except Exception as e:
    print(f'删除任务表时出错: {e}')
finally:
    # 关闭游标和连接
    cursor.close()
    conn.close()