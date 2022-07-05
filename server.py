from flask import Flask, request, render_template, jsonify, redirect
from sample_data import data_manager

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/list")
def get_all_questions_sorted_by_submission_time():
    questions = data_manager.get_sorted_questions()
    print(questions)
    return render_template('list.html', questions=questions)


@app.route("/question/<question_id>")
def get_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answer_by_id(question_id)
    # data_manager.count_visits(question_id)
    return render_template('display_question.html', data=question[0], answers=answers)


@app.route("/question/<string:id_post>/new-answer", methods=['POST', 'GET'])
def add_answer(id_post):
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.add_new_answer(id_post, message)
        blink_url = "/question/" + str(id_post)
        return redirect(blink_url, 302)
    return render_template('add_answer.html', data=id_post)


@app.route("/question/<string:id_post>/edit", methods=["POST", "GET"])
def edit_question(id_post):
    url = "/question/" + str(id_post)
    if request.method == "POST":
        message = request.form.get("message")
        title = request.form.get('title')
        data_manager.get_edit_question_message(id_post, message)
        if len(title) > 0:
            data_manager.get_edit_question_title(id_post, title)
        return redirect(url)

    else:
        count = data_manager.generate_id()
        data_of_question = data_manager.get_question_by_id(id_post)
        counts = data_manager.generate_id()
        print(type(count[0]['count']))
        id = count[0]['count']

    return render_template("edit.html", data=data_of_question[0], count=count[0])


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        id = data_manager.add_new_question(title, message)
        blink_url = "/question/" + str(id)
        return redirect(blink_url, 302)
    return render_template('ask_question.html')


@app.route("/question/<string:id_post>/delete")
def delete_question(id_post):
    data_manager.delete_row(id_post, 'question')
    return redirect('/list')


@app.route("/question/<string:id_post>/vote-up")
def vote_question_up(id_post):
    data_manager.count_votes_up(id_post)
    blink_url = "/question/" + str(id_post)
    return redirect(blink_url, 302)


@app.route("/question/<string:id_post>/vote-down")
def vote_question_down(id_post):
    data_manager.count_votes_down(id_post)
    blink_url = "/question/" + str(id_post)
    return redirect(blink_url, 302)


@app.route("/answer/<string:id_answer>/delete")
def delete_answer(id_answer):
    data_manager.delete_row(id_answer, 'answer.csv')
    return redirect('/list')


@app.route("/answer/<answer_id>/vote-up")
def vote_answer_up():
    pass


@app.route("/answer/<answer_id>/vote-down")
def vote_answer_down():
    pass


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
