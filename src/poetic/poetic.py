from partofspeechtagger import PartOfSpeechTagger
from lxml import etree
import os, sys
from copy import deepcopy

class Poetic:

    """Poetic parser """
    def __init__(self, config, wordTags):
        self._config = config
        self.__posTagger = PartOfSpeechTagger(wordTags)

    def start(self):
        print "Traversing directory: " + self._config.input
        # If this is directory.
        if os.path.isdir( self._config.input ):
            self.createoutputdir(self._config.input);

            # Loop dir for files to parse.
            for f in os.listdir( self._config.input ):
                if os.path.isfile( os.path.normpath(self._config.input) + os.sep + f ):
                    self.parse( os.path.normpath(self._config.input) + os.sep + f )

        # else is a single file for parsing.
        else:
            directory = os.path.dirname( self._config.input )
            self.createoutputdir( directory );
            self.parse( self._config.input )

    def createoutputdir(self, directory):
        self.__outputDir = directory + '/output/'

        if os.path.exists(self.__outputDir) == False:
            os.makedirs(self.__outputDir)

    def parse(self, filepath):

        # Protect against hidden files.
        bn = os.path.basename(filepath)
        if bn.startswith('.') or bn.endswith('~'):
            return

        print "Parsing: "+ filepath

        # Read file.
        self.__input = open(filepath, 'r')

        # If basename is not xml then make sure output IS xml.
        if filepath[-3:] != "xml":
            bn = bn[:-3] + "xml"

        # Create output file for writing
        outputf = open(self.__outputDir + bn, 'w+');

        # Remove all newlines before passing to NLP lib.
        inputlines = self.__input.read().splitlines()
        inputnolines = ' '.join([str(x).strip() for x in inputlines]).rstrip()

        # Parse poem through NLP lib.
        self.__posTagger.tag(inputnolines);
        output = self.__posTagger.getFormatted()
        # for element in output:
        #     print("%s - %s" % (element.get('class'), element.text))

        # Create ElementTree root for output.
        outputroot = etree.Element("output")
        outputtree = etree.ElementTree(outputroot)

        # Loop through lines in files.
        for line in inputlines:

            # Create base nodes.
            linenode = etree.SubElement(outputroot, "line")
            linetags = etree.SubElement(linenode, "tags")
            originalnode = etree.SubElement(linenode, "original")

            # For each line break into words and extract class
            # from NLP output. This assumes all words (excluding punctuation)
            # has been assigned a class by the POS tagger; including the
            # -NONE- class when a word can't be tagged.
            for word in line.split():
                for el in output:
                    eltext = str(el.text)
                    # print "Searching for: %s - %s" % (eltext, word[:len(eltext)])
                    if eltext == word[:len(eltext)]:
                        # print "MATCH! Type = %s" % el.get("class")
                        # Add to linenode.tags & remove from output.
                        if el.get("class") != "NONE":
                            linetags.append( deepcopy(el) );
                        el.getparent().remove( el );
                        break

            originalnode.text = etree.CDATA(line)

        outputtree.write(outputf, pretty_print=True)

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
