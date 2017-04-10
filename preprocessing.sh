ALIGNED=""
SENTS=""
FILE=""
LANGUAGE="en"
while [[ $# -gt 1 ]]
do
key="$1"
case $key in
    -a|--aligned)
    ALIGNED="-a "
    ;;
    -l|--lang)
    LANGUAGE="$2"
    ;;
    -f|--file)
    FILE="$2"
    ;;
    -s|--sents)
    SENTS="-s "
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done
./preprocessing_"$LANGUAGE".sh $SENTS $ALIGNED -f $FILE 
#./preprocessing_en.sh $SENT $ALIGNED -l $LANGUAGE $1 

