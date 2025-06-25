"""
Project ：Linux_pyqt_CCD
File    ：scan.py
IDE     ：PyCharm
Author  ：wj
Date    ：2025/6/13 下午2:14
role    :试纸检测界面
         在Widget中画曲线，需要导入QPainter，QColor，QApplication，QMainWindow，QVBoxLayout，QWidget，uic库。

"""

import json
import sys
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QPoint, QTimer, QRectF
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolTip
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QPolygonF
from PyQt5.QtWidgets import QWidget
from qtpy import uic

# 导入函数
from mqtt_send import mqtt_send_data
from sensor_reader import read_sensor_data, generate_random_packet
import user_manager

T_value = 50
C_value = 50
now_user = ""


# 串口接收输出线程
class SeriaReadThread(QThread):
    data_received = pyqtSignal(list)  # 定义一个信号，用于传递数据

    def run(self):
        """在线程中执行串口读取"""
        received_data = self.serial_port()
        if received_data:
            print(received_data)
            self.data_received.emit(received_data)  # 发送数据信号

    # 串口操作
    @staticmethod
    def serial_port():
        # todo 暂时模拟串口读取
        print("打开串口")
        # data_string = read_sensor_data()
        # if data_string is not None:
        #     print(data_string)
        # else:
        #     print("获取传感器数据失败。")
        #
        # byte_list = data_string.split()  # 将字符串拆分为字节列表
        # formatted_sequence = ""  # 使用循环构建格式化的字符串
        #
        # for byte in byte_list:
        #     formatted_sequence += f'0x{byte},'  # 在每个字节后加上逗号和空格
        # formatted_sequence = formatted_sequence.rstrip(', ')  # 删除最后多余的逗号和空格
        # received_data = ([formatted_sequence])
        time.sleep(2)
        packet, generated_pixels = generate_random_packet()
        print("生成的数据:", packet)

        received_data = list(packet)

        print("发送的数据:", received_data)
        return received_data


