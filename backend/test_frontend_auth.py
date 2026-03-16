import requests
import json

# 测试前台用户注册
register_url = 'http://localhost:8000/api/auth/register/'
register_data = {
    'username': 'frontend_user',
    'email': 'frontend@example.com',
    'password': '12345678'
}

print('测试前台用户注册...')
try:
    response = requests.post(register_url, json=register_data)
    print(f'状态码: {response.status_code}')
    print(f'响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}')
except Exception as e:
    print(f'错误: {e}')

# 测试前台用户登录
login_url = 'http://localhost:8000/api/auth/login/'
login_data = {
    'username': 'frontend_user',
    'password': '12345678'
}

print('\n测试前台用户登录...')
try:
    response = requests.post(login_url, json=login_data)
    print(f'状态码: {response.status_code}')
    print(f'响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}')
except Exception as e:
    print(f'错误: {e}')

# 测试创建任务
print('\n测试创建任务...')
try:
    # 先登录获取 token
    login_response = requests.post(login_url, json=login_data)
    token = login_response.json().get('access')
    
    task_url = 'http://localhost:8000/api/tasks/'
    task_data = {
        'title': '测试任务',
        'category': 'design',
        'reward': 100,
        'deadline': '2026-03-31',
        'description': '这是一个测试任务',
        'contact': 'test@example.com'
    }
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(task_url, json=task_data, headers=headers)
    print(f'状态码: {response.status_code}')
    print(f'响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}')
except Exception as e:
    print(f'错误: {e}')