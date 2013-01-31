import logging, sys
sys.path.append(r'./lib')
from collector.collector import *

# Logging
with open('debug.log', 'w'):
    pass
logging.basicConfig(filename='debug.log',level=logging.DEBUG)

collector = Collector(['../traverse-test'])
collector.start()
