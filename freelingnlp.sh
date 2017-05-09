#!/bin/bash
FREELING="/disk/ocean/public/tools/FreeLing/bin"
TMP=`mktemp`
echo "$1" > "$TMP"
"$FREELING/"analyze -f es.cfg --nec --output conll --outlv dep < "$TMP" | sed 's/  */\t/g'
#name=$(basename "$TMP")
#cat "$name.out"
rm -f "$TMP"
#rm -f "$name.out"
