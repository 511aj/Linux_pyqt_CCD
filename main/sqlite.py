"""
Project ：Linux_pyqt_CCD 
File    ：sqlite.py
IDE     ：PyCharm 
Author  ：wj
Date    ：2025/6/26 下午4:05 
role    :
"""
import sqlite3
import os

# 本地数据库路径
DB_PATH = "../data/local_data.db"

def save_to_sqlite(data):
    """
    将数据保存到 SQLite 本地数据库
    :param data: 字典格式的数据
    """
    table_name = data.get("table_name")
    if not table_name:
        print("缺少 table_name，无法保存数据")
        return

    # 连接或创建数据库文件
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 创建表（如果不存在）
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS "{table_name}_CCD" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            main_valley INTEGER,
            T_size REAL,
            C_size REAL,
            T_C_ratio REAL,
            operator TEXT,
            batch TEXT,
            single BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_sql)

        # 插入数据
        insert_sql = f"""
        INSERT INTO "{table_name}_CCD" 
        (main_valley, T_size, C_size, T_C_ratio, operator, batch, single)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_sql, (
            data["main_valley"],
            data["T_size"],
            data["C_size"],
            data["T/C_ratio"],
            data["operator"],
            data["batch"],
            data["single"]
        ))
        conn.commit()
        print(f"数据已保存至表 {table_name}_CCD")

    except Exception as e:
        print("保存数据失败:", e)
        conn.rollback()
    finally:
        conn.close()
