data=$3

./preprocessing.sh -s -f $data/$2-test.$1-en.post
python preprocessing.py -f $data/$2-test.$1-en.post
python parser.py -f $data/$2-test.$1-en.post

./preprocessing.sh -s -f $data/ldc.en-$1.post
python preprocessing.py -f $data/ldc.en-$1.post
python parser.py -f $data/ldc.en-$1.post

./preprocessing.sh -s -f $data/ldc.en-$1-en.post
python preprocessing.py -f $data/ldc.en-$1-en.post
python parser.py -f $data/ldc.en-$1-en.post

./preprocessing.sh -s -f $data/ldc.$1-en.post
python preprocessing.py -f $data/ldc.$1-en.post
python parser.py -f $data/ldc.$1-en.post
