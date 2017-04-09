#!/bin/bash
FREELING="/disk/ocean/public/tools/FreeLing/bin"
"$FREELING/"analyze -f es.cfg --nec --output conll --outlv dep < "$1" | sed 's/  */\t/g'
