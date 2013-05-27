import logging, sys, argparse
sys.path.append(r'./lib')
from config import Config
from collector.collector import *
from poetic.poetic import *
from partofspeechtagger import PartOfSpeechTagger

# Logging
with open('debug.log', 'w'):
    pass
logging.basicConfig(filename='debug.log',level=logging.DEBUG)

# Configuration.
cfg = Config('../config.cfg')

parser = argparse.ArgumentParser(description='Start either Collector or Poetic Parsing application.')
parser.add_argument('--type', metavar='t', help='determine type of application to run: "collector" or "poemparser". (default:"collector")', default='collector', required=False)

args = parser.parse_args()
exectype = args.type

if exectype == 'collector':
    # Start collector.
    collector = Collector(cfg.collector, cfg.app.wordClassTags)
    collector.start()
elif exectype == 'poemparse':
    # Start poem parser.
    poetic = Poetic(cfg.poetic, cfg.app.wordClassTags)
    poetic.start()

"""
# List tag classes.
posTagger = PartOfSpeechTagger(cfg.app.wordClassTags)

tags = posTagger.list_tags()
for item in tags:
    print item
print "Total: "+ str(len(tags))
"""
