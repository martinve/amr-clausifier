import pprint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from server.models import Sentence
import settings as cnf
import penman
from logger import logger
import propbank.propbank_api as pb
import amr_clausifier as cl

engine = create_engine(f"sqlite:///cache/{cnf.dbfile}")

Session = sessionmaker()
Session.configure(bind=engine)
db = Session()





def debug_print(var, comment=False):
    if comment:
        print(comment)
    pprint.pprint(var)
    print("---")


def db_get_amr(snt_id):
    print("ID", id)
    sent = db.query(Sentence).get(id)
    return sent.parse_amr


def get_variable_map(g):
    vars = g.variables()
    av = cl.get_attribute_values(g)
    cv = cl.get_concept_values(g)

    print("Vars", vars)
    print("AV", av)
    print("CV", cv)

    mv = {}
    for k in cv.keys():
        if k not in vars:
            continue
        if k not in av.keys():
            mv[k] = cv[k]
        else:
            mv[k] = av[k]
    return mv


def get_wiki_list(g):
    wikiattr = g.attributes(role=':wiki')
    wikilst = {}
    for it in wikiattr:
        wikilst[it[0]] = it[2]
    return wikilst


def decompose_snt(amr):
    g = penman.decode(amr)

    # Get the propbank roles for relevant mappings
    # roles = cl.get_propbank_role_dict(g)
    # pprint.pprint(roles)

    debug_print(amr)

    cv = cl.get_concept_values(g)
    debug_print(cv, "Concept Values:")

    av = cl.get_attribute_values(g)
    debug_print(av, "Attribute Values:")

    mv = get_variable_map(g)
    debug_print(mv, "Concept-Attribute Value Map")

    # ce = cl.get_concept_edges(g, cv, av)
    # pprint.pprint(ce)
    # print("---")

    wl = get_wiki_list(g)
    if len(wl):
        print("WIKI:")
        pprint.pprint(wl)
    print("---")
    print("META:")
    pprint.pprint(g.metadata)

    meta = {
        "roles": cl.get_propbank_role_dict(g),
        "ner": {}
    }


    return meta



if __name__ == "__main__":

    amrstr0 = """
# ::snt Barack Obama was born in Hawaii.
(b / bear-02
   :ARG1 (p / person
            :wiki "Barack_Obama"
            :name Barack_Obama)
   :location (s / state
                :wiki "Hawaii"
                :name Hawaii)) 


    """

    amrstr1 = """
    # ::snt Man saw Jaguar on a highway .
    (s / see-01
      :ARG0 (m / man)
      :ARG1 (c / car-make
            :wiki "Jaguar_Cars"
            :name (n / name
                  :op1 "Jaguar"))
      :location (h / highway))
    """

    amrstr2 = """
    (b / bear-02
     :ARG1 (p / poet
          :wiki "William_Shakespeare"
          :name (n / name
               :op1 "William"
               :op2 "Shakespeare"))
     :location (c / city
          :wiki "Stratford-upon-Avon"
          :name (n2 / name
               :op1 "Stratford-upon-Avon")))
   """

    amrstr = """
    # ::snt John eats soup with  a spoon and sausage with knife and fork.
    (e / eat-01
      :ARG0 (p / person
            :name (n / name
                  :op1 "John"))
      :ARG1 (a / and
            :op1 (s / soup)
            :op2 (s2 / sausage))
      :instrument (s3 / spoon)
      :instrument (a2 / and
            :op1 (k / knife)
            :op2 (f / fork)))"""

    amrstr = """
    # ::snt The colors for flag of Estonia are blue, black and white.
(c / color
   :domain (a / and
              :op1 (b / blue)
              :op2 (b2 / black-04)
              :op3 (w / white))
   :purpose (f / flag
               :poss (c2 / country
                         :wiki "Estonia"
                         :name Estonia))) 


    """

    amrstr = """
    # ::snt Titanic sank in the Atlantic in 1912.
(s / sink-01
   :ARG1 (s2 / ship
             :wiki "RMS_Titanic"
             :name Titanic)
   :location (o / ocean
                :wiki "Atlantic_Ocean"
                :name Atlantic)
   :time (d / date-entity
            :year 1912)) 

"""

    amrstr = amrstr1
    extracted = decompose_snt(amrstr)

    print("EXTRACTED:")
    pprint.pprint(extracted)