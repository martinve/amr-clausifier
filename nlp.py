import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)
pattern_ = [{'POS': 'VERB', 'OP': '?'},
           {'POS': 'ADV', 'OP': '*'},
           {'POS': 'AUX', 'OP': '*'},
           {'POS': 'VERB', 'OP': '+'}]
pattern = [
    [{"POS": "AUX"}, {"POS": "VERB"}]
]
matcher.add("verb-phrases", pattern)

def get_noun_phrases(doc):
    spans = []
    for chunk in doc.noun_chunks:
        # print("NP:", chunk.text, (chunk.start, chunk.end - 1))
        # print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
        if chunk.start == chunk.end:
            continue
        spans.append([chunk.text, (chunk.start, chunk.end - 1)])
    return spans


def get_verb_phrases(doc):
    matches = matcher(doc)
    spans = []
    for match in matches:
        span = doc[match[1]:match[2]]
        # print("VP", span, (match[1], match[2]))
        spans.append([span, (match[1], match[2])])
    return spans



def tokenize_sentence(snt_text, debug=False):
    doc = nlp(snt_text)
    words = [tok.text for tok in doc]

    word_list = []
    for idx, word in enumerate(words):
        word_list.append((idx, word))
    if debug:
        print(word_list)
    return words


def tokenize_sentence_lemmas(snt_text, debug=False):
    doc = nlp(snt_text)
    word_list = []
    words = []
    for idx, tok in enumerate(doc):
        word_list.append((idx, tok.lemma_))
        words.append(tok.lemma_)
    if debug:
        print(word_list)
    return words



def get_spans(snt_text):
    doc = nlp(snt_text)
    return get_verb_phrases(doc) + get_noun_phrases(doc)