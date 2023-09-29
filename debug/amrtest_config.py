# AMR clausification: no output
no_debug = {
    "debug_amr": False,
    "debug_propbank": False,
    "debug_get_attribute_values": False,
    "debug_print_edges": False,
    "debug_attribute_value_map": False,
    "debug_triples": False,
    "debug_concept_values": False,
    "debug_concept_edges": False,
    "debug_attr_value_map": False,
    "debug_edge_replacements": False,
    "debug_clauses": False
}

# AMR clausification: full output
full_debug = {
    "debug_amr": True,
    "debug_propbank": True,
    "debug_get_attribute_values": True,
    "debug_print_edges": True,
    "debug_attribute_value_map": True,
    "debug_triples": True,
    "debug_concept_values": True,
    "debug_concept_edges": True,
    "debug_attr_value_map": True,
    "debug_edge_replacements": True,
    "debug_clauses": True
}

# AMR clausification: dev output
dev_debug = {
    "debug_amr": True,
    "debug_propbank": True,
    "debug_triples": False,
    "debug_get_attribute_values": False,
    "debug_print_edges": False,
    "debug_attribute_value_map": False,
    "debug_concept_values": False,
    "debug_concept_edges": True,
    "debug_attr_value_map": False,
    "debug_edge_replacements": False,
    "debug_clauses": True
}


locals().update(full_debug)
# locals().update(no_debug)