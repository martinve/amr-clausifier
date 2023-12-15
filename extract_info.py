#!/usr/bin/env python3

import pprint
import sys
import amr_parser.amrconfig as amrconf
import propbank.propbank_api as pb
import propbank.propbank_amr_api as pbamr
import penman
from penman.graph import Graph
import debug.extract_info_test_cases as examples
import aligner
import formatter
import nlp
import json

from gui.unified_parser import get_amr_parse



"""
For NER types: @see: https://github.com/amrisi/amr-guidelines/blob/master/amr.md
"""

amr_ner_types = {
    "individual": ["person", "family", "animal", "language", "nationality", "ethnic-group", "regional-group", "religious-group", "political-movement"],
    "organization": ["company", "government-organization", "military", "criminal-organization", "political-party", "market-sector", "school", "university", "research-institute", "team", "league"],
    "location": ["location", "city", "city-district", "county", "state", "province", "territory", "country", "local-region", "country-region", "world-region", "continent", "ocean", "sea", "lake", "river", "gulf", "bay", "strait", "canal; peninsula", "mountain", "volcano", "valley", "canyon", "island", "desert", "forest moon", "planet", "star", "constellation"],
    "facility": [ "facility", "airport", "station", "port", "tunnel", "bridge", "road", "railway-line", "canal", "building", "theater", "museum", "palace", "hotel", "worship-place", "market", "sports-facility", "park", "zoo", "amusement-park"],
    "event": ["event", "incident", "natural-disaster", "earthquake", "war", "conference", "game", "festival"],
    "product": ["product", "vehicle", "ship", "aircraft", "aircraft-type", "spaceship", "car-make", "work-of-art", "picture", "music", "show", "broadcast-program"],
    "publication": ["publication", "book", "newspaper", "magazine", "journal"],
    "natural-object": ["natural-object"],
    "misc": ["award", "law", "court-decision", "treaty", "music-key", "musical-note", "food-dish", "writing-script", "variable", "program"]
}



def get_propbank_word(pbword):
    res = pb.describe(pbword)
    pprint.pprint(res)





def filter_triples(triples, source=None,role=None,target=None):
    if source is role is target is None:
        return triples

    triples = [
        t for t in triples
        if ((source is None or source == t[0])
            and (role is None or role == t[1])
            and (target is None or target == t[2]))
    ]
    return triples


def remove_triples(triples, sub):
    for it in sub:
        triples.remove(it)
    return triples


def simplify_amr_triples(triples):
    """
    Perform simplification of AMR triples:
    - remove empty Wiki tags
    - merge name variables and map them directly to concept
    """

    # Merge :name variables, remove unneeded steps
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

    # remove empty wikipedia links
    empty_wikis = filter_triples(triples, role=":wiki", target="-")
    for it in empty_wikis:
        triples.remove(it)

    connectives = filter_triples(triples, role=":instance", target='and')
    for conn in connectives:
        conn_children = filter_triples(triples, source=conn[0])
        print(conn_children)

    return triples


def get_propbank_mappings(triples):
    mappings_dict = {}
    roles = None
    for el in triples:

        if pb.is_amr_word(el[2]):
            #roles = describe_amr_role(el[2])
            roles = pbamr.describe(el[2])
        elif pb.is_propbank_word(el[2]):
           roles = pb.describe(el[2])

        if roles:
            mappings_dict[el[0]] = roles
            roles = None

    return mappings_dict




def get_ner_category(needle):
    for category in amr_ner_types.keys():
        for elem in amr_ner_types[category]:
            if elem == needle:
                return category
    return None



def describe_amr_role(key):
    print("Describe role:", key)
    if key in amrconf.amr_dict_roles:
        return amrconf.amr_dict_roles[key]
    return None



def map_ner_types(triples):
    debugs = []
    for idx, it in enumerate(triples):
        if it[1] != ":instance":
            continue
        category = get_ner_category(it[2])
        if category:
            debugs.append(["Category:", it[2], category, it[0]])
            triples.remove(triples[idx])
            # triples[idx] = (it[0], category, it[2])
            triples.append((it[0], "type", it[2]))
            triples.append((it[0], "category", category))

    print("NER mappings:")
    print(debugs)

    return triples


def apply_propbank_mappings(triples, propbank_mappings):
    for idx, it in enumerate(triples):
        if it[0] not in propbank_mappings.keys():
            continue
        if "roles" in propbank_mappings[it[0]].keys():
            if it[1] in propbank_mappings[it[0]]["roles"].keys():
                newrole = propbank_mappings[it[0]]["roles"][it[1]]["key"]
                triples[idx] = (it[0], newrole, it[2])


    return triples


def get_variable_map(triples):
    var_map = {}
    for it in filter_triples(triples, role=":instance"):
        var_map[it[0]] = it[2]
    return var_map



def apply_variable_map(triples, variable_map):
    return triples
    for idx, it in enumerate(triples):
        if it[0] not in variable_map.keys():
            pass
        triple = (it[0], it[1], variable_map[it[0]])
        triples.append(triple)
    return triples


