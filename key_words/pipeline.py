from summa.keywords import keywords as textrank_keywords
from rake import key_word_rake as rake_keywords
from tfidf import get_key_words as tfidf_keywords

from qe import query_expansion

from search_documents import search

query='how to unlock ipod if it says ipod is disabled connect to itunes'

keywords=tfidf_keywords(query)
keywords=[k for k,v in keywords.items()]

print('Key_words before expansion: ', keywords)

keywords=query_expansion(keywords)
print('Key_words after expansion: ', keywords)
print('Search in database: ')
print(search(words=keywords))