from pprint import pprint
import amr_clausifier as cl
import penman

def main2(amr):
    clauses = cl.extract_clauses(amr)
    pprint(clauses, indent=2)

def main(amr):
    g = penman.decode(amr)

    av = cl.get_attribute_values(g)
    cv = cl.get_concept_values(g)

    v = cl.get_concept_edges(g, cv, av)

    v = cl.edges_replace_attribute_values(v, av)

    rd = cl.get_propbank_role_dict(g)

    re = cl.replace_edges_value_keys(v, cv)

    pprint(re, indent=2)


    e = g.edges()
    print(set(v) == set(e))

    return

    ts = g.triples

    vs = {}
    for v in g.variables():
        if v not in vs.keys():
            vs[v] = []

    for t in ts:
        print(t, t[0])
        if t[0] in vs.keys():
            vs[t[0]].append(t)
            ts.remove(t)
            continue

    print(g.variables())
    print("----")
    print(ts)
    print("----")
    pprint(vs, indent=2)
    print("----")
    pprint(g.triples, indent=2)


# Write a function that takes AMR string as input and returns a list of clauses. Each clause is a triple (subject, relation, object) where subject and object are nodes and relation is a string.


if __name__ == "__main__":

    f = open("amrtest_input.txt", "r")
    amr_in = f.read()
    f.close()

    main2(amr_in)
