import re
import sys
from pathlib import Path
from xml.etree import ElementTree
import csv
from nltk.corpus import treebank, LazyCorpusLoader
from nltk.corpus.reader.propbank import PropbankCorpusReader
from texttable import Texttable

# see: https://sites.pitt.edu/~naraehan/ling1330/lecture23_PropBank_in_NLTK.html

# If datasets have not been loaded

"""
@see: Modifiers in Propbank annotation guidelines
NOTE: Modifiers are present in Propbank release 3.4 but not in release 1.0 
that is available via nltk.download()
"""

import propbank.propbank_config as acfg
import settings as cfg

modifiers = acfg.pb_role_modifiers


def load_data():
    import nltk
    nltk.download("propbank")
    nltk.download("treebank")


def is_propbank_word(word):
    if len(word) < 2:
        return
    check = bool(re.match("[a-z-]*-[0-9]{2}", word))
    return check


def is_amr_word(word):
    return '-91' == word[-3:]


def _prepare_propbank_word(word):
    word = ".".join(word.rsplit("-", 1))
    word = word.replace("-", "_")
    return word

def describe(roleset_id, do_print=False, examples=False):
    roleset_key = _prepare_propbank_word(roleset_id)

    print("\nGet Propbank roleset:\n", "key=", roleset_key, "ID", roleset_id,"\n")

    try:
        pb = init_propbank()
        rs = pb.roleset(roleset_key)
    except ValueError:
        # print(f"No PropBank role found for {roleset_id}")
        return {}


    roles = {}
    rows = []

    aliases = rs.findall("aliases/alias")
    lemmas = {}
    for el in aliases:
        pos = el.attrib.get("pos", "")
        lemma = el.text
        lemmas[pos] = lemma

    for role in rs.findall('roles/role'):
        f = role.attrib.get('f', "")

        rolelist = []
        for cls in role.findall("vnrole"):
            theta = cls.attrib["vntheta"]
            if theta not in rolelist:
                rolelist.append(theta)
        thetas = "|".join(rolelist)

        # print(f"ARG{role.attrib['n']}: {role.attrib['descr']} {f} {thetas}")
        key = ":ARG" + str(role.attrib['n'])
        descr = role.attrib.get("descr", "")

        mod = role.attrib.get("f", "")
        if mod:
            mod = modifiers.get(mod.upper(), mod)

        rows.append([key, thetas, descr, mod])
        roles.update({key: {"key": mod, "descr": descr}})


    if examples:
        print("\n=== Usage Examples ===\n")
        k = 1
        tbl = Texttable()
        tbl.set_deco(Texttable.HEADER)
        for ex in rs.findall("example"):
            text = ex.find("text").text
            text = text.replace("\n", "")
            text = " ".join(text.split())
            text = text.replace("*trace*", "")
            text = text.strip()
            tbl.add_row([ex.attrib["name"], str(text)])
        print(tbl.draw())

    return {
        "roleset": roleset_id,
        "lemmas": lemmas,
        "roles": roles
    }

    # return [[role[0], role[1]] for role in roles]


def sample():
    for item in ["abstain.01", "like.01", "stab.01", "color.01"]:
        describe(item, True, True)


def inflect(roleset_id):
    instances = propbank.instances()
    k = 0
    for inst in instances:
        if inst.roleset == roleset_id:
            break
    return inst.inflection


def explore():
    """
    Get a list of unique inflections for the whole corpus.
    """

    instances = propbank.instances()

    k = 0

    known_inflections = []

    while k < len(instances):

        # PropBankInstance
        inst = instances[k]
        # print(inst.fileid, inst.sentnum, inst.wordnum, inst.tagger, inst.inflection, inst.roleset, inst.arguments, inst.predicate)

        # PropbankInflection
        inf = str(inst.inflection)
        if inf not in known_inflections:
            known_inflections.append(inf)

            if inf[0] == "g" or True:
                print(inst.inflection, "\t", inst.roleset)

            # print(f"Roleset: {inst.roleset}, Inflection: {inst.inflection}")

        k += 1
    print(k, "Inflections:", len(known_inflections))

class MyPropbankCorpusReader(PropbankCorpusReader):
        def roleset(self, roleset_id):
            """
            :return: the xml description for the given roleset.
            """
            baseform = roleset_id.split(".")[0]


            # print(f"Searching for roleset: {roleset_id}")

            scriptpath = Path(__file__).resolve().parent
            # print(__name__, "Script_path:", scriptpath)
            framefile = scriptpath / "framelist.tsv"

            with open(framefile) as file:
                tsv_file = csv.reader(file, delimiter="\t")
                for line in tsv_file:
                    # print(f"|{line[0]}|{roleset_id}")
                    if line[0] == roleset_id:
                        baseform = line[1]
                        # print("Found:", baseform)
                        break

            framefile = "frames/%s.xml" % baseform

            if framefile not in self._framefiles:
                # print("Frameset file for %s not found" % roleset_id)
                raise ValueError("Frameset file for %s not found" % roleset_id)

            # n.b.: The encoding for XML fileids is specified by the file
            # itself; so we ignore self._encoding here.
            with self.abspath(framefile).open() as fp:
                etree = ElementTree.parse(fp).getroot()
            for roleset in etree.findall("predicate/roleset"):
                if roleset.attrib["id"] == roleset_id:
                    return roleset
            raise ValueError(f"Roleset {roleset_id} not found in {framefile}")

def init_propbank():
    """
    Overwrite reader for 'nltk.corpus.reader.propbank'
    :return:
    """

    parse_fileid_xform = lambda filename: re.sub(r"^wsj/\d\d/", "", filename)
    reader = MyPropbankCorpusReader


    reader = PropbankCorpusReader = LazyCorpusLoader(
        cfg.propbank_corpus,
        reader,
        "prop.txt",
        framefiles=r"frames/.*\.xml",
        verbsfile="verbs.txt",
        parse_fileid_xform=parse_fileid_xform,
        parse_corpus=treebank,
    )

    """
    :param parse_corpus: The corpus containing the parse trees
        corresponding to this corpus.  These parse trees are
        necessary to resolve the tree pointers used by propbank.
    """

    return reader


if __name__ == "__main__":
    pb = init_propbank()

    inp = False

    if len(sys.argv) > 1:
        inp = sys.argv[1]

    if inp:
        roles = describe(inp, True, True)
        print(roles)

    else:
        roles = describe("good.02", True, True)
        # print("Done")
        # explore()
        # sample()
