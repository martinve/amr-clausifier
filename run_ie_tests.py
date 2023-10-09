import time
import requests
import settings as cfg
from extract_info import decompose_amr

testsfile = "debug/ie_test_cases.txt"

def get_amr_parse(sent):
    res = requests.get(f"http://{cfg.amr_server_host}:{cfg.amr_server_port}/?text={sent}",
                 headers={'Accept': 'application/json'})
    return res.json()["parse"]

def run_tests():
    with open(testsfile) as f:
        tests = f.readlines()
        for snt in tests:
            snt = snt.strip()
            if snt:
                start = time.time()
                amr = get_amr_parse(snt)
                end = time.time()
                elapsed = "%.2f" % (end-start)
                print(f"Parse in {elapsed}.")
                decompose_amr(amr)
                print("\n\n\n")

if __name__ == "__main__":
    run_tests()