"""
串口通信工具类
----------------------------------------------------------
功能说明：
该模块定义了一个 SerialPort 类，用于实现串口的打开、发送数据、接收数据以及关闭等基础操作。

使用示例：
from serial_utils import SerialPort

# 初始化串口对象（根据实际设备修改串口号和波特率）
sp = SerialPort(port='COM3', baudrate=115200)

# 打开串口
if sp.open_port():
    # 发送数据（例如：发送一个字节序列）
    sp.send_data(b'\x01\x02\x03\x04')

    # 读取返回数据（例如：读取最多10个字节）
    response = sp.read_data(10)

    # 关闭串口
    sp.close_port()

----------------------------------------------------------

注意：
 1. 串口号（port）需要根据实际连接的设备修改，如 COM3（Windows）或 /dev/ttyUSB0（Linux）。
 2. 波特率（baudrate）需要根据实际设备的通信速率进行设置，如 115200。
 3. 超时时间（timeout）默认设置为 2 秒，可以根据实际情况进行调整。

依赖库：
- pyserial: 用于串口通信
- ctypes: 用于构建 C 风格字节缓冲区（兼容某些底层通信需求）

"""
import serial
import ctypes


class SerialPort:
    def __init__(self, port, baudrate=115200, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open_port(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            if self.ser.isOpen():
                print("打开串口成功。")
                return True
        except Exception as e:
            print(f"打开串口失败: {e}")
        return False

    def send_data(self, data):
        wbuf = ctypes.create_string_buffer(len(data))
        for i, byte in enumerate(data):
            wbuf[i] = byte
        write_len = self.ser.write(wbuf)
        print("串口发出{}个字节。".format(write_len))
        return write_len

    def read_data(self, size):
        com_input = self.ser.read(size)
        if com_input:
            print("接收到数据:", com_input)
            return com_input
        return None

    def close_port(self):
        if self.ser and self.ser.isOpen():
            self.ser.close()
            print("串口已关闭。")
