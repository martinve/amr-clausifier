import json


def tuples_to_dict(tuples):
    tupledict = {}
    for el in tuples:
        if len(el) == 2:
            tupledict[el[0]] = el[1]
    return tupledict

def get_sentence(triple_map):

    tok_list = []
    for tok in triple_map:
        word = tok[0]
        info = tok[1] # list[tuple]
        tok_list.append(word)


        if len(info) == 0:
            continue

        # infodict = tuples_to_dict(info)
        # print(info)
        infodict = {}
        for t in info:
            if len(t) != 2:
                continue
            if t[0] == "instance" and t[1] == word:
                continue

            infodict[t[0]] = t[1]

        if len(infodict) > 0:
            annotation = json.dumps(infodict)
            tok_list.append(annotation)

    return " ".join(tok_list)