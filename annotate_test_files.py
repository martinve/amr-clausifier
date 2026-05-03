#!/usr/bin/env python3

import sys, json, time
import nltk
from extract_info import get_amr_parse
from extract_info import decompose_amr
from logger import logger
import traceback

# nltk.download('punkt')
# nltk.download('punkt_tab')

def read_tests(filename):
    
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    tests = eval("\n".join(lines))
    return tests


def annotate_sentence(sentence):
    stime = time.time()
    amrstr = get_amr_parse(sentence)
    logger.debug(f"Parsed sentence AMR in {round(time.time() - stime, 3)} seconds")
    
    if amrstr == "":
        logger.error("Received empty AMR string. Exiting.")
        sys.exit(-1)

    logger.info("AMR: %s", amrstr)

    stime = time.time()
    res = decompose_amr(amrstr)
    logger.debug(f"Annotated sentence with AMR in {round(time.time() - stime, 3)} seconds")
    return res


def annotate_sent(sent, write_log=True):
    sa = ""
    try:
        logger.info("Annotate: %s", sent)  
        sa = annotate_sentence(sent)
        logger.info("Annotation: %s", sa)
    except Exception as e:
        logger.error("Error annotating sentence: %s", sent)
        if write_log:
            with open("annotation_errors.log", "a") as f:
                f.write("ERR: " + sent + "\n")
        logger.error(repr(e))
        logger.error(traceback.format_exc())

    return sa



def annotate_psg(passage):
    sentences = nltk.sent_tokenize(passage)
    sent_annotations = []

    logger.info(f"Passage: {" ".join(sentences)}")
    logger.info(f"Sentences: {len(sentences)}")

    ret = ""
    for idx, sent in enumerate(sentences):
        stime = time.time()
        annot = annotate_sent(sent)
        logger.debug(f"[{1+idx}/{len(sentences)}] Elapsed: {round(time.time() - stime,3)} seconds")
        if annot:
            sent_annotations.append(annot)

    return " ".join(sent_annotations)



if __name__ == "__main__":

    testset = "wikipedia" # "gsm8k"
    infile = f"tests/{testset}_test.py"
    outfile = f"tests/{testset}_annotated.py"
    maxnum = 100     # if >1, then max number of tests to be processed
    skipfirst = -1  # if >1, then skip first N tests

    tests = read_tests(infile)

    num_tests = len(tests)
    if maxnum and maxnum < num_tests:
        num_tests = maxnum

    start_time = time.time()

    testdict = []
    k = 0

    print(f"Preparing to run {maxnum} tests.")

    for test in tests:
        k += 1

        if skipfirst > 0 and k <= skipfirst:
            continue

        print(f"Process test {k}")

        test_start_time = time.time()

        passage = test[0]
        annotations = annotate_psg(passage)
        testdict.append({
            "test": passage,
            "annotations": annotations,
            "gold": test[1] 
        })

        elapsed = str(round(time.time() - test_start_time,3))
        print(f"Finished annotation {k} in {elapsed} seconds")

        if k >= num_tests:
            break

    print("Testing finished in "+str(round(time.time() - start_time,3))+" seconds")  

    with open(outfile, "w") as f:
        f.write(json.dumps(testdict, indent=2))

    print("Done.")   