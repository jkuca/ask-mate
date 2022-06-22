from sample_data import connection


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
    pass

