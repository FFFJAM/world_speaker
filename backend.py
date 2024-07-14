from word_methods import word_methods_class
import win32clipboard
import time
import datetime
import global_result
def set_clipboard_text(text):
    text = text.encode('gbk')
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()

def record_time(start_time):
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    days = elapsed_time.days
    hours, remainder = divmod(elapsed_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = "程序运行时间：{:02}天{:02}时{:02}分{:02}秒".format(days, hours, minutes, seconds)
    return formatted_time

def back_func(speak_str,window_list,flag_speaker,flag_city,second):
    start_time = datetime.datetime.now()

    set_clipboard_text(speak_str)
    wm = word_methods_class(window_list[0][0])
    if flag_city ==1:
        wm.return_to_city()

    if flag_speaker == 0:
        t = 0
        for i in range(10):
            wm.speaker()
            t+=1
            time_string = record_time(start_time)
            global_result.modify_global("ok %s 总共喊话%s次" % (time_string, str(t)))
            time.sleep(second)
        return "ok"

    elif flag_speaker == 1:
        result = ""
        t = 0
        while result != "nospeaker":
            for i in range(10):
                wm.speaker()
                t += 1
                time_string = record_time(start_time)
                global_result.modify_global("ok %s 总共喊话%s次" % (time_string, str(t)))
                time.sleep(second)
            result = wm.get_speaker_pos()
            time.sleep(5)
        time_string = record_time(start_time)
        global_result.modify_global("ok %s 总共喊话%s次" % (time_string, str(t)))
        global_result.modify_running(False)
        return "ok"

    return "failed"
