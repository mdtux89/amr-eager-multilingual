#!/usr/bin/env python
#coding=utf-8

import argparse
import cPickle as pickle
from node import Node
from buftoken import BufToken
import sys
from collections import defaultdict
import re
import copy
def _to_string(triples, root, level, last_child, seen, prefix, indexes, nodes):
    if len(root.split("/")) == 2:
        conc = root.split("/")[1].strip()
    else:
        conc = root.split()[0]
    children = [t for t in triples if str(t[0]) == root.split()[0]]
    if root in seen:
        root = root.split()[0]
        children = []
    else:
        var = root
        if " / " in root:
            var = root.split()[0]
        nodes.append((var,conc))
        indexes[var].append(prefix)
    if " / " in root:
        seen.append(root)
        graph = "(" + root
        if len(children) > 0:
            graph += "\n"
        else:
            graph += ")"
    else:
        graph = root
    j = 0
    for k, t in enumerate(children):
        if str(t[0]) == root.split()[0]:
            next_r = t[3]
            if t[4] != "":
                next_r += " / " + t[4]
            for i in range(0, level):
                graph += "    "
            seen2 = copy.deepcopy(seen)
            graph += t[2] + " " + _to_string(triples, next_r, level + 1, k == len(children) - 1, seen, prefix + "." + str(j), indexes, nodes)[0]
            if next_r not in seen2 or " / " not in next_r:
                j += 1
    if len(children) > 0:
        graph += ")"
    if not last_child:
        graph += "\n"

    return graph, indexes, nodes

def to_string(triples, root):
    children = [t for t in triples if str(t[0]) == root]
    assert(len(children)==1)
    if children[0][4] == "":
        return "(e / emptygraph)", defaultdict(list), []
    return _to_string(triples, children[0][3] + " / " + children[0][4], 1, False, [], "0", defaultdict(list), [])

def run(prefix, args):
    negation_words = open("resources_en/negations.txt").read().splitlines()
    negation_words = [n.split()[0].replace('"',"") for n in negation_words]
    amrdata = __import__("amrdata_en")
    data = amrdata.AMRDataset(prefix, amrs=False, demo = False, normalize = False)
    sentences = open(prefix).read().splitlines()
    alltokens = []
    alldependencies = []
    allrelations = []
    k = 0
    fw = open(prefix + ".parsed","w")
    for i_s, sentence in enumerate(data.getAllSents()):
        print "Sentence", i_s + 1
        snt = sentences[i_s]
        variables = ["v" + str(i) for i in range(len(sentence.tokens))]
        #for i in range(len(sentence.tokens)):
        #    variables[sentence.tokens[i]] = "v" + str(i)
        triples = []
        for d in sentence.dependencies:
            if d[1] == "ROOT":
		triples.append(("ROOT", "", "ROOT", variables[d[2]], sentence.tokens[d[2]]))
            else:
                triples.append((variables[d[0]], sentence.tokens[d[0]], d[1], variables[d[2]], sentence.tokens[d[2]]))
        graph, graph_indexes, nodes = to_string(triples, "ROOT")
        alignments = []
        for k in graph_indexes:
            idx = int(k[1:])
            alignments.append(str(idx) + "-" + str(idx + 1) + "|" + str(graph_indexes[k][0]))  
        alignments_str = " ".join(alignments)
        graph = graph.strip()
        if str(graph).startswith("(") == False:
            fw.write("# ::snt " + snt + "\n# ::tok " + " ".join([t for t in sentence.tokens]) + "\n(v / " + str(graph) + ")\n\n")
            continue

        if args.nodesedges and len(nodes) > 0:
            nodesedges = ""
            root = nodes[0][1]
            for n in nodes:
                idx = int(n[0][1:])
                nodesedges += "# ::node\t" + "+".join(graph_indexes[n[0]]) + "\t" + n[1] + "\t" + str(idx) + "-" + str(idx + 1) + "\n"
            nodesedges += "# ::root\t0\t" + root + "\n"
            for tr in triples:
                if tr[2] == "ROOT":
                    continue
                nodesedges += "# ::edge\t" + tr[1] + "\t" + tr[2] + "\t" + tr[4] + "\t" + "+".join(graph_indexes[tr[0]]) + "\t" + "+".join(graph_indexes[tr[3]]) + "\n"
            graph = nodesedges + graph
        if args.oracle:
            output = "# ::snt " + snt + "\n# ::tok " + " ".join([t for t in sentence.tokens]) + "\n" + str(graph) + "\n"
        else:
            if args.avoidalignments:
                output = "# ::snt " + snt + "\n# ::tok " + " ".join([t for t in sentence.tokens]) + "\n" + str(graph) + "\n"
            else:
                output = "# ::snt " + snt + "\n# ::tok " + " ".join([t for t in sentence.tokens]) + "\n# ::alignments " + alignments_str + "\n" + str(graph) + "\n"
        fw.write(output + "\n")

    fw.close()



if __name__ == "__main__":

        argparser = argparse.ArgumentParser(description='Process some integers.')
        argparser.add_argument("-f", "--file", help="Input file", required = True)
        argparser.add_argument("-l", "--lang", help="Language", default="en")
        argparser.add_argument("-a", "--avoidalignments", help="Doesn't output generated alignments", action='store_true')
        argparser.add_argument("-o", "--oracle", help="Run in oracle mode", action='store_true')
        argparser.add_argument("-n", "--nodesedges", help="Outputs nodes and edges in JAMR-like style", action='store_false')         
        try:
            args = argparser.parse_args()
        except:
            argparser.error("Invalid arguments")
            sys.exit(0)
        run(args.file, args)
