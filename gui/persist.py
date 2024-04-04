import pickle
from bottle import redirect
from models import Passage, Sentence, Base
import os, sys, json

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import settings as cnf
import amr_clausifier
import logicconvert

#from settings.py in parent directory, import the file as alias cnf
# import settings as cnf
# from models import Base
# engine = cnf.engine




def db_persist_parse(db, data, update=False):

    print(data)

    passage = data["passage"]

    if update:
        psg = db.query(Passage).get(data["id"])
    else:
        psg = Passage()

    # if "id" in data.keys():
    #    psg.id = data["id"]

    psg.passage = passage
    psg.filename = data["filename"]
    psg.rawdata = pickle.dumps(data)
    psg.context = ""

    for snt in data["sentences"]:
        text = snt["sentence"]
        parse_amr = snt["semparse"]["amr"]
        udraw = snt["semparse"]["ud"][0]

        parse_ud = pickle.dumps(udraw)

        try:
            logic = snt["logic"]["json"]
        except KeyError:
            logic = ""

        rawvalue = pickle.dumps(snt)

        snt = Sentence()
        if update:
            res = db.query(Sentence).where(Sentence.passage_id == psg.id).where(Sentence.text == text).first()
            if res:
                snt = res

        snt.text = text
        snt.parse_amr = parse_amr
        snt.parse_ud = parse_ud
        snt.parse_ud_raw = ""
        snt.context = ""
        snt.rawvalue = pickle.dumps(rawvalue)
        snt.logic = pickle.dumps(logic)
        snt.modelname = ""

        psg.sentences.append(snt)

    db.add(psg)
    db.commit()

    return psg.id


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

    engine = cnf.engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    for file in os.listdir(cnf.datadir):
        if file.endswith(".json"):
            with open(cnf.datadir + file) as f:
                data = json.loads(f.read())
                data["filename"] = file
                db_persist_parse(db, data)

    redirect("/")


def clear_data(db):

    engine = cnf.engine

    Base.metadata.drop_all(engine)

    for file in os.listdir(cnf.datadir):
        if not file.endswith(".json"):
            continue
        os.remove(cnf.datadir + "/" + file)

    redirect("/")