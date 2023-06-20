import sys

import config

class RoleReplacer:

    def __init__(self):
        self.role_dict = config.role_dict
        self.amr_dict = config.amr_dict


    def update_role_dict(self, role_dict):
        self,role_dict = role_dict

    def replace(self, clauses, context):
        print(clauses)
        assert(type(context) == dict)

        snt_type = context["type"]

        for k, clause in enumerate(clauses):
            clauses[k] = self.replace_roles(clause, snt_type)
            clauses[k] = self.replace_amr_dict_items(clause)
        return clauses

    def replace_roles(self, clause, snt_type):
        item = clause[0]
        if isinstance(item, str):
            clause[0] = self.role_dict.get(item, item)
        return clause

    def replace_amr_dict_items(self, clause):
        for i, item in enumerate(clause):
            if not isinstance(item, str):
                continue
            clause[i] = self.amr_dict.get(item, item)
        return clause
