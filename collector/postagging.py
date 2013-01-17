"""
    Dependencies:
    pyyaml nltk numpy (http://nltk.org/install.html)
"""
import nltk


class Tag:
    tag = ''
    word = ''
    def __init__(self, tag, word):
        self.tag = tag
        self.word = word

class POSTagging:
    """Accepts sentences and categorises words into word classes (verb, noun, adjective)"""
    wordtags = [Tag('ADJ', 'adjective'), Tag('ADV', 'adverb'),
                Tag('N', 'noun'), Tag('NP', 'proper noun'), Tag('PRO', 'proper noun'),
                Tag('V', 'verb'), Tag('MOD', 'modal verb')]
    tagdict = nltk.data.load('help/tagsets/brown_tagset.pickle')
    tagdict_b = nltk.data.load('help/tagsets/upenn_tagset.pickle')
    tagdict_c = nltk.data.load('help/tagsets/claws5_tagset.pickle')

    def tagSentence(self, sentence):
        text = nltk.word_tokenize(sentence)
        tags = nltk.pos_tag(text)
        for tag in tags:
            print tag[0]  + ' - ' + tag[1] + ' - ' + self.explainTag(tag[1])
             #for index, something in nltk.help.upenn_tagset(tag[1]):

    def explainTag(self, part):

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
