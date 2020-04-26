import re
from stanfordnlp.server import CoreNLPClient


def countNodesThatMatchTag(tree, tag):
    '''Returns the number of nodes a given CoreNLP parse tree that have a given tag.'''
    if not tree.child:
        return 0
    count = sum(countNodesThatMatchTag(branch, tag) for branch in tree.child)
    if re.match(tag, tree.value):
        count += 1
    return count
def getParseTreeLevels(tree):
    '''Returns the number of parse tree levels of a CoreNLP parse tree.'''
    if not tree.child:
        return 1
    return 1 + max(getParseTreeLevels(branch) for branch in tree.child)


class NLPClient:
    client = None
    def __init__(self):
        '''Creates the client if the client has not been created yet.'''
        if NLPClient.client is None:
            NLPClient.client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'parse'], be_quiet=True, memory='16G', threads=6, timeout=240000)
    def annotate(self, str):
        '''Returns the annotated text.'''
        return NLPClient.client.annotate(str)