# -*- coding: utf-8 -*-
"""
@author: MEHRANI Ardalan <ardalan77400@gmail.com>
"""

import numpy as np
from collections import Counter


def list_to_bytes(l):
    return np.array(l).tobytes()


def list_from_bytes(string, dtype=np.int):
    return np.frombuffer(string, dtype=dtype)


class Preprocessing():

    def __init__(self, lowercase=False):
        self.lowercase = lowercase

    def transform(self, sentence):
        """
        sentences: list(str) 
        output: list(str)
        """
        if self.lowercase:
            return sentence.lower().split()
        else:
            return sentence.split()


class Vectorizer():
    def __init__(self,word_dict=None, min_word_count=5):
        self.word_dict = word_dict
        self.word_counter = Counter()
        self.min_word_count= min_word_count
        self.n_transform = 0
        self.longest_sequence=0

        if self.word_dict:
            self.n_transform += 1
    
    def partial_fit(self, l):
        """
        l: list(str)
        """
        self.word_counter.update(l)
        self.longest_sequence = max(self.longest_sequence, len(l))

    def transform(self,l):
        """
        l: list(str)
        returns s: list(int) 
        """

        if self.n_transform == 0:
            
            # "We only retain words appearing more than 5 times in building the vocabulary and replace the words that appear 5 times with a special UNK token"
            self.word_counter = {k : v for k,v in self.word_counter.items() if v > self.min_word_count}
            self.word_dict =  {w: i for i,w in enumerate(self.word_counter, start=2)}
            self.word_dict["_pad_"] = 0
            self.word_dict["_unk_"] = 1
            print("Dictionnary has {} words".format(len(self.word_dict)))
        self.n_transform += 1
        
        assert self.word_dict, "No dictionnary to vectorize text \n-> call method build_dict \n-> or set a word_dict attribute \n first"

        s = [self.word_dict.get(w, self.word_dict["_unk_"]) for w in l]
        return s

