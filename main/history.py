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

import user_manager
import test_config

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox
)
import sqlite3


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

        self.table_combo = self.findChild(QtWidgets.QComboBox, 'table_combo')
        self.refresh_btn = self.findChild(QtWidgets.QPushButton, 'refresh_btn')
        self.query_btn = self.findChild(QtWidgets.QPushButton, 'query_btn')
        self.table = self.findChild(QtWidgets.QTableWidget, 'table')
        self.delete_btn = self.findChild(QtWidgets.QPushButton, 'delete_btn')

        self.refresh_btn.clicked.connect(self.load_table_names)
        self.query_btn.clicked.connect(self.load_data)
        self.delete_btn.clicked.connect(self.delete_selected_row)

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

    def get_connection(self):
        try:
            return sqlite3.connect("local_data.db")
        except Exception as e:
            QMessageBox.critical(self, "数据库错误", f"连接失败: {e}")
            return None

    def load_table_names(self):
        conn = self.get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%_CCD'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            self.table_combo.clear()
            self.table_combo.addItems(tables)
        finally:
            conn.close()

    def load_data(self):
        table_name = self.table_combo.currentText()
        if not table_name:
            return

        conn = self.get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `{table_name}`")
            result = cursor.fetchall()

            self.table.setRowCount(0)
            for row_data in result:
                row = self.table.rowCount()
                self.table.insertRow(row)

                display_indices = [1, 2, 3, 4, 5, 6, 7, 8]  # 假设从第 2 列开始是你要显示的字段
                for col, idx, in enumerate(display_indices):
                    value = row_data[idx]
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row, col, item)

        finally:
            conn.close()

    def delete_selected_row(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "提示", "请先选择一行数据")
            return

        table_name = self.table_combo.currentText()
        item_id = self.table.item(selected_row, 0).text()

        confirm = QMessageBox.question(
            self, "确认删除", f"确定要删除 ID 为 {item_id} 的记录吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            conn = self.get_connection()
            if not conn:
                return

            try:
                # 移除 Cursor 的 with 语句
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM `{table_name}` WHERE id = ?", (item_id,))
                conn.commit()
                self.load_data()
                QMessageBox.information(self, "成功", "删除成功")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除失败: {e}")
            finally:
                conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = HistoryWindow()
    main_window.show()
    sys.exit(app.exec_())
