pb_role_modifiers = {
    "COM": "Comitative",
    "LOC": "Locative",
    "DIR": "Directional",
    "GOL": "Goal",
    "MNR": "Manner",
    "TMP": "Temporal",
    "EXT": "Extent",
    "REC": "Reciprocals",
    "PRD": "Secondary_Predication",
    "PRP": "Purpose",
    "CAU": "Cause",
    "DIS": "Discourse",
    "ADV": "Adverbials",
    "ADJ": "Adjectival",
    "MOD": "Modal",
    "NEG": "Negation",
    "DSP": "Direct_Speech",
    "LVB": "Light_Verb",
    "CXN": "Construction",
    "PAG": "Agent",
    "PPT": "Patient",
    "VSP": "Verb-specific"
}


# AMR clausification: dev output
dev_debug = {
    "debug_amr": False,
    "debug_propbank": True,
    "debug_triples": False,
    "debug_get_attribute_values": False,
    "debug_print_edges": False,
    "debug_attribute_value_map": False,
    "debug_concept_values": False,
    "debug_concept_edges": False,
    "debug_attr_value_map": False,
    "debug_edge_replacements": False,
    "debug_clauses": False,
    "debug_warnings": False
}

locals().update(dev_debug)