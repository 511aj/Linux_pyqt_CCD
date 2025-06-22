"""
串口读取传感器数据
----------------------------------------------------------
使用方法：
from sensor_reader import read_sensor_data  # 导入函数

# 调用函数并获取 input_data
sensor_data = read_sensor_data()

# 输出获取的传感器数据
if sensor_data is not None:
    print(sensor_data)
else:
    print("获取传感器数据失败。")
----------------------------------------------------------
注意：
 串口号需要根据实际情况修改。
 ser 对应 传感器板
 ser2 对应 电机控制板
"""

import serial
import time
import random


def generate_random_packet():
    # 固定帧头和帧尾
    frame_header = [0x12, 0x34, 0x56, 0x78]  # 示例帧头，可以根据实际修改
    frame_footer = [0xAB, 0xCD]  # 示例帧尾，可以根据实际修改

    # 像素个数：3648 个像素点，每个像素占 2 字节
    num_pixels = 3648
    pixel_bytes = []

    # 随机生成像素值（16位无符号整数，范围 0~65535）
    pixels = [random.randint(0, 65535) for _ in range(num_pixels)]

    # 转为高低字节排列
    for value in pixels:
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF
        pixel_bytes.append(high_byte)
        pixel_bytes.append(low_byte)

    # 组合成完整数据包：帧头 + 像素数据 + 帧尾
    full_data = bytes(frame_header) + bytes(pixel_bytes) + bytes(frame_footer)

    return full_data, pixels


# 读取传感器数据,电机和传感器的都写好了，直接调用就返回传感器数据
# todo 需要修改串口号,电机发送位置信息还要找一下
def read_sensor_data():
    ser = serial.Serial("COM4", 256000, timeout=1)  # 打开串口
    ser2 = serial.Serial("COM7", 115200, timeout=1)  # 打开另一个串口

    if not ser.isOpen() or not ser2.isOpen():
        print("串口打开失败。")
        return None

    time.sleep(1)

    # 电机运动指令
    stop_str = "\x5A\xa5\x01\x01\x03\x0f\xf9\x01\x0d"  # todo 需要修改走到传感器下面 x0f\xf9\位置 x01\前进 x0d校验
    ser2.write(stop_str.encode('utf-8'))

    time.sleep(1)

    # 传感器读数据指令
    ser.write("@c0007#@".encode('utf-8'))
    time.sleep(1)

    ser.write("@c0080#@".encode('utf-8'))
    time.sleep(1)

    com_input = ser.read(8000)  # com_input就是传感器读到的数据
    input_data = ""

    if com_input:  # 如果读取结果非空，处理数据
        byte_input = com_input.split()

        for byte in byte_input:
            input_data += f'0x{byte},'

        input_data = input_data.rstrip(', ')  # 删除最后多余的逗号和空格

    # 电机运动指令 走到终点
    stop_end = "\x5A\xa5\x01\x01\x03\x0f\xf9\x01\x0d"  # \x5A\xa5\x01\x01\x03  这几项和为  104
    ser2.write(stop_end.encode('utf-8'))

    time.sleep(1)

    # 电机运动指令 回到起点
    stop_start = "\x5A\xa5\x01\x01\x03\x0f\xf9\x00\x0c"  # \x5A\xa5\x01\x01\x03\x0f   和为  113
    ser2.write(stop_start.encode('utf-8'))

    ser.close()  # 关闭串口
    ser2.close()  # 关闭另一个串口

    return input_data  # 返回传感器得到的数据


"""
----------------------------------------------------------
import random

def generate_random_packet():
    # 固定帧头和帧尾
    frame_header = [0x12, 0x34, 0x56, 0x78]  # 示例帧头，可以根据实际修改
    frame_footer = [0xAB, 0xCD]  # 示例帧尾，可以根据实际修改

    # 像素个数：3648 个像素点，每个像素占 2 字节
    num_pixels = 3648
    pixel_bytes = []

    # 随机生成像素值（16位无符号整数，范围 0~65535）
    pixels = [random.randint(0, 65535) for _ in range(num_pixels)]

    # 转为高低字节排列
    for value in pixels:
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF
        pixel_bytes.append(high_byte)
        pixel_bytes.append(low_byte)

    # 组合成完整数据包：帧头 + 像素数据 + 帧尾
    full_data = bytes(frame_header) + bytes(pixel_bytes) + bytes(frame_footer)

    return full_data, pixels

# 使用示例
packet, generated_pixels = generate_random_packet()
print("生成的数据长度:", len(packet))
print("前10个原始像素值:", generated_pixels[:10])
"""