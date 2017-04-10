def run():
    amr = open("../amr-eager-github/data/eseuroparl-train.en.parsed").read().split("\n\n")
    es = open("data/eseuroparl-train.out").read().split("\n\n")

    for sentence, annot in zip(es, amr):
        tokens = []
        for line in sentence.split("\n"):
            if len(line.split("\t")) == 0:
                return
            tokens.append(line.split("\t")[1])
        print "\n".join(annot.split("\n")[0:2])
        print "# ::tok-es " + " ".join(tokens)
        print "\n".join(annot.split("\n")[2:])
        print ""
run()
