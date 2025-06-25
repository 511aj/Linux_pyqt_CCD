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
import user_manager
import test_config


class SETWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SETWindow, self).__init__()
        # 加载test UI文件
        self.now_name = None
        self.now_act = None
        self.is_widget = None
        self.now_is = None
        self.refresh_button = None
        self.name_widget = None
        self.act_widget = None
        self.window = None
        uic.loadUi('../ui/set_ui.ui', self)

        # 初始化时间和日期相关控件
        self.timeLabel = self.findChild(QtWidgets.QLabel, 'timeLabel')  # 寻找时间标签
        self.dateLabel = self.findChild(QtWidgets.QLabel, 'dateLabel')  # 寻找日期标签

        self.backBtn = self.findChild(QtWidgets.QFrame, 'backBtn')  # 寻找返回主页按钮
        self.dateEdit = self.findChild(QtWidgets.QDateEdit, 'dateEdit')  # 寻找日期编辑框
        self.timeEdit = self.findChild(QtWidgets.QTimeEdit, 'timeEdit')  # 寻找时间编辑框

        # 按钮信号绑定
        self.reset_all.clicked.connect(self.reset_all_settings)  # 连接重置所有设置按钮信号槽
        self.self_test.clicked.connect(self.reset_settings)  # 连接自检按钮信号槽
        self.uptime_online.clicked.connect(self.set_time_ntpdate)  # 连接NTP同步按钮信号槽

        # 检查是否成功找到控件
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

        # 设置默认时间和日期
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.timeEdit.setTime(QtCore.QTime.currentTime())
        self.update_time()  # 初始化显示

        # 用户管理部分
        self.refresh_button = self.findChild(QtWidgets.QPushButton, 'refresh_button')
        self.change_button = self.findChild(QtWidgets.QPushButton, 'change_button')
        self.delete_button = self.findChild(QtWidgets.QPushButton, 'delete_button')
        self.act_widget = self.findChild(QtWidgets.QListWidget, 'act_widget')  # 账号列表
        self.name_widget = self.findChild(QtWidgets.QListWidget, 'name_widget')  # 用户名列表
        self.is_widget = self.findChild(QtWidgets.QListWidget, 'is_widget')  # 是否管理员列表

        self.now_act = self.findChild(QtWidgets.QLabel, 'now_act')  # 当前账号显示
        self.now_name = self.findChild(QtWidgets.QLabel, 'now_name')  # 当前用户名显示
        self.now_is = self.findChild(QtWidgets.QLabel, 'now_is')  # 当前用户类型显示

        # 绑定事件
        self.refresh_button.clicked.connect(self.refresh_user_list)
        self.change_button.clicked.connect(self.change_user)
        self.delete_button.clicked.connect(self.delete_user_btn)
        self.act_widget.itemClicked.connect(self.change_user_select)

        # 初始化加载用户数据
        self.selected_user = None  # 存储选中的完整用户字典
        self.refresh_user_list()

        # 加载测试配置
        self.spin_batch = self.findChild(QtWidgets.QSpinBox, 'spin_batch')  # 批次数量
        self.combo_tabel = self.findChild(QtWidgets.QComboBox, 'combo_tabel')  # 表格名称
        self.combo_save = self.findChild(QtWidgets.QComboBox, 'combo_save')  # 保存位置
        self.combo_sampled = self.findChild(QtWidgets.QComboBox, 'combo_sampled')  # 采样方式

        self.spin_batch.setValue(test_config.get_batch_size())  # 加载批次数量
        self.combo_tabel.addItems(test_config.get_table_fields())  # 加载表格名称
        if test_config.get_save_flag():
            self.combo_save.setCurrentIndex(0)  # 加载保存位置
        else:
            self.combo_save.setCurrentIndex(1)
        if test_config.get_sampled_flag():
            self.combo_sampled.setCurrentIndex(0)
        else:
            self.combo_sampled.setCurrentIndex(1)

        # 绑定信号
        self.spin_batch.valueChanged.connect(self.spijn_batch_changed)
        self.combo_tabel.activated.connect(self.combo_sampled_changed)
        self.combo_save.activated.connect(self.combo_save_changed)
        self.combo_sampled.activated.connect(self.combo_tabel_changed)

    def update_time(self):
        # 获取当前时间和日期
        current_time = QtCore.QTime.currentTime().toString("hh:mm:ss")
        current_date = QtCore.QDate.currentDate().toString("yyyy-MM-dd")

        # 更新标签显示
        if self.timeLabel and self.dateLabel:
            self.timeLabel.setText(current_time)
            self.dateLabel.setText(current_date)

    def back_to_main(self, event):
        print("回到主界面")
        from main import MainMenu as main_menu_ui
        self.window = main_menu_ui()
        self.close()
        self.window.show()

    @staticmethod
    def reset_all_settings():
        """重置所有设置"""
        write_setting('date', "2025,6,13")
        write_setting('time', "s")

    @staticmethod
    def reset_settings():
        """执行自检"""
        read_sensor_data()

    def set_time_ntpdate(self):
        """通过 NTP 同步网络时间"""
        try:
            subprocess.run(["ntpdate", "pool.ntp.org"], check=True)
            print("时间同步成功")
            self.dateEdit.setDate(QtCore.QDate.currentDate())
            self.timeEdit.setTime(QtCore.QTime.currentTime())
            return True
        except subprocess.CalledProcessError as e:
            print(f"时间同步失败: {e}")
            return False

    def refresh_user_list(self):
        """刷新用户列表和当前用户信息"""
        user_data = user_manager.load_data()
        users = user_manager.get_users(user_data)

        # 清空列表
        self.act_widget.clear()
        self.name_widget.clear()
        self.is_widget.clear()

        # 填充列表
        for user in users:
            self.act_widget.addItem(user['account'])
            self.name_widget.addItem(user['username'])
            self.is_widget.addItem(str(user['is_admin']))

        # 显示当前用户信息
        current_user = user_manager.load_data().get("current_user")
        if current_user:
            self.now_act.setText(current_user['account'])
            self.now_name.setText(current_user['username'])
            self.now_is.setText("是" if current_user['is_admin'] else "否")
        else:
            print("当前用户信息不存在")

    def change_user_select(self):
        """点击用户列表项时记录选中的用户"""
        row = self.act_widget.currentRow()
        if row < 0:
            print("未选择任何用户")
            return

        user_data = user_manager.load_data()
        users = user_manager.get_users(user_data)

        self.selected_user = users[row]  # 保存完整用户字典
        print("已选择用户：", self.selected_user)

    def change_user(self):
        """切换当前用户并刷新界面"""
        print("切换用户")

        if not hasattr(self, 'selected_user') or self.selected_user is None:
            print("未选择要切换的用户")
            return

        # 加载数据
        user_data = user_manager.load_data()

        # 设置当前用户
        user_manager.set_current_user(user_data, self.selected_user)

        # 刷新用户列表和当前用户显示
        self.refresh_user_list()

    def delete_user_btn(self):
        """删除选中的用户"""
        row = self.act_widget.currentRow()
        if row < 0:
            print("未选择任何用户")
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除用户 '{self.act_widget.currentItem().text()}' 吗？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if confirm != QtWidgets.QMessageBox.Yes:
            return

        user_data = user_manager.load_data()

        try:
            # 删除用户
            user_manager.delete_user(user_data, row)

            # 如果删除的是当前用户，则设置 current_user 为 None 或第一个用户
            if self.selected_user and row == self.act_widget.currentRow():
                if len(user_data['users']) > 0:
                    user_manager.set_current_user(user_data, user_data['users'][0])
                else:
                    user_manager.set_current_user(user_data, None)

            # 刷新界面
            self.refresh_user_list()
            print("用户删除成功")

        except Exception as e:
            print("删除失败:", e)
            QtWidgets.QMessageBox.critical(self, "错误", "删除用户时发生错误")

    def spijn_batch_changed(self):
        """批次数量改变时更新测试配置"""
        batch_num = self.spin_batch.value()
        test_config.set_batch_size(batch_num)

    def combo_sampled_changed(self):
        """表格名称改变时更新测试配置"""
        table_selected = self.combo_tabel.currentText()
        test_config.set_now_table(table_selected)

    def combo_save_changed(self):
        """保存位置改变时更新测试配置"""
        save_selected = self.combo_save.currentText()
        if save_selected == "是":
            test_config.set_save_flag(True)
        else:
            test_config.set_save_flag(False)

    def combo_tabel_changed(self):
        """采样方式改变时更新测试配置"""
        sampled_selected = self.combo_sampled.currentText()
        if sampled_selected == "单次采样":
            test_config.set_sampled_flag(True)
        else:
            test_config.set_sampled_flag(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SETWindow()
    main_window.show()
    sys.exit(app.exec_())
