
def run():
	amr = open("../amr-eager-github/data/europarl-train.en.parsed").read().split("\n\n")
	it = open("data/europarl-train.it.out").read().split("\n\n")

	for sentence, annot in zip(it, amr):
		tokens = []
		for line in sentence.split("\n"):
			if len(line.split()) == 0:
				return
			if line.startswith("# FIELDS") == False:
				tokens.append(line.split()[2])
		print "\n".join(annot.split("\n")[0:2])
		print "# ::tok-it " + " ".join(tokens)
		print "\n".join(annot.split("\n")[2:])
		print ""

run()
