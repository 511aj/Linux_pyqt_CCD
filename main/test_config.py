"""
Project ：Linux_pyqt_CCD 
File    ：test_config.py
IDE     ：PyCharm 
Author  ：wj
Date    ：2025/6/25 下午10:43
role    : 测试配置管理模块

调用方式：
1. 导入模块 import test_manager
2. 调用 load_config() 获取当前配置数据
3. 调用相关函数进行修改，如 add_table_field(), update_batch_size(), set_save_flag() 等
4. 修改后调用 save_config(data) 保存回文件
"""

import json
import os

CONFIG_FILE = "../data/test_config.json"


def load_config():
    """
    加载配置文件内容。

    如果文件不存在或为空，则返回默认结构。
    默认结构如下：
    {
        "table_name": ["temp", "long", "lat", "alt"],
        "batch": 100,
        "save": true
    }

    Returns:
        dict: 配置字典对象
    """
    if not os.path.exists(CONFIG_FILE):
        return {
            "table_name": ["temp", "long", "lat", "alt"],
            "batch": 100,
            "save": True
        }

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # 如果文件损坏，返回默认值
            return {
                "table_name": ["temp", "long", "lat", "alt"],
                "batch": 100,
                "save": True
            }


def save_config(data):
    """
    将配置数据写入文件。

    Args:
        data (dict): 要保存的配置字典
    """
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def get_table_fields():
    """
    获取所有 table_name 字段列表。

    Returns:
        list: 表字段名称列表
    """
    config = load_config()
    return config.get("table_name", [])


def add_table_field(field_name):
    """
    添加一个字段到 table_name 列表中。

    Args:
        field_name (str): 要添加的字段名

    Returns:
        bool: 添加成功返回 True，如果字段已存在则返回 False
    """
    config = load_config()
    fields = config["table_name"]

    if field_name in fields:
        return False

    fields.append(field_name)
    save_config(config)
    return True


def remove_table_field(field_name):
    """
    从 table_name 列表中移除指定字段。

    Args:
        field_name (str): 要移除的字段名

    Returns:
        bool: 移除成功返回 True，如果字段不存在则返回 False
    """
    config = load_config()
    fields = config["table_name"]

    if field_name not in fields:
        return False

    fields.remove(field_name)
    save_config(config)
    return True


def set_batch_size(new_size):
    """
    更新 batch 字段值。

    Args:
        new_size (int): 新的批量大小值

    Returns:
        None
    """
    config = load_config()
    config["batch"] = new_size
    save_config(config)


def get_batch_size():
    """
    获取当前 batch 值。

    Returns:
        int: 批量大小
    """
    config = load_config()
    return config.get("batch", 100)


def set_save_flag(flag):
    """
    设置 save 标志。

    Args:
        flag (bool): True 或 False

    Returns:
        None
    """
    config = load_config()
    config["save"] = flag
    save_config(config)


def get_save_flag():
    """
    获取 save 标志值。

    Returns:
        bool: 当前保存状态
    """
    config = load_config()
    return config.get("save", True)


def set_sampled_flag(flag):
    """
    设置 采样标志标志位

    Args:
        flag (bool): True 或 False

    Returns:
        None
    """
    config = load_config()
    config["sampled"] = flag
    save_config(config)


def get_sampled_flag():
    """
    获取 sampled 标志值。

    Returns:
        bool: 当前保存状态
    """
    config = load_config()
    return config.get("sampled", True)


def get_now_table():
    """
    获取当前 table 值。

    Returns:
        str: 当前表名
    """
    config = load_config()
    return config.get("now_table", "temp")


def set_now_table(now_table_name):
    """
    设置 now_table 名字

    Args:
        now_table_name (str): 表名

    Returns:
        None
    """
    config = load_config()
    config["now_table"] = now_table_name
    save_config(config)

