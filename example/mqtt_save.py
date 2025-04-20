'''
@Project ：Linux_pyqt_CCD 
@File    ：mqtt_save.py.py
@IDE     ：PyCharm 
@Author  ：wj
@Date    ：2025/4/20 下午10:39 
'''
from flask import Flask, request, json
import pymysql

# 初始化MySQL数据库连接
db = pymysql.connect(
    host='127.0.0.1',  # 数据库服务器地址
    user='root',  # 数据库用户名
    password='511321',  # 数据库密码
    database='mqtt_user'  # 要连接的数据库名称
)

# 创建数据库游标对象，用于执行SQL语句
cursor = db.cursor()


# 定义数据存储函数
def storage_data(username, main_valley, T_size, C_size, T_C_ratio):
    # 创建表的SQL语句（如果表不存在）
    create_sql = (f'CREATE TABLE IF NOT EXISTS {username}_Data ('
                  f'id INT AUTO_INCREMENT PRIMARY KEY,'
                  f'main_valley FLOAT,'
                  f'T_size FLOAT,'
                  f'C_size FLOAT,'
                  f'T_C_ratio FLOAT,'
                  f'upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);')

    # 插入数据的SQL语句
    insert_sql = (f'INSERT INTO {username}_CCD '
                 f'(main_valley, T_size, C_size, T_C_ratio) '
                 f'VALUES ({main_valley}, {T_size}, {C_size}, {T_C_ratio});')

    try:
        # 执行创建表语句
        cursor.execute(create_sql)
        # 执行插入数据语句
        cursor.execute(insert_sql)
        # 提交事务
        db.commit()
    except Exception as e:
        # 如果发生错误，回滚事务并打印错误信息
        print(f"Error occurred: {e}")
        db.rollback()


# 创建Flask应用
app = Flask(__name__)


# 定义接收数据的路由
@app.route('/receiveData', methods=['POST'])
def receive_messages():
    # 获取POST请求中的JSON数据
    message = request.get_json()

    if not message:
        reply = {"result": "error", "message": "No JSON data received"}
        return json.dumps(reply), 400

    # 解析payload字段
    payload_str = message.get('payload')
    if not payload_str:
        reply = {"result": "error", "message": "Payload is missing"}
        return json.dumps(reply), 400

    try:
        # 将payload从字符串解析为字典
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        reply = {"result": "error", "message": "Invalid JSON format in payload"}
        return json.dumps(reply), 400

    # 检查payload中是否包含必要的字段
    required_fields = {'main_valley', 'T_size', 'C_size', 'T/C_ratio'}
    if not all(field in payload for field in required_fields):
        reply = {"result": "error", "message": "Missing required fields in payload"}
        return json.dumps(reply), 400

    # 获取用户名
    username = message.get('username')
    if not username:
        reply = {"result": "error", "message": "Username is missing"}
        return json.dumps(reply), 400

    # 从payload中提取各个传感器数据
    main_valley = payload.get('main_valley')
    T_size = payload.get('T_size')
    C_size = payload.get('C_size')
    T_C_ratio = payload.get('T/C_ratio')

    # 调用存储函数将数据存入数据库
    storage_data(username, main_valley, T_size, C_size, T_C_ratio)

    # 返回成功响应
    reply = {"result": "ok", "message": "Data successfully stored"}
    return json.dumps(reply), 200


# 主程序入口
if __name__ == '__main__':
    # 启动Flask应用，监听所有网络接口的8001端口
    app.run('0.0.0.0', 8001)
