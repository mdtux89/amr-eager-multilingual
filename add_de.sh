echo "TRAINING"
java -mx6g -cp "stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props "german.properties" -file "data/deeuroparl-train.de" -outputFormat text -replaceExtension --outputDirectory "data"

echo "DEV"
java -mx6g -cp "stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props "german.properties" -file "data/deeuroparl-dev.de" -outputFormat text -replaceExtension --outputDirectory "data"

echo "TEST"
java -mx6g -cp "stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props "german.properties" -file "data/deeuroparl-test.de" -outputFormat text -replaceExtension --outputDirectory "data"