# 画图类
class PlotWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.pixels = self.extract_pixel_data(data)

    @staticmethod
    def extract_pixel_data(data):
        """从接收到的数据中提取像素值"""
        if len(data) < 4 + 3648 * 2 + 2:  # 添加检测确保数据长度足够
            raise ValueError("Received data is too short")
        pixel_data = data[4:-2]  # 除去帧头和帧尾
        pixels = []
        for i in range(0, len(pixel_data), 2):
            high_byte = pixel_data[i]
            low_byte = pixel_data[i + 1]
            pixel_value = (high_byte << 8) | low_byte  # 组合成一个像素值
            pixels.append(pixel_value)
            # print(len(pixels))
        """ 使曲线平滑"""
        for i in range(5, 3640, 1):
            pixels[i] = (pixels[i - 5] + pixels[i - 4] + pixels[i - 3] + pixels[i - 2] + pixels[i - 1] + pixels[i] +
                         pixels[i + 1] + pixels[i + 2] + pixels[i + 3] + pixels[i + 4] + pixels[i + 5]) / 11
        """ 求斜率"""
        xielv = [0] * 3630
        for i in range(1, 3560, 1):
            xielv[i] = (pixels[i + 1] - pixels[i - 1]) / 2

        # 初始化列表来存储所有波谷的起点、顶点和终点
        valleys = []

        # 遍历范围
        for i in range(1000, 2000, 1):
            xielv[i] = (xielv[i + 6] + xielv[i + 7] + xielv[i + 8] + xielv[i + 9] +
                        xielv[i] + xielv[i + 1] + xielv[i + 2] + xielv[i + 3] +
                        xielv[i + 4] + xielv[i + 5]) / 10

            # 如果找到第一个小于-0.5的斜率（起点）
            if len(valleys) == 0 or (len(valleys) > 0 and valleys[-1]['end'] is not None):
                if xielv[i] < -0.5:
                    valleys.append({'start': i, 'peak': None, 'end': None})  # 记录起点

            # 找到第一个大于0.4的斜率（顶点）
            if len(valleys) > 0 and valleys[-1]['peak'] is None and xielv[i] > 0.4:
                valleys[-1]['peak'] = i  # 记录顶点

            # 找到第一个小于0.4的斜率（终点）
            if len(valleys) > 0 and valleys[-1]['peak'] is not None and valleys[-1]['end'] is None and xielv[i] < 0.4:
                valleys[-1]['end'] = i  # 记录终点

        # 初始化变量 算出面积 打印结果
        Cs = None  # C波谷面积
        Ts = None  # T波谷面积
        main_valley = None  # 主波谷

        for valley in reversed(valleys):
            if valley['start'] is not None and valley['peak'] is not None and valley['end'] is not None:
                start = valley['start']
                peak = valley['peak']
                end = valley['end']
                # 计算波谷的面积
                Bl = (pixels[start] + pixels[start - 1] + pixels[start - 2] + pixels[start + 1] + pixels[start + 2]) / 5
                Br = (pixels[end] + pixels[end - 1] + pixels[end - 2] + pixels[end + 1] + pixels[end + 2]) / 5
                result_value = (Bl + Br) * (end - start) / 2

                s = 0
                for i in range(start, end, 1):
                    s += pixels[i]
                s = result_value - s

                # 判断波谷是否是主波谷（顶点在1800附近）
                if abs(peak - 1800) < 100:  # 假设主波谷顶点在1800附近（误差范围±100）
                    main_valley = valley
                # 根据位置关系判断是C波谷还是T波谷
                if main_valley is not None:
                    if peak < main_valley['peak']:  # 在主波谷之前的波谷
                        if Ts is None:  # 如果T波谷还没有被赋值，则当前波谷是T波谷
                            Ts = s
                        elif Cs is None:  # 如果T波谷已经赋值，则当前波谷是C波谷
                            Cs = s

                # print(f"波谷 起点: {start}, 顶点: {peak}, 终点: {end}, 计算结果: {result_value}, 面积: {s}")

            # 输出C波谷和T波谷的面积以及比值
        if Cs is not None and Ts is not None:
            ratio = Ts / Cs
            print(f"主波谷: {main_valley['peak']},T波谷面积: {Ts}, C波谷面积: {Cs},比值 Ts/Cs: {ratio}")
        else:
            print("未能找到足够的波谷来计算面积和比值")

        # 调用 mqtt 发送函数
        topic = "resr"

        messages = {
            "username": "wj",
            "main_valley": main_valley['peak'],
            "T_size": Ts,
            "C_size": Cs,
            "T/C_ratio": ratio,
            "operator": now_user
        }

        json_messages = json.dumps(messages)
        print(json_messages)
        mqtt_send_data(topic, json_messages)
        return pixels

    # 画笔
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))  # 设置画笔颜色

        width = self.width()
        height = self.height()

        start_index = 1000  # 数据起始索引
        end_index = 2500  # 数据结束索引

        if end_index > len(self.pixels):
            end_index = len(self.pixels)

        # 定义偏移量
        axis_offset = 0  # 坐标轴下移的偏移量
        curve_offset = 20  # 曲线上移的偏移量

        # 绘制 x 轴刻度
        painter.setPen(QColor(100, 100, 100))  # 刻度颜色
        tick_length = 5  # 刻度线长度
        font = painter.font()
        font.setPixelSize(10)
        painter.setFont(font)

        # 计算 x 轴刻度间隔（每 100 个像素点画一个刻度）
        tick_interval = 100
        num_ticks = (end_index - start_index) // tick_interval

        for i in range(num_ticks + 1):
            data_index = start_index + i * tick_interval  # 实际像素索引（1000, 1100, 1200...）
            if data_index >= end_index:
                continue

            # 计算 x 坐标（基于 0 开始，因为 (index - start_index)）
            x = (data_index - start_index) * (width / (end_index - start_index))

            # 绘制刻度线（使用 height - axis_offset 作为新的 y 基准）
            painter.drawLine(int(x), height - axis_offset - 10, int(x), height - axis_offset - tick_length - 10)

            # 绘制刻度标签（显示实际像素索引，如 1000, 1100, ...）
            painter.drawText(int(x), height - axis_offset - tick_length + 5, f"{data_index}")

        # 绘制曲线（原代码）
        painter.setPen(QColor(0, 0, 0))  # 恢复画笔颜色
        previous_x = None
        previous_y = None

        for index in range(start_index, end_index):
            x = (index - start_index) * (width / (end_index - start_index))  # x 从 0 开始计算
            # y = height - (self.pixels[index] / max(self.pixels) * height) - curve_offset
            y = (self.pixels[index] / max(self.pixels) * height) - curve_offset  # 图像上下翻转，波峰变成波谷，面积计算一样的

            if previous_x is not None and previous_y is not None:
                painter.drawLine(previous_x, previous_y, int(x), int(y))

            previous_x = int(x)
            previous_y = int(y)


