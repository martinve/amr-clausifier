import pprint
import pickle

def truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


def format_json(blob):
    if isinstance(blob, str):
        return blob
    data = pickle.loads(blob)
    return pprint.pformat(data, indent=2)


def format_logic(logic):
    if isinstance(logic, bytes):
        logic = pickle.loads(logic)
        print(logic)
    if not isinstance(logic, list):
        try:
            logic = json.loads(logic)
        except:
            pass
    return pprint.pformat(logic, indent=2)