import re
import json
import sys
import pprint

def strip_annotations(annot_text):
    text = re.sub("\{.*?\}","",annot_text)
    return text


class clause1:
    def __init__(self, predicate, data, value):
        self.predicate = predicate
        self.data = data
        self.value = value

class clause2:
    def __init__(self, predicate, event, data, value):
        self.predicate = predicate
        self.event = event
        self.data = data
        self.value = value



def replace_predicate_key(key):

    replacement_keys = {
        "evt": "event",
        "cat": "category",
        "descr":  "description"
    }

    if key not in replacement_keys.keys():
        return key
    
    return replacement_keys[key]

def extract_json(text):

    match = re.search(r'\{.*?\}(.*)', text)
    if match:
        return match.group(0).strip()
    else:
        print("No match")
    return None


def clausify(annot_text):
    original_text = strip_annotations(annot_text)
    word_tokens = original_text.split(" ")
    word_tokens = list(filter(None, word_tokens))
    # print(word_tokens)

    # print(annot_text)

    clause_list = []
    clauses = []

    for word in word_tokens:

        data = None

        annot_text = annot_text[annot_text.find(word) + len(word):].strip()
        if not annot_text.startswith("{"):
            continue

        data = annot_text[:annot_text.find("}") + 1]
        data = json.loads(data)

        # print(word, "|", data)
        evts = []
        event = "E0"
        for key in data.keys():
            predicate = replace_predicate_key(key)

            if predicate == "event":
                event = data[key]
                evts.append(data[key])
                continue

            clause_list.append([predicate, data[key], word])

            if predicate == "role":
                clause = f"{predicate}({event}, {data[key]}, {word})."
            else:
                clause = f"{predicate}({data[key]},{word})."

            print(clause)

            clauses.append(clause)

    print("Events:",evts)
        # print(annot_text)
    # pprint.pprint(clauses, indent=2)


# write a function that returns everything following the word encapsulated in square brackets
# e.g. Titanic {"role": "Patient", "wiki": "RMS_Titanic", "cat": "product", "evt": "sink-01", "role_descr": "thing sinking", "type": "ship"}
# returns {"role": "Patient", "wiki": "RMS_Titanic", "cat": "product", "evt": "sink-01", "role_descr": "thing sinking", "type": "ship"}



if __name__ == "__main__":
    annot_text = 'Titanic {"role": "Patient", "wiki": "RMS_Titanic", "cat": "product", "evt": "sink-01", "role_descr": "thing sinking", "type": "ship"} sank {"instance": "sink-01", "location": "Atlantic", "time": "1912", "vncls": "other_cos-45.4"} in the Atlantic {"wiki": "Atlantic_Ocean", "cat": "location", "type": "ocean"} in 1912 {"instance": "date-entity", "year": "1912"} .'
    
    annot_text = 'John {"role": "Patient", "cat": "individual", "evt": "smart-06", "role_descr": "intelligent agent/action (may require concatenation)", "type": "person"} is smart {"instance": "smart-06"} .'
    
    annot_text = """
    A man {"role": "Agent", "evt": "see-01", "role_descr": "viewer"} saw {"instance": "see-01", "location": "highway", "vncls": "characterize-29.2-1"} a Jaguar {"role": "Patient", "wiki": "Jaguar_Cars", "cat": "product", "evt": "see-01", "role_descr": "thing viewed", "type": "car-make"} on a higway .    
    """

    clausify(annot_text)