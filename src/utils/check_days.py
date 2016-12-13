import json
from collections import Counter
from datetime import datetime
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("missing tweets filename")
        sys.exit(1)

    fname = sys.argv[1]

    x = []
    k = 0
    for ldx, l in enumerate(open(fname)):
        try:
            j = json.loads(l)
        except:
            break

        dt = datetime.strptime(j['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        x.append(str(dt.date()))

        if ldx % 1000 == 0:
            print('loaded {} tweets'.format(ldx))

    print('loaded {} tweets'.format(ldx))

    xc = Counter(x)
    print(xc)

    with open('days_distribution.txt', 'w') as f:
        for l in xc:
            f.write(l + '\n')

    print("saved days_distribution.txt")
