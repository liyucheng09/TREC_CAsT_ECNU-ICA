from key_words.rake import key_word_rake as rake_keywords
from key_words.summa.keywords import keywords as textrank_keywords
from key_words.tfidf import get_key_words as tfidf_keywords
from key_words.qe import query_expansion
from key_words.find_entity import Annotate

from lemmatizer import word_lemmatize
from search_documents import search as search_candidate
import sys
import nltk
from allennlp.predictors.predictor import Predictor
import json
import subprocess
from get_answers import ranking_answers
import os

COREF_RESOLER = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz")


# def get_result(query, mod='tfidf', item_number=10):
#     if mod == 'rake': keyword = list(rake_keywords(query).keys())
#     if mod == 'textrank': keyword = textrank_keywords(query).split('\n')
#     if mod == 'tfidf': keyword = list(tfidf_keywords(query).keys())
#     if keyword != [''] and len(keyword) != 0: 
#         try:
#           keyword = word_lemmatize(keyword)
#           print("complete lemmatize word")
#           key_word = query_expansion(keyword)
#           print("complete word expansion")
#         except:
#           pass
#     print('keyword: ', keyword)
#           
#     print("writing tsv")
#     candidates = search_candidate(keyword, size=item_number)
#     with open('bert/test/test.tsv', "w", encoding='utf-8') as f:
#         f.write("index	#1 ID	#2 ID	#1 String	#2 String\n")
#         for _, item in enumerate(candidates):
#             f.write("{}\t{}\t{}\t{}\t{}\n".format(_, item['_id'], 0,
#                                                ' '.join(nltk.word_tokenize(item['_source']['BODY'].strip())), query.strip()))
#     print("complete")


def get_result(utte, keywords, num_sess, num_utte, item_number=10):
	"""
	Given keywords, do lemmatize and query expansion,
	then search in database, finally, write result in test.tsv file
	ready to rerank by bert.

	:param keywords: a dict of keywords
	:param item_number:
	"""
	if len(keywords) != 0:
		# try:
		#     keyword = word_lemmatize(keyword)
		#     print("complete lemmatize word")
		#     key_word = query_expansion(keyword)
		#     print("complete word expansion")
		# except:
		#     pass
		keywords = word_lemmatize(keywords)
		print("complete lemmatize word")
		key_words = query_expansion(keywords)
		print("complete word expansion")
	print('keyword: ', keywords)
	candidates = search_candidate(keywords, size=item_number)
	with open('Before_rerank/'+str(num_sess)+'_'+str(num_utte)+'.tsv', "w", encoding='utf-8') as f:
		f.write("index	#1 ID	#2 ID	#1 String	#2 String\n")
		for _, item in enumerate(candidates):
			f.write("{}\t{}\t{}\t{}\t{}\n".format(_, item['_id'], 0,
												  ' '.join(nltk.word_tokenize(item['_source']['BODY'].strip())),
												  ' '.join(nltk.word_tokenize(utte.strip()))))
	with open('score_of_retrieval/'+str(num_sess)+'_'+str(num_utte)+'.json', "w", encoding='utf-8') as f:
		score_of_retrieval={item['_id']:item['_score'] for item in candidates}
		json.dump(score_of_retrieval, f, ensure_ascii=False, indent=4)
	# return candidates
	print("Finsh write result in test.tsv")


