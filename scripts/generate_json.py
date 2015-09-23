import os, sys, re
from os.path import basename
import json

#{"path":"data/dickinson/OneSeries-ADay.xml","filename":"OneSeries-ADay.xml","directory":"./data/dickinson"},

poet = 'dickinson'
path = 'data/{0}/{1}'
directory = './data/{0}'.format(poet)

sourcedir = '../data/poem-parser/{0}/output'.format(poet)

def iteratefiles():

    lst = []
    for file in os.listdir( sourcedir ):
      if file.endswith(".xml"):

        data = {}
        data['path'] = path.format(poet, file)
        data['filename'] = file
        data['directory'] = directory.format(poet)
        lst.append(data)

    with open('{0}/content.json'.format(sourcedir), 'w') as out:
      json.dump(lst, out)


iteratefiles()
