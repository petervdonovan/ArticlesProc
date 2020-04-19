import xml.etree.ElementTree as ET
import os
import re
from People.Name import Name
from People.Contributor import Contributor
from People.Contributor import ContributorsDB
from Citations.Citation import Citation
from Articles.Article import Article
from Articles.ArticleSet import ArticleSet
import statistics
from Utils.textProcUtils import stripMarkup, replaceWhiteSpaceWithSpace, escapeDoubleQuotes
from Utils.nlpUtils import countNodesThatMatchTag, getParseTreeLevels, NLPClient
from guess_language import guess_language

import stanfordnlp.server.client
import requests.exceptions
#from nltk.tokenize import sent_tokenize, word_tokenize

class RealArticle(Article):
    """Represents an article based on an XML metadata file from JSTOR."""
    MAX_ABSTRACT_LENGTH = 750 #Length in characters
                               #TODO: Consider cutting the text and rejecting sentence fragments where it was cut instead of rejecting the whole thing.
                               #Only the beginning will be selected. This is not perfect for comparison, but it partially solves the problem of having
                               #non-english translations at the ends, and to pick a random slice that is completely within the beginning and end of the 
                               #abstract would cause the beginning and end to be selected less. So, there is no totally clean way of doing it.
    MIN_ABSTRACT_LENGTH = 120  #This is the length in characters of what was (somewhat arbitrarily) determined to be a "medium-length" sentence.
    def __init__(self, root, path, rootElement=None, articleMeta=None, abstract=None, properties=None):
        '''Default initialization.'''
        self.root = root
        '''The root file path to the article XML files.'''
        self.path = path
        '''The path to the raw article XML from the root. If the root is the folder containing the article XML files, this is the name of the file.'''
        self.rootElement = rootElement
        '''The root element of the contents of the article XML.'''
        self.articleMeta = articleMeta
        '''The metadata at the top of the article XML file.'''
        self.abstract = abstract
        '''The annotated StanfordCoreNLP object representation of the abstract. To save time, self.abstract remains None if it is not necessary to get the annotated abstract.'''
        Article.__init__(self, properties=properties)
        # Load the title and contributors into properties
        self.getTitle()
        self.getContributors()
    @classmethod
    def initFromFile(cls, rootFilePath, relativeFilePath):
        '''Factory method for initialization.'''
        root = rootFilePath
        '''The root file path to the article XML files.'''
        path = relativeFilePath
        '''The path to the raw article XML from the root. If the root is the folder containing the article XML files, this is the name of the file.'''
        rootElement = ET.parse(os.path.join(root, path)).getroot()
        '''The root element of the contents of the article XML.'''
        articleMeta = rootElement.find('front').find('article-meta')
        '''The metadata at the top of the article XML file.'''       
        return cls(root, path, rootElement=rootElement, articleMeta=articleMeta)

    @classmethod
    def initFromRaw(cls, raw):
        '''Reconstructs the article based on its data saved in a raw format.'''
        assert(type(raw[0]) == str)
        root = raw[0]
        '''The root file path to the article XML files.'''
        assert(type(raw[1]) == str)
        path = raw[1]
        '''The path to the raw article XML from the root. If the root is the folder containing the article XML files, this is the name of the file.'''
        properties = raw[2]
        return cls(root, path, properties=properties)
    def getPath(self):
        '''Returns the name of the original XML file.'''
        return self.path
    def getFullPath(self):
        '''Returns the path to the original XML file.'''
        return os.path.join(self.root, self.path)
    def getRootElement(self):
        '''Get the root element of the XML file from which article data is to be drawn.'''
        if not self.rootElement:
            file = open(self.getFullPath(), encoding='utf-8')
            '''The opened XML file.'''
            self.rootElement = ET.parse(file).getroot()
        return self.rootElement
    def getArticleMeta(self):
        '''Get the XML file's article-meta, where most metadata about the article is located.'''
        if not self.articleMeta:
            self.articleMeta = self.getRootElement().find('front').find('article-meta')
        return self.articleMeta
    def getSaveableData(self):
        '''Returns a summary of the data needed to QUICKLY reconstruct this Article.'''
        return (self.root, self.path, self.properties)
    def getRawAbstract(self):
        '''Returns the raw string form of the abstract.'''
        if not 'raw abstract' in self.properties:
            if not self.getArticleMeta().find('abstract'):
                self.properties['raw abstract'] = None
            else:
                self.properties['raw abstract'] = stripMarkup(ET.tostring(self.getArticleMeta().find('abstract'), encoding='unicode')).strip()
        return self.properties['raw abstract']
    def getTitle(self):
        '''Returns the title of the article.'''
        if not 'title' in self.properties:
            if not self.getArticleMeta().find('title-group'):
                self.properties['title'] = None
            else:
                self.properties['title'] = self.getArticleMeta().find('title-group').find('article-title').text
        return self.properties['title']
    def getPublicationYear(self):
        '''Returns the publication year of the article.'''
        if not 'publicationYear' in self.properties:
            try:
                self.properties['publicationYear'] = self.getArticleMeta().find('pub-date').find('year').text
            except:
                self.properties['publicationYear'] = None
        return self.properties['publicationYear']
    def getReportedLanguage(self):
        '''Returns the language of the article (as reported in the XML file).'''
        if not 'language' in self.properties:
            self.properties['language'] = ""
            for customElement in self.getArticleMeta().iter('custom-meta'):
                if customElement.find('meta-name').text == 'lang':
                    try:
                        self.properties['language'] = customElement.find('meta-value').text.lower()
                    except AttributeError:
                        pass
        return self.properties['language']
    def getAbstractLanguage(self):
        '''Gets the dominant language of the abstract.'''
        if self.getRawAbstract():
            return guess_language(self.getRawAbstract())
        return ''
    @staticmethod
    def getSentencesAnnotatedByLanguage(text):
        '''Gets a list of ordered pairs of a string delimited by a possible sentence break and the language of that string, in the abstract.'''
        pairs = []
        if text:
            for possibleSentence in re.split(r'\b\.\s+\b', text):
                pairs.append((possibleSentence, guess_language(possibleSentence)))
        return pairs
    @staticmethod
    def getSentencesWithPossibleMathFlagged(text, minLengthMostWords=2, maxProportionOfGroupingSymbols=0.25):
        '''Gets a list of possible sentences, with possible sentences flagged if they possibly contain math.'''
        pairs = []
        if text:
            for possibleSentence in re.split(r'\b\.\s+\b', text):
                possibleMath = (
                    bool(re.search(r'\+|=|(\b(x|y|z)\b)', possibleSentence)) or  #Check for math symbols
                    statistics.mean([len(word) for word in re.split(r'\b', possibleSentence)]) < 2 or #check for very short words that might be variables
                    len(re.findall(r'\)|\(|\[|\]|\|', possibleSentence)) / len(possibleSentence) > maxProportionOfGroupingSymbols or #Check for a high proportion of grouping symbols
                    bool(re.search(r'\{|\}|(\$\\\[.*?\]\$)', possibleSentence))
                    )
                pairs.append((possibleSentence, possibleMath))
        return pairs
    def getAbstract(self):
        '''Returns the abstract of the article, or None if no abstract exists.'''
        if not self.abstract:
            # Get and processs stringAbstract
            stringAbstract = '. '.join(sent for (sent, lang) in RealArticle.getSentencesAnnotatedByLanguage(self.getRawAbstract()) if lang == 'en') + '.'
            stringAbstract = '. '.join(sent for (sent, possibleMath) in RealArticle.getSentencesWithPossibleMathFlagged(stringAbstract) if not possibleMath) + '.'
            if len(stringAbstract) > RealArticle.MAX_ABSTRACT_LENGTH:
                stringAbstract = stringAbstract[:RealArticle.MAX_ABSTRACT_LENGTH]
            # Try to annotate stringAbstract
            if not stringAbstract:
                self.abstract = None
            else:
                try:
                    self.abstract = NLPClient().annotate(stringAbstract)
                except(stanfordnlp.server.client.TimeoutException):
                    print('***********************TIMED_OUT********************************')
                    self.abstract = None
                    self.properties['abstract invalid for unknown reason'] = True
                except(requests.exceptions.HTTPError):
                    print('**************HTTP_ERROR_(INTERNAL_SERVER_ERROR?)***************')
                    self.abstract = None
                    self.properties['abstract invalid for unknown reason'] = True
            #for sent in self.abstract.sentence:
            #    print(sent.parseTree)
            if self.abstract and not any(countNodesThatMatchTag(sentence.parseTree, r'S') != 0 
                for sentence in self.abstract.sentence if sentence.parseTree.child[0].value == 'S'):
                self.abstract = None
        return self.abstract
    def getAbstractInvalidForUnknownReason(self):
        if 'abstract invalid for unknown reason' in self.properties:
            return self.properties['abstract invalid for unknown reason']
        return False
    def recordContributors(self):
        '''Registers all the Contributors who contributed to this article in
        the ContributorsDB singleton and all the Contributors whose articles
        art cited by this Article.'''
        if 'contributors' in self.properties:
            del self.properties['contributors']
        for contributor in self.getContributors():
            ContributorsDB().registerContributor(contributor)
        for citation in self.getCitations():
            citation.record()
    def getContributors(self):
        if not 'contributors' in self.properties:
            contributorsList = []
            for name in self.getContributorNames():
                contributor = Contributor.make(name, articles=ArticleSet(set([self])))
                contributorsList.append(contributor)
            self.properties['contributors'] = contributorsList
        return self.properties['contributors']
    def getContributorNames(self):
        '''Returns a list of Names of the contributors to the article.'''
        if not 'contributorNames' in self.properties:
            contributorsList = []
            '''The list of contributors' names.'''
            for contrib in self.getArticleMeta().iter('contrib'):
                surname=''
                givenName=''
                middleName=''
                middleNameInitials=[]
                # Get given name and middle name
                try:
                    givenNames = contrib.find('string-name').find('given-names').text
                    givenName = givenNames.split()[0]
                    if len(givenNames.split()) > 1:
                        middle = givenNames.split()[1:]
                        initials = [initial.strip() for initial in middle.split('.') 
                                    if len(initial.strip()) == 1]
                        if len(initials) > 1:
                            middleNameInitials = initials
                        else:
                            middleName = ' '.join(middle)
                except(AttributeError): givenName = ''
                try:
                    surname = contrib.find('string-name').find('surname').text
                except(AttributeError): surname = ''
                # Attempt to make a Name out of the information found thus far
                if surname:
                    name = Name(
                        surname=surname, givenName=givenName, middleName=middleName, 
                        middleNameInitials=middleNameInitials
                        )
                    contributorsList.append(name)
                else:
                    # Case in which the above 20ish lines of code FAILED 
                    # to retrieve a name that makes sense
                    surname=''
                    givenName=''
                    middleName=''
                    middleNameInitials=[]
                    givenNameInitials=[]
                    try:
                        namesRaw = contrib.find('string-name').text
                        namesStr = namesRaw.replace('.', ' ')
                        # remove dots next to initials
                        names = namesStr.split()
                        surname = names[-1]
                        if len(names) > 1:
                            if len(names[0]) == 1:
                                givenNameInitials.append(names[0])
                            else:
                                givenName = names[0]
                        middleNameInitials = [name for name in names[1:-1] if len(name) == 1]
                        middleName = ' '.join([name for name in names[1:-1] if len(name) > 1])
                    except AttributeError: surname = ''
                    except IndexError: surname = ''
                    # Try again to make a Name out of the information found
                    if surname:
                        name = Name(
                            surname=surname, givenName=givenName, middleName=middleName, 
                            givenNameInitials=givenNameInitials, middleNameInitials=middleNameInitials
                            )
                        contributorsList.append(name)
            self.properties['contributorNames'] = contributorsList
        return self.properties['contributorNames']
    def getEtAl(self):
        '''Returns whether there are contributors who are not accounted for.'''
        return False
    def getCitations(self):
        '''Returns a list of all the citations in the article (and stores the list in the properties dictionary).'''
        if not 'citations' in self.properties:
            self.properties['citations'] = []
            for citation in self.getRootElement().iter('mixed-citation'):
                simplifiedCitationRaw = stripMarkup(ET.tostring(citation, encoding='unicode')).strip()
                simplifiedCitationRaw = replaceWhiteSpaceWithSpace(simplifiedCitationRaw)
                self.properties['citations'].append( Citation(simplifiedCitationRaw, self) )
        return self.properties['citations']
    def getStyleGuides(self):
        '''Gets a set of all the style guides that appear in the citations list.'''
        citations = self.getCitations()
        styleGuides = set()
        for citation in citations:
            for styleGuide in citation.getStyleGuides():
                styleGuides.add(styleGuide)
        return styleGuides
    def getSentenceCount(self):
        return len((_ for _ in self.getAbstract().sentence if _.parseTree.child[0].value == 'S'))
    def hasValidAbstract(self):
        '''Return true if it has an abstract that contains at least one declarative clause.'''
        if not 'hasValidAbstract' in self.properties:
            #self.properties['hasValidAbstract'] = (self.getRawAbstract() and 
            #    len(self.getRawAbstract()) > RealArticle.MIN_ABSTRACT_LENGTH and
            #    (self.getReportedLanguage() == "eng" or self.getReportedLanguage() == ''))
            # THE FOLLOWING ALTERNATIVE METHOD YIELDS IDEAL OUTPUT, BUT IT IS NOT LIGHTWEIGHT.

            #self.properties['hasValidAbstract'] = self.getAbstract() and \
            #any(countNodesThatMatchTag(sentence.parseTree, r'S') != 0 
            #    for sentence in self.getAbstract().sentence if sentence.parseTree.child[0].value == 'S')
            self.properties['hasValidAbstract'] = bool(self.getAbstract())
        return self.properties['hasValidAbstract']
    def getTokensPerSentence(self):
        '''Returns the mean number of tokens per sentence in the abstract.'''
        if self.hasValidAbstract():
            if not 'tokens per sentence' in self.properties:
                sentences = [sent for sent in self.getAbstract().sentence if sent.parseTree.child[0].value == 'S']
                '''The list of sentences in the abstract.'''
                self.properties['tokens per sentence'] = statistics.mean(len(sentence.token) for sentence in sentences)
            self.conditionallyEraseAbstract()
            return self.properties['tokens per sentence']
        else:
            return None
    def getMeanParseTreeLevels(self):
        '''Returns the mean number of parse tree levels per sentence in the abstract.'''
        if not self.hasValidAbstract():
            return None
        if not 'parse tree levels' in self.properties:
            self.properties['parse tree levels'] = statistics.mean(getParseTreeLevels(sentence.parseTree) for sentence in self.getAbstract().sentence if sentence.parseTree.child[0].value == 'S')
        self.conditionallyEraseAbstract()
        return self.properties['parse tree levels']
    def getMeanNodesPerSentence(self, nodeName):
        '''Returns the mean number of parse tree nodes per sentence in the abstract.'''
        if not self.hasValidAbstract():
            return None
        propertyName = 'mean ' + nodeName + ' per sentence'
        if not propertyName in self.properties:
           self.properties[propertyName] = statistics.mean(countNodesThatMatchTag(sentence.parseTree, nodeName) for sentence in self.getAbstract().sentence if sentence.parseTree.child[0].value == 'S')
        self.conditionallyEraseAbstract()
        return self.properties[propertyName]
    def getMeanDependentClauses(self):
        '''Returns the mean number of dependent clauses per sentence in the abstract.'''
        return self.getMeanNodesPerSentence(r'SBAR')
    def getMeanPrepositionalPhrases(self):
        '''Returns the mean number of prepositional phrases per sentence in the abstract.'''
        return self.getMeanNodesPerSentence(r'PP')
    def getCitationsCount(self):
        '''Returns the number of citations in the references list of the article.'''
        return len(self.citations)
    def conditionallyEraseAbstract(self):
        '''Erases the abstract if the needed information as already been 
        gotten from it.'''
        nodeNames = ['SBAR', 'PP']
        properties = ['parse tree levels', 'tokens per sentence'] + \
            ['mean ' + nodeName + ' per sentence' for nodeName in nodeNames]
        if all(property in self.properties for property in properties) or not self.hasValidAbstract():
            print("erasing abstract because all information has been gotten from it.")
            self.abstract = None
    def print(self, verbose=False):
        if verbose:
            for prop in self.properties:
                print(prop, '-->', self.properties[prop])
            print()
        else:
            print("\nTitle:", self.getTitle(),
              '\nAll of the following data is per sentence.',
              "\nMean tokens:", self.getTokensPerSentence(),
              "\nMean parse tree levels:", self.getMeanParseTreeLevels(),
              '\nMean dependent clauses:', self.getMeanDependentClauses(),
              '\nMean prepositional phrases:', self.getMeanPrepositionalPhrases())
    def getJournal(self):
        '''Returns a string representing the name of the journal in all caps, with whitespace
        stripped for uniformity.'''
        if not 'journal' in self.properties:
            try:
                self.properties['journal'] = journalTitleGroup = self.getRootElement().find('front').find('journal-meta').find('journal-title-group').find('journal-title').text.upper().strip()
            except:
                self.properties['journal'] = None
        return self.properties['journal']
    def evaluateProperties(self):
        '''Calls all the methods that result in information being added to properties.
        This method is for debugging and for saving data for rapid access later.'''
        self.getRawAbstract()
        self.getTitle()
        self.getPublicationYear()
        self.getReportedLanguage()
        self.getAbstract()
        self.getContributors()
        self.getContributorNames()
        self.getCitations()
        self.hasValidAbstract()
        self.getTokensPerSentence()
        self.getMeanParseTreeLevels()
        self.getMeanDependentClauses()
        self.getMeanPrepositionalPhrases()
        self.getJournal()
    def combine(self, other):
        return RealArticle.initFromRaw((self.root, self.path, super().combine(other).properties))