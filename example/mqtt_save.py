"""
@Project ：Linux_pyqt_CCD
@File    ：mqtt_save.py.py
@IDE     ：PyCharm
@Author  ：wj
@Date    ：2025/4/20 下午10:39
"""
from flask import Flask, request, jsonify
import pymysql
import json

app = Flask(__name__)

# 数据库配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '511321',
    'database': 'mqtt_user',
    'charset': 'utf8mb4'
}


def get_db_connection():
    """每次请求都新建一个数据库连接"""
    return pymysql.connect(**DB_CONFIG)


def storage_data(table_name, main_valley, T_size, C_size, T_C_ratio, operator, batch, single):
    """
    存储数据到以 table_name 命名的数据库表中
    """
    db = get_db_connection()
    try:
        with db.cursor() as cursor:
            # 创建表（如果不存在）
            create_sql = f"""
                CREATE TABLE IF NOT EXISTS `{table_name}_CCD` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    main_valley FLOAT,
                    T_size FLOAT,
                    C_size FLOAT,
                    T_C_ratio FLOAT,
                    operator VARCHAR(50),
                    batch VARCHAR(50),
                    single BOOLEAN,
                    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            cursor.execute(create_sql)

            # 插入数据（使用参数化查询）
            insert_sql = f"""
                INSERT INTO `{table_name}_CCD` 
                (main_valley, T_size, C_size, T_C_ratio, operator, batch, single)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_sql, (main_valley, T_size, C_size, T_C_ratio, operator, batch, single))

        db.commit()
    except Exception as e:
        print(f"Database error: {e}")
        db.rollback()
    finally:
        db.close()


@app.route('/receiveData', methods=['POST'])
def receive_messages():
    message = request.get_json()
    print("Received message:", message)

    if not message:
        return jsonify({"result": "error", "message": "No JSON data received"}), 400

    payload_str = message.get('payload')
    if not payload_str:
        return jsonify({"result": "error", "message": "Payload is missing"}), 400

    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        return jsonify({"result": "error", "message": "Invalid JSON format in payload"}), 400

    required_fields = {'table_name', 'main_valley', 'T_size', 'C_size', 'T/C_ratio', 'operator', 'batch', 'single'}
    if not all(field in payload for field in required_fields):
        return jsonify({"result": "error", "message": "Missing required fields in payload"}), 400

    table_name = payload.get('table_name')  # 使用 table_name 替代 username
    main_valley = payload.get('main_valley')
    T_size = payload.get('T_size')
    C_size = payload.get('C_size')
    T_C_ratio = payload.get('T/C_ratio')
    operator = payload.get('operator')
    batch = payload.get('batch')
    single = payload.get('single')

    try:
        storage_data(table_name, main_valley, T_size, C_size, T_C_ratio, operator, batch, single)
        return jsonify({"result": "ok", "message": "Data successfully stored"}), 200
    except Exception as e:
        print(f"Error storing data: {e}")
        return jsonify({"result": "error", "message": "Internal server error"}), 500


if __name__ == '__main__':
    app.run('0.0.0.0', 8002)
