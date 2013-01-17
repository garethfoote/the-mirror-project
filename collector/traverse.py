"""
    Dependencies:

"""

class Mapping:
    def __init__(self):

import os
from os.path import join, getsize

maxsizemb = 10
maxsizebytes = maxsizemb*1024*1024
permittedtypes = ['txt']

# Traverse from specified start point
for root, dirs, files in os.walk('collector'):
    print '\n', root, dirs,
    for name in files:
        print name + ' ',

    #print root, "consumes",
    #print sum(getsize(join(root, name)) for name in files),
    #print "bytes in", len(files), "non-directory files"
    #if 'ebooks' in dirs:
    #    dirs.remove('ebooks')  # don't visit CVS directories
