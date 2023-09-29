import pickle
from bottle import redirect
from models import Passage, Sentence
import os, sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import amrutil
import amr_clausifier
import logicconvert

#from settings.py in parent directory, import the file as alias cnf
import settings as cnf
from models import Base

engine = cnf.engine




def db_persist_parse(db, data):
    passage = data["passage"]
    p2 = passage

    exists = db.query(Passage).filter(Passage.passage == passage).first()
    if exists:
        # TODO: Add it to paassage
        redirect("/")  # Passage already exists

    exp = Passage()
    exp.passage = passage
    exp.rawdata = pickle.dumps(data)
    exp.context = ""

    for snt in data["sentences"]:
        text = snt["sentence"]
        parse_amr = snt["semparse"]["amr"]
        udraw = snt["semparse"]["ud"]
        parse_ud = pickle.dumps(udraw)

        try:
            logic = snt["logic"]["json"]
        except KeyError:
            logic = ""

        rawvalue = pickle.dumps(snt)
        parse_ud_raw = pickle.dumps(udraw)

        snt = Sentence()
        snt.text = text
        snt.parse_amr = parse_amr
        snt.parse_ud = parse_ud
        snt.parse_ud_raw = ""
        snt.context = ""
        snt.rawvalue = pickle.dumps(rawvalue)
        snt.logic = pickle.dumps(logic)

        exp.sentences.append(snt)

    db.add(exp)
    db.commit()

    return exp.id


def db_update_snt_logic(db, snt):
    sntobj = {
        "sentence": snt.text,
        "semparse": {
            "amr": snt.parse_amr,
            "ud": pickle.loads(snt.parse_ud)
        }
    }

    res = logicconvert.get_sentence_clauses(sntobj, 0, ud_shift=True, debug=False, json_ld_logic=False)
    if not res:
        return
    (logic, context) = res

    # simpl_logic = amrutil.get_simplified_logic(snt.parse_amr)

    simpl_logic = ""
    try:
        simpl_logic = amr_clausifier.extract_clauses(snt.parse_amr)
    except:
        siml_logic = "ERROR"

    snt.logic = pickle.dumps(logic)
    snt.context = pickle.dumps(context)
    snt.simpl_logic = pickle.dumps(simpl_logic)
    db.commit()

    return logic, simpl_logic, context


def recreate_data(db):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    for file in os.listdir(cnf.datadir):
        if file.endswith(".json"):
            with open(cnf.datadir + file) as f:
                data = json.loads(f.read())
                persist.db_persist_parse(db, data)

    redirect("/")

