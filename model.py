import util
import os

class Model(object):
    """docstring for ."""
    def __init__(self):
        self.prior_prob = {}
        self.type_model = {}
        self.sources = ['edu','health','finance','tech','baby','sports','mil','ent','auto','games','news']
    def get_prior_prob(self):
        return self.prior_prob
    def get_type_model(self):
        return self.type_model
    def train(self):
        def get_data_num(source):
            return len(os.listdir('/'.join([os.getcwd(),source])))
        def train_prior_prob():
            count = 0
            for source in self.sources:
                self.prior_prob[source] = get_data_num(source)
                count += get_data_num(source)
            for source in self.prior_prob:
                self.prior_prob[source] /= count
        def train_type_model():
            for source in self.sources:
                 type_dict = util.get_type_dict(source)
                 for word in type_dict:
                     type_dict[word] /= get_data_num(source)
        train_prior_prob()
        train_type_model()
    def classify(self,vec):
        pass

if __name__ == '__main__':
    model = Model()
    model.train()
    print(model.get_prior_prob())
    print(model.get_type_model())
