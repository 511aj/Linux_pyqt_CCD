from flask import Flask, json, request
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
def storage_data(username, temperature, soil_humidity, light):
    # 创建表的SQL语句（如果表不存在）
    create_sql = (f'CREATE TABLE IF NOT EXISTS {username} ('
                  f'id INT AUTO_INCREMENT PRIMARY KEY,'
                  f'temperature INT,'
                  f'soil_humidity INT,'
                  f'light INT,'
                  f'upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'
                  f'')

    # 插入数据的SQL语句
    insert_sql = f'INSERT INTO {username} (temperature,soil_humidity,light) VALUES ({temperature},{soil_humidity},{light});'

    try:
        # 执行创建表语句
        cursor.execute(create_sql)
        # 执行插入数据语句
        cursor.execute(insert_sql)
        # 提交事务
        db.commit()
    except:
        # 如果发生错误，回滚事务
        db.rollback()


# 创建Flask应用
app = Flask(__name__)


# 定义接收数据的路由
@app.route('/receiveData', methods=['POST'])
def print_messages():
    # 获取POST请求中的JSON数据
    message = request.get_json()
    # 解析payload字段（从字符串转换为JSON对象）
    payload = json.loads(message['payload'])

    # 检查payload中是否包含temperature字段（注意：这里检查的是字符串）
    if 'temperature' not in message['payload']:
        # 如果不包含，返回错误响应
        reply = {"result": "ok", "message": "error"}
        return json.dumps(reply), 200

    # 从payload中提取各个传感器数据
    temperature = payload['temperature']
    soil_humidity = payload['soil_humidity']
    light = payload['light']
    # 获取用户名
    username = message['username']

    # 调用存储函数将数据存入数据库
    storage_data(username, temperature, soil_humidity, light)

    # 返回成功响应
    reply = {"result": "ok", "message": "success"}
    return json.dumps(reply), 200


# 主程序入口
if __name__ == '__main__':
    # 启动Flask应用，监听所有网络接口的8000端口
    app.run('0.0.0.0', 8000)