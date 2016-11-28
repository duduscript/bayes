import util
import os
import tfidf
import time

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class Model(object):
    """docstring for ."""
    def __init__(self):
        self.prior_prob = {}
        self.type_model = {}
        self.sources = ['edu','finance','tech','sports','mil','ent','auto','games']
        self.train()
    def get_prior_prob(self):
        return self.prior_prob
    def get_type_model(self):
        return self.type_model
    def get_data_num(self,source):
        return len(os.listdir('/'.join([os.getcwd(),source])))
    def train(self):
        def train_prior_prob():
            count = 0
            for source in self.sources:
                self.prior_prob[source] = self.get_data_num(source)
                count += self.get_data_num(source)
            for source in self.prior_prob:
                self.prior_prob[source] /= count
        def train_type_model():
            for source in self.sources:
                 dic = __import__(source).dic
                 self.type_model[source] = dic
        train_prior_prob()
        train_type_model()
    def classify(self,vec):
        def get_prob(vec,source):
            smooth_prob = 0.001
            prob = self.prior_prob[source]
            for word in vec:
                if word not in self.type_model[source]:
                    prob *= smooth_prob
                else:
                    prob *= self.type_model[source][word]/self.get_data_num(source)
            return prob
        max_prob,result = 0,''
        for i in range(len(self.sources)):
            prob = get_prob(vec,self.sources[i])
            if prob > max_prob:
                max_prob,result = prob,self.sources[i]
        return result


if __name__ == '__main__':
    tfidf = tfidf.TfIdf()
    model = Model()
    paras = os.listdir('test')
    for para in paras:
        with open('/'.join([os.getcwd(),'test',para])) as p:
            print(para)
            text = p.read()
            print(model.classify(tfidf.paragraph2vec(text)))
