import sys
for line1, line2 in zip(open(sys.argv[1]),open(sys.argv[2])):
	print line1.strip() + ' ||| ' + line2.strip()
