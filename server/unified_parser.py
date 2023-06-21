import json
import sys, os
import subprocess
import warnings
import amrlib
import time


from logger import logger

import stanza
import spacy_stanza
import textacy

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from debugger import debug_print


warnings.filterwarnings('ignore')
os.environ['TOKENIZERS_PARALLELISM'] = 'true'

dirname = os.path.dirname(__file__)

# model_stog_dir = os.path.join(dirname, "models/model_parse_xfm_bart_base-v0_1_0")
model_stog_dir = os.path.join(dirname, "../models/model_stog")

model_gtos_dir = os.path.join(dirname, "../models/model_gtos")

stanza_nlp = None
nlp = None

debug = False


def init_pipeline():
    global stanza_nlp, nlp

    debug_print("Initializing model pipeline.")

    amrlib.load_stog_model(model_dir=model_stog_dir)
    # gtos = amrlib.load_gtos_model(model_dir=model_gtos_dir)
    amrlib.setup_spacy_extension()

    nlp = spacy_stanza.load_pipeline("en", processors='tokenize,ner,pos,lemma,constituency,depparse')
    stanza_nlp = stanza.Pipeline(lang='en', processors='tokenize,ner,pos,lemma,constituency,depparse')



def udparse(text):
    start = time.time()

    if stanza_nlp is None:
        init_pipeline()

    doc = stanza_nlp(text)
    docpy = doc.to_dict()
    debug_print("[Parse 1] UD in:", time.time() - start)
    return docpy


def get_word_types(sent):
    """
    :type sent: spacy.tokens.span.Span
    """

    wordtypes = {}
    for token in sent:
        if token.pos_ in ["DET", "PUNCT"]:
            continue
        if token.pos_ not in wordtypes.keys():
            wordtypes[token.pos_] = []
        wordtypes[token.pos_].append(token.text)
    return wordtypes


def get_named_entities(sent):
    """
    :type sent: spacy.tokens.span.Span
    """
    ner = {}
    for ent in sent.ents:
        if ent.label_ not in ner.keys():
            ner[ent.label_] = []
        ner[ent.label_].append(ent.text)
    return ner


def get_wordnet_hierarchy(sent):
    start = time.time()

    wordnet = []
    cmd = "python3 wordnet_tree.py -s"

    wordnet_types = {
        "VERB": "v",
        "NOUN": "n"
    }

    for token in sent:
        if token.pos_ not in wordnet_types.keys():
            continue
        syn = ".".join([token.lemma_, wordnet_types[token.pos_], "01"])
        # debug_print(token, syn, sep=" -> ")

        outp = subprocess.run(cmd + " " + syn, stdout=subprocess.PIPE, shell=True)
        res = str(outp.stdout, 'utf-8')
        parents = [x.strip() for x in list(filter(None, res.split("\n")))]
        parents.reverse()

        word = {"word": token.text, "syn": syn, "parents": parents}

        wordnet.append(word)

    if debug:
        debug_print("[Onto] Wordnet:", time.time() - start)

    return wordnet


def get_noun_phrases(sent):
    """
    :type sent: spacy.tokens.span.Span
    """
    chunks = []
    for np in sent.noun_chunks:
        chunks.append(np.text)
    return chunks


def get_verb_phrases(sent):
    chunks = []
    pattern = r'<VERB>?<ADV>*<VERB>+'

    pattern = [{'POS': 'VERB', 'OP': '?'},
               {'POS': 'ADV', 'OP': '*'},
               {'POS': 'VERB', 'OP': '+'}]

    lists = textacy.extract.token_matches(sent, pattern)
    for chunk in lists:
        chunks.append(chunk.text)
    return chunks


def get_svo_triples(sent):
    triples = textacy.extract.triples.subject_verb_object_triples(sent)
    svo = []
    for t in triples:
        item = {
            "s": '_'.join([str(x) for x in t.subject]),
            "v": '_'.join([str(x) for x in t.verb]),
            "o": '_'.join([str(x) for x in t.object])
        }
        svo.append(item)
    return svo


def format_clause(txt):
    """
    Remove AMR specific clause modifiers, e.g :ARG0 is transformed to ARG0
    """
    return txt.replace(":", "")


def format_constant(txt):
    """
    Constants are lowercase
    """
    ret = txt.lower().strip('"')
    return ret


def format_variable(txt):
    """
    Variables are uppercase
    """
    return txt.upper()


def get_sentence_analysis(sent: object):
    """
    :type sent: spacy.tokens.span.Span
    """
    if len(sent.text.strip()) < 1:
        return False

    # debug_print("Sent typr", type(sent))

    sent_ud = udparse(sent.text)

    # start = time.time()
    # svo_triples = get_svo_triples(sent)
    # debug_print("[Parse 3] triples in:", time.time() - start)

    parsed: dict[str, object] = {
        "sentence": sent.text,
        "wordtypes": get_word_types(sent),
        "ner": get_named_entities(sent),
        # "wordnet": get_wordnet_hierarchy(sent),
        "syntaxparse": {
            "verbphrase": get_verb_phrases(sent),
            "nounphrase": get_noun_phrases(sent)
        },
        "semparse": {
            "amr": get_amr_parse(sent),
            "ud": sent_ud
        }
    }

    return parsed


def get_amr_parse(sent):
    start = time.time()
    parse = sent._.to_amr()[0]
    if debug:
        debug_print("[Parse 0] AMR in:", time.time() - start)
    return parse


def get_passage_analysis(passage: str, context=False):
    st0 = time.time()

    if nlp is None:
        init_pipeline()

    doc = textacy.make_spacy_doc(passage, lang=nlp)
    debug_print("textacy.make_spacy_doc in:", time.time() - st0)

    # debug_print("DOC", type(doc))

    # meta = {"passage": passage, "context": context, "sentences": [], "spacy": doc.to_json()}
    meta = {"passage": passage, "context": context, "sentences": []}

    k = 0
    for sent in doc.sents:
        start = time.time()
        parsed = get_sentence_analysis(sent)
        end = time.time()
        debug_print(k, "get_sentence_analysis:", time.time() - start)

        if not parsed:
            continue

        meta["sentences"].append(parsed)
        k = k + 1

    return meta


if __name__ == "__main__":

    if len(sys.argv) == 1:
        debug_print("No input passage provided")
        sys.exit()

    passage_in = sys.argv[1]

    init_pipeline()

    passage_meta = get_passage_analysis(passage_in, "default")
    debug_print(json.dumps(passage_meta, indent=2))
