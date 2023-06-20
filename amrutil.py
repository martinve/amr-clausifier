import sys
import warnings

import penman

import udutil
import config
from logger import logger

def format_amr(amr_graph):
    ret = []
    for line in amr_graph.split("\n"):
        if line[0] != "#":
            ret.append(line)
    return "\n".join(ret)


def get_root(amr_graph):
    """
    Extract root lemma and type for AMR graph
    :param amr_graph:
    :return:
    """
    print(f"(get_root) amr_graph={amr_graph}")

    root_instance = amr_graph[0][1].split("-", 1)[0]
    # print(amr_graph[0][1], "->", root_instance)
    root_word = udutil.get_word(config.snt_ud, root_instance)
    pb_form = amr_graph[0][1].replace("-", ".")
    if root_word:
        return {
            "upos": root_word["upos"],
            "lemma": root_word["lemma"],
            "pbverb": pb_form
        }
    return {"upos": "", "lemma": "", "pbverb": ""}


def check_edge(edge, parent):
    return
    print("Parent:", parent)
    print("Edge", edge)


def parse_init_root(json_list, edge):
    root = get_root(json_list)
    if root:
        lemma = root["lemma"]
        upos = root["upos"]
        rtype = "instance"
        if "NOUN" == upos:
            rtype = "isa"
        return [rtype, lemma, edge[0]]
    else:
        return [edge[1], edge[0]]


def extract_name_variable(edge):
    names = [it[1] for it in edge[2:]]
    return ["name", "_".join(names)]


count = 0
relations = []


def extract_relations(lst, parent=None, debug=False):
    global relations
    for edge in lst:
        if isinstance(edge, list) and isinstance(edge[0], str) and isinstance(edge[1], str):
            if parent:
                if edge[0] == ":polarity":
                    edge.reverse()
                if debug: print(f"var: {edge[1]} := {edge[0]} (parent={parent})")
                relations.append([edge[1], edge[0], parent])
            else:
                if debug: print(f"var: {edge[1]} := {edge[0]}")
                if not parent:
                    relations = []
                    parent = edge[0]
                    relations.append([edge[1], edge[0], None])

        if isinstance(edge, list) and isinstance(edge[0], str) and isinstance(edge[1], list):
            # print(f"edge: {edge[0]} ({len(edge[1:])}): {edge[1:]}")
            if debug: print(f"rel: edge := '{edge[0]}' parent := '{parent}'")
            relations.append(["relation", edge[0], parent])
            extract_relations(edge[1:], edge[0], debug)
    return relations


"""
def parse_logic_list(lst, parent=None):
    for edge in lst:
        if isinstance(edge, list):

            # [':instrument', ['k', 'knife']]
            if len(edge) == 2 and isinstance(edge[1], list) or len(edge) > 2:
                print("Further:", edge)
                parse_logic_list(edge, parent)

            parent = edge[0]

        print("len:", len(edge), "parent: ", parent, edge)
"""


def generate_clauses(amr_string):
    import penman
    import json
    from server.unified_parser import format_variable, format_clause, format_constant
    """
    Generate clauses from AMR string
    """
    g = penman.decode(amr_string)

    constant_dict = {}
    for c in g.attributes():
        constant_dict[c[0]] = c[1]

    clauses = []

    # Get base concepts
    for inst in g.instances():
        value = format_variable(inst[0])

        # We do not create clauses for constants
        if inst[0] in constant_dict:
            continue

        arity = max(
            len(g.edges(source=inst[0])),
            len(g.edges(target=inst[0]))
        )

        expr = [inst[2], value]
        if arity > 1:
            for edge in g.edges(source=inst[0]):
                val = format_variable(edge[2])
                if edge[2] in constant_dict:
                    val = format_constant(edge[2])
                expr.append(val)
        clauses.append(expr)

    # Get concept relations
    for rel in g.edges():
        value = format_variable(rel[2])
        constants = g.attributes(source=rel[2])
        if len(constants) > 0:
            value = format_constant(constants[0][2])

        predicate = format_clause(rel[1])

        if predicate in config.role_dict.keys():
            predicate = config.role_dict[predicate]

        clause = [
            predicate,
            format_variable(rel[0]),
            value]
        clauses.append(clause)

    # return json.dumps(intersperse(clauses, "&"))
    return json.dumps(clauses)


def parse_logic_list_(json_list, depth=0, parse=[]):
    global count

    print("Parse:", count, json_list)
    count += 1

    if isinstance(json_list, list):
        for edge in json_list:
            print(f"{depth * ''}Depth={depth}, edge={edge}")
            if not parse:
                parse.append(parse_init_root(json_list, edge))
                continue
            if ":name" == edge[0]:
                parse.append(extract_name_variable(edge))
                del edge
                continue
            if ":polarity" == edge[0]:
                warnings.warn("Parsing polarity")
            if isinstance(edge, list):
                parse_logic_list(edge, depth + 1, parse)

    print(parse)
    print("Finalcount", count)
    return parse

    # print(parse)
    # sys.exit(-1)


def replace_role(rel):
    print("Rel:", rel)
    rel_replace_dict = {
        ":domain": "isa",
        ":name": "hasName",
        ":location": "locatedAt",
        ":poss": "belongsTo",
        ":ARG0": "agent",
        ":ARG1": "patient",
        "i": "me"
    }
    if rel in rel_replace_dict.keys():
        rel = rel_replace_dict[rel]
    return rel


def assign_value(o, attrs):
    if o in attrs.keys():
        o = attrs[o]
    return o


def amr_extract_concepts(g, polarity):
    concepts = []
    for s, v, o in g.instances():
        if o not in ["name"]:
            for p in polarity:
                if p[0] == s:
                    o = "-" + o
            concepts.append([o, s])
    return concepts



def amr_extract_relations(g, attrs):
    rels = []
    for s, v, o in g.edges():
        if s == o:
            continue
        rel = [replace_role(v), s, assign_value(o, attrs)]
        rels.append(rel)
    return rels


def get_simplified_logic(amr_str):
    try:
        # Decode AMR to Graph object
        g = penman.decode(amr_str)
    except:
        logger.error("Cannot decode logic")
        return []


    attrs = {}
    polarity = []
    for s, v, o in g.attributes():
        if v == ":polarity":
            polarity.append([s, o])
            continue

        if s not in attrs.keys():
            attrs[s] = []

        o = o.strip('\"')
        attrs[s].append(o)

    for a in attrs.keys():
        if isinstance(attrs[a], list):
            attrs[a] = "_".join(attrs[a])

    concepts = amr_extract_concepts(g, polarity)
    relations = amr_extract_relations(g, attrs)



    logic = concepts + relations
    return logic
