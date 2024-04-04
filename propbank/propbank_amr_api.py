import sys

import propbank.propbank_api as api
from xml.etree import ElementTree as ET
import nltk

def _transform_predicate(descr, key):

    if key != "Verb-specific":
        return key

    descr = descr.replace('the ', "")
    descr = descr.replace(",", "")
    descr = descr.replace("/", " ")
    descr = descr.replace("'", "")
    descr = descr.lower()
    words = descr.split(" ")

    if len(words) == 1:
        return descr



    if words[0] in ["start",  "role", "end", 'description', "degree", "unit", "period", "attribute", "id", 'venue', "value", "p-value", "r-squared", "deviation", "experience", "source", "zip", "state", "degree", "experience", "superlative", "lower", "upper", "radius", "confidence", "text", "center", "photographer", "range", "direction", "sound", "type", "significance", "alternative", "element", "clause", "resemble"]:
        return words[0]

    keys = ["event", "thing", "entity", "polarity", "interval", "category", "resemblance", "item", "quantity", "organization", "condition", "holder", "referent", "threshold", "perceiver", "basis", "text", "scale", "size", "constant", "figure", "part"]
    for key in keys:
        if key in words:
            return key

    replace_dict = {
        "instead of that": "instead_of",
        "title of office held": "office",
        "worst score on scale": "min_score",
        "best score on scale": "max_score",
        "street number": "street_no",
        "of what": "example_of",
        "intensifier downtoner or equal": "modifier"
    }

    if descr in replace_dict.keys():
        return replace_dict[descr]


def _prepare_propbank_word(word):
    word = ".".join(word.rsplit("-", 1))
    return word

def get_roleset_file():
    return nltk.data.path[0] + "/corpora/propbank-3.4/AMR-UMR-91-rolesets.xml"


def describe(roleset_id, do_print=False, examples=False):
    roleset_key = _prepare_propbank_word(roleset_id)

    file = get_roleset_file()

    tree = ET.parse(file)
    root = tree.getroot()

    path = f"predicate/roleset[@id='{roleset_key}']"
    #print("Get from path:", path)
    rolesets = root.findall(path)

    if len(rolesets):
        rs = rolesets[0]
        data = api.extract_data(rs, roleset_id)

        roles = data["roles"].copy()

        for idx in data["roles"].keys():
            role = roles[idx]
            key = role["key"]
            descr = role["descr"]
            roles[idx]["key"] =  _transform_predicate(descr, key)

        data["roles"] = roles
        return data


