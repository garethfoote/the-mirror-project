import logging
from collector.collector import *

# Logging
with open('debug.log', 'w'):
    pass
logging.basicConfig(filename='debug.log',level=logging.DEBUG)

collector = Collector(['traverse-test'])
collector.startTraverse()
