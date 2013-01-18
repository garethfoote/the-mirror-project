"""
    Dependencies:
    pyyaml nltk numpy (http://nltk.org/install.html)
"""
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.data import load

class POSTagger:
    """Accepts sentences and categorises words into word classes (verb, noun, adjective)"""
    tags = []
    wordtags = ['adverb', 'adjective', 'noun', 'pronoun', 'verb']
    tagdict = load('help/tagsets/brown_tagset.pickle')
    tagdict_b = load('help/tagsets/upenn_tagset.pickle')
    tagdict_c = load('help/tagsets/claws5_tagset.pickle')

    def __init__(self, wordtags=[]):
        self.wordtags = wordtags

    def tag_sentence(self, sentence):
        self.tags = pos_tag(word_tokenize(sentence))
        # for tag in self.tags:
        #     print tag[0]  + ' - ' + tag[1] + ' - ' + self.explain_tag(tag[1])

    def get_by_class(self):
        words=namedtuple('literal', self.wordtags)(**{'name': 'John Smith', 'age':23})
        # for tag in self.tags:
        #     print tag[0]  + ' - ' + tag[1] + ' - ' + self.explain_tag(tag[1])

    def list_tags(self, filters=[]):
        output = []
        alldicts = {}
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
