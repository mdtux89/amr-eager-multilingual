import cPickle as pickle
import sys
pt = pickle.load(open(sys.argv[1], "rb"))
print(pt)
print(len([x for x in pt.keys() if len(pt[x].nodes) == 0]) / float(len(pt.keys())))
