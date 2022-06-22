import time

def get_time():
    local_time = time.localtime()
    current_time= time.strftime("%H:%M", local_time)
    return current_time