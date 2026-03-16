import requests

# 测试接受任务功能
print("测试接受任务功能...")
try:
    # 先获取一个未被接受的任务
    response = requests.get('http://localhost:8000/api/tasks/?page=1')
    tasks = response.json()['results']
    
    # 找到一个未被接受且发布者不是"测试用户"的任务
    target_task = None
    for task in tasks:
        if not task.get('assignee') and task['publisher'] != '测试用户':
            target_task = task
            break
    
    if not target_task:
        print("没有找到适合测试的任务")
    else:
        print(f"找到测试任务: {target_task['title']} (ID: {target_task['id']}, 发布者: {target_task['publisher']})")
        
        # 模拟登录获取token
        login_data = {
            "username": "testuser",
            "password": "test123456"
        }
        login_response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['access']
            print("登录成功，获取到token")
            
            # 测试接受任务
            headers = {
                "Authorization": f"Bearer {token}"
            }
            accept_response = requests.patch(
                f"http://localhost:8000/api/tasks/{target_task['id']}/",
                json={"assignee": "testuser"},
                headers=headers
            )
            
            print(f"接受任务状态码: {accept_response.status_code}")
            if accept_response.status_code == 200:
                updated_task = accept_response.json()
                print(f"任务接受成功，接受者: {updated_task['assignee']}")
            else:
                print(f"接受任务失败: {accept_response.json()}")
        else:
            print(f"登录失败: {login_response.json()}")
            
            # 如果登录失败，先注册一个用户
            register_data = {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "test123456"
            }
            register_response = requests.post('http://localhost:8000/api/auth/register/', json=register_data)
            print(f"注册状态码: {register_response.status_code}")
            if register_response.status_code == 201:
                print("注册成功")
                # 再次尝试登录
                login_response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
                if login_response.status_code == 200:
                    token = login_response.json()['access']
                    print("登录成功，获取到token")
                    
                    # 测试接受任务
                    headers = {
                        "Authorization": f"Bearer {token}"
                    }
                    accept_response = requests.patch(
                        f"http://localhost:8000/api/tasks/{target_task['id']}/",
                        json={"assignee": "testuser"},
                        headers=headers
                    )
                    
                    print(f"接受任务状态码: {accept_response.status_code}")
                    if accept_response.status_code == 200:
                        updated_task = accept_response.json()
                        print(f"任务接受成功，接受者: {updated_task['assignee']}")
                    else:
                        print(f"接受任务失败: {accept_response.json()}")

except Exception as e:
    print(f"错误: {e}")