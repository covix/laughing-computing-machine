from __future__ import division, print_function

import sys
from sklearn.model_selection import StratifiedKFold
import re
import numpy as np
import fasttext as ft
from utils import mkdir_p
import os
from scipy.stats import itemfreq


def read_file_into_arrays(filename, label_prefix='__label__', original=False):
    r = re.compile(
        '{label_prefix}(?P<y>\d)+, (?P<x>.+)'.format(label_prefix=label_prefix))

    X, y = [], []
    lines = [] if original else None

    with open(filename) as f:
        for l in f:
            g = r.match(l.strip()).groupdict()
            X.append(g['x'])
            y.append(int(g['y']))

            if original:
                lines.append(l.strip())

    X = np.array(X)
    y = np.array(y)
    lines = np.array(lines)

    ret = (X, y, lines) if original else (X, y)
    return ret


def save_file(lines, filename):
    with open(filename, 'w') as f:
        for l in lines:
            f.write('{}\n'.format(l))


def train_model(lines, filename='/tmp/model.train',
                output='model/model', dim=10, lr=0.1, epoch=6,
                min_count=1, word_ngrams=1, bucket=10000000, thread=4, silent=1,
                label_prefix='__label__', remove_after=False):
    save_file(lines, filename)

    mkdir_p(os.path.dirname(output))

    classifier = ft.supervised(filename, output, dim=dim, lr=lr, epoch=epoch,
                               min_count=min_count, word_ngrams=word_ngrams,
                               bucket=bucket, thread=thread, silent=silent,
                               label_prefix=label_prefix)

    if remove_after:
        os.remove(filename)
        os.remove(output + '.bin')

    return classifier


def test_model(lines, classifier, filename='/tmp/model.test',
               remove_after=False):
    save_file(lines, filename)

    result = classifier.test(filename)

    if remove_after:
        os.remove(filename)

    return result


if __name__ == '__main__':
    n_splits = 5
    infname = sys.argv[1]

    X, y, lines = read_file_into_arrays(infname, original=True)

    print("Labels distribution:")
    print(itemfreq(y))

    print("Performing {}-Fold Cross Validation".format(n_splits))
    skf = StratifiedKFold(n_splits=n_splits)
    skf.get_n_splits(X, y)

    precisions, recalls = [], []
    for train_index, test_index in skf.split(X, y):
        print('X/y: {}/{}'.format(len(train_index), len(test_index)))
        lines_train, lines_test = lines[train_index], lines[test_index]
        clf = train_model(lines_train, remove_after=True)
        result = test_model(lines_train, clf, remove_after=True)

        precisions.append(result.precision)
        recalls.append(result.recall)

        print('P@1:', result.precision)
        print('R@1:', result.recall)
        # print('Number of examples:', result.nexamples)
        print()

    precisions = np.array(precisions)
    recalls = np.array(recalls)

    print('P@1: {:.2f} (+/- {:.2f})'.format(precisions.mean(),
                                            precisions.std() * 2))
    print('R@1: {:.2f} (+/- {:.2f})'.format(recalls.mean(), recalls.std() * 2))

    print("\nTraining final model")
    train_model(lines, output='model/{}'.format(os.path.basename(os.path.splitext(infname)[0])))
