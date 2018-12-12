# -*- coding: utf-8 -*-

from flask import Flask, request
import sqlite3
from gevent.wsgi import WSGIServer
import json
from pysearch import settings
from flask import abort


app = Flask(__name__)
db = sqlite3.connect(settings.db, check_same_thread=False)


@app.route('/')
def index():
    return """
    WELCOME TO SEARCH API v1.0\n\n
    current archive: {}
    current db: {}\n
    enter search mask with / as delimiter
    sets intersect and values are searching by default\n
    to union use flag "d" as param argument
    to search keys use flag "key" as search argument\n\n
    Respectfully yours,
    "TRAMS DRIFT" inc. - 2018
    """.format(settings.path, settings.db)


@app.route("/<path:varargs>/")
def multiple(varargs=None):
    multiple_search = varargs.split("/")
    words_h = {w.lower(): set() for w in multiple_search}

    f_db = ','.join("?" * len(words_h))
    tables = "keys_idx" if request.args["search"] == "key" else "values_idx"
    words = db.execute('select * from {} where value in ({})'.format(tables, f_db), tuple(words_h.keys())).fetchall()
    for word, files_str in words:
        files = set(map(int, files_str.split(',')))
        words_h[word] = files
    list_of_sets = list(words_h.values())
    res = set.union(*list_of_sets) if request.args["param"] == 'd' else set.intersection(*list_of_sets)
    if res:
        files = db.execute('select path from files where id in (' + ','.join(['?'] * len(res)) + ')',
                           list(res)).fetchall()
        list_of_files = list(map(lambda t: t[0], files))
        total = len(list_of_files)
        search_request = tuple(words_h.keys())
        body_dict = {'total matches': total, 'files': list_of_files, 'search_request': search_request}
        return json.dumps(body_dict)
    else:
        abort(404)


def run_server():
    http_server = WSGIServer(('', settings.port), app)
    http_server.serve_forever()
