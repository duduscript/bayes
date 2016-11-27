import os
import jieba
import re

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class Util(object):
	"""docstring for ."""
	def __init__(self):
		self.type_dic = {}
		self.sources = ['edu','health','finance','tech','baby','sports','mil','ent','auto','games','news']
		#for source in sources:
		#	self.type_dic[source] = self.get_type_dict(source)
	def get_type_dic(self):
		return self.type_dic
	def get_sources(self):
		return self.sources
	def split_paragraph(self,paragraph):
		s,sentences = set(),filter(lambda x:len(x),re.split('，|。|：|；|　| |,|/.|;| |\n|/?',paragraph))
		for sentence in sentences:
			words = jieba.cut(sentence, cut_all=False)
			s |= set(words)
		return s
	def get_type_dict(self,type):
		paragraphs, dic = self.get_type_paragraphs(type),{}
		for paragraph in paragraphs:
			word_set = self.split_paragraph(paragraph)
			for word in word_set:
				dic[word] = dic[word]+1 if word in dic else 1
		return dic
	def get_type_paragraphs(self,type):
		path = os.getcwd() + '/' + type
		if not os.path.exists(path):
			return []
		file_paths = os.listdir(path)
		for file_path in file_paths:
			with open(path + '/' + file_path,'r') as file:
				yield file.read()

if __name__ == '__main__':
	util = Util()
	for source in util.get_sources():
		dic = __import__(source).dic
		print(source,len(dic))
