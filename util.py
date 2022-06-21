import time

def get_time():
    named_tuple = time.localtime()
    current_time= time.strftime("%H:%M", named_tuple)
    return current_time