import errno
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def load_ds(path, label=False):
    with open(path) as f:
        for l in f:
            tmp = l.split(',')
            if label:
                lbl, line = '{}, '.format(tmp[0]), ','.join(tmp[1:]).strip()
            else:
                lbl, line = '', l
            
            yield (lbl, line) if label else line

