from __future__ import division, print_function

import sys
import os
from random import shuffle


if __name__ == '__main__':
    infname = sys.argv[1]
    proportion = float(sys.argv[2])

    basename = os.path.splitext(infname)[0]
    train_fname = basename + '.train'
    test_fname = basename + '.test'

    with open(infname) as f:
        lines = f.readlines()

    shuffle(lines)

    n_train_lines = int(len(lines) * proportion)

    with open(train_fname, 'w') as f:
        for i in lines[:n_train_lines]:
            f.write(i)

    with open(test_fname, 'w') as f:
        for i in lines[n_train_lines:]:
            f.write(i)
