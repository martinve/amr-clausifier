import json


def tuple_to_dict(tuples):
    tupledict = {}
    for el in tuples:
        if len(el) == 2:
            tupledict[el[0]] = el[1]
    return tupledict

def get_sentence(triple_map):
    tok_list = []
    for tok in triple_map:
        tok_list.append(tok[0])
        if len(tok[1]) > 0:
            info = tuple_to_dict(tok[1])
            if len(info):
                annotation = json.dumps(info)
                tok_list.append(annotation)

    return " ".join(tok_list)