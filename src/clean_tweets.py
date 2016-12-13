from preprocess_twitter import tokenize
import sys

if __name__ == '__main__':
    infname = sys.argv[1]
    outfname = sys.argv[2]

    with open(infname) as inf:
        tweets = [tokenize(tweet) for tweet in inf]

    with open(outfname, 'w') as outf:
        for l in tweets:
            outf.write('{0}\n'.format(l))
