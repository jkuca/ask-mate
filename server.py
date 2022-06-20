from flask import Flask, request, render_template, jsonify
import csv

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/list")
def question():
    _list = []
    with open('sample_data/question.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            _list.append(row)
    return jsonify({"lista" : _list})


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
