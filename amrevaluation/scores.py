#!/usr/bin/env python
#coding=utf-8

'''
Computes AMR scores for concept identification, named entity recognition, wikification,
negation detection, reentrancy detection and SRL.

@author: Marco Damonte (m.damonte@sms.ed.ac.uk)
@since: 03-10-16
'''

import sys
import smatch.amr as amr
import smatch.smatch_fromlists as smatch
from collections import defaultdict

def concepts(v2c_dict):
    return [str(v) for v in v2c_dict.values()]

def namedent(v2c_dict, triples):
    return [str(v2c_dict[v1]) for (l,v1,v2) in triples if l == "name"]

def negations(v2c_dict, triples):
    return [v2c_dict[v1] for (l,v1,v2) in triples if l == "polarity"]    

def wikification(triples):
    return [v2 for (l,v1,v2) in triples if l == "wiki"]

def everything(v2c_dict, triples):
        lst = []
        vrs = []
        for t in triples:
            c1 = t[1]
            c2 = t[2]
            if t[1] in v2c_dict:
                c1 = v2c_dict[t[1]]
            if t[2] in v2c_dict:
                c2 = v2c_dict[t[2]]
            lst.append((t[0],c1,c2))
        return lst

def reentrancy(v2c_dict, triples):
    lst = []
    vrs = []
    for n in v2c_dict.keys():
        parents = [(l,v1,v2) for (l,v1,v2) in triples if v2 == n and l != "instance"]
        if len(parents) > 1:
            #extract triples involving this (multi-parent) node
            for t in parents:
                lst.append(t)
                vrs.extend([t[1],t[2]])
    #collect var/concept pairs for all extracted nodes
    dict1 = {}
    for i in v2c_dict:
         if i in vrs:
            dict1[i] = v2c_dict[i]
    return (lst, dict1)

def srl(v2c_dict, triples):
    lst = []
    vrs = []
    for t in triples:
        if t[0].startswith("ARG"):
            #although the smatch code we use inverts the -of relations
            #there seems to be cases where this is not done so we invert
            #them here
            if t[0].endswith("of"):
                lst.append((t[0][0:-3],t[2],t[1]))
                vrs.extend([t[2],t[1]])
            else:
                lst.append(t)
                vrs.extend([t[1],t[2]])

    #collect var/concept pairs for all extracted nodes            
    dict1 = {}
    for i in v2c_dict:
        if i in vrs:
            dict1[i] = v2c_dict[i]
    return (lst, dict1)

def var2concept(amr):
    v2c = {}
    for n, v in zip(amr.nodes, amr.node_values):
        v2c[n] = v
    return v2c

pred = open(sys.argv[1]).read().strip().split("\n\n")
gold = open(sys.argv[2]).read().strip().split("\n\n")

inters = defaultdict(int)
golds = defaultdict(int)
preds = defaultdict(int)
reentrancies_pred = []
reentrancies_gold = []
srl_pred = []
srl_gold = []

k = 0
tot = 0
correct = 0
for amr_pred, amr_gold in zip(pred, gold):
    amr_pred = amr.AMR.parse_AMR_line(amr_pred.replace("\n","")) 
    dict_pred = var2concept(amr_pred)
    triples_pred = []
    for t in amr_pred.get_triples()[1] + amr_pred.get_triples()[2]:
        if t[0].endswith('-of'):
            triples_pred.append((t[0][:-3], t[2], t[1]))
        else:
            triples_pred.append((t[0], t[1], t[2]))

    amr_gold = amr.AMR.parse_AMR_line(amr_gold.replace("\n",""))
    dict_gold = var2concept(amr_gold)
    triples_gold = []
    for t in amr_gold.get_triples()[1] + amr_gold.get_triples()[2]:
        if t[0].endswith('-of'):
            triples_gold.append((t[0][:-3], t[2], t[1]))
        else:
            triples_gold.append((t[0], t[1], t[2]))
  
#    anon_triples_pred = []
#    anon_triples_gold = []
#    for x in triples_pred:
#        if x[1] in dict_pred:
#            b = dict_pred[x[1]]
#        else:
#            b = x[1]
#        if x[2] in dict_pred:
#            c = dict_pred[x[2]]
#        else:
#            c = x[2]
#        anon_triples_pred.append((x[0], b, c))
 
#    for x in triples_gold:
#        if x[1] in dict_gold:
#            b = dict_gold[x[1]]
#        else:
#            b = x[1]
#        if x[2] in dict_gold:
#            c = dict_gold[x[2]]
#        else:
#            c = x[2]
#        anon_triples_gold.append((x[0], b, c))
#    anon_triples_pred = sorted(anon_triples_pred)
#    anon_triples_gold = sorted(anon_triples_gold)
#    if anon_triples_pred == anon_triples_gold:
#        correct += 1
#    tot += 1
    
    list_pred = concepts(dict_pred)
    list_gold = concepts(dict_gold)
    inters["Concepts"] += len(list(set(list_pred) & set(list_gold)))
    preds["Concepts"] += len(set(list_pred))
    golds["Concepts"] += len(set(list_gold))

    list_pred = namedent(dict_pred, triples_pred)
    list_gold = namedent(dict_gold, triples_gold)
    inters["Named Ent."] += len(list(set(list_pred) & set(list_gold)))
    preds["Named Ent."] += len(set(list_pred))
    golds["Named Ent."] += len(set(list_gold))

    list_pred = negations(dict_pred, triples_pred)
    list_gold = negations(dict_gold, triples_gold)
    inters["Negations"] += len(list(set(list_pred) & set(list_gold)))
    preds["Negations"] += len(set(list_pred))
    golds["Negations"] += len(set(list_gold))

    list_pred = wikification(triples_pred)
    list_gold = wikification(triples_gold)
    inters["Wikification"] += len(list(set(list_pred) & set(list_gold)))
    preds["Wikification"] += len(set(list_pred))
    golds["Wikification"] += len(set(list_gold))

    list_pred = everything(dict_pred, triples_pred)
    list_gold = everything(dict_gold, triples_gold)
    inters["IgnoreVars"] += len(list(set(list_pred) & set(list_gold)))
    preds["IgnoreVars"] += len(set(list_pred))
    golds["IgnoreVars"] += len(set(list_gold))

    reentrancies_pred.append(reentrancy(dict_pred, triples_pred))
    reentrancies_gold.append(reentrancy(dict_gold, triples_gold))
   
    srl_pred.append(srl(dict_pred, triples_pred))
    srl_gold.append(srl(dict_gold, triples_gold))

for score in preds:
    print score, "->",
    if preds[score] > 0:
        pr = inters[score]/float(preds[score])
    else:
        pr = 0
    if golds[score] > 0:
        rc = inters[score]/float(golds[score])
    else:
        rc = 0
    if pr + rc > 0:
        f = 2*(pr*rc)/(pr+rc)
        print 'P: %.2f, R: %.2f, F: %.2f' % (float(pr), float(rc), float(f))
    else: 
        print 'P: %.2f, R: %.2f, F: %.2f' % (float(pr), float(rc), float("0.00"))

pr, rc, f = smatch.main(reentrancies_pred, reentrancies_gold, True)
print 'Reentrancies -> P: %.2f, R: %.2f, F: %.2f' % (float(pr), float(rc), float(f))
pr, rc, f = smatch.main(srl_pred, srl_gold, True)
print 'SRL -> P: %.2f, R: %.2f, F: %.2f' % (float(pr), float(rc), float(f))

#acc = float(correct) / tot
#print 'Full parse', acc
