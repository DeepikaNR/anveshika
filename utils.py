# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from langdetect import detect
from cassandra.cqlengine import connection
import os

def db_connect():
    connection.setup(['127.0.0.1'], 'dev3')

def get_file_content(filename):
    """

    :param filename: absolute file path
    :return: content : contents of file as string
    """

    f = open(filename, 'r')
    url = f.readline().strip()
    content = f.read()
    f.close()

    return url, content

def file_to_wordlist(file_path):
    """

    :param file_name: words stored separated by whitespace(combination of ' '
    or \t or \n
    :return: list of words
    """
    s = open(file_path, 'r')
    wordlist = s.read().split()
    s.close()
    return wordlist

def get_unicode_iterable(iterable):
    for index, w in enumerate(iterable):
        if not isinstance(w, unicode):
            iterable[index] = unicode(w, 'utf-8')
    return iterable

def print_unicode_iterable(iterable):
    for i in iterable:
        print i

def detect_lang(text):
    """

    :param text: string or unicode
    :return: language code u'en' or u'kn'
    """
    try:
        return detect(unicode(text, 'utf-8'))
    except TypeError:
        return detect(text)

def get_filenames(folder_path):  # '/Users/deepikaravi/yojana/'
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filenames.append(folder_path + filename)
    return filenames