def sort_triples(triples, top):
    tops = filter_triples(triples, source=top)

    for el in tops:
        triples.remove(el)

    return tops + sorted(triples)


def replace_triples(triple_map, value_map):

    print("TM")
    pprint.pprint(triple_map, indent=2)

    print("VM", value_map)
    pprint.pprint(value_map, indent=2)

    tm_ = triple_map

    for key in triple_map.keys():
        for idx, val in enumerate(triple_map[key]):
            if val[1] in value_map.keys():
                triple_map[key][idx] = (val[0], value_map[val[1]])

    print("RM")
    pprint.pprint(triple_map, indent=2)

    print(triple_map == tm_)

    return triple_map


def triple_map_add_roles(triple_map):
    """
    Clean up roles for triples
    """
    new_map = {}
    for key in triple_map.keys():
        if key not in new_map.keys():
            new_map[key] = []
        for idx, el in enumerate(triple_map[key]):
            if el[0] in pb.get_role_labels():
                role = el[0]
                subject = el[1]
                if subject not in new_map.keys():
                    new_map[subject] = []
                new_map[subject].append(("role", role))
            else:
                new_map[key].append(el)

    return new_map


def graph_encode_snt(triples, sent):
    """
    Encode sentence metadata to AMR graph
    """
    graph = Graph(triples)
    graph.metadata["snt"] = sent
    graph = penman.encode(graph)
    return graph


def triple_map_annotate_propbank(triple_map, propbank_mappings):
    pprint.pprint(propbank_mappings)
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

def decompose_amr(amrstr):
    g = penman.decode(amrstr)
    print("Graph:")
    print(amrstr, "\n")

    try:
        snt_text = g.metadata['snt']
    except:
        snt_text = None
    print('Sentence:', snt_text, "\n")

    triples = simplify_amr_triples(g.triples)

    amr_new = graph_encode_snt(triples, snt_text)
    g = penman.decode(amr_new)

    print("Simplified Graph")
    print(amr_new, '\n')

    # amr_alignments, text_alignments = aligner.get_alignments(snt_text, graph_new, debug=True)
    # amr_alignments, text_alignments = aligner.get_alignments_faa(snt_text, graph_new, debug=True)
    amr_alignments, text_alignments = aligner.get_alignments_rbw(snt_text, amr_new, debug=True)

    print("Alignments:")
    pprint.pprint(amr_alignments)
    pprint.pprint(text_alignments)

    # nlp.tokenize_sentence(snt_text, debug=True)
    # nlp.tokenize_sentence_lemmas(snt_text, debug=True)


    propbank_mappings = get_propbank_mappings(triples)
    print("\nPropbank mappings:")
    pprint.pprint(propbank_mappings)

    triples = apply_propbank_mappings(triples, propbank_mappings)

    triples = map_ner_types(triples)

    ## variable_map = get_variable_map(triples)
    import amr_ie as ie
    variable_map = ie.map_concept_attribute_values(g)

    print("\nVariable map:")
    pprint.pprint(variable_map, indent=2)

    triples = apply_variable_map(triples, variable_map)

    triples = sort_triples(triples, g.top)
    print("\nSorted Triples:")
    pprint.pprint(triples)

    # graph_new = Graph(triples)
    # print(graph_new)

    triple_map = {}
    for t in triples:
        idx = t[0]
        if idx not in triple_map.keys():
            triple_map[idx] = []

        # if idx == g.top:
        #     if ("amr_root", "True") not in triple_map[idx]:
        #        triple_map[idx].append(("amr_root", "True"))

        key = t[1].replace(":", "")
        val = t[2].replace('"', "")
        triple_map[idx].append((key,val))

    triple_map = triple_map_add_roles(triple_map)
    triple_map = triple_map_annotate_propbank(triple_map, propbank_mappings)

    print("\nGrouped Triples:")
    pprint.pprint(triple_map)

    spans = nlp.get_spans(snt_text)
    print("\nNP/VP spans:")
    pprint.pprint(spans)

    # removed text alignments from arguments, check logic
    alignment_map = aligner.map_alignments(snt_text, amr_alignments)
    print("\nAlignment Map:")
    pprint.pprint(alignment_map, indent=2)

    print("\nTriple map")
    pprint.pprint(triple_map, indent=2)
    print(">>>")
    triple_map = replace_triples(triple_map, variable_map)
    pprint.pprint(triple_map, indent=2)
    print("---")

    alignment_triple_map = aligner.map_triples(alignment_map, triple_map)

    print("\nAlignment triple map:")
    pprint.pprint(alignment_triple_map)

    aligned_sent = formatter.get_sentence(alignment_triple_map)

    print("===")
    print("IN", snt_text)
    print("OUT", aligned_sent)







if __name__ == "__main__":

    snt = sys.argv[1:]
    if len(snt) < 1:
        _amr = examples.amr4  # test_case
        decompose_amr(_amr)

    snt = " ".join(snt)
    amr = get_amr_parse(snt)
    decompose_amr(amr)
