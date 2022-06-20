from flask import Flask, request, render_template, jsonify
import csv

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')

@app.rout("/list")
def question():
    _list = []
    with csv.open("/question.csv", "r", newline="") as file:
        read = file.readlines()
        header = read


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
