#!/bin/bash
wget --post-data "$1" 'localhost:9000/?properties={"annotators": "tokenize,ssplit,pos,lemma,ner,parse", "outputFormat": "text"}' -O -