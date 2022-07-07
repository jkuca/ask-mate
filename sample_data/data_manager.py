import database_common as database_common
from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@database_common.connection_handler
def get_sorted_questions(cursor, parameter, value_parameter):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {parameter} {value_parameter}"""
    cursor.execute(query)
    return cursor.fetchall()
    # questions = connection.read_file("question.csv")
    # questions.sort(key=sorting)
    # return questions


@database_common.connection_handler
def get_sorted_comments(cursor, parameter, id:str):
    query = f"""
        SELECT *
        FROM comment
        WHERE {parameter} = '{id}'"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, id):
<<<<<<< HEAD
    query = f"""
            SELECT *
            FROM question
            WHERE id = {id}"""
    cursor.execute(query)
    return cursor.fetchall()
=======
    print(id)
    query = """
            SELECT *
            FROM question
            WHERE id = %(id)s"""
    cursor.execute(query, {"id": id})
    return cursor.fetchone()
>>>>>>> adam


@database_common.connection_handler
def get_answer_by_id(cursor, id):
    query = f"""
                SELECT *
                FROM answer
                WHERE question_id = {id}
                """
    cursor.execute(query)
    return cursor.fetchall()


<<<<<<< HEAD
def write_message_update(row):
    connection.update_file(row, "question.csv")


def get_edit_question(id_post, title, message):
    data_of_question = get_question_by_id(id_post)
    data_to_save = {'id': data_of_question['id'], 'submission_time': data_of_question['submission_time'], 'view_number': data_of_question['view_number'],
                    'vote_number': data_of_question['vote_number'], 'title': title, 'message': message, "image": ""}
    write_message_update(data_to_save)
=======
@database_common.connection_handler
def get_edit_question_message(cursor, id_post, message):
    query = f"""
                    UPDATE question
                    SET message = %(message)s                    
                    WHERE id = %(id)s
                    """
    cursor.execute(query, {"id": id_post, "message": message})
>>>>>>> adam


def generate_id(file):
    data = connection.read_file(file)
    generated_id = int(data[-1]['id'])+1
    return generated_id


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
    cursor.execute(query, {'time': submission_time,
                   'title': title, 'message': message})
    return cursor.fetchone()


@database_common.connection_handler
def add_new_comment(cursor, message, id_question = 'NULL', id_answer = 'NULL'):
    submission_time = util.get_time()
<<<<<<< HEAD


def add_new_answer(question_id, message):
    data_to_save = connection.get_row("answer.csv")
    data_to_save['id'] = generate_id("answer.csv")
    data_to_save['submission_time'] = util.get_time()
    data_to_save['message'] = message
    data_to_save['question_id'] = question_id

    write_new_row(data_to_save, "answer.csv")
=======
    query = f"""
                    INSERT INTO comment
                    VALUES (DEFAULT, {id_question}, {id_answer}, %(message)s, '{submission_time}', 0)
                    """
    cursor.execute(query, {'message': message})
>>>>>>> adam


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
