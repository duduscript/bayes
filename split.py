import jieba
import os

def split_paragraph(paragraph):
	s,sentences = set(),paragraph.split()
	for sentence in sentences:
		words = jieba.cut(sentence, cut_all=False)
		s |= set(words)
	return s

def get_type_dict(paragraphs):
	dic = {}
	for paragraph in paragraphs:
		word_set = split_paragraph(paragraph)
		for word in word_set:
			dic[word] = dic[word]+1 if word in dic else 1
	return dic

def get_type_set(paragraphs):
	s = set()
	for paragraph in paragraphs:
		word_set = split_paragraph(paragraph)
		s |= word_set
	return s

def get_type_paragraphs(type):
	path = os.getcwd() + '/' + type
	if not os.path.exists(path):
		return None
	file_paths = os.listdir(path)
	for file_path in file_paths:
		with open(path + '/' + file_path,'r') as file:
			yield file.read()