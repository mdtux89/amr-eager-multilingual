#!/bin/bash

# Preprocessing script for AMR data
# For preocessing unaligned amr annotations, use: ./preprocessing.sh <file>
# For preprocessing amr annotations aligned with JAMR (or other aligner that generate similar output), use: ./preprocessing.sh -a <file>
# For preprocessing English sentences (parsing only), use: ./preprocessing.sh -s <file>


JAMR="/disk/ocean/public/tools/jamr2016"
TINT="tint"
FASTALIGN="/disk/ocean/public/tools/fast_align/build" # if you don't know why is this here, just ignore it, you don't need it

if [[ "$JAMR" != "" ]];
then
	source $JAMR/scripts/config.sh
fi

SENTS="0"
while [[ $# -gt 1 ]]
do
key="$1"
case $key in
    -s|--sents)
    SENTS="1"
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

if [ "$#" -ne 1 ]; then
    echo "Usage: preprocessing.sh AMR_annotation_file"
    exit
fi
workdir=$(dirname $1)

if [[ $SENTS -eq "0" ]];
then
	echo "Extracting AMR graphs.."
	cat $1 | grep -v '^#' > "$1.graphs"

	if [[ $JAMR != "" ]];
	then
		echo "Running JAMR aligner.."
		source $JAMR/scripts/config.sh
		$JAMR/scripts/ALIGN.sh < "$1" > "$1.tmp"
	else
		echo "JAMR path not specified"
	fi

	cat "$1.tmp" | grep '# ::tok-it ' | sed 's/^# ::tok-it //' > "$1.sentences"
	cat "$1.tmp" | grep '# ::tok ' | sed 's/^# ::tok //' > "$1.sentences_en"
	cat "$1.tmp" | grep '# ::alignments ' | grep '::annotator Aligner' | sed 's/^# ::alignments //' | cut -d":" -f1 > "$1.alignments_en"
	python combine.py "$1.sentences_en" "$1.sentences" > "$1.parallel"

	if [ ! -e "resources/fwd_params" ]; 
	then
        echo "NEED TO RUN fastalign_train.sh FIRST!"
		exit
    fi	
	${FASTALIGN}/force_align.py resources/fwd_params resources/fwd_err resources/rev_params resources/rev_err grow-diag-final-and <"$1.parallel" >"$1.wordalign"
	python transfer_alignments.py "$1.alignments_en" "$1.wordalign" > "$1.alignments"

	rm "$1.sentences_en"
	rm "$1.alignments_en"
	rm "$1.wordalign"
	rm "$1.parallel"
	rm "$1.tmp"
else
	cp "$1" "$1.sentences"
fi
echo "Running Tint.."
${TINT}/tint.sh -c 'tint.properties' -f "textpro" < "$1.sentences" > "$1.out" 

echo "Done!"
