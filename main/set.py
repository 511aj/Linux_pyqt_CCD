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
from json_config_set import read_setting, write_setting
from sensor_reader import read_sensor_data
import subprocess


# 设置界面
class SETWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SETWindow, self).__init__()
        # 加载test UI文件
        self.window = None
        uic.loadUi('../ui/set_ui.ui', self)

        self.timeLabel = self.findChild(QtWidgets.QLabel, 'timeLabel')  # 寻找时间标签
        self.dateLabel = self.findChild(QtWidgets.QLabel, 'dateLabel')  # 寻找日期标签

        self.backBtn = self.findChild(QtWidgets.QFrame, 'backBtn')  # 寻找返回主页按钮
        self.dateEdit = self.findChild(QtWidgets.QDateEdit, 'dateEdit')  # 寻找日期编辑框
        self.timeEdit = self.findChild(QtWidgets.QTimeEdit, 'timeEdit')  # 寻找时间编辑框

        self.reset_all.clicked.connect(self.reset_all_settings)  # 连接重置所有设置按钮信号槽
        self.self_test.clicked.connect(self.reset_settings)  # 连接自检按钮信号槽
        self.uptime_online.clicked.connect(self.set_time_ntpdate)  # 连接自检按钮信号槽

        # 检查标签是否成功找到
        if self.timeLabel is None:
            print("Error: timeLabel not found in UI")
        if self.dateLabel is None:
            print("Error: dateLabel not found in UI")
        if self.backBtn is not None:
            self.backBtn.mousePressEvent = self.back_to_main
        else:
            print("Error: backBtn not found in UI")

        # 创建定时器，每秒更新时间和日期
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每1秒触发一次

        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.timeEdit.setTime(QtCore.QTime.currentTime())
        print(QtCore.QDate.currentDate())
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

    def back_to_main(self, event):
        print("回到主界面")
        from main import MainMenu as main_menu_ui
        # 回到主界面
        self.window = main_menu_ui()
        # 关闭当前窗口
        self.close()
        # 显示主界面
        self.window.show()

    @staticmethod  # 重置所有设置
    def reset_all_settings():

        write_setting('date', "2025,6,13")
        write_setting('time', "s")

    @staticmethod  # 自检
    def reset_settings():
        # todo 做一个等待自检的提示
        read_sensor_data()

    # 同步NTP时间
    def set_time_ntpdate(self):
        try:
            # 执行 ntpdate 命令同步时间（需 root 权限）
            subprocess.run(["ntpdate", "pool.ntp.org"], check=True)
            print("时间同步成功")
            self.dateEdit.setDate(QtCore.QDate.currentDate())
            self.timeEdit.setTime(QtCore.QTime.currentTime())
            return True
        except subprocess.CalledProcessError as e:
            print(f""
                  f" 时间同步失败: {e}")
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SETWindow()
    main_window.show()
    sys.exit(app.exec_())
