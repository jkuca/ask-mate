import database_common as database_common
from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import util


@database_common.connection_handler
def get_sorted_questions(cursor, parameter, value_parameter):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {parameter} {value_parameter}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_sorted_comments(cursor, parameter, id: str):
    query = f"""
        SELECT *
        FROM comment
        WHERE {parameter} = '{id}'"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, id):
    print(id)
    query = """
            SELECT *
            FROM question
            WHERE id = %(id)s"""
    cursor.execute(query, {"id": id})
    return cursor.fetchone()


@database_common.connection_handler
def get_answer_by_id(cursor, id):
    query = f"""
                SELECT *
                FROM answer
                WHERE question_id = {id}
                """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_edit_question_message(cursor, id_post, message):
    query = f"""
                    UPDATE question
                    SET message = %(message)s                    
                    WHERE id = %(id)s
                    """
    cursor.execute(query, {"id": id_post, "message": message})


def generate_id(file):
    pass


@database_common.connection_handler
def add_new_question(cursor, title, message):
    # question_id = generate_id()
    submission_time = util.get_time()
    query = """
                    INSERT INTO question
                    VALUES (DEFAULT, %(time)s, 0, 0, %(title)s, %(message)s, NULL)
                    RETURNING id;
                    """
    cursor.execute(query, {'time': submission_time,
                   'title': title, 'message': message})

    return cursor.fetchone()


@database_common.connection_handler
def add_new_comment(cursor, message, id_question='NULL', id_answer='NULL'):
    submission_time = util.get_time()
    query = f"""
                    INSERT INTO comment
                    VALUES (DEFAULT, {id_question}, {id_answer}, %(message)s, '{submission_time}', 0)
                    """
    cursor.execute(query, {'message': message})


def count_visits(id):
    pass


def delete_row(id, directory):
    pass


def get_votes(data_of_question):
    pass


def count_votes_up(id):
    pass


def count_votes_down(id):
    pass


@database_common.connection_handler
def search_questions(cursor, search_phrase):
    sql = '''select distinct question.id, question.title, question.message from question
            left join answer on answer.question_id = question.id
            WHERE question.message LIKE '%%%s%%' OR question.title LIKE '%%%s%%' OR answer.message LIKE '%%%s%%' 
            ORDER BY question.id;''' % (search_phrase, search_phrase, search_phrase)
    cursor.execute(sql)
    question_data = cursor.fetchall()
    return question_data


@database_common.connection_handler
def get_latest_questions(cursor, count):
    cursor.execute("""SELECT * FROM question
                      ORDER BY submission_time DESC
                      LIMIT %(count)s;""",
                   {'count': count})
    latest_questions = cursor.fetchall()
    return latest_questions


@database_common.connection_handler
def edit_answer(cursor, answer_id, edited_data):
    cursor.execute("""UPDATE answer
                      SET submission_time = %(submission_time)s, message = %(message)s,
                      #image = %(image)s
                      WHERE id=%(id)s;""",
                   {'submission_time': util.get_time(),
                    'message': edited_data['message'],
                    # 'image': edited_data['image'],
                    'id': answer_id})


@database_common.connection_handler
def delete_question_by_id(cursor, question_id):
    cursor.execute("""DELETE FROM comment
                      WHERE question_id=%(id)s;""",
                   {'id': question_id})
    cursor.execute("""SELECT id FROM answer
                      WHERE question_id=%(id)s;""",
                   {'id': question_id})
    answer_ids = cursor.fetchall()
    for answer_id in answer_ids:
        delete_answer_by_id(answer_id['id'])
    cursor.execute("""DELETE FROM question
                      WHERE id=%(id)s;""",
                   {'id': question_id})
