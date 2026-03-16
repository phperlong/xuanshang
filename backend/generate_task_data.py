import os
import django
from datetime import date, timedelta
import random

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xuanshang_backend.settings')
django.setup()

from tasks.models import Task

# 生成任务数据
def generate_task_data():
    # 分类列表
    categories = ['reward', 'game', 'charity', 'development', 'trade']
    category_names = {
        'reward': '悬赏',
        'game': '游戏',
        'charity': '公益',
        'development': '开发',
        'trade': '交易'
    }
    
    # 发布者列表
    publishers = ['张三', '李四', '王五', '赵六', '孙七', '周八', '吴九', '郑十']
    
    # 任务标题模板
    titles = {
        'reward': [
            '寻找丢失的宠物',
            '寻找目击证人',
            '寻找失踪物品',
            '寻求技术帮助',
            '寻求专业建议',
            '寻求合作伙伴',
            '寻求投资机会',
            '寻求市场推广',
            '寻求产品测试',
            '寻求用户反馈'
        ],
        'game': [
            '游戏代练服务',
            '游戏账号交易',
            '游戏装备交易',
            '游戏攻略制作',
            '游戏视频剪辑',
            '游戏直播合作',
            '游戏测试员',
            '游戏策划咨询',
            '游戏美术设计',
            '游戏音效制作'
        ],
        'charity': [
            '公益活动志愿者',
            '公益项目策划',
            '公益宣传推广',
            '公益物资募集',
            '公益资金管理',
            '公益活动摄影',
            '公益活动记录',
            '公益项目评估',
            '公益教育讲座',
            '公益环保活动'
        ],
        'development': [
            '网站开发',
            '移动应用开发',
            '软件定制开发',
            '前端开发',
            '后端开发',
            '全栈开发',
            '数据库开发',
            'API开发',
            '系统集成',
            '技术咨询'
        ],
        'trade': [
            '二手物品交易',
            '电子产品交易',
            '服装鞋帽交易',
            '图书音像交易',
            '家居用品交易',
            '交通工具交易',
            '办公用品交易',
            '收藏品交易',
            '体育用品交易',
            '其他物品交易'
        ]
    }
    
    # 生成任务数据
    for category in categories:
        for i in range(10):  # 每个分类生成10个任务
            # 随机选择标题
            title = random.choice(titles[category])
            
            # 随机生成悬赏金额
            reward = round(random.uniform(100, 1000), 2)
            
            # 随机生成截止日期（1-30天）
            deadline = date.today() + timedelta(days=random.randint(1, 30))
            
            # 生成任务描述
            description = f'这是一个{category_names[category]}类任务，需要完成{title}的相关工作。'
            
            # 随机生成联系方式
            contact = f'13{random.randint(1000000000, 9999999999)}'
            
            # 随机选择发布者
            publisher = random.choice(publishers)
            
            # 创建任务
            task = Task(
                title=title,
                category_id=category,
                reward=reward,
                deadline=deadline,
                description=description,
                contact=contact,
                publisher=publisher,
                status='open'
            )
            task.save()
            print(f'生成任务: {title} ({category_names[category]})')

if __name__ == '__main__':
    generate_task_data()
    print('任务数据生成完成！')
