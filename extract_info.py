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
from logger import logger

debug = False


def debug_print(*text):
    if debug:
        print(*text)


def get_aligned_triples(amrstr):
    g = penman.decode(amrstr)

    if debug:
        logger.info("Graph:")
        logger.debug(amrstr)

    snt_text = g.metadata.get("snt")

    if debug:
        logger.debug("Sentence: %s", snt_text)

    triples = triplemgr.simplify_amr_triples(g.triples)

    amr_new = pipeline.graph_encode_snt(triples, snt_text)
    g = penman.decode(amr_new)

    if debug:
        logger.info("Simplified Graph:")
        logger.debug(amr_new)


    amr_alignments = aligner.get_alignments_rbw(snt_text, amr_new, debug=False)
    alignments_dict = aligner.alignments_to_dict(amr_alignments)

    if debug and False:
        logger.info("AMR Alignments:")
        pprint.pprint(alignments_dict, indent=2)
    # debug_print("Text:")
    # pprint.pprint(text_alignments)

    propbank_mappings = pipeline.get_propbank_mappings(triples)
    
    if debug:
        logger.info("Propbank mappings:")
        pprint.pprint(propbank_mappings)

    triples = pipeline.apply_propbank_mappings(triples, propbank_mappings)
    triples = pipeline.map_ner_types(triples, debug)

    variable_map = ie.get_variable_map(g, debug=debug)
    if debug: 
        logger.info("Variable map: %d", len(variable_map))
        pprint.pprint(variable_map, indent=2)


    triples = triplemgr.sort_triples(triples, g.top)
    if debug: 
        logger.info("Sorted Triples: %d", len(triples))
        pprint.pprint(triples)


    variable_map_copy = variable_map.copy()
    _subj_counts = []

    triple_subj_count = triplemgr.subject_count(triples, debug=debug)

    # sort triples by subject
    for t in triple_subj_count:
        key = t[0]
        if key not in variable_map_copy.keys():
            logger.error("Key error: %s", key)
            logger.error("triple_subj_count: %s", triple_subj_count) 
            logger.error("variable_map_copy: %s", variable_map_copy)
            logger.error("Available keys: %s", variable_map_copy.keys())
            continue
        _subj_counts.append((key, t[1], variable_map_copy[key]))
    if debug: 
        logger.info("Triple subject count")
        pprint.pprint(_subj_counts)

    # graph_new = Graph(triples)
    # debug_print(graph_new)

    pb_role_labels = pipeline.get_role_labels()

    triple_map = triplemgr.triples_to_dict(triples)

    # logger.info("triplemgr.triples_to_dict")
    # pprint.pprint(triple_map)

    triple_map = triplemgr.triple_map_add_roles(triple_map, pb_role_labels)

    # logger.info("triplemgr.triple_map_add_roles")
    # pprint.pprint(triple_map)

    triple_map = triplemgr.triple_map_annotate_propbank(triple_map, propbank_mappings)

    # logger.info("triplemgr.triple_map_annotate_propbank")
    # pprint.pprint(triple_map)

    triple_map = triplemgr.triple_map_remove_connectives(triple_map)

    # logger.info("triplemgr.triple_map_remove_connectives")
    # pprint.pprint(triple_map)
    # sys.exit(-1)

    triple_map = triplemgr.triple_map_apply_variables(triple_map, variable_map)

    if debug:
        logger.info("triplemgr.triple_map_apply_variables")
        pprint.pprint(triple_map)

    if debug:
        logger.info("Grouped Triples")
        pprint.pprint(triple_map)

    spans = nlp.get_spans(snt_text)
    if spans and debug:
        logger.info("NP/VP spans:")
        pprint.pprint(spans)

    # removed text alignments from arguments, check logic
    alignment_map = aligner.map_alignments(snt_text, alignments_dict)
    if debug: 
        logger.info("Alignment Map:")
        pprint.pprint(alignment_map, indent=2)

    if debug:
        logger.info("Triple map")
        pprint.pprint(triple_map, indent=2)

    # debug_print(">>>")
    # triple_map = replace_triples(triple_map, variable_map)
    # pprint.pprint(triple_map, indent=2)
    # debug_print("<<<")

    alignment_triple_map = aligner.map_triples(alignment_map, triple_map)

    if debug: 
        logger.info("Alignment triple map:")
        pprint.pprint(alignment_triple_map)
        print("\n===\n")

    return alignment_triple_map


def snt_from_triples(triple_map):
    snt = []
    for triple in triple_map:
        snt.append(triple[0])
    return " ".join(snt)


def decompose_amr(amr):
    aligned_triples = get_aligned_triples(amr)
    aligned_sent = outputter.get_sentence(aligned_triples)
    return aligned_sent


def decompose_amr_triples(amr):
    aligned_triples = get_aligned_triples(amr)
    lemmas = nlp.tokenize_sentence_lemmas(snt_from_triples(aligned_triples))
    pprint.pprint(aligned_triples)

    clauses = []
    for idx, triple in enumerate(aligned_triples):
        lemma = lemmas[idx]
        clause = (lemma, triple[1])
        clauses.append(clause)    

    # pprint.pprint(clauses)
    # sys.exit(-1)


if __name__ == "__main__":

    snt = sys.argv[1:]
    if len(snt) < 1:
        _amr = examples.amr8  # test_case
        decompose_amr(_amr)
    else:
        snt = " ".join(snt)
        amr = get_amr_parse(snt)
        
        # out = decompose_amr(amr)
        out = decompose_amr_triples(amr)
        print(out)
