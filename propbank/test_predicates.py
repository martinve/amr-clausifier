import pprint
import propbank_amr_api as pb


if __name__ == "__main__":
    preds = ["have-degree-91", "have-org-role-91"]
    for pred in preds:
        pprint.pprint(pb.describe(pred))
        print("---")