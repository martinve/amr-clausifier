import propbank.propbank_api as api
from xml.etree import ElementTree as ET
import nltk

def _prepare_propbank_word(word):
    word = ".".join(word.rsplit("-", 1))
    return word

def describe(roleset_id, do_print=False, examples=False):
    roleset_key = _prepare_propbank_word(roleset_id)

    file = nltk.data.path[0] + "/corpora/propbank-3.4/AMR-UMR-91-rolesets.xml"

    tree = ET.parse(file)
    root = tree.getroot()

    path = f"predicate/roleset[@id='{roleset_key}']"
    #print("Get from path:", path)
    rolesets = root.findall(path)

    if len(rolesets):
        rs = rolesets[0]
        return api.extract_data(rs, roleset_id)

