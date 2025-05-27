import sys

from logger import logger
from classifier.sentence_heuristic_classifier import snt_type_label


def simplify(clauses, snt_type):
    # logger.info(f"Simpl: len(initial): {len(clauses)}, snt_type={snt_type_label(snt_type)}")

    # TODO: Implemenet clause simplifier

    logger.warning("TODO: Implement simplifier.simplify()")

    var_dict = {}
    try:
        for cl in clauses:
            # logger.info(f"Clause: {cl}")
            if len(cl) == 2 and isinstance(cl[0], str) and isinstance(cl[1], str):
                var_dict[cl[0]] = cl[1]
            if cl[1] in ["and", "or"]:
                cl[2] = find_one(clauses, "conn:" + cl[1])[1:][0]
                cl[1] = "$" + cl[1]
        return clauses
    except TypeError:
        return []


def find(clause_list, idx0=False, idx1=False, idx2=False):
    matches = []
    for it in clause_list:
        if idx0 and it[0] == idx0:
            matches.append(it)
            clause_list.remove(it)
        if idx1 and it[1] == idx1:
            matches.append(it)
            clause_list.remove(it)
        if idx2 and it[2] == idx2:
            matches.append(it)
            clause_list.remove(it)
    return matches


def find_one(clause_list, idx0=False, idx1=False, idx2=False):
    try:
        return find(clause_list, idx0, idx1, idx2)[0]
    except IndexError:
        pass

    # logger.info(f"Variables: {var_dict}")