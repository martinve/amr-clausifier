import setup_path
import os, sys, json
import bottle
from bottle import run, request
import settings as cfg
import stanza

try:
    import amrlib
except:
    print("""Install the requirements by running 'pip install -r requirements.txt'""")
    sys.exit(0)

host_name = cfg.ud_server_host
server_port = cfg.ud_server_port
logfile = "/dev/null"

# ====== globals used during work ========

nlp = None  # at startup nlp is assigned the stanza pipeline

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
    doc = nlp(text)
    result = {
        "text": text,
        "parse": [doc.to_dict()],
        "model": None
    }

    return result



def setup_routing(myapp):
    myapp.route("/", ["GET", "POST"], index)
    myapp.route("/info", ["GET", "POST"], info)


setup_routing(app)

if __name__ == "__main__":
    if nlp is None:
        nlp = stanza.Pipeline(lang='en', processors='tokenize,ner,pos,lemma,depparse',
                                   download_method=stanza.DownloadMethod.REUSE_RESOURCES)
    run(host="localhost", port=server_port, app=app)
