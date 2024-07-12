import win32gui
from get_world_window import get_all_windows
import win32api,win32con
import pyautogui
import cv2
import numpy as np
import time

class word_methods():

    def __init__(self):
        super().__init__()
        self.hwnd = get_all_windows()[0][0]
        print(self.hwnd)
        self.getWorldPositon()
        self.method = cv2.TM_CCOEFF

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

    def speaker(self):
        speaker_position = self.get_rela_pos(0.15 ,0.98)
        world_channel_pos = self.get_rela_pos(0.1, 0.22)
        text_pos = self.get_rela_pos(0.1, 0.07)
        send_pos = self.get_rela_pos(0.1, 0.5)
        delete_pos = self.get_rela_pos(0.93, 0.1)
        self.mouse_click(speaker_position)
        self.mouse_click(world_channel_pos)
        self.mouse_click(text_pos)
        win32api.keybd_event(17, 0, 0, 0)  # ctrl按下
        win32api.keybd_event(86, 0, 0, 0)  # v按下
        win32api.keybd_event(86, 0, 0, 0)  # v抬起
        win32api.keybd_event(17, 0, 0, 0)  # ctrl抬起
        self.mouse_click(send_pos)
        self.mouse_click(delete_pos)
        self.mouse_click(delete_pos)

    def get_speaker_pos(self):
        medcial_position = self.get_rela_pos(0.45, 0.85)
        self.mouse_click(medcial_position)
        world_png = pyautogui.screenshot(region=[self.left, self.top ,self.width , self.height])
        world_png = cv2.cvtColor(np.asarray(world_png), cv2.COLOR_RGB2BGR)
        ask_png = cv2.imread('ba.PNG')
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
            # 显示结果
            return "ok"


    def get_rela_pos(self,x,y):
        return [self.left + int(x * self.width),self.top + int(y* self.height)]

if __name__ == '__main__':
    wm = word_methods()
    wm.get_speaker_pos()