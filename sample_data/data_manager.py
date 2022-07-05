from sample_data import connection
import util


def sorting(element):
    return element['submission_time']


def get_sorted_questions():

    questions = connection.read_file("question.csv")
    questions.sort(key=sorting)
    return questions


def get_question_by_id(id):
    question = connection.read_file("question.csv")
    for item in question:
        if item['id'] == id:
            return item


def get_answer_by_id(id):
    answer = connection.read_file("answer.csv")
    for item in answer:
        if item['id'] == id:
            return item


def get_quetion_and_answers(id):
    question = get_question_by_id(id)
    list_of_answers = []
    answers = connection.read_file('answer.csv')
    for answer in answers:
        if answer["question_id"] == id:
            list_of_answers.append(answer)
    return question, list_of_answers


def write_message_update(row):
    connection.update_file(row, "question.csv")


def get_edit_question(id_post, title, message):
    data_of_question = get_question_by_id(id_post)
    data_to_save = {'id': data_of_question['id'], 'submission_time': data_of_question['submission_time'], 'view_number': data_of_question['view_number'],
                    'vote_number': data_of_question['vote_number'], 'title': title, 'message': message, "image": ""}
    write_message_update(data_to_save)


def generate_id(file):
    data = connection.read_file(file)
    generated_id = int(data[-1]['id'])+1
    return generated_id


def write_new_row(row, directory):
    connection.add_new_row(row, directory)


def add_new_question(title, message):
    data_to_save = connection.get_row("question.csv")
    data_to_save['id'] = generate_id("question.csv")
    data_to_save['submission_time'] = util.get_time()
    data_to_save['title'] = title
    data_to_save['message'] = message
    write_new_row(data_to_save, "question.csv")
    return data_to_save['id']


def add_new_answer(question_id, message):
    data_to_save = connection.get_row("answer.csv")
    data_to_save['id'] = generate_id("answer.csv")
    data_to_save['submission_time'] = util.get_time()
    data_to_save['message'] = message
    data_to_save['question_id'] = question_id

    write_new_row(data_to_save, "answer.csv")


def count_visits(id):
    data_of_question = get_question_by_id(id)
    data_of_question['view_number'] = int(data_of_question['view_number']) + 1
    write_message_update(data_of_question)


def delete_row(id, directory):
    connection.delete_row({'id': id}, directory)


def get_votes(data_of_question):
    return int(data_of_question['vote_number'])


def count_votes_up(id):
    data_of_question = get_question_by_id(id)
    data_of_question['vote_number'] = get_votes(data_of_question) + 1
    write_message_update(data_of_question)


def count_votes_down(id):
    data_of_question = get_question_by_id(id)
    data_of_question['vote_number'] = get_votes(data_of_question) - 1
    write_message_update(data_of_question)
