"""
Project ：Linux_pyqt_CCD
File    ：read_json_settings.py
IDE     ：PyCharm
Author  ：wj
Date    ：2025/4/21 下午2:08
role    : 读取或写入 JSON 文件中的设置

调用方式：
1. 导入模块：from read_json_settings import read_setting, write_setting
2. 读取设置：setting_value = read_setting("setting_name")
3. 写入设置：write_setting("setting_name", setting_value)
"""

import json
import os

# 设置文件路径
SETTINGS_FILE = "settings.json"


def load_settings():
    """加载 JSON 文件中的设置，如果文件不存在则创建一个空设置文件"""
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as file:
            json.dump({}, file)
        return {}
    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings):
    """将设置保存到 JSON 文件中"""
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def read_setting(setting_name):
    """读取指定设置的值"""
    settings = load_settings()
    return settings.get(setting_name, None)  # 如果设置不存在，返回 None


def write_setting(setting_name, setting_value):
    """写入或更新指定设置的值"""
    settings = load_settings()
    settings[setting_name] = setting_value
    save_settings(settings)


# # 测试代码（可选，用于验证模块功能）
# if __name__ == "__main__":
#     # 写入设置
#     # write_setting("resolution", "90090")
#     # write_setting("fullscreen", True)
#     # write_setting("volume", 75)
#
#     # 读取设置
#     print("Resolution:", read_setting("resolution"))
#     print("Fullscreen:", read_setting("fullscreen"))
#     print("Volume:", read_setting("volume"))
