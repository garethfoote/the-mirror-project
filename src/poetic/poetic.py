from partofspeechtagger import PartOfSpeechTagger
from lxml import etree
import os

class Poetic:
    """Poetic parser """
    def __init__(self, config, wordTags):
        self._config = config
        self.__posTagger = PartOfSpeechTagger(wordTags)

    def start(self):
        if os.path.isdir( self._config.input ):
            self.__outputDir = self._config.input + '/output/'
            self.createoutputdir();

            # Loop dir for files to parse.
            for f in os.listdir( self._config.input ):
                if os.path.isfile( self._config.input + f ):
                    self.parse( self._config.input + f )
        else:
            dir = os.path.dirname( self._config.input )
            self.__outputDir = dir + '/output/'
            self.createoutputdir();

            self.parse( self._config.input )

    def createoutputdir(self):
        if os.path.exists(self.__outputDir) == False:
            os.makedirs(self.__outputDir)

    def parse(self, filepath):

        bn = os.path.basename(filepath)
        if bn.startswith('.') or bn.endswith('~'):
            return

        print "Parsing: "+ filepath

        try:
            self.__input = etree.parse(filepath)
        except etree.XMLSyntaxError:
            self.__input = open(filepath, 'r')

        # Create output file for writing
        outputf = open(self.__outputDir + bn, 'w+');

        outputroot = etree.Element("output")
        # Create ElementTree to compare against input
        outputtree = etree.ElementTree(outputroot)
        # If input is an XML document...
        if type(self.__input) == type(outputtree):
            # Loop through all poems
            for poem in self.__input.findall('poem'):
                for line in iter(poem.text.splitlines()):
                    # print line
                    self.__posTagger.tag(line);
                    lineoutput = self.__posTagger.getFormatted(self._config.format)
                    poem.text = ""
                    linenode = etree.SubElement(poem, "line")
                    linenode.append( etree.fromstring('<tags>'+lineoutput+'</tags>') )
                    originalnode = etree.SubElement(linenode, "original")
                    originalnode.text = etree.CDATA(line)
                    # print "linetagged:"+lineoutput

            # ...then output is also an xml document.
            self.__input.write(outputf)
        else:
            lineoutput = ''
            # Loop through lines in files.
            for line in self.__input:
                # Write line by line (append).
                self.__posTagger.tag(line);
                lineoutput = self.__posTagger.getFormatted(self._config.format)

                if self._config.forceXMLOutput == "true":
                    linenode = etree.SubElement(outputroot, "line")
                    linenode.append( etree.fromstring('<tags>'+lineoutput+'</tags>') )
                    originalnode = etree.SubElement(linenode, "original")
                    originalnode.text = etree.CDATA(line)
                else:
                    # Or else write it line by line.
                    outputf.write(lineoutput+'\n');

            if self._config.forceXMLOutput == "true":
                outputtree.write(outputf, pretty_print=True)
                # print etree.tostring(outputroot, pretty_print=True)


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
