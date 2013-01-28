"""
Dependencies:
    docx  - https://github.com/mikemaccana/python-docx.git (docx)
    pyth - http://pypi.python.org/pypi/pyth/ (RTF)
"""
import re, sys, zipfile
from HTMLParser import HTMLParser
from docx.docx import *
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter

class TextParser(object):
    """Abstract parsing class"""
    def __init__(self, data, config=[]):
        self._data = data
        self._config = config

    def parse(self):
        return self._data


class HTMLTextParser(TextParser):
    """Concrete HTML parser"""
    def __init__(self, data, config=[]):
        super(HTMLTextParser, self).__init__(data, config)
        self.__parsedData = ""
        self.__nativeHTMLParser = HTMLParser()
        self.__collect = False

    def parse(self):
        self.__nativeHTMLParser.handle_data = self.__handle_data
        self.__nativeHTMLParser.handle_starttag = self.__handle_starttag
        self.__nativeHTMLParser.feed(self._data)

        return self.__parsedData

    def __handle_starttag(self, tag, attrs):
        if 'acceptedTags' not in self._config:
            raise LookupError('Config does not contain HTML tag whitelist')
        if tag in self._config['acceptedTags']:
            self.__collect = True

    def __handle_data(self, data):
        if self.__collect == True:
            self.__parsedData += data + "\n"
            self.__collect = False



class MSDocXParser(TextParser):
    """Concrete docx parser"""
    def __init__(self, data, config=[]):
        super(MSDocXParser, self).__init__(data, config)
        self.__parsedData = ""

    def parse(self):
        doc = opendocx(self._config['filePath'])
        paratextlist = getdocumenttext(doc)
        # Make explicit unicode version
        newparatextlist = []
        for paratext in paratextlist:
            newparatextlist.append(paratext.encode('utf-8'))
        self.__parsedData = '\n\n'.join(newparatextlist)

        return self.__parsedData



class RTFDocParser(TextParser):
    """Concrete RTF document parser"""
    def __init__(self, data, config=[]):
        super(RTFDocParser, self).__init__(data, config)
        self.__parsedData = ""

    def parse(self):
        doc = Rtf15Reader.read(open(self._config['filePath'], "rb"))
        self.__parserData = PlaintextWriter.write(doc).getvalue()

        return self.__parsedData



class ODTDocParser(TextParser):
    """ Open Office document parser"""
    def __init__(self, data, config=[]):
        super(ODTDocParser, self).__init__(data, config)
        self.__nativeHTMLParser = HTMLParser()
        self.__parsedData = ""

    def parse(self):
        odtFile = zipfile.ZipFile(self._config['filePath'],'r')
        xmlData = odtFile.read('content.xml')

        self.__nativeHTMLParser.handle_data = self.__handle_data
        self.__nativeHTMLParser.feed(xmlData)

        return self.__parsedData

    def __handle_data(self, data):
        self.__parsedData += data + "\n"
