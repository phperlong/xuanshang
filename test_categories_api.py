import requests

# 测试分类API
try:
    response = requests.get('http://localhost:8000/api/categories/')
    print('Status code:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print('Error:', str(e))
