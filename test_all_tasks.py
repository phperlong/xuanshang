import requests

# 测试获取所有任务
try:
    # 不使用分页，获取所有任务
    response = requests.get('http://localhost:8000/api/tasks/?status=open&page_size=100')
    print('Status code:', response.status_code)
    tasks = response.json()['results']
    print('Total tasks:', len(tasks))
    
    # 统计各分类的任务数量
    categories = {}
    for task in tasks:
        category = task['category']
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    print('Tasks by category:', categories)
    
    # 打印前20个任务的分类
    print('First 20 tasks categories:')
    for i, task in enumerate(tasks[:20]):
        print(f'{i+1}. {task["title"]} - {task["category"]}')
        
except Exception as e:
    print('Error:', str(e))
