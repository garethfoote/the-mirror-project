import re
from HTMLParser import HTMLParser


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
