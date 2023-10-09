from amrlib.alignments.faa_aligner import FAA_Aligner
import debug.amr_test_cases as tc
import pprint
import re

inference = FAA_Aligner()

"""
To use the software we must first install FAA aligner binaries
"""

def test_faa_aligner(sent, graph):
    sents = [sent]
    graph_strings = [graph]
    amr_surface_aligns, alignment_strings = inference.align_sents(sents, graph_strings)
    amr_align = amr_surface_aligns[0]
    alignment_strings = alignment_strings[0]
    alignments = alignment_strings.strip().split(" ")
    pprint.pprint(alignments)
    print(amr_align)

    toks = sent.split(" ")

    for it in alignments:
        i, j = it.split("-")
        print(toks[int(i)], i, j)




if __name__ == "__main__":
    graph, sent = tc.get_example_snt(13)
    test_faa_aligner(sent, graph)

