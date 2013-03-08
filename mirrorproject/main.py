import logging, sys
sys.path.append(r'./lib')
from config import Config
from collector.collector import *
from poetic.poetic import *

# Logging
with open('debug.log', 'w'):
    pass
logging.basicConfig(filename='debug.log',level=logging.DEBUG)

# Configuration.
cfg = Config('../config.cfg')

#"""
# Start collector.
collector = Collector(cfg.collector, cfg.app.wordClassTags)
collector.start()
#"""

"""
poetic = Poetic(cfg.poetic, cfg.app.wordClassTags)
poetic.start()
"""
