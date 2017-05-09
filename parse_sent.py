#!/usr/bin/env python
#coding=utf-8

'''
Script used to parse sentences into AMR graphs in the live demo.

@author: Marco Damonte (m.damonte@sms.ed.ac.uk)
@since: 03-10-16 
'''

import subprocess
import cPickle as pickle
from transition_system import TransitionSystem
from transition_system import loadModels
import preprocessing
import copy
from buftoken import BufToken
from embs import Embs
from resources import Resources
from collections import defaultdict

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

def run(sentence, language='en'):
    #sentence = subprocess.check_output(['cdec-master/corpus/tokenize-anything.sh', sentence])
    loadModels(language)
    if language == 'en':
        model_dir = "ENGLISH"
        parse = subprocess.check_output(['./corenlp.sh', sentence])
        #ps = subprocess.Popen(('echo', sent), stdout=subprocess.PIPE)
        #sent = subprocess.check_output(('cdec-master/corpus/tokenize-anything.sh'), stdin=ps.stdout)
        #ps.wait() 
    elif language == 'it':
        model_dir = "ITALIAN"
        parse = subprocess.check_output(['./tintnlp.sh', sentence])
    elif language == 'es':
        model_dir = "SPANISH"
        parse = subprocess.check_output(['./freelingnlp.sh', sentence])
        #ps = subprocess.Popen(('echo', sent), stdout=subprocess.PIPE)
        #sent = subprocess.check_output(('cdec-master/corpus/tokenize-anything.sh'), stdin=ps.stdout)
        #ps.wait()
    elif language == 'de':
        model_dir = "GERMAN"
        parse = subprocess.check_output(['./corenlp_de.sh', sentence])
        #ps = subprocess.Popen(('echo', sent), stdout=subprocess.PIPE)
        #sent = subprocess.check_output(('cdec-master/corpus/tokenize-anything.sh'), stdin=ps.stdout)
        #ps.wait()
    elif language == 'zh':
        model_dir = "CHINESE"
        parse = subprocess.check_output(['./corenlp_zh.sh', sentence])
        #ps = subprocess.Popen(('echo', sent), stdout=subprocess.PIPE)
        #sent = subprocess.check_output(('cdec-master/corpus/tokenize-anything.sh'), stdin=ps.stdout)
        #ps.wait()
   
    dependencies, tokens = preprocessing.run_single(parse, language)

    Resources.init_table(model_dir, False)
    embs = Embs("resources_" + language + "/", model_dir)

    data = (copy.deepcopy(tokens), copy.deepcopy(dependencies))
    ununderscored = []
    sent_ranges = {}
    i = 0
    for t in tokens:
        units = t.word.split("_")
        sent_ranges[t] = str(i) + "-" + str(i + len(units))
        ununderscored.extend(units)
        i += len(units)
    t = TransitionSystem(embs, data, "PARSE", language, model_dir)

    triples = t.relations()
    output = ""
    if triples == []:
        return "# ::snt " + " ".join([t for t in ununderscored]) + "\n" + "(v / emptygraph)\n"

    graph, graph_indexes, nodes = to_string(triples, "TOP")
    output = str(graph)
    if output.startswith("(") == False:
        return "# ::snt " + " ".join([t for t in ununderscored]) + "\n" + "(v / " + output + ")"

    align_line = ""
    for t, nodes in t.alignments():
        if len(nodes) > 0:
            align_line += sent_ranges[t] + "|"
            for n in nodes:
                for i in graph_indexes[n]:
                    align_line += i + "+"
                align_line = align_line[0:-1] + " "
    output = "# ::snt " + " ".join([t for t in ununderscored]) + "\n# ::alignments " + align_line + "\n" + output
    return output


#print run ("The boy doesn't want to go", "en")
#print run("Il ragazzo non vuole andare", "it")
#print run ("Der Junge will nicht gehen", "de")
#print run ("El chico no quiere ir", "es")
#print run ("男孩不想去", "zh")

