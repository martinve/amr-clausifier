import json
import os
import subprocess
import pprint

solver_path = os.path.abspath("./solver/")
solver_fname = solver_path + "/gk"
solver_in_fname = solver_path + "/gk_in.js"


def run_solver(question, print_logic=False):

    js = json.dumps(question, indent=2)
    # print("js:", js)
    pp = pprint.pformat(question, indent=2, compact=False)
    instr = pp.replace("'", "\"")
    if print_logic:
        print("\nProver input:\n", instr)

    infile = open(solver_in_fname, "w")
    infile.write(instr)
    infile.close()

    path = solver_fname
    params = solver_in_fname

    calc = subprocess.Popen([path, params, "-mbsize", "100"], stdout=subprocess.PIPE).communicate()[0]
    sres = calc.decode('ascii')

    if print_logic:
        print("prover output:\n", sres)
    if "\"answer\": true" in sres:
        if "\"confidence\": 1" in sres:
            result = True
        else:
            result = False
    elif "\"answer\": false" in sres:
        result = False
    else:
        result = None
    print("result:",result)
    return result
