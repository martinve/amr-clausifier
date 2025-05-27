from extract_info import decompose_amr, get_amr_parse

if __name__ == "__main__":
    a = get_amr_parse("Boy ate steak with knife and fork and soup with spoon.")
    decompose_amr(a)