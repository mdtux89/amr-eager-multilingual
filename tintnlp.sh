#!/bin/bash
#string=$( printf "%s\n" "$1" | sed 's/ /%20/g' )
#wget http://localhost:8012/tint?text=$string&format=text

echo "$1" | /disk/ocean/mdamonte/tint/tint.sh -f "textpro"
