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

    """
    q = Query(["/Users/deepikaravi/yojana/anveshika/harvest/54.txt", "/Users/deepikaravi/yojana/anveshika/harvest/56.txt", "/Users/deepikaravi/yojana/anveshika/harvest/60.txt", "/Users/deepikaravi/yojana/anveshika/harvest/102.txt","/Users/deepikaravi/yojana/anveshika/harvest/100.txt","/Users/deepikaravi/yojana/anveshika/harvest/101.txt",
               "/Users/deepikaravi/yojana/anveshika/harvest/120.txt","/Users/deepikaravi/yojana/anveshika/harvest/121.txt","/Users/deepikaravi/yojana/anveshika/harvest/122.txt"])

    print "*" * 100
    print "One word query : Positive test case: Existing word: |Sringeri| "
    print "*" * 100
    print q.print_url(q.one_word_query("sringeri"))
    print "\n\n\n"

    print "*" * 100
    print "One word query : Negative test case: Non-Existing word: |SriLanka| "
    print "*" * 100
    print q.print_url(q.one_word_query("SriLanka"))
    print "\n\n\n"

    print "*" * 100
    print "Phrase query : Positive test case: Existing phrase: |Coastal Karnataka| "
    print "*" * 100
    print q.print_url(q.phrase_query("Coastal Karnataka"))
    print "\n\n\n"

    print "*" * 100
    print "Phrase query : Negative test case: Non-Existing phrase: |Himalayan ranges| "
    print "*" * 100
    print q.print_url(q.phrase_query("Himalayan ranges"))
    print "\n\n\n"

    print "*" * 100
    print "Free text query : Positive test case: Existing text: |national language india| "
    print "*" * 100
    print q.print_url(q.free_text_query("national language india"))
    print "\n\n\n"

    print "*" * 100
    print "Free text query : Negative test case: Non-Existing text: |banjar| "
    print "*" * 100
    print q.print_url(q.free_text_query("address"))
    print "\n\n\n"

    """