"""
preprocess-twitter.py

python preprocess-twitter.py "Some random text with #hashtags, @mentions and http://t.co/kdjfkdjf (links). :)"

Script for preprocessing tweets by Romain Paulus
with small modifications by Jeffrey Pennington
with translation to Python by Motoki Wu

Translation of Ruby script to create features for GloVe vectors for Twitter data.
http://nlp.stanford.edu/projects/glove/preprocess-twitter.rb
"""

import sys
import re
import json

_FLAGS = re.MULTILINE | re.DOTALL


def _hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    if hashtag_body.isupper():
        result = "<hashtag> {} <allcaps>".format(hashtag_body)
    else:
        result = " ".join(
            ["<hashtag>"] + re.split(r"(?=[A-Z])", hashtag_body, flags=_FLAGS))
    return result


def _allcaps(text):
    text = text.group()
    return text.lower() + " <allcaps>"


def tokenize(text):
    text = (x.strip() for x in text.splitlines())
    text = ' '.join((x for x in text if x != ''))

    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    # function so code less repetitive
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=_FLAGS)

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "<url>")
    text = re_sub(r"/", " / ")
    text = re_sub(r"@\w+", "<user>")
    text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes,
                                                  nose, nose, eyes), "<smile>")
    text = re_sub(r"{}{}p+".format(eyes, nose), "<lolface>")
    text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes,
                                            nose, nose, eyes), "<sadface>")
    text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), "<neutralface>")
    text = re_sub(r"<3", "<heart>")
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", "<number>")
    text = re_sub(r"#\S+", _hashtag)
    text = re_sub(r"([!?.]){2,}", r"\1 <repeat>")
    text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 <elong>")

    # -- I just don't understand why the Ruby script adds <allcaps> to everything so I limited the selection.
    # text = re_sub(r"([^a-z0-9()<>'`\-]){2,}", _allcaps)
    text = re_sub(r"([A-Z]){2,}", _allcaps)

    return text.lower()


if __name__ == '__main__':
    infname = sys.argv[1]
    outfname = sys.argv[2]

    with open(infname) as inf:
        with open(outfname, 'w') as outf:
            for idx, l in enumerate(inf):
                cleaned_tweet = tokenize(json.loads(l)['text'].encode('utf8'))
                outf.write("{}\n".format(cleaned_tweet))

                if (idx + 1) % 1000 == 0:
                    print 'processed {} tweets'.format(idx)
