import os, sys
from glob import glob
import csv

import nltk
from xml.etree import ElementTree as ET

idx = 1

def extract_amr_frames(debug=False):
    file = nltk.data.path[0] + "/corpora/propbank-3.4/AMR-UMR-91-rolesets.xml"
    if debug:
        print("ID", "Frameset", "Arg", "Func", "Descr", sep='\t')
    extract_propbank_file(file, debug)


def extract_propbank_frames(debug=False):
    framedir = nltk.data.path[0] + "/corpora/propbank-3.4/frames"
    k = 0

    if debug:
        print("ID", "Frameset", "Arg", "Func", "Descr", sep='\t')

    for file in sorted(glob(framedir + "/*.xml")):
        extract_propbank_file(file, debug)
        k += 1
        if k > 100000000000000:
            break


def extract_propbank_file(file, debug=False):
    global idx

    filename = os.path.basename(file)

    tree = ET.parse(file)
    root = tree.getroot()

    rolelist = []

    predicates = root.findall("predicate")
    for pred in predicates:
        lemma = pred.attrib["lemma"]
        rolesets = pred.findall("roleset")
        for rs in rolesets:
            # print(lemma, rs.attrib["id"], rs.attrib["name"])
            roles = rs.findall("roles/role")
            for role in roles:
                descr = role.attrib["descr"].replace('"', '')
                roledata = [rs.attrib["id"], f"ARG{role.attrib['n']}", role.attrib["f"], descr]
                rolelist.append(roledata)
                if debug:
                    print(idx, rs.attrib["id"], f"ARG{role.attrib['n']}", role.attrib["f"], descr, sep="\t")
                idx += 1
    return rolelist

def get_propbank_args_summary():

    with open("propbank_args.txt") as file:
        reader = csv.reader(file, delimiter="\t")
        role_cls = {}
        for line in reader:
            cls = line[1]
            if cls not in role_cls.keys():
                role_cls[cls] = 1
            else:
                role_cls[cls] += 1

    print(dict(sorted(role_cls.items(), key=lambda x:x[1], reverse=True)))


def normalize_description(descr):
    descr = descr.lower()
    descr = descr.replace("'", "")

    begin_words = ['agent', "topic", "causer", "utterance", "victim", "time", "target", "experiencer", "source", "cause", "activity", "theme", "subject"]
    for w in begin_words:
        if descr.startswith(w):
            return w

    contain_words = ["thing", "entity", "start", "end"]
    for w in contain_words:
        if w in descr:
            return w

    return descr


def get_propbank_label_summary():
    with open("propbank_args.txt") as file:
        reader = csv.reader(file, delimiter="\t")
        k = 0
        descr_list = []
        for line in reader:
            k += 1
            descr = normalize_description(line[2])
            if descr not in descr_list:
                descr_list.append(descr)
                continue

        print("Total:", k, "Unique:", len(descr_list))
        # return

        descr_list = sorted(descr_list)
        # for it in descr_list: print(it)

        k = 0
        for descr in descr_list:
            descrarr = descr.split(" ")
            if len(descrarr) > 1:
                print(k, descr)

                k += 1
"""
# import propbank_amr_api as pbamr
def get_amr_elem(key):
    pbamr.describe(key)

"""


if __name__ == "__main__":
    extract_propbank_frames(True)
    # extract_amr_frames(True)
    # get_propbank_args_summary()
    # get_propbank_label_summary()
    # print("Done", k)
    # get_amr_elem("have-org-role-91")