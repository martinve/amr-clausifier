import sys
import pprint
from collections import OrderedDict
from amrlib.alignments.faa_aligner import FAA_Aligner
import penman

aligner = FAA_Aligner()

def get_alignments(sent, amr_graph, debug=False):
    sents = [sent]
    graph_strings = [amr_graph]
    amr_surface_aligns, alignment_strings = aligner.align_sents(sents, graph_strings)

    amr_align = amr_surface_aligns[0]
    alignment_strings = alignment_strings[0]

    g = penman.decode(amr_align)
    print("Aligned graph:")
    print(penman.encode(g))

    amr_alignments = penman.surface.alignments(g)
    role_alignments = penman.surface.role_alignments(g)
    # amr_alignments.update(role_alignments)

    print("AMR alignments")
    pprint.pprint(penman.surface.alignments(g))

    print("Role alignments")
    pprint.pprint(penman.surface.role_alignments(g))



    text_alignments = alignment_strings.strip().split(" ")

    return amr_alignments, text_alignments



def get_aligned_graph(sent, graph):
    pass



def map_alignments(snt_text, amr_alignments, text_alignments):
    tok_words = tokenize_sentence(snt_text)
    word_list = []
    for w in tok_words:
        word_list.append((w, []))

    print("Alignment keys", amr_alignments.keys())

    for k in amr_alignments.keys():
        a: penman.surface.Alignment = amr_alignments[k]
        word_idx = a.indices[0]
        word_list[word_idx] = (word_list[word_idx][0], k)

    return word_list


def map_triples(alignment_map, triple_map):
    for idx, word in enumerate(alignment_map):
        if len(word[1]) == 3:
            key = word[1][0]
            if key in triple_map.keys():
                alignment_map[idx] = (word[0], triple_map[key])
    return alignment_map


def tokenize_sentence(snt_text, debug=False):
    words = snt_text.split(" ")
    if debug:
        words_list = []
        for idx, word in enumerate(words):
            words_list.append((idx, word))
        print(words_list)
    return words
