import pprint
import sys

import penman
import re
from penman import Graph

import config
import pprint
import types_util

import propbank.propbank_api as pb


from debug.amr_test_cases import get_example_snt
import debug.amrtest_config as cfg
from logger import logger

"""
In addition to `amrtest.py`, and/or connective handling in implemented
"""

connectives = ["and", "or"]


def get_attribute_values(g):
    """
    Attributes don’t include concept triples or those where
    the target is a nonterminal.

    :param g:
    :return:
    """
    attr_value_map = {}

    for val in g.attributes():
        if val.role in [':wiki', ':polarity']:
            continue

        target = val.target.replace('"', "")
        if val.source not in attr_value_map.keys():
            attr_value_map[val.source] = []
        attr_value_map[val.source].append(target)

    for val in attr_value_map.keys():
        values = list(set(attr_value_map[val]))
        # minlen = len(min(values, key=len))
        # shortest = [word for word in values if len(word) == minlen]

        attr_value_map[val] = "_".join(values)

    if cfg.debug_get_attribute_values:
        logger.info("Create attribute key-value map")
        logger.debug(f"g.attributes(): {g.attributes()}")
        logger.debug(f"attribute_values: {attr_value_map}")

    return attr_value_map




def get_concept_values(g):
    concept_values = dict()
    _k = 0
    for c in g.instances():
        _target = c.target
        if _target in concept_values.values():
            if not pb.is_propbank_word(c.target):
                # _target = f"{c.target}{_k}"
                _target = c.target
                _k += 1
        concept_values.update({c.source: _target})

    if cfg.debug_concept_values:
        logger.debug(f"concept_values: {concept_values}")

    return concept_values




def get_top_verb(g):
    for it in g.instances():
        if it.source == g.top:
            # return it.target.replace('-', '.')
            return ".".join(it.target.rsplit("-", 1))
    return False








def get_propbank_words(g):
    word_list = []
    for t in g.triples:
        for el in list(t):
            if pb.is_propbank_word(el):
                word_list.append(el)
    return word_list


def propbank_fetch_word(word):
    pb_key = pb.prepare_propbank_word(word)
    if cfg.debug_propbank:
        logger.info(f"Attempt to fetch propbank roles for `{word}` ({pb_key})")
    roles = pb.describe(pb_key)
    logger.info(f"200 {roles}")
    return roles


def get_propbank_role_dict(g):
    """
    Get role dictionary for propbank words
    :param g: AMR graph
    :return: role_dict
    """

    if cfg.debug_propbank:
        logger.info(f"Propbank words to check: {get_propbank_words(g)}")

    role_dict = {}
    not_mapped_roles = []
    for t in g.triples:
        if pb.is_propbank_word(t[0]):
            roles = propbank_fetch_word(t[0])
            if roles:
                role_dict.update({t[0]: roles})
            else:
                not_mapped_roles.append(t[0])
        if pb.is_propbank_word(t[2]):
            roles = propbank_fetch_word(t[2])
            if roles:
                role_dict.update({t[2]: roles})
            else:
                not_mapped_roles.append(t[2])

    if len(not_mapped_roles) > 0:
        cfg.debug_propbank: logger.warning(f"not mapped roles: {role_dict}")

        for r in not_mapped_roles:
            if r in config.amr_dict_roles.keys():
                role_dict.update({r:  config.amr_dict_roles[r]["roles"]})
                not_mapped_roles.remove(r)

    if cfg.debug_propbank:
        logger.info(f"role_dict: {role_dict}")
        if len(not_mapped_roles) > 0:
            logger.warning(f"Not mapped: {not_mapped_roles}")



    return role_dict


def find_from_clauses(clauses, source=None, role=None, target=None):
    if source is None and role is None and target is None:
        return clauses
    match = []
    for cl in clauses:
        if role:
            if cl[1] == role:
                match.append(cl)
        if target:
            if cl[2] == target:
                match.append(cl)

    if len(match) == 1:
        match = match[0]

    return match


