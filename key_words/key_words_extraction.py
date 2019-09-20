from summa.keywords import keywords as textrank_keywords
from rake import key_word_rake as rake_keywords

from tfidf import get_key_words as tfidf_keywords

query='how to unlock ipod if it says ipod is disabled connect to itunes'

print('* rake:  ', rake_keywords(query))
print('* textrank:   ', textrank_keywords(query))
print('* tfidf:   ', tfidf_keywords(query))