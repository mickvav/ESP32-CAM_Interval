#!/usr/bin/env python3

import flask
from flask import request
from os import mkdir, chdir, listdir, environ
import re
import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True

re_id = re.compile("^[a-z0-9]{1,10}$")
re_jpeg = re.compile("^[0-9]{1,20}.jpg")

uploads_path = "/tmp/uploads"
app.config["UPLOADS_PATH"] = uploads_path


@app.route("/join", methods=["GET"])
def join():
    if "id" in request.args:
        client_id = request.args["id"]
        if re_id.match(client_id):
            try:
                mkdir(f"{uploads_path}/{client_id}")
                return str(int(datetime.datetime.timestamp(datetime.datetime.now())))
            except Exception:
                return f"Problems: {client_id}"
    return "problems"


@app.route("/lastfile", methods=["GET"])
def lastfile():
    if "id" in request.args:
        client_id = request.args["id"]
        if re_id.match(client_id):
            files = sorted(listdir(f"{uploads_path}/{client_id}"))
            if files:
                return files[-1]
            else:
                return "0.jpg"
        return "miss"
    return "error"


@app.route("/put", methods=["POST"])
def put():
    if "id" in request.form:
        client_id = request.form["id"]
        if re_id.match(client_id):
            if "file" in request.files:
                f = request.files["file"]
                if re_jpeg.match(f.filename):
                    f.save(f"{uploads_path}/{client_id}/{f.filename}")
                    return "done"
                return f"bad_name:{f.filename}"
            return "no_file"
        return "bad_id"
    return "no_id"


@app.route("/", methods=["GET"])
def home():
    return "nothing here"


if __name__ == "__main__":
    try:
        mkdir(uploads_path)
    except Exception:
        print(f"Path {uploads_path} already exists, that's fine")
    if "HOST" in environ:
        app.run(host=environ["HOST"])
    else:
        app.run()
