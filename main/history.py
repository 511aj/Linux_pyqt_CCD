"""
Project ：Linux_pyqt_CCD 
File    ：history.py
IDE     ：PyCharm 
Author  ：wj
Date    ：2025/6/13 下午2:18 
role    :
"""

import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from qtpy import uic

from ui.检测历史 import Ui_Form as HistoryUI


# 检测历史窗口
class HistoryWindow(QtWidgets.QWidget):
    def __init__(self):
        super(HistoryWindow, self).__init__()
        # self.ui = HistoryUI()  # 使用导入的 HistoryUI 类
        # self.ui.setupUi(self)
        self.window = None
        uic.loadUi('../ui/history_ui.ui', self)  # 使用 uic 加载 ui 文件

        # 初始化时间和日期
        self.timeLabel = self.findChild(QtWidgets.QLabel, 'timeLabel')
        self.dateLabel = self.findChild(QtWidgets.QLabel, 'dateLabel')

        self.backBtn = self.findChild(QtWidgets.QFrame, 'backBtn')

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        if self.backBtn is not None:
            self.backBtn.mousePressEvent = self.back_to_main
        else:
            print("backBtn is None")

    def update_time(self):
        current_time = QtCore.QTime.currentTime().toString("hh:mm:ss")
        current_date = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
        if self.timeLabel and self.dateLabel:
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = HistoryWindow()
    main_window.show()
    sys.exit(app.exec_())
