import os
import django
from datetime import datetime, timedelta
import random

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xuanshang_backend.settings')
django.setup()

from tasks.models import Task

# 生成任务数据
print("开始生成任务数据...")

# 任务标题模板
title_templates = [
    "开发{software}功能",
    "设计{design}界面",
    "撰写{article}文章",
    "翻译{document}文档",
    "其他{other}任务"
]

# 分类选项
categories = ['design', 'development', 'writing', 'translation', 'other']

# 软件名称
software_names = ['网站', '应用', '系统', '工具', '平台']

# 设计类型
design_types = ['网页', '移动应用', 'logo', '海报', 'UI']

# 文章类型
article_types = ['技术', '营销', '产品', '用户故事', '案例分析']

# 文档类型
document_types = ['技术', '产品', '用户手册', 'API', '帮助']

# 其他任务类型
other_types = ['数据录入', '市场调研', '用户测试', '内容审核', '客服支持']

# 发布者名称
publishers = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十', '郑一', '王二']

# 联系方式
contacts = ['13800138000', '13900139000', '13700137000', '13600136000', 'test@example.com', 'contact@test.com']

# 生成100条任务
tasks = []
for i in range(100):
    # 随机选择分类
    category = random.choice(categories)
    
    # 根据分类生成标题
    if category == 'development':
        title = title_templates[0].format(software=random.choice(software_names))
    elif category == 'design':
        title = title_templates[1].format(design=random.choice(design_types))
    elif category == 'writing':
        title = title_templates[2].format(article=random.choice(article_types))
    elif category == 'translation':
        title = title_templates[3].format(document=random.choice(document_types))
    else:
        title = title_templates[4].format(other=random.choice(other_types))
    
    # 生成其他字段
    reward = round(random.uniform(50, 1000), 2)
    deadline = datetime.now() + timedelta(days=random.randint(1, 30))
    description = f"这是一个{category}类任务，需要完成{title}的相关工作。"
    contact = random.choice(contacts)
    publisher = random.choice(publishers)
    status = 'open' if random.random() > 0.3 else 'completed'
    
    # 创建任务对象
    task = Task(
        title=title,
        category=category,
        reward=reward,
        deadline=deadline.date(),
        description=description,
        contact=contact,
        publisher=publisher,
        status=status
    )
    tasks.append(task)

# 批量创建任务
Task.objects.bulk_create(tasks)
print(f"成功添加{len(tasks)}条任务数据！")

# 验证数据
print(f"当前任务总数：{Task.objects.count()}")