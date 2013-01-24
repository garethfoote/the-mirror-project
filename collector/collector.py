import re
from partofspeechtagger import PartOfSpeechTagger
from traverse import Traverse
from textparser.parser import *

class Collector:
    """Collector application"""
    def __init__(self, dirs):
        self.__traverse = Traverse(dirs)
        self.__posTagger = PartOfSpeechTagger(['RB', 'JJ', 'JJR', 'AJS', 'NN', 'NNS', 'NN1', 'PN', 'VB', 'VBP'])

    def startTraverse(self):
        self.__traverse.restrict({'maxSize': 20*1024*1024 })
        self.__traverse.allowTypes(['text/html'])
        self.__traverse.onFilePass += self.__fileFoundHandler
        self.__traverse.start()
        # traverse.allowTypes(['text/plain', 'text/html', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'])

    def __initParser(self, data, mimeType):
       return {
            'text/plain': TextParser(data),
            'text/html': HTMLTextParser(data, { "acceptedTags":['p','h1']}),
            'application/msword': HTMLTextParser(data),
            }[mimeType]

    def __fileFoundHandler(self, filePath, mimeType):
        print "File found: %s - %s" % (filePath, mimeType)
        f = open(filePath, 'r')
        data = f.read()
        parser = self.__initParser(data, mimeType);
        parsedData = parser.parse()
        self.__tagText(parsedData)

    def __tagText(self, text):
        self.__posTagger.tag_sentence(text)
        print self.__posTagger.get_by_class()

"""
# Part of Speech Tagging
pos_tagger = PartOfSpeechTagger(['RB', 'JJ', 'JJR', 'AJS', 'NN', 'NNS', 'NN1', 'PN', 'VB', 'VBP'])

# Get list of all tag shortcode and their defintion+examples
# alltags = pos_tagger.list_tags(['noun', 'verb', 'adjective'])
# print "%s\nlength:%s" % (''.join(alltags), str(len(alltags)))

# Pass sentence to PoS Tagger and categorise by class
# print pos_tagger.tag_sentence('And now for something completely different')
pos_tagger.tag_sentence('They refuse to permit us to obtain the refuse permit. The rain in spain falls mainly on the plain.')
print pos_tagger.get_formatted("<replace class='%s'>%s</replace>")
# print pos_tagger.get_by_class()

# RB - Adverb
# JJ - Adjective or numeral, ordinal
# JJR - Adjective comparative
# AJS - superaltive adjective
# NN - noun, common, singular
# NNS - noun, common, plural
# NN1 - singular noun
# PN = pronoun
# VB - verb, base form
"""
