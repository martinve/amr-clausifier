#!/usr/bin/env python3

import pprint
import sys

import penman
import debug.extract_info_test_cases as examples
import aligner
import outputter
import nlp
import amr_ie as ie
import triplemgr
import pipeline

from gui.unified_parser import get_amr_parse


debug = True


def debug_print(*text):
    if debug:
        print(*text)


def decompose_amr(amrstr):
    g = penman.decode(amrstr)
    
    debug_print("Graph:")
    debug_print(amrstr, "\n")

    snt_text = g.metadata.get("snt")
    debug_print('Sentence:', snt_text, "\n")

    triples = triplemgr.simplify_amr_triples(g.triples)

    amr_new = pipeline.graph_encode_snt(triples, snt_text)
    g = penman.decode(amr_new)

    debug_print("Simplified Graph")
    debug_print(amr_new, '\n')

    


    amr_alignments = aligner.get_alignments_rbw(snt_text, amr_new, debug)
    alignments_dict = aligner.alignments_to_dict(amr_alignments)

    debug_print("Alignments:")

    debug_print("AMR:")
    pprint.pprint(alignments_dict, indent=2)
    # debug_print("Text:")
    # pprint.pprint(text_alignments)

    propbank_mappings = pipeline.get_propbank_mappings(triples)
    debug_print("Propbank mappings:")
    pprint.pprint(propbank_mappings)



    triples = pipeline.apply_propbank_mappings(triples, propbank_mappings)
    triples = pipeline.map_ner_types(triples, debug)

 

    variable_map = ie.get_variable_map(g, debug)

  

    debug_print("\nVariable map:", len(variable_map))
    if debug: pprint.pprint(variable_map, indent=2)

    triples = triplemgr.sort_triples(triples, g.top)
    debug_print("\nSorted Triples:", len(triples))
    if debug: pprint.pprint(triples)

    debug_print("\nTriple Subject Count")
    variable_map_copy = variable_map.copy()
    tmp = []
    for t in triplemgr.subject_count(triples):
        tmp.append((t[0], t[1], variable_map_copy[t[0]]))
    if debug: pprint.pprint(tmp)

    # graph_new = Graph(triples)
    # debug_print(graph_new)

    pb_role_labels = pipeline.get_role_labels()

    triple_map = triplemgr.triples_to_dict(triples)
    triple_map = triplemgr.triple_map_add_roles(triple_map, pb_role_labels)
    triple_map = triplemgr.triple_map_annotate_propbank(triple_map, propbank_mappings)
    triple_map = triplemgr.triple_map_remove_connectives(triple_map)

    triple_map = triplemgr.triple_map_apply_variables(triple_map, variable_map)

    debug_print("\nGrouped Triples:")
    if debug:
        pprint.pprint(triple_map)

    spans = nlp.get_spans(snt_text)
    if spans:
        if debug:
            debug_print("\nNP/VP spans:")
            pprint.pprint(spans)

    # removed text alignments from arguments, check logic
    alignment_map = aligner.map_alignments(snt_text, alignments_dict)
    debug_print("\nAlignment Map:")
    if debug: pprint.pprint(alignment_map, indent=2)

    debug_print("\nTriple map")
    if debug: pprint.pprint(triple_map, indent=2)
    # debug_print(">>>")
    # triple_map = replace_triples(triple_map, variable_map)
    # pprint.pprint(triple_map, indent=2)
    # debug_print("<<<")

    alignment_triple_map = aligner.map_triples(alignment_map, triple_map)

    debug_print("\nAlignment triple map:")
    if debug: pprint.pprint(alignment_triple_map)

    aligned_sent = outputter.get_sentence(alignment_triple_map)

    print("===")
    print("IN:", snt_text)
    print('')
    print("OUT:", aligned_sent)




if __name__ == "__main__":

    snt = sys.argv[1:]
    if len(snt) < 1:
        _amr = examples.amr4  # test_case
        decompose_amr(_amr)


    snt = " ".join(snt)
    amr = get_amr_parse(snt)
    decompose_amr(amr)
