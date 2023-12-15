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


# source: https://www.isi.edu/~ulf/amr/lib/amr-dict.html
# Roles: https://github.com/amrisi/amr-guidelines/blob/master/amr.md#special-frames-for-roles
amr_dict_roles = {
    'have-rel-role-91': {
        'roles': {
            ':ARG0': {'key': 'entityA'},
            ':ARG1': {'key': 'entityB'},
            ':ARG2': {'key': 'entityA_role'},
            ':ARG3': {'key': 'entityB_role'},
            ':ARG4': {'key': 'Basis'}  # relationship basis (contract, case; rarely used)
        }
    },
    'have-org-role-91': {
        'roles': {
            ':ARG0': {'key': "Agent"},
            ':ARG1': {'key': 'Organization'},
            ':ARG2': {'key': 'Role'},
            ':ARG4': {'key': 'Responsibility'}
        }
    },
    "have-degree-91": { # https://www.isi.edu/~ulf/amr/ontonotes-4.0-frames/have-degree-v.html
        "roles": {
            ":ARG0": {'key': "Entity"},
            ":ARG1": {'key': "Attribute"},
            ":ARG2": {'key': "Degree"},
            ":ARG3": {'key': "Compared-to"},
            ":ARG4": {'key': "Superlative"},
            ":ARG5": {'key': "Reference"}
        }
    }
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