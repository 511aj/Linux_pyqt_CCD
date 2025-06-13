"""
Project ：Linux_pyqt_CCD 
File    ：set.py
IDE     ：PyCharm 
Author  ：wj
Date    ：2025/6/13 下午2:14 
role    :设置界面的实现
"""
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from qtpy import uic


# 设置界面
class SETWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SETWindow, self).__init__()
        # 加载test UI文件
        uic.loadUi('./set.ui', self)

        self.timeLabel = self.findChild(QtWidgets.QLabel, 'timeLabel')  # 寻找时间标签
        self.dateLabel = self.findChild(QtWidgets.QLabel, 'dateLabel')  # 寻找日期标签

        # 检查标签是否成功找到
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

    def update_time(self):
        # 获取当前时间和日期
        current_time = QtCore.QTime.currentTime().toString("hh:mm:ss")
        current_date = QtCore.QDate.currentDate().toString("yyyy-MM-dd")

        # 设置时间和日期到标签
        if self.timeLabel and self.dateLabel:  # 确保标签存在
            self.timeLabel.setText(current_time)
            self.dateLabel.setText(current_date)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SETWindow()
    main_window.show()
    sys.exit(app.exec_())
