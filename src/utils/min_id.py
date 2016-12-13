import json
from collections import Counter
from datetime import datetime
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("missing tweets filename")
        sys.exit(1)

    fname = sys.argv[1]

    x = None
    k = 0
    for ldx, l in enumerate(open(fname)):
        try:
            j = json.loads(l)
        except:
            break

        if int(j['id']) < x or x is None:
            x = int(j['id'])

        if ldx % 1000 == 0:
            print('loaded {} tweets'.format(ldx))

    print('loaded {} tweets'.format(ldx))

    with open('min_id.txt', 'w') as f:
        f.write('{}\n'.format(x))

    print("saved min_id.txt")
