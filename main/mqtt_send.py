"""
    python_mqtt_发布
    time:2024.5.4
    # 导入mqtt库 pip install paho.mqtt
    调用示例：
        from mqtt_send import run
        topic = "主题"
        message = {"username": "testuser", "temperature": 25, "soil_humidity": 60, "light": 500}
        run(topic, message)
"""
import time
import paho.mqtt.client as mqtt


def mqtt_send_data(topic, data):
    # 判断是否连接上mqtt服务器
    def on_connect(client, userdata, flags, rc):
        """连接回调函数"""
        if rc == 0:
            print("Connected to MQTT successfully!")  # 如果连接成功，打印成功信息
        else:
            print("Failed to connect, return code {0}".format(rc))  # 如果连接失败，打印错误代码

    # 创建客户端实例对象，参数为回调API版本和客户端ID
    client = mqtt.Client(client_id="python_mqtt_test_1")
    # 设置用户名和密码
    client.username_pw_set(username="test", password="123456")
    # 设置连接回调函数
    client.on_connect = on_connect
    # 连接mqtt服务器 (虚拟机测试地址，部署到服务器需要修改地址并开放端口)
    client.connect("8.137.62.230", 1883, 60)  # 参数(ip,端口,超时时间)
    # 启动网络循环（新线程负责接收和发送）
    client.loop_start()

    # 等待连接建立
    time.sleep(1)
    # 发布消息
    client.publish(topic, str(data), 0)  # QoS服务等级为0，True表示保留消息
    print(f"消息发送成功: {data}\n")

    # 停止网络循环并断开连接
    client.loop_stop()      # 停止网络循环
    client.disconnect()     # 断开与MQTT服务器的连接