def get_concept_edges(g, concept_values, attribute_values):
    concept_edges = []
    for var in concept_values.keys():
        edges = g.edges(source=var)
        if len(edges) > 0:
            for e in edges:
                if cfg.debug_print_edges:
                    logger.info(f"Edge [{concept_values[var]}]: {e}")
                concept_edges.append(e)
        else:
            if var not in attribute_values:
                if cfg.debug_print_edges:
                    logger.warning(f"Add to attribute values: {var} ({concept_values[var]})")
                attribute_values.update({var: concept_values[var]})
            else:
                if cfg.debug_print_edges:
                    logger.warning(f"Ignore {var} ({concept_values[var]})")

    return concept_edges


def edges_replace_attribute_values(concept_edges, attribute_values):

    # logger.warning(concept_edges)
    # logger.warning(attribute_values)


    for idx, e in enumerate(concept_edges):
        if e.target in attribute_values.keys():
            concept_edges[idx] = e._replace(target=attribute_values[e.target])

    if cfg.debug_concept_edges:
        logger.info("Replaced Edge target with `attribute_values` values")
        logger.debug(f"concept_edges: {concept_edges}")

    return concept_edges


def replace_edges_value_keys(concept_edges, concept_values, polarities):
    #logger.error(polarities)
    for idx, e in enumerate(concept_edges):
        if e.target in concept_values.keys():
            val = concept_values[e.target]

            concept_edges[idx] = e._replace(target=val)
    for idx, e in enumerate(concept_edges):
        if e.source in concept_values.keys():
            val = concept_values[e.source]
            if e.source in polarities.keys():
                val = polarities[e.source] + val
            concept_edges[idx] = e._replace(source=val)
    return concept_edges


def get_polarities(g):

    polarities = {}

    edges = g.attributes(role=":polarity")
    for e in edges:
        polarities[e.source] = e.target
    return polarities


