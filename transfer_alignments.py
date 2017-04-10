import sys
from collections import defaultdict

def transfer(line, wordal):
	#print line
	#print wordal
	wordal_dict = defaultdict(list)
	for a in wordal.split(" "):
		if a.strip() == "":
			continue
		s, t = a.split("-")
		wordal_dict[int(s)].append(int(t))
	# print wordal_dict

	al = {}
	for a in line.split(" "):
		if a.strip() == "":
			continue
		start = a.split("|")[0].split("-")[0]
		if start[0] == "*":
			start = start[1:]
		start = int(start)
		end = int(a.split("|")[0].split("-")[1])
		for i in range(int(start),int(end)):
			for segment in a.split("|")[1].split("+"):
				if start in wordal_dict and (end - 1) in wordal_dict:
					start2 = min(wordal_dict[start])
					end2 = max(wordal_dict[end - 1])
					if end2 < start2:
						tmp = start2
						start2 = end2
						end2 = tmp 
					end2 += 1
					assert(end2 > start2)
					if start2 not in al:
						al[start2] = defaultdict(list)
					if segment not in al[start2][end2]:
						al[start2][end2].append(segment)
	print al
	for index in al.keys():
		lst = []
		max_i = index
		for end in al[index]:
			if end > max_i:
				max_i = end
			lst.extend(al[index][end])
		print str(index) + "-" + str(max_i) + "|" + "+".join(sorted(lst)),
	print ""
	#raw_input()
#transfer("0-1|0 3-4|0.0","0-0 1-0 2-1 3-2")
transfer("0-1|0 1-2|0.0","0-0 0-1 1-0")
# if __name__ == "__main__":

# 	amr_align = sys.argv[1]
# 	word_align = sys.argv[2]
# 	for line in zip(open(amr_align),open(word_align)):
# 		#print "->",line[0]
# 		#print amr_align
# 		transfer(line[0],line[1])
# 		#raw_input()
