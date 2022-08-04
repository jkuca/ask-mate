from datetime import datetime
from sample_data import data_manager


def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def is_accepted(data):
    if data['accepted'] == 1:
        return 15
    else:
        return 10


def exists_specify_tag(question_id, tag):
    question_tag = data_manager.getQuestionTagById(question_id)
    for value in question_tag:
        if value['tag_id'] == int(tag):
            return True
    return False