# 画CT指示器
class LineWithArrows(QWidget):
    """
    复用方法：
    # 获取或创建布局
    layout = self.line_widget.layout() or QVBoxLayout(self.line_widget)
    self.line_widget.setFixedHeight(50)
    self.lineWithArrows.set_arrow_positions(3, 400)
    # 添加新的绘图部件
    layout.addWidget(self.lineWithArrows)
    self.lineWithArrows.set_arrow_positions(60, 50)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_y = 30  # 固定线的位置（y 坐标）
        self.arros_height = 30  # 箭头高度
        self.arrow_size = 5  # 箭头大小
        self.arrow_x_left = 0  # 左箭头的 x 坐标
        self.arrow_x_right = self.width()  # 右箭头的 x 坐标

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置画笔
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # 绘制水平线（固定位置）
        line_start = QPointF(0, self.line_y)
        line_end = QPointF(self.width(), self.line_y)
        painter.drawLine(line_start, line_end)

        """
        原理：QPolygonF 是一个点的集合，可以用来绘制多边形。
        这里使用 QPolygonF 来绘制箭头。
        给三角形的三个点赋值，然后绘制即可。
        """

        arrow_left = QPolygonF([
            QPointF(self.arrow_x_left, self.line_y - self.arros_height),
            QPointF(self.arrow_x_left - self.arrow_size, self.line_y),
            QPointF(self.arrow_x_left + self.arrow_size, self.line_y)
        ])
        painter.setBrush(Qt.red)
        painter.drawPolygon(arrow_left)

        # 右箭头（朝下）
        arrow_right = QPolygonF([
            QPointF(self.arrow_x_right, self.line_y - self.arros_height),
            QPointF(self.arrow_x_right - self.arrow_size, self.line_y),
            QPointF(self.arrow_x_right + self.arrow_size, self.line_y)
        ])
        painter.setBrush(Qt.blue)
        painter.drawPolygon(arrow_right)

    def set_arrow_positions(self, left_x, right_x):
        """设置左右箭头的位置"""
        self.arrow_x_left = left_x
        self.arrow_x_right = right_x
        self.update()  # 触发重绘


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.line_widget = None
        self.thread = None
        self.window = None
        self.plot_widget = None

        uic.loadUi('../ui/scan_ui.ui', self)  # 加载 UI 文件

        # 日期和时间显示
        self.timeLabel = self.findChild(QtWidgets.QLabel, 'timeLabel')  # 寻找时间标签
        self.dateLabel = self.findChild(QtWidgets.QLabel, 'dateLabel')  # 寻找日期标签
        if self.timeLabel is None:
            print("Error: timeLabel not found in UI")
        if self.dateLabel is None:
            print("Error: dateLabel not found in UI")
        # 创建定时器，每秒更新时间和日期
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每1秒触发一次
        # 初始化时间和日期显示
        self.update_time()

        # 动态创建进度条并加入 widget 布局
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setRange(0, 0)  # 不确定模式
        self.progressBar.hide()
        self.Porgress_bar = self.findChild(QtWidgets.QWidget, 'Porgress_bar')
        # 获取 widget 的布局，如果没有就新建一个
        layout = self.Porgress_bar.layout()
        if layout is None:
            layout = QVBoxLayout(self.Porgress_bar)
        layout.addWidget(self.progressBar)

        # 连接按钮事件
        self.scanBtn.clicked.connect(self.update_plot)
        self.backBtn.clicked.connect(self.back_to_main)

        # T/C值标签
        self.T_label = self.findChild(QtWidgets.QLabel, 'T_label')
        self.C_label = self.findChild(QtWidgets.QLabel, 'C_label')

        # 滑动条
        self.horizontalSlider_T = self.findChild(QtWidgets.QSlider, 'horizontalSlider_T')
        self.horizontalSlider_C = self.findChild(QtWidgets.QSlider, 'horizontalSlider_C')

        self.horizontalSlider_T.setValue(50)
        self.horizontalSlider_C.setValue(50)

        self.horizontalSlider_T.valueChanged.connect(self.vslider_T_changeda)
        self.horizontalSlider_C.valueChanged.connect(self.vslider_C_changeda)

        # C/T箭头指示器
        self.lineWithArrows = LineWithArrows()
        layout_line = self.line_widget.layout() or QVBoxLayout(self.line_widget)
        self.line_widget.setFixedHeight(50)
        self.lineWithArrows.set_arrow_positions(3, 400)
        # 添加进布局
        layout_line.addWidget(self.lineWithArrows)

        # 设置气泡字体
        QToolTip.setFont(QFont('Microsoft YaHei', 12))

        current_user = user_manager.load_data().get("current_user")
        global now_user
        now_user = current_user['account']
        print("当前用户：" + now_user)

    def update_time(self):
        """更新时间和日期"""
        current_time = QtCore.QTime.currentTime().toString("hh:mm:ss")
        current_date = QtCore.QDate.currentDate().toString("yyyy-MM-dd")

        # 设置时间和日期到标签
        if self.timeLabel and self.dateLabel:
            self.timeLabel.setText(current_time)
            self.dateLabel.setText(current_date)

    def back_to_main(self):
        """回到主界面"""
        from main import MainMenu as main_menu_ui
        # 回到主界面
        self.window = main_menu_ui()
        # 关闭当前窗口
        self.close()
        # 显示主界面
        self.window.show()

    def update_plot(self):
        """更新 PlotWidget 的数据并重新绘制"""
        if self.thread and self.thread.isRunning():
            print("线程已在运行，跳过重复启动")

            pos = self.Porgress_bar.mapToGlobal(self.Porgress_bar.rect().topLeft())
            # 位置偏移
            final_pos = pos + QPoint(0, 0)
            QToolTip.showText(final_pos, "请等待测量完成", self.Porgress_bar)

            # 使用 QTimer 在2秒后隐藏提示
            QTimer.singleShot(2000, QToolTip.hideText)
            return

        # 显示进度条
        self.progressBar.show()

        # 启动线程读取串口数据
        self.thread = SeriaReadThread()
        self.thread.data_received.connect(self.handle_received_data)
        self.thread.start()

    def handle_received_data(self, received_data):
        # 隐藏进度条
        self.progressBar.hide()

        # 清理旧的绘图部件
        if self.plot_widget:
            self.plot_widget.deleteLater()
        self.plot_widget = PlotWidget(received_data)

        # 获取或创建布局
        layout = self.widget.layout() or QVBoxLayout(self.widget)

        # 清空布局中的所有控件（只保留布局本身）
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 添加新的绘图部件
        layout.addWidget(self.plot_widget)

    def vslider_T_changeda(self):
        """T线滑动条变化事件"""
        global T_value
        T_value = self.horizontalSlider_T.value()
        self.T_label.setText("T线:" + str(T_value))
        self.lineWithArrows.set_arrow_positions(T_value, C_value)

    def vslider_C_changeda(self):
        """C线滑动条变化事件"""
        global C_value
        C_value = self.horizontalSlider_C.value()
        self.C_label.setText("C线:" + str(C_value))
        self.lineWithArrows.set_arrow_positions(T_value, C_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
