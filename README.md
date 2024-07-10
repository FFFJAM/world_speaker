# **世界OL喊话工具**

- 阅读本指南应具备的能力：Python基础、PyCharm基础、Pyqt5基础、OpenCV2基础以及一定的世界OL游玩经验。

- 本指南面向的对象：技术热爱者、工具受益者、世界OL玩家作者。

  


## **<u>Day1</u>：功能设计**

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

## <u>Day2</u>：前端界面的绘制与句柄获取功能：

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

最终效果如图所示：![演示](https://github.com/FFFJAM/tuchuang/blob/main/show.gif)