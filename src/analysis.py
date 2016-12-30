import utils
from preprocess_twitter import tokenize
from nltk.corpus import stopwords
import re
from scipy.stats import itemfreq
import pandas as pd
import fasttext as ft
import numpy as np
import sys

ds_name = sys.argv[1]
ds_filename = './data/{}_cleaned.txt'.format(ds_name)
model_filename = './model/{}_cleaned.bin'.format(ds_name)
stopset = set(stopwords.words('english'))

loaded_ds = [(x[0], x[1]) for x in utils.load_ds(ds_filename, True)]

labels = [x[0] for x in loaded_ds]
tweets = [tokenize(x[1]) for x in loaded_ds]

tweets = [' '.join([w for w in tw.split() if w not in stopset]) for tw in tweets]
tweets = [' '.join([w for w in tw.split() if not w.startswith('<')]) for tw in tweets]

r = re.compile('[^a-z\s]')
tweets = [r.sub('', tw).strip() for tw in tweets]

with open('./output/{}_w2v_tweets.txt'.format(ds_name), 'w') as f:
    for i in range(len(tweets)):
        f.write('{}{}\n'.format(labels[i], tweets[i]))
    

words = [w for tw in tweets for w in tw.split()]

m = ft.load_model(model_filename)

with open('./output/{}_w2v_word_vectors.txt'.format(ds_name), 'w') as f:
    for w in sorted(set(words)):
        vec = np.array(m._model.get_vector(w, m.encoding))
        if vec.any():
            f.write('{} {}\n'.format(w, ' '.join(str(i) for i in vec)))

# it = itemfreq(words)

# df = pd.DataFrame(it)
# df[1] = df[1].values.astype(np.int)
# df = df.sort_values(1)
# df.to_csv('it.txt')
