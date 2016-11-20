import split
import os

'''
def get_prior_probabilities(type_freq):
	count = sum(type_freq.keys())
	type_prob = {}
	for item in type_freq.items():
		type,frequency = item,key[item]
		type_prob[type] = frequency/count
	return type_prob

def get_type_freq(type):
	pwd = os.getcwd()
	return [type,len(os.listdir(pwd+'/'+type))]
'''

def get_feature_set(type):
	return split.get_type_set(split.get_type_paragraphs(type))

def get_feature_dict(type):
	return split.get_type_dict(split.get_type_paragraphs(type))

def get_types():
	return filter(lambda x:os.path.isdir(x) and not x.startswith('.') and not x.startswith('_'),os.listdir())

def get_all_features():
	types,s = get_types(),set()
	for type in types:
		s |= split.get_type_set(type)
	return list(s)

def get_paragraph_vector(paragraph):
	features, paragraph_set = get_all_features(),split.split_paragraph(paragraph)
	for feature in features:
		yield 1 if feature in paragraph_set else 0

