import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, \
    QMessageBox, QCheckBox, QTextEdit, QSpinBox
from PyQt5.QtCore import QThread, pyqtSignal
import random
import time
from get_world_window import get_all_windows
class Worker(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            print("Method A is running...")
            #待实装喊话功能
            time.sleep(1)
            self.finished.emit()

    def stop(self):
        self.running = False


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = Worker()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("世界OL喊话工具")
        self.setGeometry(100, 100, 550, 320)

        left_group = QGroupBox("②填入喊话内容文本")
        left_layout = QVBoxLayout()

        left_group.setLayout(left_layout)
        self.speak_edit = QTextEdit(self)
        self.speak_edit.setGeometry(50, 50, 400, 300)

        row_layout11 = QHBoxLayout()
        row_layout1 = QHBoxLayout()
        row_layout1.addWidget(self.speak_edit)
        left_layout.addLayout(row_layout11)
        left_layout.addLayout(row_layout1)

        right_top_group = QGroupBox("①获取世界OL窗口句柄")
        right_top_layout = QVBoxLayout()
        right_top_group.setLayout(right_top_layout)

        self.get_window_button = QPushButton('点击获取窗口句柄')
        self.hidden_label = QLabel("")
        self.hidden_label.setStyleSheet("color: red")
        self.hidden_label.setVisible(False)

        right_top_layout.addWidget(self.get_window_button)
        right_top_layout.addWidget(self.hidden_label)
        right_top_layout.addStretch(0)
        self.get_window_button.clicked.connect(self.get_window)

        right_bottom_group = QGroupBox("③选择附加功能")
        right_bottom_layout = QHBoxLayout()
        right_bottom_group.setLayout(right_bottom_layout)

        radio4 = QCheckBox("自动使用喇叭")
        radio5 = QCheckBox("自动回到城市")

        radio_layout1 = QHBoxLayout()

        radio_layout1.addWidget(radio4)
        radio_layout1.addWidget(radio5)

        self.label_second = QLabel('间隔时间（秒）:', self)
        self.spinBox_second = QSpinBox(self)
        self.spinBox_second.setMinimum(60)
        self.spinBox_second.setMaximum(300)
        self.spinBox_second.setValue(60)

        radio_layout3 = QHBoxLayout()
        radio_layout3.addWidget(self.label_second)
        radio_layout3.addWidget(self.spinBox_second)

        radio_layout_T = QVBoxLayout()
        radio_layout_T.addLayout(radio_layout1)
        radio_layout_T.addLayout(radio_layout3)
        right_bottom_layout.addLayout(radio_layout_T)

        right_down_group = QGroupBox("④开始喊话")
        right_down_layout = QVBoxLayout()
        right_down_group.setLayout(right_down_layout)

        self.submit_button = QPushButton('开始')
        self.cancel_button = QPushButton('取消')

        bt_layout1 = QHBoxLayout()
        bt_layout2 = QHBoxLayout()

        bt_layout1.addWidget(self.submit_button)
        bt_layout2.addWidget(self.cancel_button)
        right_down_layout.addLayout(bt_layout1)
        right_down_layout.addLayout(bt_layout2)

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_group)
        sub_layout = QVBoxLayout()  # 右侧上下排列

        sub_layout.addWidget(right_top_group)
        sub_layout.addWidget(right_bottom_group)
        sub_layout.addWidget(right_down_group)

        main_layout.addLayout(sub_layout)

        self.setLayout(main_layout)
        self.submit_button.clicked.connect(self.start_speaker)
        self.cancel_button.clicked.connect(self.stop_or_cancel_speaker)


    def get_window(self):
        #获取窗口句柄
        window_list = get_all_windows()
        if len(window_list) == 0:
            self.hidden_label.setText("未获取到模拟器句柄")
            self.hidden_label.setStyleSheet("color:red")
            self.hidden_label.setVisible(True)
        else:
            self.hidden_label.setText("已获取模拟器句柄:%s"% (window_list[0][0]))
            self.hidden_label.setStyleSheet("color:black")
            self.hidden_label.setVisible(True)



    def start_speaker(self):
        if not self.worker.isRunning():
            self.submit_button.setEnabled(False)
            self.cancel_button.setText("停止")
            self.worker.start()

    def stop_or_cancel_speaker(self):
        if self.worker.isRunning():
            self.submit_button.setEnabled(True)
            self.cancel_button.setText("取消")
            self.worker.stop()
        if not self.worker.isRunning():
            self.close()

    def showMessageBox_success(self, text):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('执行结果')
        if text == "ok":
            msgBox.setText("执行成功!")
        else:
            msgBox.setText("执行失败!\n" + text)

        msgBox.setStandardButtons(QMessageBox.Ok)
        custom_font = QFont('', 10)
        msgBox.setFont(custom_font)
        returnValue = msgBox.exec_()

        if text == "ok":
            self.close()


    def showMessageBox(self, warn_text):

        msgBox = QMessageBox()
        msgBox.setWindowTitle('Warning!')
        msgBox.setText(warn_text + "\n的内容不能为空!")


    def stop_or_cancel_speaker(self):
        if self.worker.isRunning():
            self.submit_button.setEnabled(True)
            self.cancel_button.setText("取消")
            self.worker.stop()
        if not self.worker.isRunning():
            self.close()


    def showMessageBox_success(self, text):

        # 创建一个消息框
        msgBox = QMessageBox()
        msgBox.setStandardButtons(QMessageBox.Ok)
        custom_font = QFont('', 10)
        msgBox.setFont(custom_font)
        returnValue = msgBox.exec_()
        if returnValue == QMessageBox.Ok:
            return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
