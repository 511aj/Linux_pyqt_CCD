"""
    python_mqtt_订阅
    time:2024.5.4
"""

# 导入mqtt库 如果未安装，先安装此库 cmd - pip install paho.mqtt
import paho.mqtt.client as mqtt


def run():
    # 判断是否连接上mqtt服务器
    def on_connect(self, client, userdata, flags, rc):
        """连接回调函数"""
        if flags == 0:
            print("Connected to MQTT successfully!")
        else:
            print("Failed to connect, return code {0}".format(flags))

    # 订阅的主题中有新消息发布，则触发回调函数打印
    def on_message(client, userdata, msg):
        """消息回调函数"""
        print(msg.topic + " " + ":" + msg.payload.decode())

    # 创建客户端实例对象，参数为回调API版本，客户端的ID
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="python_mqtt_test_2")
    client.on_connect = on_connect  # 设置回调函数
    client.on_message = on_message  # 设置回调函数
    client.connect("192.168.31.43", 1883, 60)  # 连接mqtt服务器，参数(ip,端口,超时时间)
    client.subscribe("topic")  # 订阅"topic"主题
    client.loop_forever()  # 在当前线程中开启消息循环


if __name__ == '__main__':
    run()