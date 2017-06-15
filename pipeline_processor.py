# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import string

from utils import file_to_wordlist, print_unicode_iterable, get_unicode_iterable, get_filenames, get_file_content
from constants import *
from kannada_lemmatizer import moola
from nltk.stem import WordNetLemmatizer

import nltk
nltk.data.path.append('/Users/deepikaravi/my_nltk_data')

def tokenise(text, lang_code):
    """

    :param text: string
    :param lang_code: u'en' or u'kn'
    :return: list of strings
    list of alpha numeric chars. works for unicode as well
    """
    if lang_code == 'kn':
        #text = unicode(text, 'utf-8')
        pass
    else:
        text = text.lower()

    # delete punctuation marks. retain alpha numeric chars.
    try:
        text = text.encode('utf-8').translate(None, string.punctuation)
    except UnicodeDecodeError:
        text = unicode(text, 'utf-8')
        text = text.encode('utf-8').translate(None, string.punctuation)

    text = text.split()
    return text

def remove_stopwords(text_list, lang_code):
    if lang_code == 'kn':
        stopwords = file_to_wordlist(KANNADA_STOPWORDS_FILE_PATH)
    else:
        stopwords = file_to_wordlist(ENGLISH_STOPWORDS_FILE_PATH)
    text_list = [w for w in text_list if w not in stopwords]
    return text_list

def lemmatize(text_list, lang_code):

    if lang_code == 'kn':
        text = [moola(unicode(w, 'utf-8')) for w in text_list]
    else:
        text = []
        lemmatizer = WordNetLemmatizer()

        for w in text_list:
            try:
                lemma = lemmatizer.lemmatize(w, 'v')
            except UnicodeDecodeError:
                lemma = w
            text.append(lemma)

    return text

def process_pipeline(text, lang_code):

    # tokenise
    text = tokenise(text, lang_code)

    # stopwords removal
    text = remove_stopwords(text, lang_code)

    # lemmatization
    text = lemmatize(text, lang_code)

    # convert to unicode if not already unicode
    text = get_unicode_iterable(text)

    return text

def process_harvest():

    file_to_terms = {}

    for kan_filename in get_filenames(KANNADA_HARVEST_PATH):
        url, file_string = get_file_content(kan_filename)
        file_to_terms[url] = process_pipeline(file_string, 'kn')

    for eng_filename in get_filenames(ENGLISH_HARVEST_PATH):

        url, file_string = get_file_content(eng_filename)
        file_to_terms[url] = process_pipeline(file_string, 'en')

    return file_to_terms

if __name__ == '__main__':

    #print process_harvest()
    url, file_string = get_file_content('anveshika/harvest/kannada/156.txt')
    print_unicode_iterable(process_pipeline(file_string, 'kn'))

