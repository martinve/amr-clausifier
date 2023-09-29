from pprint import pprint
import amr_clausifier as cl
import penman

def main2():
    clauses = cl.extract_clauses(amr)
    pprint(clauses, indent=2)

def main2(amr):
    g = penman.decode(amr)
    pprint(g.triples)
    pprint(g.variables())


# Write a function that takes AMR string as input and returns a list of clauses. Each clause is a triple (subject, relation, object) where subject and object are nodes and relation is a string.


if __name__ == "__main__":

    f = open("amrtest_input.txt", "r")
    amr = f.read()
    f.close()

    main(amr)