def extract_clauses(amr_str):
    if cfg.debug_amr: logger.info(amr_str)

    # Parse AMR string to penman.Graph
    g: Graph = penman.decode(amr_str)

    attribute_values = get_attribute_values(g)
    concept_values = get_concept_values(g)
    polarities = get_polarities(g)

    # The list of triples that make up the graph.

    if cfg.debug_triples:
        """
        Edges don't include terminal triples (concepts or attributes).
        """
        _triples = pprint.pformat(g.triples, indent=2)
        _edges = pprint.pformat(g.edges(), indent=2)
        logger.info(f"Graph triples ({len(_triples)}): {_triples}")
        logger.info(f"Graph edges ({len(_edges)}): {_edges}")


    concept_edges = get_concept_edges(g, concept_values, attribute_values)

    if cfg.debug_concept_edges:
        _val = pprint.pformat(concept_edges)
        logger.debug(f"concept_edges: {_val}")

    if cfg.debug_attribute_value_map:
        logger.info("Mapped concept values to edges")
        _val = pprint.pformat(attribute_values)
        logger.debug(f"attribute_values: {_val}")

    concept_edges = edges_replace_attribute_values(concept_edges, attribute_values)

    role_dict = get_propbank_role_dict(g)

    _exists = []
    for idx, e in enumerate(concept_edges):
        if e.source in concept_values.keys():
            role_key = concept_values[e.source]
            if role_key not in _exists:
                if is_propbank_word(role_key):
                    _exists.append(role_key)
                    if cfg.debug_propbank:
                        logger.debug(f"Propbank candidate: {role_key}")

        concept_role_dict = {}
        if role_key in role_dict.keys():
            concept_role_dict = role_dict[role_key]

        if e.role in concept_role_dict.keys():
            concept_edges[idx] = e._replace(role=concept_role_dict[e.role])




    if cfg.debug_concept_edges:
        logger.info("Replaced Edge roles with Propbank arguments")
        logger.debug(f"concept_edges: {pprint.pformat(concept_edges)}")

    # Edges don’t include terminal triples (concept_values or attributes).
    # debug_var(g.edges(), "Edges")
    for idx, e in enumerate(concept_edges):
        if e.role in config.amr_dict.keys():
            concept_edges[idx] = e._replace(role=config.amr_dict[e.role])

    if cfg.debug_concept_edges:
        logger.info("Replaced Edge roles with AMR dictionary items")
        logger.debug(f"concept_edges: {pprint.pformat(concept_edges)}")

    # Merge connectives
    for conn in connectives:
        if conn not in concept_values.values():
            continue

        conn_key = types_util.dict_find_key(concept_values, conn)
        conn_edges = g.edges(source=conn_key)
        for e in conn_edges:
            if types_util.is_op(e.role):
                pass
                # concept_edges.remove(e)

                # Nice-01, Good-02 (under better.01)


    """
    Replace the concept edges with value_keys
    """

    concept_edges = replace_edges_value_keys(concept_edges, concept_values, polarities)

    if cfg.debug_edge_replacements:
        logger.info("Replaced Edge source and target with values from `concept_values`")
        logger.debug(f"concept_edges: {pprint.pformat(concept_edges)}")

    clauses = []

    for e in concept_edges:
        clauses.append([e.role, e.source, e.target])
        # clauses.append([e.source, e.role, e.target])

    """
    Simple connectives (See example 10)
    """
    for _conn in connectives:
        parent = find_from_clauses(clauses, target=_conn)
        # if len(parent) == 0: continue
        children = find_from_clauses(clauses, role=_conn)
        if len(children) > 0:
            _values = []
            for child in children:
                clauses.remove(child)
                _values.append(child[2])
            if parent:
                parent[2] = "$" + _conn
                parent.append(_values)
            else:
                pass  # TODO: Hanging connective


    """
    for idx, cl in enumerate(clauses):
        if cl[2] in connectives:
            _conn = cl[2]
            children = find_from_clauses(clauses, role=_conn)

            if cfg.debug_edge_replacements:
                logger.warning(children)

            if children:
                _values = []
                for child in children:
                    clauses.remove(child)
                    _values.append(child[2])
                cl[2] = "$" + _conn
                cl.append(_values)
    """

    # Reorder clauses
    clauses_prev = clauses
    clauses = []
    for cl in clauses_prev:
        clauses.append([cl[1], cl[0], cl[2]])


    if cfg.debug_clauses:
        _clauses = pprint.pformat(clauses, indent=2)
        logger.info(f"Clauses:\n{_clauses}")

    return clauses


def debug_graph(amr_str):
    g: Graph = penman.decode(amr_str)

    logger.debug(amr_str)

    _label = "Variables"
    _var = g.variables()
    logger.debug(f"{_label}:\n{pprint.pformat(_var, indent=2)}\n---")

    _label = "Instances"
    _var = g.instances()
    logger.debug(f"{_label}:\n{pprint.pformat(_var, indent=2)}\n---")

    _label = "Edges"
    _var = g.edges()
    logger.debug(f"{_label}:\n{pprint.pformat(_var, indent=2)}\n---")

    _label = "Attributes"
    _var = g.attributes()
    logger.debug(f"{_label}:\n{pprint.pformat(_var, indent=2)}\n---")

    _label = "Triples"
    _var = g.triples
    logger.debug(f"{_label}:\n{pprint.pformat(_var, indent=2)}\n---")




if __name__ == "__main__":
    # Connectives: 2, 10, 11
    # AMR roles: 3
    # Weird: 4
    # Cannot fetch roles 14
    # FairytaleQA: 14
    # Done: Have org-role-91 resolves, but not 'have-rel-role-91' 3/19

    amr, label = get_example_snt(19)
    logger.info(label)

    # debug_graph(amr)

    simpl = extract_clauses(amr)
    pprint.pprint(simpl)

    # snt
    # triples
    # explanation for predicates

