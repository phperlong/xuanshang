import requests
import json

# 测试登录 API
login_url = 'http://localhost:8000/api/auth/login/'
login_data = {
    'username': '111',
    'password': '123'
}

print('测试登录 API...')
try:
    response = requests.post(login_url, json=login_data)
    print(f'状态码: {response.status_code}')
    print(f'响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}')
except Exception as e:
    print(f'错误: {e}')

# 测试注册 API
register_url = 'http://localhost:8000/api/auth/register/'
register_data = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': '12345678'
}

print('\n测试注册 API...')
try:
    response = requests.post(register_url, json=register_data)
    print(f'状态码: {response.status_code}')
    print(f'响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}')
except Exception as e:
    print(f'错误: {e}')