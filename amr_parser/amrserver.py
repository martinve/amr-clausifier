#!/usr/bin/env python3

import os, sys, json
import bottle
from bottle import run, request

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import settings as cfg

try:
    import amrlib
except:
    print("""Install the requirements by running 'pip install -r requirements.txt'""")
    sys.exit(0)

host_name = cfg.amr_server_host
server_port = cfg.amr_server_port
logfile = "/dev/null"

# ====== globals used during work ========

stog = None  # at startup nlp is assigned the stanza pipeline

port = 9003
app = bottle.Bottle()

count = 0


# === request processing ===

def index():
    if request.forms.get("text"):
        text = request.forms.get("text")
    else:
        text = request.query.get("text", "")
    result = []
    if text:
        result = parse_text(text)
    return json.dumps(result)


def info():
    data = {
        "model": cfg.model
    }
    return json.dumps(data)


# ====== starting ======

def parse_text(text):
    global stog
    g = stog.parse_sents([text])
    amr = g[0]
    result = {
        "text": text,
        "amr": amr,
    }

    return result


def setup_routing(myapp):
    myapp.route("/", ["GET", "POST"], index)
    myapp.route("/info", ["GET", "POST"], info)


setup_routing(app)

if __name__ == "__main__":
    if stog is None:
        stog = amrlib.load_stog_model(model_dir="models/model_stog/" + cfg.amr_parse_model)
    run(host="localhost", port=port, app=app)
