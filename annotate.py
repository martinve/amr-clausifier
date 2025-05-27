#!/usr/bin/env python3

import sys, json, time
import nltk
from extract_info import get_amr_parse
from extract_info import decompose_amr
from logger import logger

# nltk.download('punkt')
# nltk.download('punkt_tab')

def read_tests(filename):
    
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    tests = eval("\n".join(lines))
    return tests


def annotate_sentence(sentence):
    amrstr = get_amr_parse(sentence)
    logger.info("AMR: %s", amrstr)
    res = decompose_amr(amrstr)
    return res


def annotate(passage):
    sentences = nltk.sent_tokenize(passage)
    sent_annotations = []

    ret = ""
    for sent in sentences:
        try:
            logger.info("Annotate: %s", sent)  
            sa = annotate_sentence(sent)
            logger.info("Annotation: %s", sa)
            sent_annotations.append(sa)
        except:
            logger.error("Error annotating sentence: %s", sent)
            with open("annotation_errors.log", "a") as f:
                f.write("ERR:" + sent + "\n")

            continue

    return " ".join(sent_annotations)



if __name__ == "__main__":

    testset = "wikipedia" # "gsm8k"
    infile = f"tests/{testset}_test.py"
    outfile = f"tests/{testset}_annotated.py"
    maxnum = -1     # if >1, then max number of tests to be processed
    skipfirst = -1  # if >1, then skip first N tests

    tests = read_tests(infile)

    start_time = time.time()

    testdict = []
    k = 0

    print(f"Preparing to run {len(tests)} tests.")

    for test in tests:
        k += 1

        if skipfirst > 0 and k <= skipfirst:
            continue

        print(f"Process test {k}")

        test_start_time = time.time()

        passage = test[0]
        annotations = annotate(passage)
        testdict.append({
            "test": passage,
            "annotations": annotations,
            "gold": test[1] 
        })

        elapsed = str(round(time.time() - test_start_time,3))
        print(f"Finished test {k} in {elapsed} seconds")

        if maxnum > 0 and k >= maxnum:
            break

    print("Testing finished in "+str(round(time.time() - start_time,3))+" seconds")  

    with open(outfile, "w") as f:
        f.write(json.dumps(testdict, indent=2))

    print("Done.")   