# import string
from nltk.corpus import wordnet
from nltk import data
data.path.append('/home/trec/nltk_data')
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords

def query_expansion(dict_of_keywords):
	synonyms = []
	count = 0
	new_dict = {}
	for x in dict_of_keywords.keys():
		new_dict.setdefault(x, dict_of_keywords[x])
		for syn in wordnet.synsets(x):
			for l in syn.lemmas():
				if (count < 3):
					if l.name() not in new_dict.keys():
						new_dict.setdefault(l.name(), dict_of_keywords[x])
						count += 1

		count = 0
	return new_dict
