from postagging import PartOfSpeechTagger

pos_tagger = PartOfSpeechTagger(['RB', 'JJ', 'JJR', 'AJS', 'NN', 'NNS', 'NN1', 'PN', 'VB', 'VBP'])

# Get list of all tag shortcode and their defintion+examples
# alltags = pos_tagger.list_tags(['noun', 'verb', 'adjective'])
# print "%s\nlength:%s" % (''.join(alltags), str(len(alltags)))

# Pass sentence to PoS Tagger and categorise by class
#print pos_tagger.tag_sentence('And now for something completely different')
pos_tagger.tag_sentence('They refuse to permit us to obtain the refuse permit. The rain in spain falls mainly on the plain.')
print pos_tagger.get_formatted("<replace class='%s'>%s</replace>")
# print pos_tagger.get_by_class()

# RB - Adverb
# JJ - Adjective or numeral, ordinal
# JJR - Adjective comparative
# AJS - superaltive adjective
# NN - noun, common, singular
# NNS - noun, common, plural
# NN1 - singular noun
# PN = pronoun
# VB - verb, base form
