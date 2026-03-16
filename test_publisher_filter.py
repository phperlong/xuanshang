import requests

# 测试publisher参数功能
print("测试publisher参数功能...")
try:
    # 测试筛选发布者为"张三"的任务
    response = requests.get('http://localhost:8000/api/tasks/?publisher=张三')
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"筛选后的数据条数: {len(data['results'])}")
    print(f"总任务数: {data['count']}")
    
    # 打印前几条任务的发布者，确认筛选正确
    print("\n前5条任务的发布者:")
    for i, task in enumerate(data['results'][:5]):
        print(f"{i+1}. {task['title']} - {task['publisher']}")
    
except Exception as e:
    print(f"错误: {e}")