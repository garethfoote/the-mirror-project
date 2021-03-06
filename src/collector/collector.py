import re, datetime, logging, json, copy, operator, os, grp, pwd
from stat import *
from collections import namedtuple
from itertools import groupby

from partofspeechtagger import PartOfSpeechTagger
from traverse import Traverse
from parser import *
class Collector:

    """Collector application"""
    def __init__(self, config, wordTags):
        self._config = config
        self.__traverse = Traverse(config.dirs)
        self.__posTagger = PartOfSpeechTagger(wordTags)
        self.__taggedData = dict()
        self.__initOutputs()


    def start(self):
        self.__traverse.restrict({'maxSize': 20*1024*1024 })

        # Debugging.
        # self.__traverse.allowTypes(['application/rtf'])
        self.__traverse.allowTypes(self._config.acceptedFiles)

        self.__traverse.onFilePass += self.__fileFoundHandler
        self.__traverse.start()
        self.__output.write(json.dumps(self.__taggedData))
        self.__progressLog.truncate(0)


    def __initOutputs(self):
        # now = datetime.datetime.now()
        # nowFormatted = now.strftime("%y-%m-%d-%H%M%S")
        # Need this file to be consitent when app is run multiple times.
        nowFormatted = ''
        # Progress
        progressLog = 'collector/progress%s.log' % nowFormatted
        # Clear log.
        open(progressLog,'w').close()
        # Open in append mode.
        self.__progressLog = open(progressLog, 'a')
        # Output
        output = '%scollector%s.json' % (self._config.output, nowFormatted)
        try:
            self.__output = open(output, 'w')
        except IOError as e:
            print "[ERROR] Directory %s does not exist. Check config.cfg and create directory if necessary" % self._config.output
            raise


    def __fileFoundHandler(self, filePath, mimeType):
        # Write to stdout.
        print "File found: %s - %s" % (filePath, mimeType)
        # Open file (read only).
        try:
            with open(filePath, 'r') as f:
                data = f.read()
        except IOError:
            self.__handleIOError(filePath)
        else:
            # Get parser dependant on mimetype and do some taggging.
            parser = self.__initParser(data, filePath, mimeType);
            parsedData = parser.parse()
            # Use POSTagger to tag words in parsed text/data.
            self.__posTagger.tag(parsedData)
            self.__merge(self.__posTagger.getByClass())
            # If merge is successful write this filePath to progres log.
            self.__progressLog.write(filePath+'\n')
            f.close()


    def __initParser(self, data, filePath, mimeType):

        config = { "acceptedTags": self._config.htmltags, "filePath": filePath }
        return {
            'text/plain': TextParser(data),
            'text/html': HTMLDocParser(data, config),
            'application/rtf': RTFParser(data, config),
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': MSDocXParser('', config),
            'application/vnd.oasis.opendocument.text': ODTParser('', config),
            'application/pdf': PDFParser('', config),
            #'application/msword': RTFDocParser(data, config),
            }[mimeType]

    def __merge(self, newData):
        # Alphabetise words for grouping.
        for tagKey in newData:
            newData[tagKey] = sorted(newData[tagKey])
        if len(self.__taggedData) == 0:
            # No data yet as this is first file and this is not a
            # continuation of previous scan.
            for tagKey in newData:
                self.__taggedData[tagKey] = {key: len(list(group)) for key, group in groupby(newData[tagKey])}
        else:
            # Either data exists from prior files or from a partial json
            # file created during a previous scan.
            for tagKey in newData:
                for word in newData[tagKey]:
                    if word in self.__taggedData[tagKey]:
                        self.__taggedData[tagKey][word] = self.__taggedData[tagKey][word] + 1
                    else:
                        self.__taggedData[tagKey][word] = 1

    def __orderByFrequency(self):
        for tagKey in self.__taggedData:
            self.__taggedData[tagKey] = sorted(self.__taggedData[tagKey].iteritems(), key=operator.itemgetter(1), reverse=True)
            print self.__taggedData[tagKey]

    def __handleIOError(self, filePath):
        # If IO error then write mask, user and group to log.
        statInfo = os.stat(filePath)
        user = pwd.getpwuid(statInfo.st_uid)[0]
        group = grp.getgrgid(statInfo.st_gid)[0]
        permMask = str(oct(statInfo[ST_MODE] & 0777))
        errorMsg = 'Cannot open file %s. [mask: %s, user: %s, group: %s]' % (filePath, permMask, user, group)
        logging.error(errorMsg)
        print '[ERROR] ' + errorMsg

