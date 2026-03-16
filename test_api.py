import requests

# 测试任务API
try:
    response = requests.get('http://localhost:8000/api/tasks/?page=1&status=open')
    print('Status code:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print('Error:', str(e))
