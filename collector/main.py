from postagging import POSTagger

post = POSTagger()
alltags = post.list_tags(['noun', 'verb', 'adjective'])
print "%s\nlength:%s" % (''.join(alltags), str(len(alltags)))
#posT.tag_sentence('And now for something completely different')
