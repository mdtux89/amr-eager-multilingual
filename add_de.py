import re
def run():
    amr = open("data/deub2-train.en.parsed").read().split("\n\n")
    de = open("data/deub2-train.en.out").read().split("\n\n")

    for sentence, annot in zip(de, amr):
        tokens = []
        if len(de) == 1:
            break
        block = de.pop(0).strip().split("\n")
        i = 2
        while block[i].startswith("[Text"):
            tokens.extend([t[5:-1] for t in re.findall('Text=[^\s]* ', block[i])])
            i += 1
        print "\n".join(annot.split("\n")[0:2])
        print "# ::tok-de " + " ".join(tokens)
        print "\n".join(annot.split("\n")[2:])
        print ""
        
        if de[0].startswith("\n") == False:
            de.pop(0)

run()