def main(session_path, mod, item_number):
	def merge_dic(dic1, dic2):
		"""

		:param dic1:
		:param dic2:
		:return: final_dic: a dict of keywords after de-repetitions
		"""
		for key in dic1:
			if key in dic2:
				v = max(dic1[key], dic2[key])
				dic2[key] = v
			else:
				dic2[key] = dic1[key]
		final_dic = dic2
		return final_dic

	def find_keywords():
		if os.path.isfile('after_find_keywords.json'):
			with open('after_find_keywords.json', 'r', encoding='utf-8') as f:
				all_sessions = json.load(f)
			return all_sessions

		with open(session_path.strip(), 'r', encoding='utf-8') as f:
			all_sessions = json.load(f)
		# all_sessions = all_sessions[:1]
		# coreference resolving for all sessions
		for index, sess in enumerate(all_sessions):
			sess['turn'] = coreference_resolve(sess['turn'])
			print('Session NO.%d, Finish Corf_resolve! ' % index)

			for utte in sess['turn']:
				# Get entities
				resolved_entities = Annotate(utte['resolved_utterance'], theta=0.1)
				raw_entities = Annotate(utte['raw_utterance'], theta=0.1)
				resolved_entities = {k[1]: v for k, v in resolved_entities.items()}
				raw_entities = {k[1]: v for k, v in raw_entities.items()}
				final_entities = merge_dic(resolved_entities, raw_entities)
				utte['entities'] = final_entities

				# Get keywords
				resolved_keywords = tfidf_keywords(utte['resolved_utterance'])
				raw_keywords = tfidf_keywords(utte['raw_utterance'])
				final_keywords = merge_dic(resolved_keywords, raw_keywords)
				utte['keywords'] = final_keywords

			# sess['keywords_of_description']=tfidf_keywords(sess['description'])
			sess['entities_of_description'] = \
				{k[1]: v for k, v in
				 Annotate((sess['description'] if 'description' in sess else '') + ' ' + sess['title']).items()}

		with open('after_find_keywords.json', 'w', encoding='utf-8') as f:
			json.dump(all_sessions, f, indent=4, ensure_ascii=False)
		return all_sessions
	def find_keywords_():
		if os.path.isfile('without_resolved_keywords.json'):
			with open('without_resolved_keywords.json', 'r', encoding='utf-8') as f:
				all_sessions = json.load(f)
			return all_sessions

		with open(session_path.strip(), 'r', encoding='utf-8') as f:
			all_sessions = json.load(f)
		# all_sessions = all_sessions[:1]
		# coreference resolving for all sessions
		for index, sess in enumerate(all_sessions):
			# sess['turn'] = coreference_resolve(sess['turn'])
			print('Session NO.%d, Begin Annotation! ' % index)

			for utte in sess['turn']:
				# Get entities
				resolved_entities = Annotate(utte['resolved_utterance'], theta=0.1)
				# raw_entities = Annotate(utte['raw_utterance'], theta=0.1)
				resolved_entities = {k[1]: v for k, v in resolved_entities.items()}
				# raw_entities = {k[1]: v for k, v in raw_entities.items()}
				# final_entities = merge_dic(resolved_entities, raw_entities)
				utte['entities'] = resolved_entities

				# Get keywords
				resolved_keywords = tfidf_keywords(utte['resolved_utterance'])
				# raw_keywords = tfidf_keywords(utte['raw_utterance'])
				# final_keywords = merge_dic(resolved_keywords, raw_keywords)
				utte['keywords'] = resolved_keywords

			# sess['keywords_of_description']=tfidf_keywords(sess['description'])
			# sess['entities_of_description'] = \
			# 	{k[1]: v for k, v in
			# 	 Annotate((sess['description'] if 'description' in sess else '') + ' ' + sess['title']).items()}

		with open('without_resolved_keywords.json', 'w', encoding='utf-8') as f:
			json.dump(all_sessions, f, indent=4, ensure_ascii=False)
		return all_sessions

	# all_sessions = find_keywords()
	all_sessions=find_keywords_()

	'''
	Now sess will be look like:
		{
			description:'....',
			entities_of_description:{'US':0.8, ...},
			title:'',
			turn:[
				{
					'number':1,
					'raw_utterance':'',
					'resolved_utterance':'',
					'entities':{...},
					'keywords':{...}
				},
				...
			]
		
		}
	'''

	def sample_keywords(num, dic):
		dic = {k: float(v) for k, v in dic.items()}
		selected_keywords = sorted(dic, key=lambda x: dic[x], reverse=True)[:num]
		return {w: round(dic[w], 4) for w in selected_keywords}

	for index_sess, sess in enumerate(all_sessions):
		for index_utte, utte in enumerate(sess['turn']):
			# if hasattr(utte, 'candidates'):
			# 	continue
			if os.path.isfile('score_of_retrieval/'+str(index_sess)+'_'+str(index_utte)+'.tsv'):
				continue
			# keywords=merge_dic(merge_dic(utte['entities'], utte['keywords']),
			#                    sess['entities_of_description'])
			keywords = merge_dic(utte['entities'], utte['keywords'])
			# print(keywords)
			keywords = {k: round(float(v), 4) for k, v in keywords.items()}
			# if len(keywords) < 5:
			# 	print('Origin_keywords: ', keywords)
			# 	expand_keywords = sample_keywords(5 - len(keywords), sess['entities_of_description'])
			# 	keywords = merge_dic(keywords, expand_keywords)
			# 	print('Expanded keywords: ', expand_keywords)
			retry = 3
			while retry > 0:
				try:
					# utte['candidates'] = get_result(utte['resolved_utterance'], keywords, item_number=item_number)
					get_result(utte['resolved_utterance'], keywords, index_sess, index_utte, item_number=item_number)
				# with open('Before_rerank_result.json', 'w', encoding='utf-8') as f:
				# 	json.dump(all_sessions, f, indent=4, ensure_ascii=False)
					break
				except:
					retry -= 1
					continue
	# subprocess.call(['bash', '/home/trec/TREC/tools/bert/reranking.sh'])
	# answers=ranking_answers('bert/test/test.tsv', 'bert/test/test_results.tsv')
	# utte['answers']=answers[:1000]

	# with open('Before_rerank_result.json', 'w', encoding='utf-8') as f:
	#	json.dump(all_sessions, f, indent=4, ensure_ascii=False)
	print('Finsh write candidates to file.')


def coreference_resolve(sess):
	'''

	:param sess: a list of utterance, format based on TREC CAsT official
			evaluate file
	:return: sess: a list of utterance, coreference already
			replaced by corresponding entity
	'''
	global COREF_RESOLER
	context = ''
	for index, utte in enumerate(sess):
		if index == 0:
			context += utte['raw_utterance'] + ' '
			utte['resolved_utterance'] = utte['raw_utterance']
			continue
		raw_utterance = utte['raw_utterance']
		text = context + '\n' + raw_utterance
		resolved_text = COREF_RESOLER.coref_resolved(document=text)
		try:
			resolved_utterance = resolved_text.split('\n')[1]
		except:
			resolved_utterance = raw_utterance
		context += resolved_utterance + ' '
		utte['resolved_utterance'] = resolved_utterance

	return sess


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3])
