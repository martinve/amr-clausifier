import csv
import nltk
import os, sys

if __name__ == "__main__":
    basedir = nltk.data.path[0]
    datadir = basedir + "/corpora/propbank-3.4"

    if not os.path.exists(datadir):
        print("Path does not exist", datadir)
        sys.exit(-1)

    datafile = datadir + "/framelist.tsv"

    with open (datafile) as file:
        reader = csv.reader(file, delimiter="\t")

        k = 0
        diff_dict = {}
        for line in reader:
            baseform = line[0].split(".")[0].split("_")[0]
            if baseform != line[1]:
                print(line, baseform)
                k += 1
        print("Differences in: ", k)
