import re
def run():
    amr = open("data/ted-test.en.parsed").read().split("\n\n")
    zh = open("data/ted-test.zh.out").read().split("\n\n")

    for sentence, annot in zip(zh, amr):
        tokens = []
        if len(zh) == 1:
            break
        block = zh.pop(0).strip().split("\n")
        i = 2
        while block[i].startswith("[Text"):
            tokens.extend([t[5:-1] for t in re.findall('Text=[^\s]* ', block[i])])
            i += 1
        print "\n".join(annot.split("\n")[0:2])
        print "# ::tok-zh " + " ".join(tokens)
        print "\n".join(annot.split("\n")[2:])
        print ""

        if zh[0].startswith("\n") == False:
            zh.pop(0)
run()
