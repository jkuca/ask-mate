from flask import Flask, request, redirect, render_template, jsonify
import csv
import util
import connection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/list")
def get_all_questions_sorted_by_submission_time():

    _list = []
    with open('sample_data/question.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            _list.append(row)

    def sorting(element):
        return element['submission_time']

    _list.sort(key=sorting)
    return jsonify({"list": _list})


@app.route('/question/<question_id>')
def display_question():

    header = ["Question Title", "Message"]
    answers = 'ok'

    return render_template('display_question.html', answers=answers, header=header)

@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        id = '3' #len listy +1?
        submission_time = util.get_time()
        # view_number = request.form[]
        # vote_number = request.form[]
        title = request.form['question_title']
        message = request.form['question']
        # image = request.form[]
        questions = connection.read_file('question') 
        data_to_save = [id,submission_time,"view_number","vote_number",title,message,"image"]

        connection.write_file(data_to_save, 'question.csv')
        data = connection.read_file('question')

        return render_template('list.html', data=data, title=title, id=id)
    return render_template('add_question.html')

if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )

