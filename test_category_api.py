import requests

# 测试分类API
print("测试分类API...")
try:
    # 测试获取所有分类
    print("\n1. 获取所有分类:")
    response = requests.get('http://localhost:8000/api/categories/')
    print(f"状态码: {response.status_code}")
    print(f"返回内容: {response.text}")
    
    # 测试添加新分类
    print("\n2. 添加新分类:")
    new_category = {
        "name": "测试分类"
    }
    response = requests.post('http://localhost:8000/api/categories/', json=new_category)
    print(f"状态码: {response.status_code}")
    print(f"返回内容: {response.text}")
    
except Exception as e:
    print(f"错误: {e}")