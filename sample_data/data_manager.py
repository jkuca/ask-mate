from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common
from typing import List, Dict
import util

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
#https://www.postgresqltutorial.com/wp-content/uploads/2018/03/PostgreSQL-Cheat-Sheet.pdf



@database_common.connection_handler
def get_sorted_questions(cursor, parameter, value_parameter):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {parameter} {value_parameter}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_sorted_comments(cursor, parameter, id:str):
    query = f"""
        SELECT *
        FROM comments
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
                WHERE question_id = %(id)s
                """
    cursor.execute(query, {"id": id})
    return cursor.fetchall()


def write_message_update(row):
    connection.update_file(row, "question.csv")


@database_common.connection_handler
def get_edit_question_message(cursor, id_post, message):
    query = f"""
                    UPDATE question
                    SET message = %(message)s                    
                    WHERE id = %(id)s
                    """
    cursor.execute(query, {"id": id_post, "message": message})


@database_common.connection_handler
def get_edit_question_title(cursor, id_post, title):
    query = """
                    UPDATE question
                    SET title = %(title)s                  
                    WHERE id = %(id)s
                    """
    cursor.execute(query, {"id": id_post, "title": title})


@database_common.connection_handler
def generate_id(cursor):
    query = """
                Select count(*)
                FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


def write_new_row(row, directory):
    connection.add_new_row(row, directory)


@database_common.connection_handler
def add_new_question(cursor, title, message):
    # question_id = generate_id()
    submission_time = util.get_time()
    query = """
                    INSERT INTO question
                    VALUES (DEFAULT, %(time)s, 0, 0, %(title)s, %(message)s, NULL);
                    SELECT ID
                    FROM question;
                    """
    cursor.execute(query, {'time': submission_time, 'title': title, 'message': message})
    return cursor.fetchall()

@database_common.connection_handler
def add_new_comment(cursor, message, id_question = 'NULL', id_answer = 'NULL'):
    submission_time = util.get_time()
    query = f"""
                    INSERT INTO comment
                    VALUES (DEFAULT, {id_question}, {id_answer}, %(message)s, '{submission_time}', 0)
                    """
    cursor.execute(query, {'message': message})


def add_new_answer(question_id, message):
    data_to_save = connection.get_row("answer.csv")
    data_to_save['id'] = generate_id("answer.csv")
    data_to_save['submission_time'] = util.get_time()
    data_to_save['message'] = message
    data_to_save['question_id'] = question_id





def count_visits(id):
    data_of_question = get_question_by_id(id)
    data_of_question.view_number = int(data_of_question.view_number) + 1
    write_message_update(data_of_question)


def delete_row(id, name_table):
    query = f"""
                        DELETE FROM {name_table}                 
                        WHERE id = %(id)s
                        """
    cursor.execute(query, {"id": id})


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
