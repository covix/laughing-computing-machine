from __future__ import print_function

from preprocess_twitter import tokenize
import sys


if __name__ == '__main__':
    infname = sys.argv[1]
    outfname = sys.argv[2]

    with open(infname) as inf:
        with open(outfname, 'w') as outf:
            for idx, l in enumerate(inf):
                cleaned_tweet = tokenize(json.loads(l)['text'].encode('utf8'))
                outf.write("{}\n".format(cleaned_tweet))

                if (idx + 1) % 1000 == 0:
                    print('processed {} tweets'.format(idx))
