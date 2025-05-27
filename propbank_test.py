from propbank import propbank_api as pb
import pprint


if __name__ == "__main__":
    res = pb.describe("live-01")
    pprint.pprint(res, indent=2)