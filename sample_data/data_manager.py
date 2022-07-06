from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
#https://www.postgresqltutorial.com/wp-content/uploads/2018/03/PostgreSQL-Cheat-Sheet.pdf
import database_common


@database_common.connection_handler
def get_sorted_questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC"""
    cursor.execute(query)
    return cursor.fetchall()
    # questions = connection.read_file("question.csv")
    # questions.sort(key=sorting)
    # return questions


<<<<<<< HEAD
=======
@database_common.connection_handler
>>>>>>> 360f07a19225cb2b51355ae0b1f3e604f676c105
def get_question_by_id(id):
    query = """
            SELECT *
            FROM question
            WHERE id = {id}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_id(id):
    query = """
                SELECT *
                FROM answer
                WHERE question_id = {id}
                """
    cursor.execute(query)
    return cursor.fetchall()


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
