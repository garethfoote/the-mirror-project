"""
    Dependencies:
"""
import os, logging
from os.path import join, getsize
from mimetypes import guess_type

from gfte.events.eventhook import *

class Traverse:

    def __init__(self, root_dirs=['traverse-test']):
        self.__roots = root_dirs
        self.__config = { 'maxSize': 0 }
        self.__permittedTypes = []
        self.onFilePass = EventHook()

    def start(self):
        """Start traversal"""
        # Traverse from specified start point
        for dir in self.__roots:
            for root, dirs, files in os.walk(dir):
                # print '\n', root, dirs,
                for name in files:
                    fullPath = join(root, name)
                    if self.__fileSuccess(fullPath) == True:
                        self.onFilePass.fire(fullPath)

    def allowTypes(self, permittedTypes):
        self.__permittedTypes = permittedTypes

    def restrict(self, config):
        self.__config.update(config)

    def __fileSuccess(self, file):
        passed = False
        type = guess_type(file)
        # Test against file type whitelist.
        if len(self.__permittedTypes) > 0 :
            passed = type[0] in self.__permittedTypes
        else:
            passed = True

        if passed == False:
            logging.info('[%s] Type: %s not permitted.' % (file, type[0]))

        # If passed successfully, check against maxSize restrictions
        if passed == True and self.__config['maxSize'] > 0:
            passed = getsize(file) < self.__config['maxSize']

        return passed


#print root, "consumes",
#print sum(getsize(join(root, name)) for name in files),
#print "bytes in", len(files), "non-directory files"
#if 'ebooks' in dirs:
#    dirs.remove('ebooks')  # don't visit CVS directories
