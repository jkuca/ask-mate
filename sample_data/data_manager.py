from sample_data import connection
from flask import request
import util


def get_sorted_questions():

    _list = connection.read_file("question.csv")

    def sorting(element):
        return element['submission_time']

    _list.sort(key=sorting)
    return _list


def get_question_by_id(id):
    _list = connection.read_file("question.csv")
    for item in _list:
        if item['id'] == id:
            return item


def get_quetion_and_answers(id):
    question = get_question_by_id(id)
    list_of_answers = []
    answers = connection.read_file('answer.csv')
    for answer in answers:
        if answer["question_id"] == id:
            list_of_answers.append(answer)
    question.setdefault("answers", list_of_answers)
    return question


def write_message_update(row):
    connection.update_file(row, "question.csv")


def get_edit_question(id_post):
    data_of_question = get_question_by_id(id_post)
    message = request.form.get("message")
    title = request.form.get('title')
    data_to_save = {'id': data_of_question['id'], 'submission_time': data_of_question['submission_time'], 'view_number': data_of_question['view_number'],
                    'vote_number': data_of_question['vote_number'], 'title': title, 'message': message, "image": ""}
    write_message_update(data_to_save)


def generate_id(file):
    _list = connection.read_file(file)
    generated_id = len(_list)+1
    return generated_id


def write_message_new(row):
    connection.add_new_row(row, "question.csv")


def add_new_question():
    id = generate_id("question.csv")
    submission_time = util.get_time()
    view_number = 0
    vote_number = 0
    title = request.form.get('title')
    message = request.form.get('message')
    data_to_save = {'id': id, 'submission_time': submission_time, 'view_number': view_number,
                    'vote_number': vote_number, 'title': title, 'message': message, "image": ""}
    write_message_new(data_to_save)
    return id


def write_answer_new(row):
    connection.add_new_row(row, "answer.csv")


def add_new_answer(question_id):
    id = generate_id('answer.csv')
    submission_time = util.get_time()
    vote_number = 0
    message = request.form.get('message')
    data_to_save = {'id': id, 'submission_time': submission_time,
                    'vote_number': vote_number, 'question_id': question_id, 'message': message, "image": ""}
    write_answer_new(data_to_save)


def count_visits(id):
    data_of_question = get_question_by_id(id)
    data_of_question['view_number'] = int(data_of_question['view_number']) + 1
    write_message_update(data_of_question)


def delete_row(id):
    connection.delete_row({'id': id}, 'question.csv')


def get_votes(id):
    data_of_question = get_question_by_id(id)
    return int(data_of_question['vote_number'])


def count_votes_up(id):
    data_of_question = get_question_by_id(id)
    data_of_question['vote_number'] = get_votes(id) + 1
    write_message_update(data_of_question)


def count_votes_down(id):
    data_of_question = get_question_by_id(id)
    data_of_question['vote_number'] = get_votes(id) - 1
    write_message_update(data_of_question)
