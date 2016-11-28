import model
import math
import os
import util
#import util

class TfIdf(object):
    """docstring for T."""
    def __init__(self):
        #self.tfs = {}
        self.mdl = model.Model()
        self.dic = __import__('dict').dic
        self.doc_num = sum(map(lambda x:len(os.listdir(x)),self.mdl.sources))
        self.util = util.Util()
        #self.tfs = {x:self.dic[x]/self.doc_num for x in self.dic}
    def get_word_tf(self,word,paragraph):
        para_dict = self.util.get_dict_from_paragraph(paragraph)
        return para_dict[word]/max(para_dict.values()) if word in para_dict else 0
    def get_word_idf(self,word):
        return math.log(self.doc_num/(self.dic[word]+1))
    def get_word_tfidf(self,word,paragraph):
        return self.get_word_tf(word,paragraph)*self.get_word_idf(word)
    def paragraph2vec(self,paragraph):
        words = self.util.split_paragraph(paragraph)
        word_tfidf = {}
        for word in words:
            word_tfidf[word] = self.get_word_tfidf(word,paragraph)
        return sorted(word_tfidf.keys(),key=lambda x:word_tfidf[x])[:30]


'''
if __name__ == '__main__':
    tfidf = TfIdf()
    paras = os.listdir('test')
    for para in paras:
        with open('/'.join([os.getcwd(),'test',para])) as p:
            print(para)
            text = p.read()
            print(tfidf.paragraph2vec(text))
'''
