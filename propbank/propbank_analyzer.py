import os, sys
from glob import glob
import csv

import nltk
from xml.etree import ElementTree as ET


def extract_propbank_frames():
    framedir = nltk.data.path[0] + "/corpora/propbank-3.4/frames"
    k = 0
    for file in sorted(glob(framedir + "/*.xml")):

        filename = os.path.basename(file)

        tree = ET.parse(file)
        root = tree.getroot()

        predicates = root.findall("predicate")
        for pred in predicates:
            lemma = pred.attrib["lemma"]
            rolesets = pred.findall("roleset")
            for rs in rolesets:
                # print(lemma, rs.attrib["id"], rs.attrib["name"])
                roles = rs.findall("roles/role")
                for role in roles:
                    print(rs.attrib["id"], role.attrib["f"], role.attrib["descr"], sep="\t")
                    # print(f"ARG{role.attrib['n']}", role.attrib["f"], role.attrib["descr"], sep="\t")
                    k += 1

        if k > 100000000000000:
            break


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


if __name__ == "__main__":
    # extract_propbank_frames()
    # get_propbank_args_summary()
    get_propbank_label_summary()
    # print("Done", k)