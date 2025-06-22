"""
Project ：Linux_pyqt_CCD 
File    ：key.py
IDE     ：PyCharm 
Author  ：wj
Date    ：2025/6/22 下午10:20 
role    :
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit


class VirtualKeyboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 创建 QLineEdit 用于显示输入内容
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        # 创建键盘布局
        keyboard_layout = QVBoxLayout()

        # 添加字母按键
        for row in ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM']:
            h_layout = QHBoxLayout()
            for letter in row:
                button = QPushButton(letter)
                button.clicked.connect(lambda char=letter: self.on_button_click(char))
                h_layout.addWidget(button)
            keyboard_layout.addLayout(h_layout)

        # 添加功能键（如退格）
        backspace_button = QPushButton('Backspace')
        backspace_button.clicked.connect(self.on_backspace_click)
        keyboard_layout.addWidget(backspace_button)

        # 将键盘布局添加到主布局
        layout.addLayout(keyboard_layout)

    def on_button_click(self, char):
        current_text = self.line_edit.text()
        self.line_edit.setText(current_text + char)

    def on_backspace_click(self):
        current_text = self.line_edit.text()
        self.line_edit.setText(current_text[:-1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VirtualKeyboard()
    window.show()
    sys.exit(app.exec_())
