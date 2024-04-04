import propbank_amr_api as apb
import propbank_analyzer as a

count = 0

def get_predicate(descr, role):


    descr = descr.replace('the ', "")
    descr = descr.replace(",", "")
    descr = descr.replace("/", " ")
    descr = descr.replace("'", "")
    descr = descr.lower()
    words = descr.split(' ')

    if len(words) == 1:
        return descr

    if words[0] in ["start", "end", 'description', "unit", "period", "attribute", "id", 'venue', "value", "p-value", "r-squared", "deviation", "experience", "source", "zip", "state", "degree", "experience", "superlative", "lower", "upper", "radius", "confidence", "text", "center", "photographer", "range", "direction", "sound", "type", "significance", "alternative", "element", "clause", "resemble"]:
        return words[0]

    keys = ["event", "thing", "entity", "polarity", "interval", "category", "resemblance", "item", "quantity", "organization", "condition", "holder", "role", "referent", "threshold", "perceiver", "basis", "text", "scale", "size", "constant", "figure", "part"]
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



if __name__ == "__main__":
    file = apb.get_roleset_file()
    rolelist = a.extract_propbank_file(file)

    k = 0
    predicates = set()
    roles = set()
    for el in rolelist:
        predicates.add(el[0])
        roles.add(el[1])
        pred = get_predicate(el[2], el[1])
        if pred:
            print(pred)
        else:
            print(el)
            k += 1

    print(len(predicates), len(rolelist), len(roles), k, len(rolelist) - k)
    print(predicates)