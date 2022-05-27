import pytest
import requests
import pandas as pd
from flask import jsonify
from flask import request

def test_health():
    r = requests.get("http://127.0.0.1:5000/health")
    #assert r.status_code == 200


def test_column_stat():
    r = requests.get("http://127.0.0.1:5000/compute/stats")
    path = "/Users/Gassama/pper/APIStarter/stat.json"
    compare_list = calc_stat(path, ['age'])
    assert compare_list == r


def test_file_name():
    r = requests.get("http://127.0.0.1:5000/file")
    name = "/Users/Gassama/pper/APIStarter/stat.json"
    assert name == r.content

def test_column():
    r = request.get("http://127.0.0.1.5000/send_columns")
    cols = request.get_json()['cols']
    assert cols == r

def test_group_by():
    r = requests.get("http://127.0.0.1:5000/compute/groupby")
    print(r)
    path = "/Users/Gassama/pper/APIStarter/stat.json"
    assert path == r


def calc_stat(file, cols):
    last_list = []
    my_df = pd.read_json(file)
    for i in range(len(cols)):
        mean, variance, std = (
            my_df[cols[i]].mean(),
            my_df[cols[i]].var(),
            my_df[cols[i]].std(),
        )
        dic = {"mean": mean, "variance": variance, "ecart": std}
        last_list.append((cols[i], dic))
        return last_list


"""path = "/Users/Gassama/pper/APIStarter/stat.json"
listo = calc_stat(path, ["number", "age"])
print(listo)"""