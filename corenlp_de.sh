#!/bin/bash
CORENLP="stanford-corenlp-full-2015-12-09/"

TMP=`mktemp`
echo "$1" > "$TMP"
java -mx6g -cp "$CORENLP/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props "german.properties" -file "$TMP" -outputFormat text -O -
name=$(basename "$TMP")
cat "$name.out"
rm -f "$TMP"
rm -f "$name.out"
