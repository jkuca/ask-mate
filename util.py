from datetime import datetime


def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def is_accepted(data):
    if data['accepted'] == 1:
        return 15
    else:
        return 10
