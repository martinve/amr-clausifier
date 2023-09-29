import json
import sys, os
import time
import requests
import stanza

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from debugger import debug_print

pipeline = None

def get_amr_parse(sent):
    res = requests.get(f"http://localhost:9003/?text={sent}",
                 headers={'Accept': 'application/json'})
    return res.json()["amr"]


def get_stanza():
    global pipeline
    if pipeline is None:
        pipeline = stanza.Pipeline(lang='en', processors='tokenize,ner,pos,lemma,depparse',
                              download_method=stanza.DownloadMethod.REUSE_RESOURCES)
    return pipeline
def get_passage_analysis(passage: str, context=False):
    global init_nlp
    st0 = time.time()

    meta = {"passage": passage, "context": context, "sentences": []}
    nlp = get_stanza()

    doc = nlp(passage)
    k = 0
    for i, sent in enumerate(doc.sentences):
        sent_text = " ".join([token.text for token in sent.tokens])
        parsed = {
            "sentence": sent_text,
            "semparse": {
                "amr": get_amr_parse(sent_text),
                "ud": sent.to_dict()
            }
        }
        meta["sentences"].append(parsed)
        k = k + 1

    return meta



if __name__ == "__main__":

    passage_in = " ".join(sys.argv[1:])



    passage_meta = get_passage_analysis(passage_in, "default")
    print(json.dumps(passage_meta, indent=2))
