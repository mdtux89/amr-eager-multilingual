#!/bin/bash
CORENLP="stanford-corenlp-full-2015-12-09/"
java -mx6g -cp "$CORENLP/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props "german.properties" -file "$1" -outputFormat text -O -
