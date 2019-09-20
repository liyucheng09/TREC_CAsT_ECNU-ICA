# This script turn rerank result to TREC CAsT 2019 submission file format.
# Format is as fellowing:
# <TOPICID>_<TURNID> Q0 <CAR_9918559420932915201> <1> <34.4> <samplerun>
# TOPICID_TURNID Q0 MARCO_12491099185594209 2 31.2 samplerun
# TOPICID_TURNID Q0 WAPO_b2e89334-33f9-11e1-825f-dabc29fd7071-1 3 30.2 samplerun

import os
import json
import time

BASE_PATH='/home/trec/TREC/tools/'

def origin_retrieval_rank():
	output_str_list=[]

	result_dir='score_of_retrieval/'
	files=os.listdir(BASE_PATH+result_dir)
	files=sorted(files, key=lambda file: int(file.split('.')[0].split('_')[0])*100+int(file.split('.')[0].split('_')[1]))
	for file in files:
		sess_num, utte_num=file.split('.')[0].split('_')
		with open(BASE_PATH+result_dir+file) as f:
			data=json.load(f)
		selected_instances=sorted(data, key=lambda x:data[x], reverse=True)[:1000]
		for index, instance in enumerate(selected_instances):
			one_line_result='%d_%d Q0 %s %d %.5f ECNUICA_ORI' % (int(sess_num)+31,
																 int(utte_num)+1,
																 instance,
																 index+1,
																 data[instance])
			output_str_list.append(one_line_result)
	# output_str_list=sorted(output_str_list)
	with open('ECNUICA_ORI.txt', 'w', encoding='utf-8') as f:
		for line in output_str_list:
			f.write(line+'\n')

def bert_rank():
	def sort_file(file):
		file = file.replace('rerank_result', '')
		sess_num, utte_num = file.split('.')[0].split('_')
		return int(sess_num)*100+int(utte_num)
	output_str_list = []

	result_dir = 'rerank_result/'
	files = os.listdir(BASE_PATH + result_dir)
	files=sorted(files, key=lambda f:sort_file(f))
	for file in files:
		with open(BASE_PATH + result_dir + file) as f:
			data = json.load(f)
		file = file.replace('rerank_result', '')
		sess_num, utte_num = file.split('.')[0].split('_')
		selected_instances = [(i[0][0], i[1]) for i in data[:1000]]
		for index, (instance, score) in enumerate(selected_instances):
			one_line_result = '%d_%d Q0 %s %d %.5f ECNUICA_BERT' % (int(sess_num) + 31,
																   int(utte_num) + 1,
																   instance,
																   index + 1,
																   score)
			output_str_list.append(one_line_result)
	with open('ECNUICA_BERT.txt', 'w', encoding='utf-8') as f:
		for line in output_str_list:
			f.write(line + '\n')

def mix_rank():
	def sort_file(file):
		file = file.replace('rerank_result', '')
		sess_num, utte_num = file.split('.')[0].split('_')
		return int(sess_num)*100+int(utte_num)
	output_str_list=[]

	ori_result_dir='score_of_retrieval/'
	bert_result_dir='rerank_result/'
	ori_files = os.listdir(BASE_PATH + ori_result_dir)
	bert_files=os.listdir(BASE_PATH+bert_result_dir)
	ori_files=sorted(ori_files, key=lambda file: int(file.split('.')[0].split('_')[0])*100+int(file.split('.')[0].split('_')[1]))
	bert_files = sorted(bert_files, key=lambda f: sort_file(f))
	for (ori_file, bert_file) in zip(ori_files, bert_files):
		bert_file_str = bert_file.replace('rerank_result', '')
		sess_num, utte_num = bert_file_str.split('.')[0].split('_')
		sess_num_, utte_num_ = ori_file.split('.')[0].split('_')

		assert sess_num==sess_num_ and utte_num==utte_num_, "Two kinds of results file are not aligned!"

		with open(BASE_PATH+ori_result_dir+ori_file) as f:
			data=json.load(f)
		data={k:[v, 0.5] for k,v in data.items()}
		with open(BASE_PATH+bert_result_dir+bert_file) as f:
			bert_=json.load(f)
			for ins in bert_:
				if ins[0][0] in data:
					data[ins[0][0]]=[data[ins[0][0]][0], ins[1]]
			id2doc={ins[0][0]:ins[0][1] for ins in bert_}

		# decay_weight_for_bert=0.7
		weight_for_bert=3
		final_score={k:v[0]+v[1]*weight_for_bert for k,v in data.items()}
		selected_instances=sorted(final_score, key=lambda x:final_score[x], reverse=True)[:1000]
		for index, instance in enumerate(selected_instances):
			one_line_result = '%d_%d Q0 %s %d %.5f ECNUICA_MIX' % (int(sess_num) + 31,
																   int(utte_num) + 1,
																   instance,
																   index + 1,
																   final_score[instance])
			output_str_list.append(one_line_result)
	with open('ECNUICA_MIX.txt', 'w', encoding='utf-8') as f:
		for line in output_str_list:
			f.write(line+'\n')
		# for ins in top10:
		# 	print('%s_%s\t%s\t%s' % (sess_num, utte_num, ins, id2doc[ins]))
		# time.sleep(1)


# origin_retrieval_rank()
# bert_rank()
mix_rank()
