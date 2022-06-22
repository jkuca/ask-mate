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


def generate_id():

    _list = connection.read_file("question.csv")
    generated_id = len(_list)+1
    return generated_id


def write_message(row):
    connection.write_file(row, "question.csv")


def get_answer_and_question(question_id):
    questions = connection.read_file('question.csv')
    answers = connection.read_file('answer.csv')
    for q in questions:
        if question_id == q[0]:
            question = q
    answer = [a for a in answers if a[0] == question_id]
    return question, answer


def add_new_question():
    id = generate_id()
    submission_time = util.get_time()
    view_number = 0
    vote_number = 0
    title = request.form['title']
    message = request.form['message']
    # image = request.form[]
    questions = connection.read_file('question.csv')
    data_to_save = {'id': id, 'submission_time': submission_time, 'view_number': view_number,
                    'vote_number': vote_number, 'title': title, 'message': message, "image": "image"}
    write_message(data_to_save)
    data = connection.read_file('question.csv')
