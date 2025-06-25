"""
Project ：Linux_pyqt_CCD 
File    ：user_manager.py
IDE     ：PyCharm 
Author  ：wj
Date    ：2025/6/25 下午4:54 
role    :用户管理模块
调用方式：
1. 导入模块 import user_manager
2. 调用load_data()函数获取用户数据，并进行相关操作
3. 调用user_manager模块中的函数，如：add_user、update_user、delete_user等


data = load_data()

"""
import json
import os

DATA_FILE = 'users.json'


#  加载和保存 JSON 数据
def load_data():
    if not os.path.exists(DATA_FILE):
        # 如果文件不存在，初始化默认数据
        default_data = {
            "current_user": None,
            "users": []
        }
        save_data(default_data)
        return default_data

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(user_data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)


def set_current_user(data, user):
    data["current_user"] = user
    save_data(data)


# 获取当前用户
def get_current_user(user_data):
    return user_data.get("current_user")


# 获取用户列表
def get_users(user_data):
    return user_data.get("users", [])


# 新增用户
def add_user(user_data, account, username, is_admin=False):
    users = user_data["users"]
    for user in users:
        if user["account"] == account:
            raise ValueError("该账号已存在！")

    new_user = {
        "account": account,
        "username": username,
        "is_admin": is_admin
    }
    users.append(new_user)
    save_data(user_data)
    return True


# 修改用户信息
def update_user(user_data, index, new_account=None, new_username=None, new_is_admin=None):
    users = user_data["users"]
    if index < 0 or index >= len(users):
        raise IndexError("无效的用户索引")

    user = users[index]
    if new_account:
        user["account"] = new_account
    if new_username:
        user["username"] = new_username
    if new_is_admin is not None:
        user["is_admin"] = new_is_admin

    save_data(user_data)
    return True


# 删除用户
def delete_user(user_data, index):
    users = user_data["users"]
    if index < 0 or index >= len(users):
        raise IndexError("无效的用户索引")

    del users[index]
    save_data(user_data)
    return True


if __name__ == "__main__":
    data = load_data()

    print("当前用户：", get_current_user(data))

    print("\n用户列表：")
    for i, user in enumerate(get_users(data)):
        print(f"{i}: 账号: {user['account']}, 用户名: {user['username']}, 管理员: {user['is_admin']}")

    # 示例：添加用户
    try:
        add_user(data, "newuser", "新用户", False)
        print("✅ 添加用户成功")
    except Exception as e:
        print("❌ 添加失败:", e)

    # 示例：修改用户
    try:
        update_user(data, 1, new_username="修改后的名字", new_is_admin=True)
        print("✅ 修改用户成功")
    except Exception as e:
        print("❌ 修改失败:", e)

    # 示例：删除用户
    try:
        delete_user(data, 0)
        print("✅ 删除用户成功")
    except Exception as e:
        print("❌ 删除失败:", e)

    # 刷新查看结果
    data = load_data()
    print("\n更新后用户列表：")
    for i, user in enumerate(get_users(data)):
        print(f"{i}: 账号: {user['account']}, 用户名: {user['username']}, 管理员: {user['is_admin']}")
