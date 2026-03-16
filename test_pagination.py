import requests

# 测试分页功能
print("测试分页功能...")
try:
    # 测试第一页
    response = requests.get('http://localhost:8000/api/tasks/?page=1')
    print(f"第一页状态码: {response.status_code}")
    data = response.json()
    print(f"第一页数据条数: {len(data['results'])}")
    print(f"总任务数: {data['count']}")
    print(f"第一页第一条任务: {data['results'][0]['title']}")
    
    # 测试第二页
    response = requests.get('http://localhost:8000/api/tasks/?page=2')
    print(f"\n第二页状态码: {response.status_code}")
    data = response.json()
    print(f"第二页数据条数: {len(data['results'])}")
    print(f"第二页第一条任务: {data['results'][0]['title']}")
    
    # 测试带筛选条件的分页
    response = requests.get('http://localhost:8000/api/tasks/?page=1&category=development')
    print(f"\n带筛选条件的分页状态码: {response.status_code}")
    data = response.json()
    print(f"带筛选条件的数据条数: {len(data['results'])}")
    print(f"带筛选条件的总任务数: {data['count']}")
    
except Exception as e:
    print(f"错误: {e}")