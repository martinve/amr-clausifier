import stanza

import setup_path
import json
import sys, os
import time
import requests
import settings as cfg


def get_amr_parse(sent):
    srv = f"http://{cfg.amr_server_host}:{cfg.amr_server_port}"
    try:
        res = requests.get(f"{srv}/?text={sent}",
                     headers={'Accept': 'application/json'})
        return res.json()["parse"]
    except:
        print(f"""
        Cannot reach AMR parser API endpoint at {srv}.
        To run the parser server run `amrserver.py` under `./amr_parser` directory.
        To configure AMR parser server, consult `README.md.`
        """)
        sys.exit("Exiting")




def get_ud_parse(sent):
    res = requests.get(f"http://{cfg.ud_server_host}:{cfg.ud_server_port}/?text={sent}",
                 headers={'Accept': 'application/json'})
    return res.json()["parse"]


def get_passage_analysis(passage: str):

    print("Get AMR parse.")
    aparse = get_amr_parse(passage)
    aparse = get_amr_parse(passage)

    print("Get UD parse.")
    uparse = get_ud_parse(passage)

    parsed = {
        "sentence": passage,
        "semparse": {
            "amr": aparse,
            "ud": uparse
        }
    }

    return {
        "passage": passage,
        "sentences": [
            parsed
        ]
    }




if __name__ == "__main__":

    passage_in = " ".join(sys.argv[1:])

    passage_in = "Snow is white."

    print("Start parsing: ", passage_in)
    passage_meta = get_passage_analysis(passage_in)
    print(json.dumps(passage_meta, indent=2))
