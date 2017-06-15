#input = [file1, file2, ...]
#res = {filename: [world1, word2]}


import math

class BuildIndex:

    def __init__(self, file_to_terms):

        self.file_to_terms = file_to_terms
        self.regdex = self.make_indices(self.file_to_terms)


    #input = [word1, word2, ...]
    #output = {word1: [pos1, pos2], word2: [pos2, pos434], ...}
    def index_one_file(self, termlist):
        fileIndex = {}
        for index, word in enumerate(termlist):
            if word in fileIndex.keys():
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]
        return fileIndex

    #input = {filename: [word1, word2, ...], ...}
    #res = {filename: {word: [pos1, pos2, ...]}, ...}
    def make_indices(self, termlists):
        total = {}
        for filename in termlists.keys():
            total[filename] = self.index_one_file(termlists[filename])
        return total

    #input = {filename: {word: [pos1, pos2, ...], ... }}
    #res = {word: {filename: [pos1, pos2]}, ...}, ...}
    def get_inverted_index(self):
        total_index = {}
        indie_indices = self.regdex
        for filename in indie_indices.keys():

            for word in indie_indices[filename].keys():

                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].append(indie_indices[filename][word][:])
                    else:
                        total_index[word][filename] = indie_indices[filename][word]
                else:
                    total_index[word] = {filename: indie_indices[filename][word]}
        return total_index


    def get_tf(self):
        tf = {}  # tf = {'rama' : 0.67}
        for url, term_list in self.file_to_terms.items():
            tf[url] = {}
            euclidean_distance = 0
            for term in set(term_list):
                term_count = term_list.count(term)
                tf[url][term] = term_count
                euclidean_distance += (term_count * term_count)

            euclidean_distance = math.sqrt(euclidean_distance)
            for word, term_count in tf[url].items():
                tf[url][word] = term_count / euclidean_distance

        return tf

if __name__ == '__main__':
    obj = BuildIndex()
