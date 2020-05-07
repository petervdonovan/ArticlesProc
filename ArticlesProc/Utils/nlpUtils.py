import re
from stanfordnlp.server import CoreNLPClient
from nltk.tokenize import sent_tokenize, word_tokenize
from guess_language import guess_language
import statistics

def getSentencesAnnotatedByLanguage(text):
    '''Gets a list of ordered pairs of a string delimited by a possible sentence break and the language of that string, in the abstract.'''
    pairs = []
    if text:
        for possibleSentence in sent_tokenize(text):
            pairs.append((possibleSentence, guess_language(possibleSentence)))
    return pairs
def getSentencesWithPossibleMathFlagged(text, minLengthMostWords=2, maxProportionOfGroupingSymbols=0.25):
    '''Gets a list of possible sentences, with possible sentences flagged if they possibly contain math.'''
    pairs = []
    if text:
        for possibleSentence in sent_tokenize(text):
            possibleMath = (
                bool(re.search(r'\+|=|(\b(x|y|z)\b)', possibleSentence)) or  #Check for math symbols
                statistics.mean([len(word) for word in re.split(r'\b', possibleSentence)]) < 2 or #check for very short words that might be variables
                len(re.findall(r'\)|\(|\[|\]|\|', possibleSentence)) / len(possibleSentence) > maxProportionOfGroupingSymbols or #Check for a high proportion of grouping symbols
                bool(re.search(r'\{|\}|(\$\\\[.*?\]\$)', possibleSentence))
                )
            pairs.append((possibleSentence, possibleMath))
    return pairs
def getEnglishSentences(text):
    '''Gets the parts of the text that can be understood as English 
    sentences: Not foreign languages, and not mathematical equations.'''
    english = '. '.join(sent for (sent, lang) in getSentencesAnnotatedByLanguage(text) if lang == 'en') + '.'
    return '. '.join(sent for (sent, possibleMath) in getSentencesWithPossibleMathFlagged(english) if not possibleMath) + '.'

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
            NLPClient.client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'parse'], be_quiet=True, memory='16G', threads=8, timeout=240000)
    def annotate(self, str):
        '''Returns the annotated text.'''
        return NLPClient.client.annotate(str)