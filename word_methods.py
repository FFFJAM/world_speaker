import win32gui
from get_world_window import get_all_windows
import time
import win32api,win32con
import pyautogui
import cv2
import numpy as np
import time,os
import math
class word_methods():

    def __init__(self):
        super().__init__()
        self.hwnd = get_all_windows()[0][0]
        print(self.hwnd)
        self.getWorldPositon()

    def press_key(self,key):
        # 模拟按下按键
        win32api.keybd_event(key, 0, 0, 0)

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
        print("世界OL窗口位置：" ,(self.left, self.top, right, bottom))
        self.width = right - self.left
        self.height = bottom - self.top


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
        self.mouse_click(speaker_position)
        self.mouse_click(world_channel_pos)
        self.mouse_click(text_pos)
        win32api.keybd_event(17, 0, 0, 0)  # ctrl按下
        win32api.keybd_event(86, 0, 0, 0)  # v按下
        win32api.keybd_event(86, 0, 0, 0)  # v抬起
        win32api.keybd_event(17, 0, 0, 0)  # ctrl抬起
        self.mouse_click(send_pos)

    def get_rela_pos(self,x,y):
        return [self.left + int(x * self.width),self.top + int(y* self.height)]

if __name__ == '__main__':
    wm = word_methods()
    wm.speaker()