from os import listdir
from os.path import isfile, join
import pickle
import time

from Articles.RealArticle import RealArticle
from Articles.ArticleSet import ArticleSet
from Utils import constants as constants

def getSummaryFromPickle(fileName):
    '''Simple out-of-box function that uses the ArticleSetBuilder to show data from a pickle.'''
    articles = ArticleSetBuilder().retrieveArticlesFromPickle(fileName).getArticles()
    articleSet = ArticleSet(articles)
    articleSet.getData()
    articleSet.makeHists()
def getSummaryAndPickleFromXML(startIndex=0, endIndex=0, sampleSize=-1, folderName="dataset", simple=False):
    '''Simple out-of-box function that uses the ArticleSetBuilder to show and store data from a folder of XML files.'''
    if type(folderName) == str:
        articles = ArticleSetBuilder().retrieveArticlesFromXML(startIndex=startIndex, endIndex=endIndex, sampleSize=sampleSize, folderName = folderName).getArticles()
    else:
        articles = set()
        for folder in folderName:
            articles=articles.union(ArticleSetBuilder().retrieveArticlesFromXML(startIndex=startIndex, endIndex=endIndex, sampleSize=sampleSize, folderName = folder).getArticles())
        folderName='_'.join(folderName)
    articleSet = ArticleSet(articles)
    print("Beginning to evaluate all data")
    startTime = time.time()
    articleSet.getData(simple=simple)
    print("Time taken to evaluate all data:", time.time() - startTime)
    #name = input("Name under which to store the pickle? ")
    name = ''
    if startIndex != 0 or endIndex != 0:
        name = '' + str(startIndex) + '_TO_' + str(endIndex)
    else:
        name = 'FULL_DATASET'
    if name: articleSet.pickleAllArticles(fileName=(name + '_' + folderName))
    else: articleSet.pickleAllArticles(fileName=folderName)
    articleSet.makeHists()

class ArticleSetBuilder(object):
    """Accesses the file system of the computer to pull article data use it to create Articles."""
    def __init__(self):
        self.articles = set()
        '''The articles found by this article set builder.'''
    def retrieveArticlesFromXML(self, startIndex=0, endIndex=0, sampleSize=-1, folderName=None):
        '''Retrieves Articles from their original XML files.'''
        if not folderName:
            folderName = input("Folder name? ")
        path = join(constants.pathToArticleData, folderName, 'metadata')
        # Get all file names
        metadataNames = [f for f in listdir(path) if isfile(join(path, f))]
        #save metadata names to a pickle
        print("Loaded", len(metadataNames), "file names by searching the file system")
        if endIndex == 0:
            endIndex = len(metadataNames)
        metadataNames = metadataNames[startIndex:endIndex]
        if sampleSize != -1:
            metadataNames = metadataNames[::int(len(metadataNames) / sampleSize)]
        for metadataName in metadataNames:
            self.articles.add(RealArticle.initFromFile(path, metadataName))
            if len(self.articles) % 10 == 0:
                print(len(self.articles), metadataName)
        return self
    def retrieveArticlesFromPickle(self, *fileNames):
        '''Retrieves Articles from their pickled form.'''
        if not fileNames:
            fileName = input("File name?")
        for fileName in fileNames:
            dbfile = open(fileName, 'rb')
            db = pickle.load(dbfile)
            for articleRaw in db:
                self.articles.add(RealArticle.initFromRaw(articleRaw))
        return self
    def getArticles(self):
        return self.articles


