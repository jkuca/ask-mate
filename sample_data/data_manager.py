import database_common as database_common
import util

################################################################################################
#QUESTIONS#


@database_common.connection_handler
def get_sorted_questions(cursor, parameter, value_parameter):
    cursor.execute(
        f'SELECT * FROM question ORDER BY {parameter} {value_parameter} ')
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute('SELECT * FROM public.question WHERE id = %s', (id))
    return cursor.fetchone()


@database_common.connection_handler
def get_latest_questions(cursor, count):
    cursor.execute(
        'SELECT * FROM question ORDER BY submission_time DESC LIMIT %s', (str(count)))
    return cursor.fetchall()


@database_common.connection_handler
def get_edit_question_message(cursor, id_post, message):
    cursor.execute(
        'UPDATE question SET message = %s WHERE id = %s', (message, id_post))


@database_common.connection_handler
def get_edit_question_title(cursor, id_post, title):
    cursor.execute(
        'UPDATE question SET title = %s WHERE id = %s ', (title, id_post))


@database_common.connection_handler
def add_new_question(cursor, title, message, user_id):
    cursor.execute('INSERT INTO question VALUES (DEFAULT, %s, 0, 0, %s, %s, NULL, %s) RETURNING id;',
                   (util.get_time(), title, message, user_id))
    return cursor.fetchone()


@database_common.connection_handler
def search_questions(cursor, search_phrase):
    sql = '''SELECT DISTINCT question.id, question.title, question.message FROM question
            LEFT JOIN answer on answer.question_id = question.id
            WHERE question.message LIKE '%%%s%%' OR question.title LIKE '%%%s%%' OR answer.message LIKE '%%%s%%'
            ORDER BY question.id;''' % (search_phrase, search_phrase, search_phrase)
    cursor.execute(sql)
    question_data = cursor.fetchall()
    return question_data


@database_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute('DELETE FROM question WHERE id= %s', (question_id))

################################################################################################
    #ANSWERS#


@ database_common.connection_handler
def get_answer_by_id(cursor, id):
    cursor.execute('SELECT * FROM answer WHERE question_id= %s', (id))
    return cursor.fetchall()


@ database_common.connection_handler
def get_one_answer_by_id(cursor, id):
    cursor.execute('SELECT * FROM answer WHERE id = %s', (id))
    return cursor.fetchone()


@database_common.connection_handler
def add_new_answer(cursor, message, id_question, user_id):
    cursor.execute(
        'INSERT INTO answer VALUES (DEFAULT, %s, 0 , %s, %s, NULL, %s, 0)',
        (util.get_time(), id_question, message, user_id))


@ database_common.connection_handler
def edit_answer(cursor, answer_id, edited_data):
    cursor.execute('UPDATE answer SET submission_time = %s, message = %s WHERE id=%s',
                   (util.get_time(), edited_data, answer_id))


@ database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute(
        'DELETE FROM comment WHERE comment.answer_id = %s', (answer_id))

################################################################################################
    #COMENTS#


@ database_common.connection_handler
def get_comment_by_id(cursor, id):
    cursor.execute('SELECT * FROM comment WHERE id= %s', (id))
    return cursor.fetchall()


@ database_common.connection_handler
def get_sorted_comments(cursor, parameter, id: str):
    cursor.execute('SELECT * FROM comment WHERE %s = %s', (parameter, id))
    return cursor.fetchall()


@ database_common.connection_handler
def add_new_comment(cursor, message, user_id, id_question=None, id_answer=None):
    cursor.execute(
        'INSERT INTO comment VALUES (DEFAULT, %s, %s , %s , %s, 0, %s)', (id_question, id_answer, message, util.get_time(), user_id))


@ database_common.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute('DELETE FROM comment WHERE comment.id = %s', (comment_id))

################################################################################################
    #COUNTS#


@ database_common.connection_handler
def count_visits(cursor, id, view_number):
    cursor.execute(
        'UPDATE question SET view_number= %s WHERE id= %s', ((view_number + 1), id))


@ database_common.connection_handler
def count_votes_up(cursor, id, vote_number):
    cursor.execute(
        'UPDATE question SET vote_number = %s WHERE id= %s', ((vote_number + 1), id))


@ database_common.connection_handler
def count_votes_down(cursor, id, vote_number):
    cursor.execute(
        'UPDATE question SET vote_number = %s WHERE id= %s', (vote_number - 1, id))


@ database_common.connection_handler
def count_votes_answer_up(cursor, id, vote_number):
    cursor.execute(
        'UPDATE answer SET vote_number = %s WHERE id= %s', (vote_number + 1, id))


@ database_common.connection_handler
def count_votes_answer_down(cursor, id, vote_number):
    cursor.execute(
        'UPDATE answer SET vote_number = %s WHERE id= %s', (vote_number - 1, id))


@ database_common.connection_handler
def getUsersInfo(cursor):
    cursor.execute('SELECT username FROM accounts')
    return cursor.fetchall()


@ database_common.connection_handler
def getUser(cursor, username, password):
    cursor.execute(
        'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
    return cursor.fetchone()


@ database_common.connection_handler
def getUserByUsername(cursor, username):
    print(username)
    cursor.execute(
        "SELECT * FROM accounts WHERE username= '{0}'".format(username))
    acount = cursor.fetchone()
    return acount


@ database_common.connection_handler
def addUser(cursor, username, password, email):
    cursor.execute('INSERT INTO accounts VALUES (DEFAULT, %s, %s, %s, %s )',
                   (username, password, email, util.get_time()))


@database_common.connection_handler
def getUserById(cursor, id):
    cursor.execute(
        'SELECT username, email, submission_time, reputation FROM accounts WHERE id = %s', (id))
    return cursor.fetchone()


@database_common.connection_handler
def updateUserData(cursos, id, email):
    pass

@database_common.connection_handler
def countUsersAskedQuestionsById(cursor, id):
    cursor.execute(
        'SELECT COUNT(*) FROM question WHERE user_id = %s', (id))
    result = cursor.fetchone()
    return result['count']

@database_common.connection_handler
def countUsersAnswersById(cursor, id):
    cursor.execute(
        'SELECT COUNT(*) FROM answer WHERE user_id = %s', (id))
    result = cursor.fetchone()
    return result['count']

@database_common.connection_handler
def countUsersCommentsById(cursor, id):
    cursor.execute(
        'SELECT COUNT(*) FROM comment WHERE user_id = %s', (id))
    result = cursor.fetchone()
    return result['count']