# -*- coding: utf-8 -*-

from datetime import datetime
tstart = datetime.now()

from cassandra.cqlengine.management import sync_table

from models import Term, Document
from cassandra.cqlengine.query import DoesNotExist

import math
from pipeline_processor import process_harvest
from build_index import BuildIndex
from utils import db_connect

class Indexer:
    def __init__(self):
        db_connect()
        sync_table(Document)
        sync_table(Term)

    def write_term(self, term, inverted_index, df, idf):
        Term.create(term=term, df=df, idf=idf, inverted_index=inverted_index)
        sync_table(Term)

    def write_documents(self, doc_tf_dict):
        for url, tf in doc_tf_dict.items():
            Document.create(url=url, tf=tf)
        sync_table(Document)

    def update_terms(self, inverted_indexer):
        N = Document.objects.count()
        for term, inverted_index in inverted_indexer.items():
            try:
                tobj = Term.get(term=term)
                index = tobj.inverted_index
                index.update(inverted_index)

                df = len(index.keys())
                try:
                    idf = math.log10(N / df)
                except ZeroDivisionError:
                    idf = 0.0
                Term.objects(term=term).update(inverted_index=index, df=df,
                                               idf=idf)
            except DoesNotExist:
                df = len(inverted_index.keys())
                idf = math.log10(N / df)
                Term.create(term=term, inverted_index=inverted_index, df=df,
                            idf=idf)
        sync_table(Term)

if __name__ == '__main__':

    ind_obj = Indexer()

    # in memory index structuring
    file_to_terms = process_harvest()
    print "**file_to_terms**"
    print file_to_terms
    print "-" * 150
    indexer = BuildIndex(file_to_terms)
    inverted_index_dict = indexer.get_inverted_index()
    print "**inverted_index_dict**"
    print inverted_index_dict
    print "-" * 160
    doc_tf_dict = indexer.get_tf()
    print "**doc_tf_dict**"
    print doc_tf_dict
    print "-" * 160

    # persistance to db
    print "**writing to db..."
    # write doc first. coz we need N(corpus size) for idf calculation in term
    ind_obj.write_documents(doc_tf_dict)
    # term update. if exists update, else write new
    ind_obj.update_terms(inverted_index_dict)

    tend = datetime.now()
    tdiff = tend - tstart
    print "execution time: %d seconds %d microseconds" %(tdiff.seconds, tdiff.microseconds)


    
