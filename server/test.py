#!/usr/bin/env python3

import flask
from flask import request
from os import mkdir, chdir, listdir
import re
import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True

re_id=re.compile("^[a-z0-9]{1-10}$")
re_jpeg=re.compile("^[0-9]{1-20}.jpg")

def gotodir(path="/tmp/uploads"):
    try:
        mkdir(path)
    except Exception:
        print(f"Path {path} already exists, that's fine")
    chdir(path)

gotodir()


@app.route('/join', methods=['GET'])
def join():
    if "id" in request.args:
        client_id=request.args["id"]
        if re_id.match(client_id):
            try:
                mkdir(client_id)
            except Exception:
                print(f"Problems creating directory {client_id}")
    return int(datetime.datetime.timestamp(datetime.datetime.now()))

@app.route('/lastfile', methods=['GET'])
def lastfile():
    if "id" in request.args:
        client_id=request.args["id"]
        if re_id.match(client_id):
            files=sorted(listdir(client_id))
            if files:
                return files[-1]
            else:
                return "0.jpg"
        return "miss"
    return "error"

@app.route('/put', methods=["POST"])
def put():
    if "id" in request.args:
        client_id=request.args["id"]
        if re_id.match(client_id):
            if "file" in request.files:
                f = request.files["file"]
                if re_jpeg.match(f.name):
                    f.save(f"{client_id}/{f.name}")

    

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()
