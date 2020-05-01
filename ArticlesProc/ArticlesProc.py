import sys
print('initial recursion depth limit:', sys.getrecursionlimit())
sys.setrecursionlimit(1000000)
print('current recursion depth limit:', sys.getrecursionlimit())

from Citations.Citation import Citation
from Articles.ArticleSet import ArticleSet, getGranularStatisticalSummariesOfSetsDict, chartDifferencesInSubsetMeans
from Articles.ArticleSetBuilder import ArticleSetBuilder, getSummaryFromPickle, getSummaryAndPickleFromXML

from DevelopmentSets.citationRecognitionLiteratureSet681 import sampleLiteratureCitations
from DevelopmentSets.citationRecognitionBiologySet981 import sampleBiologyCitations
from DevelopmentSets.citationRecognitionSociologySet711 import sampleSociologyCitations
from DevelopmentSets.citationRecognitionMathSet701 import sampleMathCitations

from People.ContributorsDB import ContributorsDB
from People.Name import Name

from Utils.timeUtils import getStringTimestamp
from Utils.textProcUtils import capitalizeFirstLetterEachWord, escapeDoubleQuotes

from random import sample
import pandas as pd

import time


#           Activate the environment
#           Navigate to folder containing CoreNLP
#           CoreNLP server start command
"""
C:/Users/pvdon/.virtualenvs/env-64bit/Scripts/activate
cd C:/Users/pvdon/stanford-corenlp-full-2018-10-05/stanford-corenlp-full-2018-10-05
java -mx16g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 240000 -threads 8
"""
#           Activate the environment
#           Navigate to the folder containing this project
#           Run this project
"""
C:/Users/pvdon/.virtualenvs/env-64bit/Scripts/activate
cd C:/Users/pvdon/documents/research/articlesproc/articlesproc
python articlesproc.py
"""
def getSampleOfRawCitations(articles):
    for article in articles:
        for citation in article.getCitations():
            print('"' + escapeDoubleQuotes(str(citation)) + '", ')

def getContributorsDBSample(sampleSize=100):
    articles = ArticleSetBuilder(None).retrieveArticlesFromPickle('FULL_ARTICLE_SET_STABLE_IDS').getArticles()
    for article in sample(articles, sampleSize):
        article.recordContributors()
        #citation.getArticle().print()
    ContributorsDB().pickle()
    ContributorsDB().print()

def showArticlesOfContributor(fileName='partial_contributorsdbs/ContributorsDB_08-Apr-2020 (22_45)', name=Name(surname='Molev', givenNameInitials=['A'])):
    ContributorsDB().getFromPickle(fileName)
    for article in ContributorsDB().get(name).getArticles().articles:
        print(article)
        for contributor in article.getContributors():
            print(contributor)
        print()

def storeContributorAndArticleDataFromXML(folderName, dbName, sampleSize=-1):
    timesToRecordContributors = []
    timesToEvaluateProperties = []
    articles = ArticleSetBuilder().retrieveArticlesFromXML(sampleSize=sampleSize, folderName=folderName).getArticles()
    count = 1
    tstart = time.time()
    for article in articles:
        print(count, "Article id", article.getId())
        count += 1
        lastTime = time.time()
        article.recordContributors()
        if time.time() - lastTime > 1:
            print('Article at', article.getFullPath(), 'took over 1 second to record contributors')
        timesToRecordContributors.append(time.time() - lastTime)
        print('Time to record contributors:', time.time() - lastTime)
        lastTime = time.time()
        article.evaluateProperties()
        timesToEvaluateProperties.append(time.time() - lastTime)
        print('Time to evaluate properties:', time.time() - lastTime)
        # Attempt to pickle progress
        if count % 100 == 0:
            ContributorsDB().pickle(fileName='biology_test_dbs_10^6_recursion/' + dbName)
    print('Total time:', time.time() - tstart)
    # print("mean record contributors time: ", sum(timesToRecordContributors) / len(timesToRecordContributors))
    # print("mean evaluate properties time: ", sum(timesToEvaluateProperties) / len(timesToEvaluateProperties))
    ContributorsDB().pickle(fileName=dbName)
    ArticleSet(articles).pickleSelf(fileName=dbName)

storeContributorAndArticleDataFromXML('receipt-id-1423981-part-001 (biology)', 'biology_highmaxrecursion_full_db')
#for article in ArticleSetBuilder(None).retrieveArticlesFromPickle('20_article_sample_18-Apr-2020 (17_41)').getArticles():
#    print(article.getFullPath())
#    print(article.properties)
#    article.print(verbose=True)
#showArticlesOfContributor('ContributorsDB_18-Apr-2020 (15_51)', Name(surname='Wang', givenName='Yafeng'))