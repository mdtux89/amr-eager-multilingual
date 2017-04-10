FREELING="/disk/ocean/mdamonte/amr-eager-es/FreeLing/bin"
echo "TRAINING"
"$FREELING/"analyze -f es.cfg --nec --output conll --outlv dep < "data/eseuroparl-train.es" | sed 's/  */\t/g' > "data/eseuroparl-train.out"

echo "DEV"
"$FREELING/"analyze -f es.cfg --nec --output conll --outlv dep < "data/eseuroparl-dev.es" | sed 's/  */\t/g' > "data/eseuroparl-dev.out"

echo "TEST"
"$FREELING/"analyze -f es.cfg --nec --output conll --outlv dep < "data/eseuroparl-test.es" | sed 's/  */\t/g'> "data/eseuroparl-test.out"
