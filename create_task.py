import requests

# 创建测试任务
print("创建测试任务...")
try:
    task_data = {
        "title": "测试任务",
        "category": "development",
        "reward": 100.0,
        "deadline": "2026-12-31",
        "description": "这是一个测试任务",
        "contact": "test@example.com",
        "publisher": "测试用户",
        "status": "open"
    }
    response = requests.post('http://localhost:8000/api/tasks/', json=task_data)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 再次获取任务列表
    print("\n获取任务列表...")
    response = requests.get('http://localhost:8000/api/tasks/')
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
except Exception as e:
    print(f"错误: {e}")