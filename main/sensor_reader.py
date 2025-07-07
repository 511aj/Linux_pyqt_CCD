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
    ser = serial.Serial("COM11", 256000, timeout=1)  # 打开串口
    ser2 = serial.Serial("COM10", 9600, timeout=1)  # 打开另一个串口

    if not ser.isOpen() or not ser2.isOpen():
        print("串口打开失败。")
        return None

    time.sleep(1)

    # ✅ 发送到电机：回到起点 104
    command_start = bytes([0x5A, 0xA5, 0x01, 0x01, 0x03, 0x08, 0xf8, 0x01, 0x05])  # 刚刚好


    ser2.write(command_start)
    print("运动到传感器下面命令：", ' '.join(f'{b:02X}' for b in command_start))


    ser.write("@c0007#@\r\n".encode('utf-8'))
    time.sleep(1)
    ser.write("@c0080#@\r\n".encode('utf-8'))
    time.sleep(1)

    com_input = ser.read(8000)

    command_start = bytes([0x5A, 0xA5, 0x01, 0x01, 0x03, 0x20, 0xf9, 0x01, 0x1E])  # 刚刚好
    ser2.write(command_start)

    time.sleep(1)

    command_start = bytes([0x5A, 0xA5, 0x01, 0x01, 0x03, 0x0f, 0xf9, 0x00, 0x0C])  # 刚刚好
    ser2.write(command_start)

    ser.close()
    ser2.close()

    # 假设帧头为 4 字节，帧尾为 2 字节
    FRAME_HEADER_SIZE = 4
    FRAME_FOOTER_SIZE = 2

    # 提取有效像素区域
    pixel_bytes = com_input[FRAME_HEADER_SIZE : len(com_input) - FRAME_FOOTER_SIZE]

    # 将像素字节转换为像素值列表
    pixels = []
    for i in range(0, len(pixel_bytes), 2):
        if i + 1 >= len(pixel_bytes):
            break  # 忽略不完整的字节对
        high = pixel_bytes[i]
        low = pixel_bytes[i + 1]
        pixel = (high << 8) | low
        pixels.append(pixel)

    # 构建 full_data（模拟生成的数据包结构）
    frame_header = com_input[:FRAME_HEADER_SIZE]
    frame_footer = com_input[-FRAME_FOOTER_SIZE:]
    full_data = frame_header + pixel_bytes + frame_footer

    return full_data, pixels