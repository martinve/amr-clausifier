from pathlib import Path
from lxml import etree as ET
import csv
import nltk

def get_rolesets(frames):
    all_rolesets = dict()
    for frame_name, xml in frames.items():
        rs = [e.get('id') for e in xml.findall('predicate/roleset')]
        for id in rs:
            all_rolesets[id] = frame_name[:-4]
    return all_rolesets


def make_frame_list(basedir):
    frame_dir = Path(basedir + "frames/")
    frame_files = frame_dir.rglob('*.xml')
    frames = dict()
    for frame_file in frame_files:
        try:
            xml = ET.parse(str(frame_file))
            frames[frame_file.name] = xml
        except Exception:
            pass
    return frames



def save_roleset_index(path):

    frames = make_frame_list(path)
    all_rolesets = get_rolesets(frames)

    with open(path + "framelist.tsv", "w") as outfile:
        writer = csv.writer(outfile, delimiter="\t")
        for key in all_rolesets.keys():
            # print(key, all_rolesets[key])
            writer.writerow([key, all_rolesets[key]])
    print("Created frame index at " + path)


if __name__ == "__main__":
    basepath = nltk.data.path[0] + "/corpora/propbank-3.4/"
    save_roleset_index(basepath)
