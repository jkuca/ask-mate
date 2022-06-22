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
    return render_template('display_question.html', question=question, question_id=question_id, answer=answer)


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        data_manager.add_new_question()
        # return render_template('display_question.html', data=data, title=title, id=id)
    return render_template('ask_question.html')


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
