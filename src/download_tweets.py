import sys
import jsonpickle
import os
import tweepy
import time
from time import gmtime, strftime, strptime, mktime
from datetime import datetime, date
import numpy as np
import glob

from settings import *


def download(query, output_folder='.'):
    lang = 'en'
    since = '2016-10-27'

    tweetsPerQry = 100  # this is the max the API permits

    # fName = 'tweets_mac_' + str(date.today().month) + \
    #     '-' + str(date.today().day) + '.txt'

    fName = 'tweets_{query}_{d}.txt'.format(
        query='_'.join(query), d=datetime.now().strftime(strftime('%Y-%m-%d-%H-%M-%S')))

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)

    ids = []
    idsfile = os.path.join(output_folder, 'min_id.txt')
    if os.path.isfile(idsfile):
        ids = np.loadtxt(idsfile, dtype=int)

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet
    # matching the search query.
    max_id = min(ids) if len(ids) else -1L

    if max_id != -1:
        print("max_id: ", max_id)

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    with open(os.path.join(output_folder, fName), 'w') as f:
        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not since):
                        new_tweets = api.search(
                            q=searchQuery, count=tweetsPerQry, lang=lang)
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                lang=lang, since=since)
                else:
                    if (not since):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1), lang=lang)
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                lang=lang, since=since)
                if not new_tweets:
                    print("No more tweets found")
                    break

                for tweet in new_tweets:
                    if tweet._json['id'] not in ids:
                        f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                                '\n')
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))


if __name__ == "__main__":
    searchQuery = [sys.argv[1]] if len(sys.argv) > 1 else ['macbook']

    download(searchQuery, output_folder='data/')
