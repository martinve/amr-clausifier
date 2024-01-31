import pprint
import sys

import nlp
from amrlib.alignments.faa_aligner import FAA_Aligner
from amrlib.alignments.rbw_aligner import RBWAligner
from amrlib.graph_processing.annotator import add_lemmas
import penman




def get_alignments_rbw(sent, amr_graph, debug=False):
    penman_graph = add_lemmas(amr_graph, snt_key='snt')
    aligner = RBWAligner.from_penman_w_json(penman_graph)
    graph_string = aligner.get_graph_string()

    g = penman.decode(graph_string)
    alignment_strings = g.metadata['alignments']

    debug = True
    if debug:
        print("RBW_align")
        print(graph_string)

    amr_alignments = penman.surface.alignments(g)
    role_alignments = penman.surface.role_alignments(g)

    text_alignments = alignment_strings.strip().split(" ")

    return amr_alignments, text_alignments


def get_alignments_faa(sent, amr_graph, debug=False):
    aligner = FAA_Aligner()

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



def get_alignments(sent, amr_graph, debug=False):
    return get_alignments_rbw(sent, amr_graph, debug)



def map_alignments(snt_text, amr_alignments):
    """
    Align AMR graph fragments to words in a sentence.

    In: sentence text, list of AMR alignments.
    Out: A list of tokens mapped to graph fragments.

    First we create a list of words t = (w, []) where w is the word and t_1 an empty list
    Then we iterate over all AMR alignments. We get the alignment index and add
    a graph fragment to the respective element in the word list.

    """

    tok_words = nlp.tokenize_sentence(snt_text)

    # print("Words:", tok_words)
    # print("Alignments")
    # pprint.pprint(amr_alignments, indent=2)

    word_list = []
    for w in tok_words:
        word_list.append((w, []))

    # print("\n aligner.map_alignments() Alignment keys:")
    # pprint.pprint(amr_alignments.keys(), indent=2)

    for k in amr_alignments.keys():
        a: penman.surface.Alignment = amr_alignments[k]
        word_idx = a.indices[0]
        word_list[word_idx] = (word_list[word_idx][0], k)

    # print("Word List")
    # pprint.pprint(word_list, indent=2)

    return word_list


def _tuple_remove_redundant(triples, word):
    triples_copy = triples.copy()
    for key, data in enumerate(triples):
        if data[0] in ["name", "instance"] and data[1].lower() == word.lower():
            triples_copy.pop(key)
    return triples_copy



def map_triples(alignment_map, triple_map):
    """
    Map word-graph alignments to the values from grouped triples.
    """

    alignment_map_copy = alignment_map.copy()
    for idx, word_tuple in enumerate(alignment_map):
        if len(word_tuple[1]) == 0:
            continue

        word = word_tuple[0]
        map_key = word_tuple[1][0]

        print("WM_Keys", word, map_key)

        if map_key not in triple_map.keys():
            continue

        triples = triple_map[map_key]
        triples = _tuple_remove_redundant(triples, word)
        alignment_map_copy[idx] = (word_tuple[0], triples)

    '''
    print('===')
    pprint.pprint(triple_map)
    print("<<<")
    pprint.pprint(alignment_map)
    sys.exit(-1)
    '''


    return alignment_map_copy


