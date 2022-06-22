from flask import Flask, request, render_template, jsonify
from sample_data import data_manager

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/list")
def get_all_questions_sorted_by_submission_time():
    _list = data_manager.get_sorted_questions()
    return jsonify({"questions": _list})


@app.route('/question/<string:id>')
def get_guestion_by_id(id):
    data = data_manager.get_quetion_and_answers(id)
    return jsonify({id: data})


@app.route("/question/<string:id_post>/edit", methods=["POST", "GET"])
def edit_question(id_post):

    if request.form.get("message"):
        new_message = request.form.get("message")

        data = data_manager.get_message_the_right_question(
            id_post, new_message)
        print(data)
        return jsonify({new_message: data})
    return render_template("edit.html")

if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
