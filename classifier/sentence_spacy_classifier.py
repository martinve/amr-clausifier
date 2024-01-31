import spacy
import math

class Predict:

    def __init__(self):
        self.sit = 0
        self.concept = 0
        self.fact = 0
        self.confidence = 0

    def adjust(self, dim, value):
        assert dim in ["sit", "concept", "fact"]
        curval = getattr(self, dim)
        setattr(self, dim, curval + value)

    def update_confidence(self):
        values = self.data().values()
        nummax = sum(1 for value in values if value == max(values))
        return math.floor(10 / nummax) / 10

    def data(self):
        return {
            "sit": self.sit,
            "concept": self.concept,
            "fact": self.fact
        }

    def __str__(self):
        data = self.data()
        data["confidence"] = self.update_confidence()
        return str(data)


nlp = spacy.load("en_core_web_sm")


def _get_ner(doc):
    ner = {}

    # print("UD type", type(snt_ud), len(snt_ud))
    # print("UD", snt_ud)

    if not doc.ents:
        return False

    ner = []
    # ent: spacy.tokens.span.Span
    for ent in doc.ents:
        if ent.label in ["CARDINAL", "DATE"]:
            continue
        print(ent, ent.label_, ent.lemma_, ent.ent_id)
        # ner[ent.label_] = ent.lemma_
    return ner

    """
    for tok in snt_ud:
    
        if tok["ner"] == "O":
            continue
        if tok["ner"][2:] in ["CARDINAL", "DATE"]:
            continue
        if tok["deprel"] in ["nmod", "nmod:poss"]:
            continue

        # print(tok["ner"], tok["lemma"])
        ner[tok["ner"]] = tok["lemma"]

    return ner
    """


def _get_upos(doc, tok_type):
    ret = []
    for tok in doc:
        if tok.pos_ == tok_type:
            ret.append(tok.lemma_)
    return ret

def _get_articles(doc):
    article_list = []
    for tok in doc:
        if isinstance(tok, list): tok = tok[0]
        if tok.pos_ == "DET":
            article_list.append(tok)
    return article_list


def get_snt_type_probabilities(doc, explain=False):

    pred = Predict()

    ner = _get_ner(doc)



    if ner:
        if explain: print(f"CLF: NER (sit + 10;fact +11)")
        pred.adjust('sit', 10)
        pred.adjust("fact", 11)
    else:
        if explain: print(f"CLF: No NER (fact -5, concept +10)")
        pred.adjust("fact", -5)
        pred.adjust("concept", 10)

    def_article_count = 0
    indef_article_count = 0
    for art in _get_articles(doc):
        if art.lemma_ == "a":
            if explain: print(f"CLF: Indefinite article (concept +10)")
            pred.adjust("concept", 10)
            indef_article_count += 1
            continue
        if art.lemma_ == "the" and def_article_count == 0:
            if explain: print(f"CLF: Definite article (concept -10)")
            pred.adjust("concept", -5)
            def_article_count += 1
            continue

    if def_article_count == 0 and indef_article_count == 0:
        if explain: print(f"CLF: No definite article (concept +10)")
        pred.adjust("concept", 10)

    verbs = _get_upos(doc, "VERB")
    remaining_verbs = verbs.copy()
    if verbs:
        if "have" in verbs:
            if explain: print(f"CLF: 'have' in verbs (fact +10)")
            pred.adjust("fact", 10)
            remaining_verbs.remove("have")

            if len(remaining_verbs) > 1:
                if explain: print(f"CLF: not 'have' in verbs (sit +11)")
                _tmpval = 10 * (1.1 * len(remaining_verbs))
                pred.adjust("sit", _tmpval)

        elif "cause" in verbs:
            if explain: print(f"CLF: 'cause' in verbs (sit -10)")
            pred.adjust("sit", -10)
        else:
            if explain: print(f"CLF: not 'have' in verbs (sit +11)")
            _tmpval = 11 * (1.1 * len(remaining_verbs))
            pred.adjust("sit", _tmpval)


    nouns = _get_upos(doc, "NOUN")
    if "example" in nouns:
        if explain: print(f"CLF: Example in nouns (concept +10)")
        pred.adjust("concept", 10)

    # if remaining_verbs != verbs:
    # print("Remaining VB", remaining_verbs)
    # print("Verbs", verbs)

    auxverbs = _get_upos(doc, "AUX")
    if auxverbs:
        if "be" in auxverbs:
            if explain: print(f"CLF: `be` in AUX (fact +10; concept +10)")
            pred.adjust("fact", 11)
            pred.adjust("concept", 10)

    pred.update_confidence()
    return pred



def clf(snt):
    doc = nlp(snt)
    pred = get_snt_type_probabilities(doc, True)
    return pred


def predict_snt_type(sent):
    sent = "John is a man."
    sent = "Titanic sank in the Atlantic on 1912."
    print(clf(sent))

