from bottle import template, redirect
from models import Passage
import persist
import pickle

def index(db):
    rows = db.query(Passage).order_by(Passage.id.desc()).all()
    return template("index", rows=rows)


def get_passage(id, db):
    passage = db.query(Passage).get(id)
    return template("passage_details", passage=passage)


def add_sent_to_passage(id, db):
    passage = db.query(Passage).get(id)
    return template("parse", passage=passage)


def test_logic(db):
    experiments = db.query(Passage).order_by(Passage.id.desc()).all()
    for exp in experiments:
        for snt in exp.sentences:
            print(snt.text, snt.logic)
            if snt.logic == pickle.dumps(""):
                persist.db_update_snt_logic(db, snt)
    return "Done."


def delete(db, id):
    msg = f"Delete passage {id}"

    x = db.query(Passage).get(id)
    db.delete(x)

    return redirect("/")
