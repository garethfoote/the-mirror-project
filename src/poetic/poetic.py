from partofspeechtagger import PartOfSpeechTagger
from lxml import etree

class Poetic:
    """Poetic parser """
    def __init__(self, config, wordTags):
        self._config = config
        self.__posTagger = PartOfSpeechTagger(wordTags)

    def start(self):
        self.parse()
        self.output()

    def parse(self):
        self.__input = etree.parse(self._config.input)

        for poem in self.__input.findall('poem'):
            self.__posTagger.tag(poem.text);
            tagged = self.__posTagger.getFormatted(self._config.format)
            poem.text = etree.CDATA(tagged)

        return self.__input

    def output(self):
        self.__input.write(self._config.output)

    def findnth(self, haystack, needle, n):
        parts= haystack.split(needle, n+1)
        if len(parts)<=n+1:
            return -1
        return len(haystack)-len(parts[-1])-len(needle)

        # Pass sentence to PoS Tagger and categorise by class
        # self.__posTagger.tag('They refuse to permit us to obtain the refuse permit. The rain in spain falls mainly on the plain.')
        # print self.__posTagger.getFormatted("<replace class='%s'>%s</replace>")








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
