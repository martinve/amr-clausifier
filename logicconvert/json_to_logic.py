import json
import pprint
import sys
import re

import amrutil
import config
import debugger
from logger import logger
from types_util import is_string, is_op, is_list, is_atom

logic_lst = []


def list_depth(lst):
    if isinstance(lst, list):
        return 1 + max(list_depth(item) for item in lst) if lst else 0
    else:
        return 0


"""
def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result
"""


def is_variable_assignment(cl):
    """
    Check the form [instance, var]
    :param cl:
    :return:
    """
    is_assignment = len(cl) == 2 and \
                    is_string(cl[0]) and \
                    is_string(cl[1]) and \
                    cl[0] not in [":polarity"]

    if not is_assignment:
        debugger.debug_print(f"Is_variable_assignment={is_assignment} {cl}")

    return is_assignment


def is_negative(cl):
    return len(cl) == 2 and cl[0] == ":polarity" and cl[1] == "-"


def is_polarity_modifier(cl):
    return is_negative(cl)


def add_clause(stmt, debug_msg):
    # pprint.pprint(f"Clauses (len:{len(logic_lst)})")
    logic_lst.append(stmt)
    if config.debug_graph_construction:
        if debug_msg:
            logger.error(f"add_clause: ({debug_msg}): {stmt}")
        else:
            logger.error(f"add_clause: {stmt}")


"""
def add_question(json_logic, question):
    if question:
        try:
            question = json.loads(question)
            json_logic.append({"@question": question})
        except:
            logger.error("Error: Invalid question")
            logger.error(question)
            sys.exit(-1)
    return json_logic
"""


def add_question_clauses(json_logic, question):
    ques = pprint.pformat(question, indent=2, compact=False)

    if not is_list(question):
        logger.error("Provided questions not a list.")
        logger.error(f"Ques: \n{ques}")
        sys.exit(-1)

    for idx, cl in enumerate(question):
        if "amr-unknown" == cl[1]:
            question.pop(idx)
            # pass

    logger.debug(f"Provided question: \n{ques}")
    json_logic.append({"@question": question})
    return json_logic


def simplify_operators(ops):
    newops = []
    for it in ops:
        if is_variable_assignment(it):
            newops.append(it[1])
        else:
            newops.append(it)
    return newops


def parse_edge(edge, parent, debug=True):
    amrutil.check_edge(edge, parent)

    if debug:
        logger.debug(f"IN_0 parent={parent} edge={edge}")

    value = edge[0:2]
    modifier = edge[2:]

    if debug:
        logger.debug(f"IN_1: val({list_depth(value)})={value}, modifier({list_depth(modifier)})={modifier}")

    # print(f"p={parent}, len={len(val)}, elen={len(edge)}, val={val}")
    # logger.debug(f"val={len(val)}, edge={len(edge)}")

    # variable assignment is in form [instance, var] e.g. [flag, f]
    if is_variable_assignment(edge):
        logger.debug(f"ISA: {edge}")
        if is_op(edge[0]):
            stmt = [parent, edge[1]]
            add_clause(stmt, "add_op")
        else:
            raise ValueError("Edge must be list", edge, parent)

    # :polarity handling
    has_polarity = False
    if is_polarity_modifier(edge):
        has_polarity = True
        polarity_mod = edge[1]
        parent[1] = polarity_mod + parent[1]
        logger.debug(f"Polarity: mod={polarity_mod} parent={parent}")

    # connectives
    try:
        if len(edge) > 1 and edge[1][1] in ["and", "or"]:
            edge[1] = "CONN:" + edge[1][1]  # ['a', 'and'] -> 'and'
            parent = edge[1]
            logger.warning(f"Connective: {edge}")
    except IndexError:
        pass


    # Operator merging
    all_ops = True
    for idx, it in enumerate(edge):
        if not is_op(it[0]):
            all_ops = False
    if all_ops:
        ops = []
        for it in edge:
            ops.append(it[1])
        ops = simplify_operators(ops)
        stmt = [parent, ops]



        add_clause(stmt, "ops")
        logger.warning(f"OP STMT {stmt}, parent={parent}, edge={edge}")
        return

    # Name handling
    if ':name' == value[0] and 'name' == value[1][1]:
        stmt = amrutil.extract_name_variable(edge)
        add_clause(stmt, "extract_name")
        if debug:
            logger.info(f"Name: {value}, mod={modifier}, stmt={stmt}")
            logger.info("Return after name extraction.")
        return

    if not has_polarity:
        if not isinstance(value, str):
            stmt = [value[0], value[1][1], value[1][0]]
            add_clause(stmt, "edge_val")

    if not parent:
        parent = edge[1][0]

    modifier = edge[2:]
    if modifier:

        if len(modifier) == 1 and is_list(modifier[0]):
            modifier = modifier[0]
            logger.warning(f"MOD1 {modifier}")

        if value != modifier:
            if not is_atom(modifier):
                logger.warning(f"Recursive: mod={modifier}")
                parse_edge(modifier, parent)
            else:
                logger.warning(f"Atom: mod={modifier}")
                if debug:
                    logger.warning(f"Modifier: {modifier}, edge={value}, parent={parent}")


def json_list_to_logic(json_list, debug=False):
    parent_var = None
    for cl in json_list:
        if debug:
            print(f"Check edge: {cl}")
        if is_variable_assignment(cl):
            if debug:
                print(f"VA: {cl}")
            if not parent_var:
                clause_type = "rootvar"
                stmt = [clause_type, cl[1], cl[0]]
                add_clause(stmt, "assign_var")
                parent_var = stmt
        else:
            if debug:
                print(f"PE: {cl}")
            parse_edge(cl, parent_var, debug)


"""
def svo_filter(clause_lst, s=None, v=None, o=None):
    ret = []
    for cl in clause_lst:
        if s and cl[0] == s:
            ret.append(cl)
        if v and cl[1] == v:
            ret.append(cl)
        if o and cl[2] == o:
            ret.append(cl)
    return ret
"""

"""
def simplify_clauses(clause_lst):
    logger.info("Simplifying clauses.")
    logger.info(clause_lst)
    return clause_lst

    simpl_lst = []

    for idx, cl in enumerate(clause_lst):
        simpl_lst.append(cl)
        if ":poss" == cl[0]:
            find = svo_filter(clause_lst, v=cl[2])
            if find:
                find = find[0]
                if find[0] == "name":
                    clause_lst[idx] = [cl[1], find[2]]
                    clause_lst.remove(find)
            logger.info(f"Find: {find}, search={cl[2]}, res={find}")

    return simpl_lst
"""


def question_from_amr(amr_str, udparse, debug=False):
    data = {
        "amr": amr_str,
        "ud": udparse
    }
    pprint.pprint(data, indent=2)
    return []
    return logic_from_amr(amr_str, constituency, debug=False)


def from_amr(json_list, debug=False):
    """
    Create FOL clauses from AMR -> JSON conversion
    :param json_list:
    :param debug:
    :return:
    """
    global logic_lst
    logic_lst = []

    if debug:
        pprint.pprint(json_list, indent=2)

    json_list_to_logic(json_list, config.debug_graph_construction)

    json_logic = logic_lst

    outp = str(json_logic)
    outp = outp.lower()
    outp = outp.replace("'", "\"")
    outp = json.loads(outp)

    if debug:
        # print("--- LOGIC (", len(json_logic), ")---")
        # pprint.pprint(json_logic)
        print(f"--- CLAUSES --- ({len(outp)})")
        pprint.pprint(outp, indent=2)

    # outp = json.loads(outp)
    return outp
