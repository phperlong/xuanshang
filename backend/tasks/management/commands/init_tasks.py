from django.core.management.base import BaseCommand
from tasks.models import Task
from datetime import date, timedelta

class Command(BaseCommand):
    help = '初始化示例任务数据'
    
    def handle(self, *args, **options):
        # 检查是否已有数据
        if Task.objects.count() > 0:
            self.stdout.write(self.style.WARNING('已存在任务数据，跳过初始化'))
            return
        
        # 示例任务数据
        tasks = [
            {
                'title': '设计公司Logo',
                'category': 'design',
                'reward': 500.00,
                'deadline': date.today() + timedelta(days=15),
                'description': '需要为一家科技公司设计一个简洁、现代的Logo，要求体现创新和科技感。需要提供至少3个设计方案供选择。',
                'contact': '微信：company_logo',
                'publisher': '科技公司',
                'status': 'open'
            },
            {
                'title': '开发小程序商城',
                'category': 'development',
                'reward': 3000.00,
                'deadline': date.today() + timedelta(days=30),
                'description': '需要开发一个微信小程序商城，包含商品展示、购物车、订单管理、支付等功能。需要有完整的前后端开发经验。',
                'contact': 'QQ：123456789',
                'publisher': '电商公司',
                'status': 'open'
            },
            {
                'title': '翻译技术文档',
                'category': 'translation',
                'reward': 800.00,
                'deadline': date.today() + timedelta(days=20),
                'description': '需要将一份英文技术文档翻译成中文，文档约5000字，要求翻译准确、专业。需要有相关技术背景。',
                'contact': '邮箱：translate@example.com',
                'publisher': '软件公司',
                'status': 'completed'
            },
            {
                'title': '撰写产品文案',
                'category': 'writing',
                'reward': 600.00,
                'deadline': date.today() + timedelta(days=25),
                'description': '需要为一款新产品撰写宣传文案，包括产品介绍、卖点提炼、广告语等。要求文案有吸引力、有感染力。',
                'contact': '微信：product_writer',
                'publisher': '品牌公司',
                'status': 'open'
            }
        ]
        
        for task_data in tasks:
            Task.objects.create(**task_data)
            self.stdout.write(self.style.SUCCESS(f'创建任务：{task_data["title"]}'))
        
        self.stdout.write(self.style.SUCCESS(f'初始化完成，共创建 {len(tasks)} 个任务'))