# encoding: utf-8
import sys
import re
lines = []
for line in open(sys.argv[1]):
    line = line.replace(".", "。")
    if line.strip().endswith('"'):
        line = line.strip()[0:-1]
    #if re.match("[.]|[!?]+|[。]|[！？]+", line.strip()[-1]) is not None:
    #    lines.append(line.strip())
    #else:
    lines.append(line.strip() + " .")

fw = open(sys.argv[1], "w")
for l in lines:
	fw.write(l+"\n")
fw.close()
