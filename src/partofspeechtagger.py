"""
    Dependencies:
    pyyaml nltk numpy (http://nltk.org/install.html)
"""
import re
from collections import namedtuple
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.data import load
from lxml import etree

class PartOfSpeechTagger:
    """Accepts sentences and categorises words into word classes (verb, noun, adjective)"""
    tags = []
    wordtags = []
    tagdict = []
    tagdict_b = []
    tagdict_c = []

    def __init__(self, wordtags=[]):
        if len(wordtags) > 0:
            self.wordtags = wordtags

    def tag(self, data):
        self.__data = data
        self.tags = pos_tag(word_tokenize(data))
        return self.tags

    def printAll(self):
        print self.tags

    def getFormatted(self, format, asXML=True):
        dataOut = ''

        for tag in self.tags:

            # TODO - Accomodate for double quotation marks.
            # NLTK doesn't handle them as expected.

            # Find strpos of word
            strstart = self.__data.index(tag[0])
            strend = strstart + len(tag[0])

            # If tag is in required type list.
            if tag[1] not in [',','.'] and (len(self.wordtags) == 0 or tag[1] in self.wordtags):
                output = format % (tag[1], tag[0])
            else:
                output = format % ("NONE", tag[0])

            # Replace in original data string to
            # ensure format retention (i.e. \n & \t)
            dataOut  += self.__data[:strstart] + output
            self.__data = self.__data[strend:]

        if asXML == True:
            outputroot = etree.fromstring("<tags>"+dataOut+"</tags>")
            outputtree = etree.ElementTree(outputroot)
            dataOut = outputroot

        return dataOut


    def getByClass(self):
        if len(self.wordtags) == 0:
            for tag in self.tags:
                if tag[1] not in self.wordtags:
                    self.wordtags.append(tag[1])

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
                        output.append("%s\t%s" % (tag, descr))
                        break
            else:
                output.append("%s\t%s" % (tag, descr))

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

    def findnth(self, haystack, needle, n):

        # parts=re.split('\b(' + needle + ')\b', haystack, n+1)
        parts = haystack.split(needle, n+1)
        if len(parts)<=n+1:
            return -1
        return len(haystack)-len(parts[-1])-len(needle)
