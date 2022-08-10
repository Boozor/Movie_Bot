# coding: utf-8

import string
import re
import ujson

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

english_stopwords = ujson.load(open('./MovieBot/utils/stopwords.json'))

LETTERS = string.ascii_lowercase
wordnet_lemmatizer = WordNetLemmatizer()

trash_words = ['Full-screen', 'full screen edition', 'VHS', 'English Subtitled', 'Two-Disc',
               'Blu-ray Combo in DVD Packaging', 'Blu-ray', 'DVD Combo', 'DVD', 'Special Edition', 'Steelbook Case',
               'The Criterion Collection', 'Family Fun Edition', 'full-screen edition', 'Widescreen', '[]', '()']


def normalize(text):
    """ Normalization function. """
    text_text = text.lower()

    letters_only = ''
    for _c in text_text:
        if _c in LETTERS:
            letters_only += _c
        else:
            letters_only += ' '

    while '  ' in letters_only:
        letters_only = letters_only.replace('  ', ' ')

    word_list = word_tokenize(letters_only)
    word_list = [wordnet_lemmatizer.lemmatize(word) for word in word_list]
    word_list = [wordnet_lemmatizer.lemmatize(word) for word in word_list if word not in english_stopwords]

    return ' '.join(word_list)
