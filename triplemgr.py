import sys
import json
import pprint

import wikivalidate
import wikivalidate as wiki

def filter_triples(triples, source=None,role=None,target=None):
    if source is role is target is None:
        return triples

    if target:
        targets = target.split("|")
    if source:
        sources = source.split("|")
    if role:
        roles = role.split("|")

    triples = [
        t for t in triples
        if ((source is None or t[0] in sources)
            and (role is None or t[1] in roles)
            and (target is None or t[2] in targets))
    ]
    return triples


def get_index(triples, triple):
    idx = None
    for idx, t in enumerate(triples):
        if t == triple:
            return idx
    return idx


def sort_triples(triples, top):
    tops = filter_triples(triples, source=top)
    for el in tops:
        triples.remove(el)
    return tops + sorted(triples)


def _remove_invalid_wiki_tags(triples):
    # remove empty wikipedia links
    wikis = filter_triples(triples, role=":wiki")
    triples_copy = triples.copy()
    for it in wikis:
        target = it[2]
        if target == "-":
            triples_copy.remove(it)
        if not wikivalidate.validate(target):
            print("Remove target:", target)
            triples_copy.remove(it)
    return triples_copy


def _simplify_name_variable(triples):
    namevars = filter_triples(triples, role=":name")
    for idx, it in enumerate(namevars):
        triples.remove(it)
        sub = filter_triples(triples, source=it[2])
        namelist = []
        for el in sub[1:]:
            namelist.append(el[2].replace("\"", ''))
        for el in sub:
            triples.remove(el)
        triples.append((it[0], it[1], "_".join(namelist)))
    return triples


def _unify_quantifiers(triples):
    """
    Replace `:mod (a / all)` with :quant (a / all) to
    normalize with other quantifiers
    """

    allquants = filter_triples(triples, role=":instance", target="all|any")
    print(allquants)
    for t in allquants:
        allmods = filter_triples(triples, role=":mod", target=t[0])
        for t0 in allmods:
            idx = get_index(triples, t0)
            if idx:
                triples[idx] = (t0[0], ":quant", t0[2])
    return triples


def simplify_amr_triples(triples):
    """
    Perform simplification of AMR triples:
    - remove empty Wiki tags
    - merge name variables and map them directly to concept
    """

    # Merge :name variables, remove unneeded steps
    triples = _simplify_name_variable(triples)
    triples = _unify_quantifiers(triples)
    triples = _remove_invalid_wiki_tags(triples)

    connectives = filter_triples(triples, role=":instance", target='and')
    for conn in connectives:
        conn_children = filter_triples(triples, source=conn[0])
        print("Conn:", conn_children)

    return triples


def triple_map_add_roles(triple_map, pb_role_labels):

    new_map = {}
    for key in triple_map.keys():
        if key not in new_map.keys():
            new_map[key] = []
        for idx, el in enumerate(triple_map[key]):
            if el[0] in pb_role_labels:
                role = el[0]
                subject = el[1]
                if subject not in new_map.keys():
                    new_map[subject] = []
                new_map[subject].append(("role", role))
            else:
                new_map[key].append(el)
    return new_map



def triple_map_annotate_propbank(triple_map, propbank_mappings):
    for key in triple_map.keys():
        if key in propbank_mappings.keys():
            values = propbank_mappings[key]["roles"]
            value_map = []
            for pbkey in values.keys():
                elem = values[pbkey]
                if "descr" in elem.keys():
                    value_map.append({elem["key"]: elem["descr"]})
            pb_values = json.dumps(value_map)
            pb_values = pb_values.replace('\"', "'")
            # triple_map[key].append(("propbank", pb_values))

    return triple_map


def triples_to_dict(triples):
    triple_map = {}
    for t in triples:
        idx = t[0]
        if idx not in triple_map.keys():
            triple_map[idx] = []

        key = t[1].replace(":", "")
        val = t[2].replace('"', "")
        triple_map[idx].append((key,val))
    return triple_map


def triple_map_remove_connectives(triple_map):
    triple_map_copy = triple_map.copy()
    for key in triple_map.keys():
        for pred, value in triple_map[key]:
            if pred == "instance" and value in ["and", "or"]:
                triple_map_copy.pop(key)
    return triple_map_copy


def triple_map_apply_variables(triple_map, variable_dict):
    triple_map_copy = triple_map.copy()
    for key in triple_map.keys():
        for idx, data in enumerate(triple_map[key]):
            if data[1] in variable_dict.keys():
                triple_map_copy[key][idx] = (data[0], variable_dict[data[1]])
    return triple_map_copy


def subject_count(triples):
    subj_count = {}
    for triple in triples:
        if triple[0] not in subj_count.keys():
            subj_count[triple[0]] = 1
            continue
        subj_count[triple[0]] += 1

    return sorted(subj_count.items(), key=lambda x:x[1])
