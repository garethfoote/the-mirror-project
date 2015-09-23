# Work our frequency of word classes in all.txt.
import nltk.corpus
from nltk.tag import pos_tag
from nltk.tokenize import WhitespaceTokenizer
f = open('all.txt')
raw = f.read()
tagged = pos_tag(WhitespaceTokenizer().tokenize(raw))
tag_fd = nltk.FreqDist(tag for (word, tag) in tagged)
print tag_fd.keys()
