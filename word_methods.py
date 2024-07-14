import base64
import win32gui
import win32api,win32con
import pyautogui
import cv2
import numpy as np
import time


class word_methods_class():

    def __init__(self,hwnd):
        super().__init__()
        self.hwnd = hwnd
        print(self.hwnd)
        self.getWorldPositon()
        self.method = cv2.TM_CCOEFF
        self.png = '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'
    def press_key(self,key):
        # 模拟按下按键
        win32api.keybd_event(key, 0, 0, 0)

    def mouse_wheel(self,delta):
        # 模拟鼠标滚轮操作
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, delta, 0)

    def release_key(self,key):
        # 释放按键
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

    def mouse_click(self,position):
        # 鼠标定位到(30,50)
        win32api.SetCursorPos(position)
        # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        # 右键单击
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(1)

    def getWorldPositon(self):
        # 通过句柄值获取当前窗口的【左、上、右、下】四个方向的坐标位置
        print("世界OL窗口句柄：", self.hwnd)
        self.left, self.top, right, bottom = win32gui.GetWindowRect(self.hwnd)

        self.width = right - self.left
        self.height = bottom - self.top

        print("世界OL窗口位置：", (self.left, self.top, self.width, self.height))

    def return_to_city(self):

        city_position = self.get_rela_pos(0.8 ,0.95)
        enter_city_pos = self.get_rela_pos(0.5, 0.85)
        delete_pos = self.get_rela_pos(0.93,0.1)
        self.mouse_click(city_position)
        self.mouse_click(enter_city_pos)
        self.mouse_click(delete_pos)
        self.mouse_click(delete_pos)

    def base64_to_image(self,base64_code):

        img_data = base64.b64decode(base64_code)
        img_array = np.fromstring(img_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
        return img

    def speaker(self):
        speaker_position = self.get_rela_pos(0.15 ,0.98)
        world_channel_pos = self.get_rela_pos(0.1, 0.22)
        text_pos = self.get_rela_pos(0.1, 0.07)
        send_pos = self.get_rela_pos(0.1, 0.5)
        delete_pos = self.get_rela_pos(0.93, 0.1)
        self.mouse_click(speaker_position)
        self.mouse_click(world_channel_pos)
        self.mouse_click(text_pos)
        self.press_key(17)
        self.press_key(86)
        self.release_key(86)
        self.release_key(17)
        self.mouse_click(send_pos)
        self.mouse_click(delete_pos)
        self.mouse_click(delete_pos)

    def get_speaker_pos(self):
        medcial_position = self.get_rela_pos(0.45, 0.85)
        self.mouse_click(medcial_position)
        world_png = pyautogui.screenshot(region=[self.left, self.top ,self.width , self.height])
        world_png = cv2.cvtColor(np.asarray(world_png), cv2.COLOR_RGB2BGR)
        ask_png = self.base64_to_image(self.png)
        target_size = (450, 807)
        world_png = cv2.resize(world_png, target_size)


        # 使用 TM_CCOEFF_NORMED 方法进行模板匹配
        result = cv2.matchTemplate(world_png, ask_png, cv2.TM_CCOEFF_NORMED)

        # 设定阈值
        threshold = 0.8

        loc = np.where(result >= threshold)
        t=0
        while len(loc[::-1][0]) == 0 and t<6:
            t+=1
            center_position = self.get_rela_pos(0.5, 0.5)
            win32api.SetCursorPos(center_position)
            self.mouse_wheel(-120)  # -120表示向下滚动
            time.sleep(1)  # 等待0.5秒

            world_png = pyautogui.screenshot(region=[self.left, self.top, self.width, self.height])
            world_png = cv2.cvtColor(np.asarray(world_png), cv2.COLOR_RGB2BGR)
            world_png = cv2.resize(world_png, target_size)
            result = cv2.matchTemplate(world_png, ask_png, cv2.TM_CCOEFF_NORMED)
            # 使用 TM_CCOEFF_NORMED 方法进行模板匹配
            loc = np.where(result >= threshold)

            print(loc)
            print(len(loc[::-1][0]))
        if len(loc[::-1][0]) == 0:
            return "nospeaker"
            # 标记匹配区域
        else:
            alt_wid = 0
            alt_higt = 0
            t = 0
            for pt in zip(*loc[::-1]) :
                if t<3:
                    t+=1
                    alt_wid +=pt[0]
                    alt_higt += pt[1]
            alt_wid = int(alt_wid/3)
            alt_higt = int(alt_higt/3)

            rate =  self.width / 450
            rate_wid = (rate * alt_wid)/self.width
            rate_higt = (rate * alt_higt)/self.height
            speaker_position_med = self.get_rela_pos(rate_wid, rate_higt)
            self.mouse_click(speaker_position_med)
            self.mouse_click(speaker_position_med)
            delete_pos = self.get_rela_pos(0.93, 0.1)
            self.mouse_click(delete_pos)
            self.mouse_click(delete_pos)
            # 显示结果
            return "ok"


    def get_rela_pos(self,x,y):
        return [self.left + int(x * self.width),self.top + int(y* self.height)]



if __name__ == '__main__':
    result = ""
    t = 0
    wm = word_methods_class(461612)
    while result != "nospeaker":
        for i in range(10):
            wm.speaker()
            t += 1
            time.sleep(5)
        result = wm.get_speaker_pos()
        time.sleep(20)
#   pr
    print("xxxx")