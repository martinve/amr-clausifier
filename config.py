debug_print_flag = False
debug_graph_construction = False
debug_clauses = False

server_port = 9002
server_host = "localhost"
server_uri = f"http://{server_host}:{server_port}"
cache_file = "parser_cache"
log_file = "server_log"

dummy_name = "Dummyname" # new vars start with this
question_var = "?:Q"

snt_ud = None

sentence_label_dict = {
    "concept": 1,
    "fact": 2,
    "sit": 3
}

role_dict = {
    ":arg0": "agent",
    ":arg1": "patient",
    ":arg2": "instrument",
    ":arg3": "startingPoint",
    ":arg4": "endingPoint",
    ":arg5": "modifier"
}


amr_dict = {
    ":domain": "isa",
    ":mod": "property", # "hasProperty",
    ":poss": "belongs", # "belongsTo",
    ":location": "located", # "isLocatedAt",
    "have-org-role-91": "role", # "hasRole"
    "have-rel-role-91": "role",
    ":name": "hasName",
    ":instrument": "instrument",
    ":quant": "$count"
}

# source: https://www.isi.edu/~ulf/amr/lib/amr-dict.html
# Roles: https://github.com/amrisi/amr-guidelines/blob/master/amr.md#special-frames-for-roles
amr_dict_roles = {
    'have-rel-role-91': {
        'roles': {
            ':ARG0': 'entityA',
            ':ARG1': 'entityB',
            ':ARG2': 'entityA_role',
            ':ARG3': 'entityB_role',
            ':ARG4': 'Basis'  # relationship basis (contract, case; rarely used)
        }
    },
    'have-org-role-91': {
        'roles': {
            ':ARG0': "Agent",
            ':ARG1': 'Organization',
            ':ARG2': 'Role',
            ':ARG4': 'Responsibility'
        }
    },
    "have-degree-91": { # https://www.isi.edu/~ulf/amr/ontonotes-4.0-frames/have-degree-v.html
        "roles": {
            ":ARG0": "Entity",
            ":ARG1": "Attribute",
            ":ARG2": "Degree",
            ":ARG3": "Compared-to",
            ":ARG4": "Superlative",
            ":ARG5": "Reference"
        }
    }
}

