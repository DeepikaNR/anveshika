# -*- coding: utf-8 -*-
from datetime import datetime
tstart = datetime.now()

from query_engine import Query
from pipeline_processor import process_pipeline
from utils import detect_lang


def start_query(query_text):

    #query_text = raw_input("Enter query::")
    #query_text = 'capital of karnataka'
    lang_code = detect_lang(query_text)

    print "-" * 160
    print "query_lemmatized_tokens"
    query_lemmatized_tokens = process_pipeline(query_text, lang_code)
    print query_lemmatized_tokens

    engine = Query()
    result_list = engine.free_text_query(query_lemmatized_tokens)
    print result_list
    print "-" * 160

    tend = datetime.now()
    tdiff = tend - tstart
    print "execution time: %d seconds %d microseconds" % (
    tdiff.seconds, tdiff.microseconds)

    return result_list

    
