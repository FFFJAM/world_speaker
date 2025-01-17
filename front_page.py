import sys
import global_result
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, \
    QMessageBox, QCheckBox, QTextEdit, QSpinBox
from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop
from backend import back_func
from get_world_window import get_all_windows

class Worker(QThread):
    finished = pyqtSignal()
    signal = pyqtSignal()
    def __init__(self,speak_str,window_list,flag_speaker,flag_city,second):
        super().__init__()
        self.running = False
        self.speaker_str = speak_str
        self.window_list = window_list
        self.flag_speaker = flag_speaker
        self.flag_city = flag_city
        self.second = second

    def stop(self):
        self.running = False
        global_result.modify_running(False)
        result = global_result.result_msg
        print(result)
        if result.startswith("ok"):
            mes_list = "\n".join(result.split(" ")[1:])
            global_result.modify_global(mes_list)
            self.showMessageBox_success_chid()
        else:
            global_result.modify_global(result + "\n请联系工具作者")
            self.showMessageBox_success_chid()

    def showMessageBox_success_chid(self):
        # 子线程中创建消息框
        self.signal.emit()
        self.signal.connect(self.onMessageBoxClosed)

    def onMessageBoxClosed(self):
        # 消息框关闭后执行的操作
        window.close()
        self.terminate()

    def run(self):
        self.running = True
        while self.running:
            self.result = back_func(self.speaker_str,self.window_list,self.flag_speaker,self.flag_city,self.second)
            self.running = global_result.running_flag
            self.finished.emit()
        self.stop()

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.flag_speaker = 0
        self.flag_city = 0

    def initUI(self):
        self.setWindowTitle("世界OL喊话工具")
        self.setGeometry(100, 100, 550, 320)

        left_group = QGroupBox("②填入喊话内容文本")
        left_layout = QVBoxLayout()

        left_group.setLayout(left_layout)
        self.speak_edit = QTextEdit(self)
        self.speak_edit.setPlaceholderText("喊话文本不可包含空格\n文本最大长度为120字符")
        self.speak_edit.setGeometry(50, 50, 400, 300)
        self.speak_edit.textChanged.connect(self.check_text_length)

        row_layout11 = QHBoxLayout()
        row_layout1 = QHBoxLayout()
        row_layout1.addWidget(self.speak_edit)
        left_layout.addLayout(row_layout11)
        left_layout.addLayout(row_layout1)

        right_top_group = QGroupBox("①获取世界OL窗口句柄")
        right_top_layout = QVBoxLayout()
        right_top_group.setLayout(right_top_layout)
        self.window_list = []
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

        self.radio4 = QCheckBox("自动使用喇叭")
        self.radio5 = QCheckBox("自动回到城市")

        radio_layout1 = QHBoxLayout()

        radio_layout1.addWidget(self.radio4)
        radio_layout1.addWidget(self.radio5)

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

    def check_text_length(self):
        max_length = 120  # 设置最大长度为120个字符
        text = self.speak_edit.toPlainText()
        if len(text) > max_length:
            self.speak_edit.setPlainText(text[:max_length])

    def get_window(self):
        #获取窗口句柄
        self.window_list = get_all_windows()
        if len(self.window_list) == 0:
            self.hidden_label.setText("未获取到模拟器句柄")
            self.hidden_label.setStyleSheet("color:red")
            self.hidden_label.setVisible(True)
        else:
            self.hidden_label.setText("已获取模拟器句柄:%s"% (self.window_list[0][0]))
            self.hidden_label.setStyleSheet("color:black")
            self.hidden_label.setVisible(True)

    def start_speaker(self):
        speak_str = self.speak_edit.toPlainText()
        chech_result = self.check(speak_str)
        if self.radio4.isChecked():
            self.flag_speaker = 1
        if self.radio5.isChecked():
            self.flag_city = 1
        second = self.spinBox_second.value()
        self.worker = Worker(speak_str,self.window_list,self.flag_speaker,self.flag_city,second)
        self.worker.signal.connect(self.showMessageBox_child)
        if chech_result == 'ok':
            if not self.worker.isRunning():
                self.submit_button.setEnabled(False)
                self.cancel_button.setText("停止")
                self.worker.start()
        else:
            self.showMessageBox(chech_result)

    def handle_result(self,result):
        return result

    def check(self,speak_str):
        warn_text = ""
        if len(speak_str) == 0:
            warn_text += "喊话文本不能为空！\n"
        else:
            if " " in speak_str:
                warn_text += "喊话文本不能包含空格！\n"
        if len(self.window_list) == 0:
            warn_text += "窗口句柄不能为空！\n"
        if len(warn_text)==0:
            return "ok"
        else:
            return warn_text

    def stop_or_cancel_speaker(self):
        if self.worker.isRunning():
            self.submit_button.setEnabled(True)
            self.cancel_button.setText("取消")
            self.worker.stop()
            result = global_result.result_msg
            print(result)
            if result.startswith("ok"):
                mes_list = "\n".join(result.split(" ")[1:])
                self.showMessageBox_success(mes_list)
            else:
                self.showMessageBox_success(result)
        if not self.worker.isRunning():
            self.close()

    def showMessageBox_success(self, text):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('执行结果')
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        custom_font = QFont('', 10)
        msgBox.setFont(custom_font)
        # 执行消息框，并获取返回值
        returnValue = msgBox.exec_()
        # 根据用户的点击响应来处理
        if returnValue == QMessageBox.Ok:
            msgBox.close()  # 手动关闭消息框


    def showMessageBox(self, warn_text):

        msgBox = QMessageBox()
        msgBox.setWindowTitle('Warning!')
        msgBox.setText(warn_text)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def showMessageBox_child(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('执行结果')
        text = global_result.result_msg
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        custom_font = QFont('', 10)
        msgBox.setFont(custom_font)
        # 执行消息框，并获取返回值
        returnValue = msgBox.exec_()
        # 根据用户的点击响应来处理
        if returnValue == QMessageBox.Ok:
            global_result.modify_ending(True)
            msgBox.close()  # 手动关闭消息框


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
