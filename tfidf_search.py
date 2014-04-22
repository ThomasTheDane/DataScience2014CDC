# 4/18/2014
# Charles O. Goddard

from __future__ import print_function

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from bs4 import BeautifulSoup

import os
import sys
import pickle


def striptext(text):
    words = []
    soup = BeautifulSoup(text, 'html5lib')
    elems = [elem for elem in soup]
    while elems:
        elem = elems.pop(0)
        if elem.string != None:
            words.append(elem.string)
        if hasattr(elem, 'contents'):
            elems += elem.contents
    res = '\n'.join(words)
    while '\n\n' in res:
        res = res.replace('\n\n', '\n')
    return res


def read_doc(fn):
    with open(fn, 'r') as f:
        text = f.read()
        return striptext(text)


def search(text, documents=None):
    if documents is None:
        documents = pickle.load(open('documents.pickle', 'rb'))

    #print('Query:', text)

    docnames = ["query"] + [d[0] for d in documents]
    documents = [text] + [d[1] for d in documents]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(documents)
    num_samples, num_features = tfidf.shape
    print('{0} samples, {1} features'.format(num_samples, num_features))

    search_vector = tfidf[0].A[0]
    match_scores = [(sum(search_vector * tfidf[i].A[0]), i) for i in range(1, num_samples)]
    match_scores.sort(reverse=True)

    return [(score, docnames[i]) for (score, i) in match_scores[:10]]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reparse':
            documents = []
            docnames = os.listdir('scraped')
            for docname in docnames:
                documents.append((docname, read_doc('scraped/'+docname)))
            print('Read in all documents')
            pickle.dump(documents, open('documents.pickle', 'wb'), -1)
            sys.exit(0)
    query = "New scorecard ranks states on their 'fertility friendliness'. For National Infertility Week, RESOLVE: The National Infertility Association has released its annual Fertility Scorecard - a map ranking each state by how easy it is for citizens to gain access to fertility support resources and treatments in that area."
    match_scores = search(query, documents)
    for score, i in match_scores[:10]:
        print('{0} -> {1}'.format(score, docnames[i]))
