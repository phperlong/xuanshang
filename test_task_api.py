import requests

# 测试任务API
print("测试任务API...")
try:
    # 测试获取任务列表
    print("\n获取任务列表:")
    response = requests.get('http://localhost:8000/api/tasks/?page=1&status=open')
    print(f"状态码: {response.status_code}")
    print(f"返回内容: {response.text}")
    
except Exception as e:
    print(f"错误: {e}")