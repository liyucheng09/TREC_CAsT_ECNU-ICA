# TREC CAsT

TREC 是美国国家标准技术研究所(NIST)举办的信息检索竞赛。Conversational Assistant Track(CAsT)是2019年新添加的一个任务，旨在推动检索式对话助手的发展。
任务介绍，任务最新情况见TREC CAsT：http://www.treccast.ai/

# Our Method

![](https://github.com/nine09/TREC_CAsT_ECNU-ICA/blob/master/pics/our_method.png)

- TREC CAsT数据的处理脚本放在`Data_processing`.
- 我们的检索工具：ElasticSearch。处理ElasticSearch所需格式的数据的脚本在`ElasticSearch_data_processing`.
- 我们使用Allennlp做指代消解。使用方法在`pipeline.py`中的`coreference_resolve()`函数中。
- `pip install tagme`，使用tagme工具将文本中的实体链接至wikipedia实体。详细使用方法在`key_words.find_entity`。
	- 另：之所以使用实体链接工具是避免在本地建立wikipedia索引，和进行检索操作。同时，tagme的效果也足够好能够应付简单的实体链接任务。
- 关键词抽取使用TFIDF或RAKE算法。`key_words.key_word_extraction`中有使用示范。
	- 注意：TFIDF需要使用词频统计表文件：`word_count_vector.plk`，并将其放在key_words文件夹下。下载请访问：https://pan.baidu.com/s/11LAjog2eoVcolYLqmtCNcw
- 我们使用WordNet做Query Expansion。具体代码在`key_words.qe`。值得注意的是我们使用上下文中出现的实体（由实体链接得到的）作为本句的检索词，为了能够起到跟踪上下文和query expansion的效果。
	- 另：由于实体已经被链接到wikipedia的条目，我们可以使用该条目的邻居实体或该条目的属性作为query expansion的一部分。经实验，该方法可以带来一定提高。
- Rerank：我们使用BERT模型对问答对的相关性建模，按照相关性进行排序。

*其他工具*
- Google爬虫：为了搜集训练数据。代码和说明在`gspider`文件夹。

# References

- ElasticSearch:https://www.elastic.co/cn/
- Allennlp:https://allennlp.org/
- tagme:https://tagme.d4science.org/tagme/
- RAKE:https://github.com/csurfer/rake-nltk
- RAKE paper:https://www.researchgate.net/profile/Stuart_Rose/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents/links/55071c570cf27e990e04c8bb.pdf
- BERT:https://github.com/google-research/bert