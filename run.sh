#!/bin/bash

DS_NAME=$1

python src/preprocess_twitter.py data/${DS_NAME}.txt True > data/${DS_NAME}_cleaned.txt
python src/split_train_test.py data/${DS_NAME}_cleaned.txt .9
python src/train.py data/${DS_NAME}_cleaned.train
python src/test.py model/${DS_NAME}_cleaned.bin data/${DS_NAME}_cleaned.test
python src/analysis.py ${DS_NAME}

cut -d , -f 2- data/${DS_NAME}.txt > data/${DS_NAME}_without_labels.txt
../../fastText/fasttext cbow -minCount 1 -dim 100 -input data/${DS_NAME}_without_labels.txt -output output/${DS_NAME}_w2v_word_vectors 
