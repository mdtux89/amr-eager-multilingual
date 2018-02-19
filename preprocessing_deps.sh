#!/bin/bash

# Preprocessing script for AMR data
# For preocessing unaligned amr annotations, use: ./preprocessing.sh <file>
# For preprocessing amr annotations aligned with JAMR (or other aligner that generate similar output), use: ./preprocessing.sh -a <file>
# For preprocessing English sentences (parsing only), use: ./preprocessing.sh -s <file>


CORENLP="stanford-corenlp-full-2015-12-09/"

echo "Running CoreNLP.."
java -mx6g -cp "$CORENLP/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props "corenlp.properties" -file "$1.sentences" --outputFormat text -replaceExtension

echo "Done!"
