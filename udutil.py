import sys

"""
Utilities for extracting informatin from Universal Dependencies
"""


def get_verbs(snt_ud):
    entities = []
    for tok in snt_ud:
        if tok["upos"] != "VERB":
            continue
        entities.append(tok["lemma"])
    return entities


def get_named_entities(snt_ud):
    """
    Get a list of named entities via token BIOES representation
    :param snt_ud: UD graph
    :return: dictionary of named entities and its prefix
    """

    if isinstance(snt_ud, str):
        return []

    entities_lst = []
    name_lst = []

    for tok in snt_ud:
        if isinstance(tok, list): tok = tok[0]
        if tok["ner"] == "O":
            continue

        # print(tok["ner"], tok["text"], tok["lemma"])

        prefix = tok["ner"][0]

        if prefix == "B":
            name_lst = [tok["text"]]
        elif prefix == "I":
            name_lst.append(tok["text"])
        elif prefix in ["E", "S"]:
            name_lst.append(tok["text"])
            entities_lst.append({
                "text": "_".join(name_lst),
                "type": tok["ner"][2:]}
            )
            name_lst = []

    return entities_lst


# ====== linguistic helpers ========

def get_word_by_keyval(sentence, key, val):
    if not sentence: return None
    for word in sentence:
        if isinstance(word, list): word = word[0]
        if word[key] == val:
            return word
    return None


def get_word(sentence, val, debug=False):
    if not sentence: return None
    for word in sentence:
        if debug: print(word)
        if word["text"] == val or word["lemma"] == val:
            return word
    return None


def get_root(sentence):
    if isinstance(sentence, str):
        return ""

    features = get_word_by_keyval(sentence, "deprel", "root")
    return {"upos": features["upos"], "lemma": features["lemma"]}


# ====== debugging and printing ========

ud_tree_lst = []


def print_tree(sentence, rootid=0, spaces="", printedids=[], feats=False):
    if not sentence: return
    # print("sentence:",sentence)
    printedids = printedids[::-1]  # copy
    for word in sentence:
        # print("word",word)
        # debug_print("word:",word)
        if word["head"] == rootid:
            deprel = word["deprel"]

            if deprel == "punct": continue

            # if deprel=="root": deprel=""
            if word["id"] in printedids:
                out =  spaces + deprel + ": id " + str(word["id"])
                print(out)
                ud_tree_lst.append(out)
            else:
                out = spaces + deprel + ": " + nice_word_strrep(word, feats)
                print(out)
                ud_tree_lst.append(out)
                printedids.append(word["id"])
                print_tree(sentence, word["id"], spaces + "  ", printedids)


def nice_word_strrep(word, feats=False):
    s = word["lemma"]
    # s += " [id:" + str(word["id"])

    if word["text"] != word["lemma"]:
        s += f" ({word['text']})"

    # s += " text:" + word["text"]

    s += " upos:" + word["upos"]
    # s += " xpos:" + word["xpos"]
    s += " lemma:" + word["lemma"]
    if word["ner"] != "O":
        s += " ner:" + word["ner"]
    if feats:
        if "feats" in word:  s += " feats:" + word["feats"]
    s += "]"
    return s


def print_plain(snt_ud):

    from tabulate import tabulate

    del_keys = ["start_char", "end_char"]
    for del_key in del_keys:
        snt_ud = [{key: val for key, val in sub.items() if key != del_key} for sub in snt_ud]

    for idx, tok in enumerate(snt_ud):
        feats = tok.get("feats")
        if feats:
            snt_ud[idx]["feats"] = "\n".join(feats.split("|"))

    # [it.update(feats=it.get("feats").split("|")) for it in snt_ud]
    # [it.update(feats="") for it in snt_ud]

    # print(snt_ud["feats"])
    # it["feats"] = it["feats"].split("|") # "\n".join()

    headers = {
        "id": "ID",
        "deprel": "Deprel",
        "feats": "Feats",
        "head": "Head",
        "lemma": "Lemma",
        "ner": "NER",
        "text": "Text",
        "upos": "upos"
    }

    print(tabulate(snt_ud, headers=headers, tablefmt="grid"), 1 * "\n")


def lst_to_dict(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


def extract_tree(sentence, rootid=0, spaces="", printedids=[], feats=False):
    if not sentence: return
    # print("sentence:",sentence)
    printedids = printedids[::-1]  # copy
    for word in sentence:
        print(word)
        if word["head"] == rootid:
            deprel = word["deprel"]
            if deprel == "punct": continue
            if word["id"] in printedids:
                out =  spaces + deprel + ": id " + str(word["id"])
                ud_tree_lst.append(out)
            else:
                out = spaces + deprel + ": " + nice_word_strrep(word, feats)
                ud_tree_lst.append(out)
                printedids.append(word["id"])
                print_tree(sentence, word["id"], spaces + "  ", printedids)
    return ud_tree_lst


def format_ud(ud):
    assert isinstance(ud, list)
    ud = ud[0]
    ud_dict = ud
    ud_tree_lst.clear()
    tree = extract_tree(ud_dict, feats=True)
    return tree



