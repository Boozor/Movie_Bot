# -*- coding: utf-8 -*-

import ujson
import nltk
from nltk.util import ngrams
import editdistance


def find_title(text, movie_names):

    text = text.lower()

    # Generate ngrams
    token = nltk.word_tokenize(text)
    ngrm = []
    for i in range(1, 5):
        for t in ngrams(token, i):
            ngrm.append(t)

    min = ('', 100)
    for ngr in ngrm:

        for title in movie_names:
            if editdistance.eval(' '.join(ngr), title) < min[1] and editdistance.eval(' '.join(ngr), title) < len(title)/3:
                min = (title, editdistance.eval(' '.join(ngr), title))  # the closes movie

    if min[0] != '':
        return min[0]
    else:
        return None
