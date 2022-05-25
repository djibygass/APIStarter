from functools import wraps

from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f38675ce86190d1196a15861c4d85e2f'


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        if token != app.config['SECRET_KEY']:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)

    return decorator


@app.route("/")
def hello_world():
    return "<p>Hello, world !</p>"


@app.route("/health", methods=["GET", "POST"])
def health():
    return "200"


@app.route("/e", methods=["GET", "POST"])
@token_required
def hello_esgi():
    return "<p>Hello, ESGI !</p>"


if __name__ == "main":
    app.run()
