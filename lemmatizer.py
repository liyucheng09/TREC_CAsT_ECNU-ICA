import nltk.stem as ns
import nltk.tokenize as tk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag

# nltk.download()
# tokens = tk.word_tokenize(words)
lemmatizer = ns.WordNetLemmatizer()
wnl = WordNetLemmatizer()


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def word_lemmatize(tokens):

    new_dict = {}
    tagged_sent = []
    value = []
    for token in tokens.keys():
        tagged_sent.append((pos_tag([token])[0][0],pos_tag([token])[0][1],tokens[token]))

    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        new_dict.setdefault(wnl.lemmatize(tag[0], pos=wordnet_pos), tag[2])

    return new_dict


#print(word_lemmatize(['showing', 'awarded']))
