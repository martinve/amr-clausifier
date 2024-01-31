import sentence_spacy_classifier as sclf

if __name__ == "__main__":
    sent = "John eats soup with  a spoon and sausage with knife and fork."
    type = sclf.predict_snt_type(sent)
    print("Clf:", type)
