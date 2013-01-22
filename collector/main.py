import logging, re
from postagging import PartOfSpeechTagger
from traverse import Traverse

# Logging
with open('debug.log', 'w'):
        pass
logging.basicConfig(filename='debug.log',level=logging.DEBUG)

# Directory traversal
def fileFoundHandler(filePath):
    print filePath
    f = open(filePath, 'r')
    content = f.read()

traverse = Traverse(['traverse-test'])
traverse.restrict({'maxSize': 20*1024*1024 })
# traverse.allowTypes(['text/plain', 'text/html', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'])
traverse.allowTypes(['application/msword'])
traverse.onFilePass += fileFoundHandler
traverse.start()


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
