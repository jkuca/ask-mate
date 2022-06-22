from flask import Flask, request, render_template, jsonify
from sample_data import data_manager, connection
import util

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/list")
def get_all_questions_sorted_by_submission_time():
    _list = data_manager.get_sorted_questions()
    return jsonify({"list": _list})


@app.route("/question/<question_id>", methods=['POST', 'GET'])
def get_question(question_id):
    question, answer = data_manager.get_answer_and_question(question_id)
    return render_template('question.html', question=question, question_id=question_id, answer=answer)


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        id = data_manager.generate_id()
        submission_time = util.get_time()
        view_number = 0
        vote_number = 0
        title = request.form['title']
        message = request.form['message']
        # image = request.form[]
        questions = connection.read_file('question.csv')
        data_to_save = {'id': id, 'submission_time': submission_time, 'view_number': view_number,
                        'vote_number': vote_number, 'title': title, 'message': message, "image": "image"}
        data_manager.write_message(data_to_save)
        data = connection.read_file('question.csv')

        return render_template('list.html', data=data, title=title, id=id)
    return render_template('ask_question.html')


@app.route('/question/<string:id>')
def get_guestion_by_id(id):
    data = data_manager.get_quetion_and_answers(id)

    return jsonify({id: data})


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
