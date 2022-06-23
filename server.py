from flask import Flask, request, render_template, jsonify, redirect, url_for
from sample_data import data_manager, connection

import util

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/list")
def get_all_questions_sorted_by_submission_time():
    _list = data_manager.get_sorted_questions()
    return render_template('list.html', _list=_list)


@app.route("/question/<question_id>")
def get_question(question_id):
        question_with_answer = data_manager.get_quetion_and_answers(question_id)
        return render_template('display_question.html', data=question_with_answer)


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        id = data_manager.add_new_question()
        blink_url = "/question/" + str(id)
        # return render_template('display_question.html', data=data, title=title, id=id)
        return redirect(blink_url, 302)
    return render_template('ask_question.html')


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
