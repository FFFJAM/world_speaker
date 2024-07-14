result_msg = ""
running_flag = True
end_flag = False
def modify_global(mes):
    global result_msg
    result_msg = mes
def modify_running(flag):
    global running_flag
    running_flag = flag
def modify_ending(e_flag):
    global end_flag
    end_flag = e_flag
