import sys
import codecs
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE


def main():
    colors = {
        'vinci': 'b',
        'potter': 'r',
        'brokeback': 'y',
        'impossible': 'g'
    }

    filmwords = {'mission', 'impossible', 'harry', 'potter', 'code', 'da', 'vinci', 'mountain', 'brokeback'}

    embeddings_file = sys.argv[1]
    wv, vocabulary = load_embeddings(embeddings_file)
    vocabulary = list(vocabulary)

    c = []
    for idx, i in enumerate(vocabulary):
        w = set(i.split('_'))
        for k in colors:
            if k in w:
                c.append(colors[k])
                break

        vocabulary[idx] = ' '.join(w.difference(filmwords))

    c = np.array(c)

    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(wv[:1000, :])

    plt.scatter(Y[:, 0], Y[:, 1], c=c)
    for label, x, y in zip(vocabulary, Y[:, 0], Y[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')

    plt.show()


def load_embeddings(file_name):
    with codecs.open(file_name, 'r', 'utf-8') as f_in:
        vocabulary, wv = zip(*[line.strip().split(' ', 1) for line in f_in])
    wv = np.loadtxt(wv)
    return wv, vocabulary


if __name__ == "__main__":
    main()
