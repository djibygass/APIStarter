from functools import wraps
from os import path


import flask
import pandas as pd

from flask import Flask, request, jsonify

app = Flask(__name__)


def verify(json_from_postman_body):
    #verify the colums and the file
    if not path.exists(json_from_postman_body["file"]):
        return 1
    my_df = pd.read_json(json_from_postman_body["file"])
    for col1 in json_from_postman_body["cols"]:
        if col1 not in my_df.columns:
            return 2


app.config["SECRET_KEY"] = "f38675ce86190d1196a15861c4d85e2f"


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        #check the token
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]
        if not token:
            return jsonify({"message": "a valid token is missing"})
        if token != app.config["SECRET_KEY"]:
            return jsonify({"message": "token is invalid"})

        return func(*args, **kwargs)

    return decorator


@app.route("/health", methods=["GET"])
@token_required
def health():
    #check the availabality of the flask server
    return flask.Response(status=200)


@app.route("/send_columns", methods=["POST"])
@token_required
def column_names():
    #return the column's nam
    my_list = []
    for col in request.get_json():
        if col == "cols":
            my_list = request.get_json()[col]
            print(" ".join(my_list))
    return " ".join(my_list)


@app.route("/file", methods=["POST"])
@token_required
def file_name():
    #return the file name from the request body
    my_file = ""
    for name in request.get_json():
        if name == "file":
            my_file = request.get_json()[name]
    return my_file


@app.route("/compute/groupby", methods=["POST"])
@token_required
def group_by():
    #groups dataframe's result based on the request body's column
    my_file = file_name()
    my_list = column_names().split()
    if verify(request.get_json()) == 1:
        return "please enter a valid path"
    if verify(request.get_json()) == 2:
        return "columns are not correct"
    my_df = pd.read_json(my_file)

    my_df = my_df.groupby(my_list).agg(list)
    my_df = my_df.to_json()
    with open(my_file, "w") as file:
        file.write(my_df)

    return my_file


@app.route("/compute/nonnull", methods = ['POST'])
def non_null():
    # delete empty dataframe's rows based on the request body's column
    my_file = file_name()
    cols = column_names()
    df = pd.read_json(my_file)
    df = df.dropna(subset = cols)
    df = df.to_json()
    return df


@app.route("/compute/stats", methods=["POST"])
@token_required
def stats():
    #calculates the means, variances and std deviations
    last_list = []
    my_file = file_name()
    my_list = column_names().split()
    dic = {"file": my_file, "cols": my_list}
    if verify(dic) == 1:
        return "please enter a valid path"
    if verify(dic) == 2:
        return "columns are not correct"
    my_df = pd.read_json(my_file)
    for i in range(len(my_list)):
        mean, variance, std = (
            my_df[my_list[i]].mean(),
            my_df[my_list[i]].var(),
            my_df[my_list[i]].std(),
        )
        dic = {"mean": mean, "variance": variance, "ecart": std}
        last_list.append((my_list[i], dic))
    return jsonify(last_list)


if __name__ == "__main__":
    app.run()
