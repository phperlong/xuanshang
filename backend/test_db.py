import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xuanshang_backend.settings')
django.setup()

from tasks.models import Task

# 测试Task模型
try:
    # 尝试获取所有任务
    tasks = Task.objects.all()
    print('Task objects count:', tasks.count())
    print('Task objects:', list(tasks))
except Exception as e:
    print('Error:', str(e))
