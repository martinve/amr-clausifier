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


# Write a mapping function for AMR to SVO triples.


if __name__ == "__main__":

    f = open("amrtest_input.txt", "r")
    amr = f.read()
    f.close()

    main(amr)
