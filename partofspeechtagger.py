"""
    Dependencies:
    pyyaml nltk numpy (http://nltk.org/install.html)
"""
from collections import namedtuple
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.data import load

class PartOfSpeechTagger:
    """Accepts sentences and categorises words into word classes (verb, noun, adjective)"""
    tags = []
    wordtags = ['RB', 'JJ', 'JJR', 'AJS', 'NN', 'NNS', 'NN1', 'PN', 'VB']
    tagdict = []
    tagdict_b = []
    tagdict_c = []

    def __init__(self, wordtags=[]):
        if len(wordtags) > 0:
            self.wordtags = wordtags

    def tag_sentence(self, sentence):
        self.tags = pos_tag(word_tokenize(sentence))
        return self.tags

    def get_formatted(self, format):
        output = ''
        for tag in self.tags:
            if tag[1] in self.wordtags:
                output += format % (tag[1], tag[0]) + " "
            else:
                if tag[0] == '.':
                    output = output[:-1] + tag[0]
                else:
                    output += tag[0] + " "
        return output

    def get_by_class(self):
        words = dict((tag, []) for tag in self.wordtags)
        for tag in self.tags:
            if tag[1] in words:
                # words[tag[1]].append(tag[0].decode('unicode_escape'))
                words[tag[1]].append(tag[0])
        return words

    def list_tags(self, filters=[]):
        output = []
        alldicts = {}

        if len(self.tagdict) == 0:
            self.tagdict = load('help/tagsets/brown_tagset.pickle')
            self.tagdict_b = load('help/tagsets/upenn_tagset.pickle')
            self.tagdict_c = load('help/tagsets/claws5_tagset.pickle')

        # Fastest method for concatenating dictionaries - http://stackoverflow.com/questions/1781571/how-to-concatenate-two-dictionaries-to-create-a-new-one-in-python
        alldicts = dict(self.tagdict, **self.tagdict_b)
        alldicts.update(self.tagdict_c)
        for tag in alldicts:
            descr = str(alldicts[tag])
            if len(filters) > 0:
                for f in filters:
                    if descr.find(f) > -1:
                        output.append("%s%s\n" % (tag, descr))
                        break
            else:
                output.append("%s%s\n" % (tag, descr))

        return output

    def __explain_tag(self, part):
        fixes = {
            'FW': 'foreign',
            'NC': 'citations',
            'HL': 'headlines',
            'TL': 'titles'
            }

        if part is None:
            return 'Unidentified'
        if part in self.tagdict:
            data = self.tagdict[part]
        elif part in self.tagdict_b:
            data = self.tagdict_b[part]
        elif part in self.tagdict_c:
            data = self.tagdict_c[part]
        else:
            if part in fixes:
                return fixes[part]
            return '?'

        return data[0]
