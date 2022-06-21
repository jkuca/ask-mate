from sample_data import connection


def get_sorted_questions():

    _list = connection.read_file("question.csv")

    def sorting(element):
        return element['submission_time']

    _list.sort(key=sorting)
    return _list
