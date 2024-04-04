import amrutil
import udutil
import classifier.sentence_heuristic_classifier as snt_clf


class PassageCtx:
    def __init__(self, idx, ud, amr):
        self.idx = idx
        self.ud = ud
        self.amr = amr



    def context(self):
        return  {
            "idx": self.idx,
            "type": snt_clf.snt_type_label(snt_clf.predict_snt_type(ud)),
            "question": False,
            "entities": udutil.get_named_entities(self.ud),
            "verbs": udutil.get_verbs(self.ud),
            "ud_root": udutil.get_root(self.ud),
            "amr_root": amrutil.get_root(self.amr)
        }
