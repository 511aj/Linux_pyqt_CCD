# 服务器安装EMQX并配置数据库

## 数据库

```c
#打开数据库
mysql -uroot -p
#设置密码
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '511321';
#创建数据库
CREATE DATABASE mqtt_user;
#显示数据库
SHOW DATABASES;
#选择数据库
use mqtt_user;
#创建用户表
CREATE TABLE IF NOT EXISTS `mqtt_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password_hash` varchar(100) DEFAULT NULL,
  `salt` varchar(35) DEFAULT NULL,
  `is_superuser` tinyint(1) DEFAULT 0,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mqtt_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO mqtt_user (username,password_hash,salt) VALUES ('test','269c74e5601e036cbb6d221e624cbd73858de8616ea3f17167363c0cfe8ba0ed','yy');
//https://www.cmd5.com/hash.aspx 加密网站
#查看一下
select *from mqtt_user;

#数据库远程连接 修改配置文件，实现远程访问
mysql默认是只允许本地主机访问127.0.0.1，并关闭了远程连接，所以安装之后打开远程连接，并修改配置允许其他ip访问；

sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf 发现bind-address = 127.0.0.1。把它注释掉
#重启一下
service mysql restart
#配置权限    
mysql -uroot -p*****;

show databases;

use mysql;

update user set host='%' where user='root' and host='localhost'; #将host设置为%表示任何ip都能连接mysql，当然您也可以将host指定为某个ip
flush privileges;        #刷新权限表，使配置生效

```

加密

<img src="C:\Users\WJ\AppData\Roaming\Typora\typora-user-images\image-20250418185726344.png" alt="image-20250418185726344" style="zoom:33%;" />

<img src="https://wj-yqt.oss-cn-chengdu.aliyuncs.com/image-20250418190119186.png" alt="image-20250418190119186" style="zoom:50%;" />









## EMQX

1. 通过以下命令配置 EMQX Apt 源：

   ```c
   curl -s https://assets.emqx.com/scripts/install-emqx-deb.sh | sudo bash
   ```

2. 运行以下命令安装 EMQX：

   ```c
   sudo apt-get install emqx
   ```

3. 运行以下命令启动 EMQX：

   ```c
   sudo systemctl start emqx
   ```

### 数据库认证

![image-20250419103023932](https://wj-yqt.oss-cn-chengdu.aliyuncs.com/image-20250419103023932.png)

### Webhooks

![image-20250419102912623](https://wj-yqt.oss-cn-chengdu.aliyuncs.com/image-20250419102912623.png)



**先启动python监听脚本监听8000端口Webhooks才能启动成功**





## python

### 环境

```c
#查看版本：
python3 --version
#安装：
sudo apt install python3

#需要的库：
pip install pymysql
pip install flask

```



### 保存到数据库脚本

```python
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
```





















