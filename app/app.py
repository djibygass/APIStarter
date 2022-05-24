import flask
from flask import Flask

app = Flask(__name__)
headers = flask.request.headers
bearer = headers.get('Authorization')  # Bearer YourTokenHere
token = bearer.split()[1]  # YourTokenHere


@app.route("/")
def hello_world():
    return "<p>Hello, world !</p>"


@app.route("/health", methods=["GET", "POST"])
def health():
    return "200"


@app.route("/e", methods=["GET", "POST"])
def hello_esgi():
    return "<p>Hello, ESGI !</p>"


if __name__ == "main":
    app.run()
