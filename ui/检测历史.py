# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'history_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 480)
        Form.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.top = QtWidgets.QFrame(Form)
        self.top.setGeometry(QtCore.QRect(1, -10, 798, 101))
        self.top.setStyleSheet("QWidget#top{\n"
                               "\n"
                               "border: 1px solid black;\n"
                               "border-radius: 10px;\n"
                               "}\n"
                               "")
        self.top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top.setObjectName("top")
        self.label = QtWidgets.QLabel(self.top)
        self.label.setGeometry(QtCore.QRect(130, 20, 471, 71))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.home = QtWidgets.QFrame(self.top)
        self.home.setGeometry(QtCore.QRect(724, 2, 70, 75))
        self.home.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.home.setFrameShadow(QtWidgets.QFrame.Raised)
        self.home.setObjectName("home")
        self.label_11 = QtWidgets.QLabel(self.home)
        self.label_11.setGeometry(QtCore.QRect(2, 0, 55, 55))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("batch.png"))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_2 = QtWidgets.QLabel(self.home)
        self.label_2.setGeometry(QtCore.QRect(0, 56, 62, 15))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.under = QtWidgets.QFrame(Form)
        self.under.setGeometry(QtCore.QRect(0, 435, 800, 51))
        self.under.setStyleSheet("background-color:rgb(170, 255, 255)")
        self.under.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.under.setFrameShadow(QtWidgets.QFrame.Raised)
        self.under.setObjectName("under")
        self.label_13 = QtWidgets.QLabel(self.under)
        self.label_13.setGeometry(QtCore.QRect(240, 14, 261, 31))
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_13.setObjectName("label_13")
        self.dateLabel = QtWidgets.QLabel(self.under)
        self.dateLabel.setGeometry(QtCore.QRect(0, 0, 130, 45))
        self.dateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dateLabel.setObjectName("dateLabel")
        self.timeLabel = QtWidgets.QLabel(self.under)
        self.timeLabel.setGeometry(QtCore.QRect(680, 0, 120, 45))
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 90, 796, 341))
        self.frame.setStyleSheet("QWidget#frame{\n"
                                 "\n"
                                 "border: 1px solid black;\n"
                                 "border-radius: 10px;\n"
                                 "}\n"
                                 "")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(580, 10, 100, 32))
        self.pushButton.setStyleSheet("background-color:rgb(27, 134, 204);\n"
                                      "color:rgb(255,255,255);\n"
                                      "border-radius: 5px; \n"
                                      "        ")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(690, 10, 100, 32))
        self.pushButton_2.setStyleSheet("background-color:rgb(27, 134, 204);\n"
                                        "color:rgb(255,255,255);\n"
                                        "border-radius: 5px; \n"
                                        "        ")
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame_7 = QtWidgets.QFrame(self.frame)
        self.frame_7.setGeometry(QtCore.QRect(0, 146, 800, 3))
        self.frame_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.frame_9 = QtWidgets.QFrame(self.frame)
        self.frame_9.setGeometry(QtCore.QRect(0, 146, 804, 3))
        self.frame_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(110, 290, 100, 31))
        self.pushButton_4.setStyleSheet("background-color:rgb(27, 134, 204);\n"
                                        "color:rgb(255,255,255);\n"
                                        "border-radius: 5px; \n"
                                        "        ")
        self.pushButton_4.setObjectName("pushButton_4")
        self.frame_8 = QtWidgets.QFrame(self.frame)
        self.frame_8.setGeometry(QtCore.QRect(10, 10, 141, 91))
        self.frame_8.setStyleSheet("QWidget#frame_8{\n"
                                   "\n"
                                   "border: 1px solid black;\n"
                                   "border-radius: 10px;\n"
                                   "}\n"
                                   "")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.label_4 = QtWidgets.QLabel(self.frame_8)
        self.label_4.setGeometry(QtCore.QRect(1, 1, 71, 21))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.frame_8)
        self.label_5.setGeometry(QtCore.QRect(6, 36, 91, 31))
        self.label_5.setStyleSheet("")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_5.setObjectName("label_5")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(110, 150, 461, 131))
        self.tableWidget.setStyleSheet("QWidget#frame{\n"
                                       "\n"
                                       "border: 1px solid black;\n"
                                       "border-radius: 10px;\n"
                                       "}\n"
                                       "")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setBackground(QtGui.QColor(141, 200, 109, 0))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(107)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(18)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(200, 10, 160, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(390, 10, 160, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.comboBox_2 = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_2.setObjectName("comboBox_2")
        self.verticalLayout_3.addWidget(self.comboBox_2)
        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(230, 290, 100, 32))
        self.pushButton_6.setStyleSheet("background-color:rgb(27, 134, 204);\n"
                                        "color:rgb(255,255,255);\n"
                                        "border-radius: 5px; \n"
                                        "        ")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.frame)
        self.pushButton_7.setGeometry(QtCore.QRect(350, 290, 100, 32))
        self.pushButton_7.setStyleSheet("background-color:rgb(27, 134, 204);\n"
                                        "color:rgb(255,255,255);\n"
                                        "border-radius: 5px; \n"
                                        "        ")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.frame)
        self.pushButton_8.setGeometry(QtCore.QRect(460, 290, 100, 32))
        self.pushButton_8.setStyleSheet("background-color:rgb(27, 134, 204);\n"
                                        "color:rgb(255,255,255);\n"
                                        "border-radius: 5px; \n"
                                        "        ")
        self.pushButton_8.setObjectName("pushButton_8")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.frame)
        self.tableWidget_2.setGeometry(QtCore.QRect(580, 150, 201, 131))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, item)
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setGeometry(QtCore.QRect(580, 300, 181, 21))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.label_18 = QtWidgets.QLabel(self.frame_5)
        self.label_18.setGeometry(QtCore.QRect(0, 0, 54, 12))
        self.label_18.setObjectName("label_18")
        self.comboBox_3 = QtWidgets.QComboBox(self.frame_5)
        self.comboBox_3.setGeometry(QtCore.QRect(36, 0, 141, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(590, 100, 161, 21))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(590, 120, 161, 21))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_3.addWidget(self.lineEdit_3)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(590, 80, 181, 21))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 230, 101, 41))
        self.pushButton_5.setStyleSheet("background-color:rgb(27, 134, 204);\n"
                                        "color:rgb(255,255,255);\n"
                                        "border-radius: 5px; \n"
                                        "        ")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 160, 99, 41))
        self.pushButton_3.setStyleSheet("background-color:rgb(27, 134, 204);\n"
                                        "color:rgb(255,255,255);\n"
                                        "border-radius: 5px; \n"
                                        "        ")
        self.pushButton_3.setObjectName("pushButton_3")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "胶体金检测分析仪"))
        self.label_2.setText(_translate("Form", "测试"))
        self.label_13.setText(_translate("Form", "检测历史"))
        self.dateLabel.setText(_translate("Form", "TextLabel"))
        self.timeLabel.setText(_translate("Form", "TextLabel"))
        self.pushButton.setText(_translate("Form", "改编号"))
        self.pushButton_2.setText(_translate("Form", "计时"))
        self.pushButton_4.setText(_translate("Form", "首页"))
        self.label_4.setText(_translate("Form", "当前用户:"))
        self.label_5.setText(_translate("Form", "admin"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "样本号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "项目"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "倒计时"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "当前状态"))
        self.label_3.setText(_translate("Form", "样本类型："))
        self.label_6.setText(_translate("Form", "项目："))
        self.pushButton_6.setText(_translate("Form", "上一页"))
        self.pushButton_7.setText(_translate("Form", "下一页"))
        self.pushButton_8.setText(_translate("Form", "尾页"))
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("Form", "子项目名"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("Form", "结果"))
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText(_translate("Form", "单位"))
        self.label_18.setText(_translate("Form", "时间："))
        self.label_8.setText(_translate("Form", "项目："))
        self.label_9.setText(_translate("Form", "样本类型："))
        self.label_7.setText(_translate("Form", "样本号："))
        self.pushButton_5.setText(_translate("Form", "删除"))
        self.pushButton_3.setText(_translate("Form", "样本+1"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
