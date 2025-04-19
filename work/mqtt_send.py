"""
    python_mqtt_发布
    time:2024.5.4
"""
import time

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

    # 创建客户端实例对象，参数为回调API版本，客户端的ID
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="python_mqtt_test_1")
    # 设置用户名和密码
    client.username_pw_set(username="test", password="123456")
    client.on_connect = on_connect  # 设置回调函数
    # 连接mqtt服务器 ,虚拟机测试地址，部署到服务器，需要修改地址并且开放端口
    # todo
    client.connect("192.168.254.140", 1883, 60)  # 连接mqtt服务器，参数(ip,端口,超时时间)
    client.loop_start()  # 开启一个新线程，负责网络的接收和发送

    time.sleep(1)
    while True:
        data = input("请输入你要发送的内容：")
        client.publish("topic", data, 0, True)  # 向"topic"主题中发布data数据，QoS服务等级为0，True为指定消息要保留
        print(f"消息发送成功: {data}\n")


if __name__ == '__main__':
    run()
