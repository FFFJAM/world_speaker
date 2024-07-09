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


