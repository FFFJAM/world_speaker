# **世界OL喊话工具**

- 工具特点：使用OpenCV图像识别，并基于win32api模拟人工操作，无需读取游戏内存，封号风险接近于0
- 本指南面向的对象：技术热爱者、工具受益者、世界OL玩家等。


------

## 使用教程

1.下载[雷电模拟器](https://www.ldmnq.com/)并安装打开

![leidian](https://github.com/FFFJAM/tuchuang/blob/main/leidian.png)

2.下载世界ol并拖入雷电模拟器

![world_raiden](https://github.com/FFFJAM/tuchuang/blob/main/world_raiden.png)

3.设置分辨率为1280x720

![image-20240714215413470](https://github.com/FFFJAM/tuchuang/blob/main/720.png)

4.打开[世界ol](http://sj.good321.net/d.action)并登录

5.双击打开喊话工具

![image-20240714221150424](https://github.com/FFFJAM/tuchuang/blob/main/exefile.png)

6.依次获取世界ol窗口句柄，填入喊话文本，设置附加功能以及间隔时间（60~300秒）后点击开始

![image-20240714221258477](https://github.com/FFFJAM/tuchuang/blob/main/toolfont.png)

------

## 制作思路

### **<u>Day1</u>：功能设计**

#### 世界OL游戏背景：

​	《世界OL》是由[广州谷得网络科技有限公司](https://baike.baidu.com/item/广州谷得网络科技有限公司/20059466?fromModule=lemma_inlink)研发的一款角色扮演回合制游戏，于2011年9月26日发行。在这款游戏中，玩家可以扮演各种各样的角色，在世界中打怪，升级。游戏以开放完善的交易系统而闻名，因而玩家出于交易或其他需求需要经常在“频道”中发言。玩家为确保自己的发言能够被不同时间进入世界的玩家看到，经常需要重复多次地输入相同的内容，大大降低游戏体验。于是世界OL喊话工具应运而生。

#### 世界OL喊话工具需求设计：

1. 能够获取模拟器上运行的世界OL窗口句柄并在屏幕上进行精确定位
2. 具备基础的输入文本定时喊话功能
3. 进阶功能：可选是否自动使用小喇叭，喊话间隔时间（最小60秒）等

#### 工具功能逻辑分析：

​	首先通过前端界面获取用户输入的各种信息，经过check后进入喊话执行子流程，并在收到结束信号后停止执行。

​	初步设计获取3类共6种信息：

​	文本框：喊话文本、间隔时间

​	按钮点击：获取窗口句柄、开始执行信号

​	单选栏：自动使用喇叭、自动回到城市

​	最终所得工具功能逻辑图如图1所示：

![image-20240709232707184](https://github.com/FFFJAM/tuchuang/blob/main/tooltotal.png)

<center>图1：工具功能逻辑图</center>

### <u>Day2</u>：前端界面的绘制与句柄获取功能：

#### 前端页面的绘制：

​	前端通过Pyqt5编写，窗体名称设定为“世界OL喊话工具”

```Python
self.setWindowTitle('世界喊话工具')
self.resize(600, 400)
```

​	设置喊话内容文本区域，并添加文本框以供输入：

```python
left_group = QGroupBox("②填入喊话内容文本")
left_layout = QVBoxLayout()

left_group.setLayout(left_layout)
self.speak_edit = QTextEdit(self)
self.speak_edit.setGeometry(50, 50, 400, 300)
```

​	设置获取窗口句柄区域，包含一个可触发获取句柄事件的按钮与文本，用于显示获取到的句柄

```python
right_top_group = QGroupBox("①获取世界OL窗口句柄")
right_top_layout = QVBoxLayout()
right_top_group.setLayout(right_top_layout)

self.get_window_button = QPushButton('点击获取窗口句柄')
self.hidden_label = QLabel("")
self.hidden_label.setStyleSheet("color: red")
self.hidden_label.setVisible(False)
```

​	设置附加功能区域，包含两个checkbox和一个QSpinBox，以供获取相关信息

```python
right_bottom_group = QGroupBox("③选择附加功能")
right_bottom_layout = QHBoxLayout()
right_bottom_group.setLayout(right_bottom_layout)

radio4 = QCheckBox("自动使用喇叭")
radio5 = QCheckBox("自动回到城市")
......
self.label_second = QLabel('间隔时间（秒）:', self)
self.spinBox_second = QSpinBox(self)
```

​	最后是按钮操作区域，设置两个按钮，开始与取消，在点击开始后，开始按钮会disabled并且取消按钮变成停止

```Py
right_down_group = QGroupBox("④开始喊话")
right_down_layout = QVBoxLayout()
right_down_group.setLayout(right_down_layout)

self.submit_button = QPushButton('开始')
self.cancel_button = QPushButton('取消')
```

​	最后将这些区域添加到主样式里

```python
main_layout = QHBoxLayout()
main_layout.addWidget(left_group)
sub_layout = QVBoxLayout()  # 右侧上下排列

sub_layout.addWidget(right_top_group)
sub_layout.addWidget(right_bottom_group)
sub_layout.addWidget(right_down_group)

main_layout.addLayout(sub_layout)
```

​	最后执行效果如图2所示

![image-20240709233958705](https://github.com/FFFJAM/tuchuang/blob/main/fontpager.png)

<center>图2：前端效果图</center>

#### 句柄获取功能：

​	本工具基于[雷电模拟器](https://www.ldmnq.com/)上运行的世界OL版本进行设计，所以获取窗口标题关键字设置为TheRender，完整代码如下

```python
import win32gui
#获取所有窗口
def get_all_windows():
    hWnd_list = []
    rander_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)
    for hWnd in hWnd_list:
        if len(get_son_windows(hWnd)) > 0:
            rander_list.append(get_son_windows(hWnd))
    return rander_list

#获取所有子窗口
def get_son_windows(parent):
    hWnd_child_list = []
    rander_list_child = []
    win32gui.EnumChildWindows(parent, lambda hWnd, param: param.append(hWnd), hWnd_child_list)
    for hWnd_child in hWnd_child_list:
        if get_title(hWnd_child) == 'TheRender':
            rander_list_child.append(hWnd_child)
    return rander_list_child

#获取窗口以及标题
def get_title(hwnd):
    title = win32gui.GetWindowText(hwnd)
    return title
```

​	参考文章：[Python----pywin32如何获取窗口句柄_pywin32获取窗口句柄-CSDN博客](https://blog.csdn.net/qq_39369520/article/details/119520185)

​	最终效果如图所示：



https://github.com/FFFJAM/world_speaker/assets/121446420/accead79-93c0-4a60-b7b8-36d01e359f99



### <u>Day3</u>：check功能以及弹窗：

​	设置QTextEdit控件默认文本，以及文本最大长度

```Python
self.speak_edit.setPlaceholderText("喊话文本不可包含空格\n文本最大长度为120字符")
self.speak_edit.textChanged.connect(self.check_text_length)
......
    def check_text_length(self):
        max_length = 120  # 设置最大长度为120个字符
        text = self.speak_edit.toPlainText()
        if len(text) > max_length:
            self.speak_edit.setPlainText(text[:max_length])
```

​	设置校验方法，检测喊话文本是否为空，是否包含空格以及窗口句柄是否获取

```Python
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
```

​	最终效果如图所示

![image-20240711001332293](https://github.com/FFFJAM/tuchuang/blob/main/check.png)

![image-20240711001421947](https://github.com/FFFJAM/tuchuang/blob/main/check2.png)

<center>图3：check效果图</center>

### <u>Day4</u>：世界OL相关操作：

​	定义操作类，在初始化时执行获取窗口句柄方法，并获取窗口位置

```Python
class word_methods():

    def __init__(self):
        super().__init__()
        self.hwnd = get_all_windows()[0][0]
        print(self.hwnd)
        self.getWorldPositon()
```

​	定义回到个人城市方法

```Python
def return_to_city(self):

    city_position = self.get_rela_pos(0.8 ,0.95)
    enter_city_pos = self.get_rela_pos(0.5, 0.85)
    delete_pos = self.get_rela_pos(0.93,0.1)
    self.mouse_click(city_position)
    self.mouse_click(enter_city_pos)
    self.mouse_click(delete_pos)
    self.mouse_click(delete_pos)
```

​	点击聊天框并将文本粘贴到输入框中并发送

```Python
def speaker(self):
    speaker_position = self.get_rela_pos(0.15 ,0.98)
    world_channel_pos = self.get_rela_pos(0.1, 0.22)
    text_pos = self.get_rela_pos(0.1, 0.07)
    send_pos = self.get_rela_pos(0.1, 0.5)
    self.mouse_click(speaker_position)
    self.mouse_click(world_channel_pos)
    self.mouse_click(text_pos)
    win32api.keybd_event(17, 0, 0, 0)  # ctrl按下
    win32api.keybd_event(86, 0, 0, 0)  # v按下
    win32api.keybd_event(86, 0, 0, 0)  # v抬起
    win32api.keybd_event(17, 0, 0, 0)  # ctrl抬起
    self.mouse_click(send_pos)
```

### <u>Day5</u>：基于OpenCV的自动使用小喇叭：

​	点击道具视图

```Python
medcial_position = self.get_rela_pos(0.45, 0.85)
self.mouse_click(medcial_position)
```

​	截取窗口，并设定截图分辨率

```Python
world_png = pyautogui.screenshot(region=[self.left, self.top ,self.width , self.height])
world_png = cv2.cvtColor(np.asarray(world_png), cv2.COLOR_RGB2BGR)
ask_png = cv2.imread('ba.PNG')
target_size = (450, 807)
world_png = cv2.resize(world_png, target_size)
```

​	使用 TM_CCOEFF_NORMED 方法进行模板匹配并设定匹配阈值

```Python
result = cv2.matchTemplate(world_png, ask_png, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
```

​	当未匹配到结果时，将光标移动到屏幕中心，并滚动鼠标滚轮

```Python
while len(loc[::-1][0]) == 0:
    center_position = self.get_rela_pos(0.5, 0.5)
    win32api.SetCursorPos(center_position)
    self.mouse_wheel(-120)  # -120表示向下滚动
    time.sleep(1)  # 等待0.5秒
```

​	重新截屏并进行图像识别

```Python
world_png = pyautogui.screenshot(region=[self.left, self.top, self.width, self.height])
world_png = cv2.cvtColor(np.asarray(world_png), cv2.COLOR_RGB2BGR)
world_png = cv2.resize(world_png, target_size)
result = cv2.matchTemplate(world_png, ask_png, cv2.TM_CCOEFF_NORMED)
loc = np.where(result >= threshold)
```

​	由于之前对屏幕截图进行像素缩放，所以重新获取对于源窗口正确的小喇叭道具位置，并点击鼠标

```Python
for pt in zip(*loc[::-1]):
    alt_wid +=pt[0]
    alt_higt += pt[1]
alt_wid = int(alt_wid/len(loc[::-1][0]))
alt_higt = int(alt_higt/len(loc[::-1][0]))

rate =  self.width / 450
rate_wid = (rate * alt_wid)/self.width
rate_higt = (rate * alt_higt)/self.height
speaker_position_med = self.get_rela_pos(rate_wid, rate_higt)
self.mouse_click(speaker_position_med)
delete_pos = self.get_rela_pos(0.93, 0.1)
self.mouse_click(delete_pos)
self.mouse_click(delete_pos)
```
