from bottle import template, request, redirect
from models import Passage
import parser as p
import settings as cnf
import controller_passage as psg
import persist, uuid, json


def index(db):
    return template("parse")


def update(db):
    passage_id = request.forms.get("passage_id")
    passage = request.forms.get("passage")

    if not passage:
        redirect("/")

    do_update = False
    if passage_id:
        passageobj = db.query(Passage).get(passage_id)
        do_update = True
        passage = passageobj.passage + " " + passage
        print("Exists")

    parser = p.Parser()
    parse_json = parser.parse_passage(passage)
    # TODO: Save to passage

    fname = passage.split()[0].lower() + "-" + str(uuid.uuid4()) + ".json"
    with open(cnf.datadir + fname, 'w') as f:
        json.dump(parse_json, f, indent=2)

    parse_json["filename"] = fname
    parse_json["id"] = passage_id

    last_id = persist.db_persist_parse(db, parse_json, do_update)

    redirect(f"/passage/{last_id}")
