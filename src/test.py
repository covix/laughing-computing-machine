from __future__ import division, print_function

import sys
from sklearn.model_selection import StratifiedKFold
import re
import numpy as np
import fasttext as ft
from utils import mkdir_p
import os
from scipy.stats import itemfreq


if __name__ == '__main__':
    model_fname = sys.argv[1]
    test_fname = sys.argv[2]

    classifier = ft.load_model(model_fname)
    result = classifier.test(test_fname)
    print('P@1:', result.precision)
    print('R@1:', result.recall)
    print('Number of examples:', result.nexamples)
