from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
import pickle
import re
import json
import os

PATH=os.path.split(os.path.realpath(__file__))[0]

def pre_process(text):
	text=text.lower()
	text=re.sub('&lt;/?.*?&gt;', '&lt;&gt ', text)
	text=re.sub("(\\d|\\W)+", " ", text)
	return text

def get_docs(file):
	with open(file, 'r', encoding='utf-8') as f:
		data=json.load(f)
		return data

def save_idf_file(docs):
	docs=[pre_process(i) for i in docs]
	cv=CountVectorizer(stop_words='english')
	wc=cv.fit_transform(docs)

	with open('word_count_vector.plk', 'wb') as f:
		pickle.dump(wc, f)
	with open('count_vectorizer.plk', 'wb') as f:
		pickle.dump(cv, f)

def get_key_words(s, top_n=10):
	def sort_coo(coo_matrix):
		tuples = zip(coo_matrix.col, coo_matrix.data)
		return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

	def extract_topn_from_vector(feature_names, sorted_items, topn=10):
		"""get the feature names and tf-idf score of top n items"""

		# use only topn items from vector
		sorted_items = sorted_items[:topn]

		score_vals = []
		feature_vals = []

		for idx, score in sorted_items:
			fname = feature_names[idx]

			# keep track of feature name and its corresponding score
			score_vals.append(round(score, 3))
			feature_vals.append(feature_names[idx])

		# create a tuples of feature,score
		# results = zip(feature_vals,score_vals)
		results = {}
		for idx in range(len(feature_vals)):
			results[feature_vals[idx]] = score_vals[idx]

		return results

	with open(PATH+'/word_count_vector.plk', 'rb') as f:
		word_count_vector=pickle.load(f)
	with open(PATH+'/count_vectorizer.plk', 'rb') as f:
		cv=pickle.load(f)

	tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
	tfidf_transformer.fit(word_count_vector)
	s=pre_process(s)
	feature_names = cv.get_feature_names()
	tf_idf_vector = tfidf_transformer.transform(cv.transform([s]))
	sorted_items = sort_coo(tf_idf_vector.tocoo())
	keywords = extract_topn_from_vector(feature_names, sorted_items, top_n)

	return keywords


# docs=[]
# count=10000000
# with open('/home/trec/TREC/train/full_marco_sessions_ann_split-train.json',
# 		  'r', encoding='utf-8') as f:
# 	s=''
# 	for line in f:
# 		s+=line
# 		if line == '}\n':
# 			data=eval(s)
# 			s=''
# 			docs+=data['text']
# 			if len(docs)>count:
# 				break
# save_idf_file(docs)


# print(get_key_words('how to unlock ipod if it says ipod is disabled connect to itunes'))
