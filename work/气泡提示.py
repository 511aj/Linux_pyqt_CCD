"""
Project ：Linux_pyqt_CCD 
File    ：气泡提示.py
IDE     ：PyCharm 
Author  ：wj
Date    ：2025/6/23 下午2:10 
role    :
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QFont


class TooltipDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('按钮气泡提示示例')
        self.resize(300, 200)

        # 设置字体
        QToolTip.setFont(QFont('Microsoft YaHei', 12))


        self.button = QPushButton('点击我显示提示', self)
        self.button.clicked.connect(self.show_custom_tooltip)

        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def show_custom_tooltip(self):
        # 获取按钮的位置（相对于父窗口）
        pos = self.button.mapToGlobal(self.button.rect().topLeft())
        final_pos = pos + QPoint(30, -50)  # -20 表示向上偏移
        # 在按钮上方显示气泡提示
        QToolTip.showText(final_pos, "气泡", self.button)

        # 使用 QTimer 在2秒后隐藏提示
        QTimer.singleShot(2000, QToolTip.hideText)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TooltipDemo()
    demo.show()
    sys.exit(app.exec_())

