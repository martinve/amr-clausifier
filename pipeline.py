import penman
import pprint
import propbank.propbank_api as pb
import propbank.propbank_amr_api as pbamr



"""
For NER types: @see: https://github.com/amrisi/amr-guidelines/blob/master/amr.md
"""

amr_ner_types = {
    "individual": ["person", "family", "animal", "language", "nationality", "ethnic-group", "regional-group", "religious-group", "political-movement"],
    "organization": ["company", "government-organization", "military", "criminal-organization", "political-party", "market-sector", "school", "university", "research-institute", "team", "league"],
    "location": ["location", "city", "city-district", "county", "state", "province", "territory", "country", "local-region", "country-region", "world-region", "continent", "ocean", "sea", "lake", "river", "gulf", "bay", "strait", "canal; peninsula", "mountain", "volcano", "valley", "canyon", "island", "desert", "forest moon", "planet", "star", "constellation"],
    "facility": [ "facility", "airport", "station", "port", "tunnel", "bridge", "road", "railway-line", "canal", "building", "theater", "museum", "palace", "hotel", "worship-place", "market", "sports-facility", "park", "zoo", "amusement-park"],
    "event": ["event", "incident", "natural-disaster", "earthquake", "war", "conference", "game", "festival"],
    "product": ["product", "vehicle", "ship", "aircraft", "aircraft-type", "spaceship", "car-make", "work-of-art", "picture", "music", "show", "broadcast-program"],
    "publication": ["publication", "book", "newspaper", "magazine", "journal"],
    "natural-object": ["natural-object"],
    "misc": ["award", "law", "court-decision", "treaty", "music-key", "musical-note", "food-dish", "writing-script", "variable", "program"]
}



def graph_encode_snt(triples, sent):
    """
    Encode sentence metadata to AMR graph
    """
    graph = penman.Graph(triples)
    graph.metadata["snt"] = sent
    graph = penman.encode(graph)
    return graph



def get_propbank_mappings(triples):
    mappings_dict = {}
    roles = None
    for el in triples:

        if pb.is_amr_word(el[2]):
            #roles = describe_amr_role(el[2])
            roles = pbamr.describe(el[2])
        elif pb.is_propbank_word(el[2]):
           roles = pb.describe(el[2])

        if roles:
            mappings_dict[el[0]] = roles
            roles = None

    return mappings_dict


def apply_propbank_mappings(triples, propbank_mappings):
    for idx, it in enumerate(triples):
        if it[0] not in propbank_mappings.keys():
            continue
        if "roles" in propbank_mappings[it[0]].keys():
            if it[1] in propbank_mappings[it[0]]["roles"].keys():
                newrole = propbank_mappings[it[0]]["roles"][it[1]]["key"]
                triples[idx] = (it[0], newrole, it[2])


    return triples


def _get_ner_category(needle):
    for category in amr_ner_types.keys():
        for elem in amr_ner_types[category]:
            if elem == needle:
                return category
    return None

def map_ner_types(triples):
    debugs = []
    for idx, it in enumerate(triples):
        if it[1] != ":instance":
            continue
        category = _get_ner_category(it[2])
        if category:
            debugs.append(["cat", it[2], category, it[0]])
            triples.remove(triples[idx])
            # triples[idx] = (it[0], category, it[2])
            triples.append((it[0], "type", it[2]))
            triples.append((it[0], "cat", category))

    print("NER Mappings:")
    pprint.pprint(debugs, indent=2)

    return triples


def get_role_labels():
    return pb.get_role_labels()