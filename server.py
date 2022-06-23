from flask import Flask, request, render_template, jsonify, redirect
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
        url = "/question/" + str(id)
        # return render_template('display_question.html', data=data, title=title, id=id)
        return redirect(url, 302)
    return render_template('ask_question.html')


@app.route("/question/<string:id_post>/edit", methods=["POST", "GET"])
def edit_question(id_post):
    url = f"/question/{id_post}"
    if request.form == "POST":
        data_manager.get_edit_question(id_post)
        return redirect(url)
    else:
        data_of_question = data_manager.get_question_by_id(id_post)
    return render_template("edit.html", data = data_of_question)


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
