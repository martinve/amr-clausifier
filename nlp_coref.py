import spacy
import spacy_experimental

from spacy.tokens import Doc
import pandas as pd

"""
pip install https://github.com/explosion/spacy-experimental/releases/download/v0.6.0/en_coreference_web_trf-3.4.0a0-py3-none-any.whl#egg=en_coreference_web_trf
"""

def init_nlp():
    nlp = spacy.load("en_core_web_sm")
    nlp_coref = spacy.load("en_coreference_web_trf")

    # use replace_listeners for the coref components
    nlp_coref.replace_listeners("transformer", "coref", ["model.tok2vec"])
    nlp_coref.replace_listeners("transformer", "span_resolver", ["model.tok2vec"])

    # we won't copy over the span cleaner
    nlp.add_pipe("coref", source=nlp_coref)
    nlp.add_pipe("span_resolver", source=nlp_coref)

    return nlp


def resolve_references(doc: Doc) -> str:
    """Function for resolving references with the coref ouput
    doc (Doc): The Doc object processed by the coref pipeline
    RETURNS (str): The Doc string with resolved references

    @see: https://github.com/explosion/spaCy/discussions/11585
    """
    # token.idx : token.text
    token_mention_mapper = {}
    output_string = ""
    clusters = [
        val for key, val in doc.spans.items() if key.startswith("coref_head_cluster")
    ]

    print("Head clusters:", clusters)

    # Iterate through every found cluster
    for cluster in clusters:
        first_mention = cluster[0]
        # Iterate through every other span in the cluster
        for mention_span in list(cluster)[1:]:
            # Set first_mention as value for the first token in mention_span in the token_mention_mapper
            token_mention_mapper[mention_span[0].idx] = first_mention.text + mention_span[0].whitespace_

            for token in mention_span[1:]:
                # Set empty string for all the other tokens in mention_span
                token_mention_mapper[token.idx] = ""

    # Iterate through every token in the Doc
    for token in doc:
        # Check if token exists in token_mention_mapper
        if token.idx in token_mention_mapper:
            output_string += token_mention_mapper[token.idx]
        # Else add original token text
        else:
            output_string += token.text + token.whitespace_

    return output_string


if __name__ == "__main__":
    nlp = init_nlp()

    text = "Bill left for Paris. He arrived at noon. Peter was staying there. He was content."
    text = "Pierre_Vinken, 61 years old, will join the board as a nonexecutive director Nov. 29. He will be happy."
    doc = nlp(text)
    ref = resolve_references(doc)
    print(ref)
