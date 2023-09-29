#!/usr/bin/env python3

"""
Convert a text passage to logic

"""
import json
import os
import sys
import pprint
import argparse

import amrutil
import api
import config

import config
from RoleReplacer import RoleReplacer
from amr_to_json import amr_to_json
import json_to_logic as json2logic
from logger import logger
from solver import run_solver

import classifier.sentence_heuristic_classifier as snt_clf

import udutil
import simplifier

load_fresh = False
save_meta = False
load_meta = True


def is_question(snt):
    return snt.endswith("?")


def get_sentence_clauses(sent, idx, debug=True, ud_shift=False, json_ld_logic=True):


    amr = sent["semparse"]["amr"]
    ud = sent["semparse"]["ud"]
    # const = sent["constituency"]

    if ud_shift:
        config.snt_ud = ud[0]
    else:
        config.snt_ud = ud

    role_replacer = RoleReplacer()

    if debug:
        print("UD:", udutil.print_tree(ud))

    # UD parse fix
    if isinstance(ud, list) and len(ud) == 1: ud = ud[0]

    json_list = amr_to_json(amr, debug=debug)

    if len(json_list) == 0:
        logger.error("Error translating sentence to JSON.")
        print(sent["sentence"])
        return None, None
        # sys.exit(-1)

    # cl2 = amrutil.parse_logic_list(json_list)
    # print(f"\nCLAUSES2:\n{pprint.pformat(cl2, compact=True)}")

    snt_type = snt_clf.predict_snt_type(ud, debug)
    question = is_question(sent['sentence'])

    ud_root = udutil.get_root(ud)
    amr_root = amrutil.get_root(json_list)

    cur_context = {
        "idx": idx,
        "type": snt_clf.snt_type_label(snt_type),
        "question": question,
        "entities": udutil.get_named_entities(ud),
        "verbs": udutil.get_verbs(ud),
        "ud_root": ud_root,
        "amr_root": amr_root
    }

    # assert(amr_root is not None)

    if ud_root["lemma"] != amr_root["lemma"] or ud_root["upos"] != amr_root["upos"]:
      cur_context["root_mismatch"] = True

    assert (type(cur_context) == dict)

    if debug:
        print(f"AMR:\n{amr}")

    clauses = json2logic.from_amr(json_list, debug=False)

    import server.propbank_api as pb
    pb.describe(amr_root["pbverb"])

    # role_replacer.update_role_dict(role_dict)

    clauses = role_replacer.replace(clauses, cur_context)

    if debug:
        print(f"\nInitial Clauses ({len(clauses)}):\n{pprint.pformat(clauses, compact=True)}")

    simpl_clauses = simplifier.simplify(clauses, snt_type)
    if simpl_clauses:
        print(f"\nSimplified Clauses ({len(simpl_clauses)}):\n{pprint.pformat(simpl_clauses, compact=True)}")

    relations = amrutil.extract_relations(json_list)
    print(f"\nRelations ({len(relations)}):\n{pprint.pformat(relations, indent=2)}")


    if not is_question(sent["sentence"]):
        for k, cl in enumerate(clauses):
            if len(cl) > 2 and isinstance(cl[2], str):
                cl[2] = cl[2] + str(idx)
            if json_ld_logic:
                clauses[k] = {"@logic": cl}
            else:
                clauses[k] = cl
        return clauses, cur_context
    else:
        # TODO: Parse question
        # TODO: Add to context
        logger.error(f"Question: {clauses}")
        question = json2logic.question_from_amr(amr, ud)
        return question, cur_context


def main(passage_raw, limit=False, debug=False):
    assert isinstance(passage_raw, dict)

    logic = []
    question = None

    if limit:
        passage_raw["sentences"] = passage_raw["sentences"][:limit]
        print("Limit:", limit)

    context = []

    for idx, sent in enumerate(passage_raw['sentences']):
        clauses, snt_ctx = get_sentence_clauses(sent, idx, debug=False, ud_shift=True)
        logic.extend(clauses)
        context.append(snt_ctx)

    if isinstance(question, list):
        logger.info("Assign question clauses.")
        logger.info(f"AMR: {amr}")
        logic = add_question_clauses(logic, question)

    if debug:
        print(f"\nContext:\n{pprint.pformat(context)}")
        print(f"\nJSON:\n{pprint.pformat(json_list, compact=True)}")
        print(f"\nClauses:\n{pprint.pformat(clauses, compact=True)}")

    run_solver(logic, print_logic=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert passage to logical form.')
    parser.add_argument("passage", nargs="?")
    parser.add_argument("-r", "--reload", action='store_true',
                        help="Re-create and fetch parse graphs from server.")
    parser.add_argument("-x", "--clear", action='store_true', help="Clear console output.")
    parser.add_argument("-l", "--load", action='store_true', help="Load already saved file.")
    parser.add_argument("-s", "--save", help="Provide custom name for cache. Otherwise default `cache` is used.")
    parser.add_argument("-n", "--limit", type=int, help="If set only specified number of sentences are processed.")
    args = parser.parse_args()

    passage = args.passage

    if args.clear:
        os.system("clear")

    file = f"./data/{config.cache_file}.json"
    print("File:", file)

    if args.load:
        file = f'./data/{args.passage}.json'
        if not os.path.exists(file):
            print(f"ERROR: Data file {file} does not exist.")
            sys.exit(-1)

        print(f"Loading: {file}")
        with open(file) as f:
            passage_meta = json.load(f)

    elif args.reload or args.save:
        passage_meta = api.fetch_parse_from_server(passage)
        file = f'./data/{config.cache_file}.json'
        if args.save:
            file = f'./data/{args.save}.json'
        with open(file, 'w') as f:
            json.dump(passage_meta, f, indent=2)
            logger.info("Saved passage meta.")

    else:
        with open(file) as f:
            passage_meta = json.load(f)

    debug = config.debug_clauses

    main(passage_meta, args.limit, debug)
