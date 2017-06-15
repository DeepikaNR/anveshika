import math

from models import Term, Document
from cassandra.cqlengine.query import DoesNotExist
from utils import db_connect

#input = [file1, file2, ...]
#res = {word: {filename: {pos1, pos2}, ...}, ...}
class Query:

    def __init__(self):
        db_connect()


    def free_text_query(self, query_list):

        hit_urls = []
        for q_word in query_list:
            try:
                tobj = Term.get(term=q_word)
                hit_urls.extend(tobj.inverted_index.keys())
            except:
                print q_word + " not in corpus"
        return self.ranker(hit_urls, query_list)



    def query_vec(self, queryls):

        q_tf = {}
        euclidean_distance = 0

        q_idf = {}
        for word in set(queryls):

            # calculate term_count from query
            q_tf[word] = queryls.count(word)
            euclidean_distance += (q_tf[word] * q_tf[word])

            # idf from db
            try:
                tobj = Term.get(term=word)
                q_idf[word] = tobj.idf
            except DoesNotExist:
                q_idf[word] = 0    # if word not in corpus, idf = 0

        # tf calculation
        euclidean_distance = math.sqrt(euclidean_distance)
        for word, tf in q_tf.items():
            q_tf[word] = tf / euclidean_distance

        # tf-idf calculation
        tf_idf = {}
        for word in queryls:
            tf_idf[word] = q_tf[word] * q_idf[word]

        return tf_idf

    def get_document_scores(self, hit_urls, query_list):
        document_score_dict = {}
        for url in hit_urls:
            try:

                dobj = Document.get(url=url)
                document_score_dict[url] = {}

                for q_word in query_list:
                    try:
                        tf = dobj.tf[q_word]
                    except KeyError:
                        tf = 0
                    try:
                        tobj = Term.get(term=q_word)
                        idf = tobj.idf
                    except DoesNotExist:
                        idf = 0
                    document_score_dict[url][q_word] = tf * idf
            except DoesNotExist:
                print "url %s not in corpus" %url

        return document_score_dict



    def dotProduct(self, vector1, vector2):

        score = 0
        for word in vector1.keys():
            score += vector1[word] * vector2[word]
        return score



    def ranker(self, hit_urls, query_list):

        cosine_similarity = {}

        query_score_dict = self.query_vec(query_list)     # {word1 : tf_idf 1}

        document_score_dict = self.get_document_scores(hit_urls, query_list)


        for url, d_score_dict in document_score_dict.items():
            cosine_similarity[url] = self.dotProduct(d_score_dict, query_score_dict)

        ranked_results = sorted(cosine_similarity.items(), key=lambda (k,v) : (v,k), reverse=True)
        rank_order = [url for url, score in ranked_results]
        return rank_order

