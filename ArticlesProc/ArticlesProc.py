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
from StatsAndVisualization.statsUtils import showNormalTransformedQQ, findPowerOfMaxRmsNormality

from random import sample
from scipy import stats
import math
import numpy as np
import matplotlib.pyplot as plt
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

"""
C:/Users/Peter/.virtualenvs/nlp64/Scripts/activate
cd C:/Users/Peter/documents/research/articlesproc/articlesproc
python articlesproc.py
"""
def getSampleOfRawCitations(articles):
    for article in articles:
        for citation in article.getCitations():
            print('"' + escapeDoubleQuotes(str(citation)) + '", ')

def getContributorsDBSample(sampleSize=100):
    articles = ArticleSetBuilder().retrieveArticlesFromPickle('FULL_ARTICLE_SET_STABLE_IDS').getArticles()
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
        if count % 1000 == 0:
            ContributorsDB().pickle(fileName='biology_test_dbs_10^6_recursion/' + dbName)
    print('Total time:', time.time() - tstart)
    # print("mean record contributors time: ", sum(timesToRecordContributors) / len(timesToRecordContributors))
    # print("mean evaluate properties time: ", sum(timesToEvaluateProperties) / len(timesToEvaluateProperties))
    ContributorsDB().pickle(fileName=dbName)
    ArticleSet(articles).pickleSelf(fileName=dbName)

# storeContributorAndArticleDataFromXML('receipt-id-1423981-part-001 (biology)', 'biology_highmaxrecursion_full_db')
def examineForNormalTransformation(pickleFileName, metric, bins, *transformation):
    '''Shows whether a transformation of the a certain metric of 
    articles yields a normal distribution. The metric must be one of the
    following strings: 'Tokens', 'Parse Tree Levels', 'Dependent Clauses',
   'Prepositional Phrases'. '''
    series = getSeriesOfMetric(pickleFileName, metric)
    showNormalTransformedQQ(series, bins, *transformation)

def getSeriesOfMetric(pickleFileName, *metrics):
    '''Using pickled articles, get a series of some measures of the articles.
    The metric must be one of the following strings: 'Tokens', 
    'Parse Tree Levels', 'Dependent Clauses', 'Prepositional Phrases'.'''
    articles = ArticleSetBuilder().retrieveArticlesFromPickle(pickleFileName).articles
    aset = ArticleSet(articles)
    data=aset.getData()
    results = [list(aset.getData()[metric]) for metric in metrics]
    if len(results) == 1:
        return results[0]
    return results

def getNormalTransformationFunction(pickleFileName, metric):
    '''Returns a function that would transform the data to make it
    resemble a Gaussian distribution.'''
    series = getSeriesOfMetric(pickleFileName, metric)
    power = findPowerOfMaxRmsNormality(series)
    print('Power found:', power)
    if power == 0: return math.log
    return lambda x: x**power

def scatterSyntacticMeasures(pickleFileName, metric1, metric2):
    '''Shows a scatterplot of the correlation betweeen 2 different
    complexity measures.'''
    results = getSeriesOfMetric(pickleFileName, metric1, metric2)
    plt.scatter(results[0], results[1], s=1)
    results[1] = [value / results[0][i] for i, value in enumerate(results[1])]
    print(stats.pearsonr(results[0], results[1]))
    print(stats.linregress(results[0], results[1]))
    plt.show()


# examineForNormalTransformation('FULL_ARTICLE_SET_STABLE_IDS', 'Combined Adjusted SBAR PP', 40, math.log)
# getNormalTransformationFunction('FULL_ARTICLE_SET_STABLE_IDS', 'Dependent Clauses')
# getSummaryFromPickle('FULL_ARTICLE_SET_STABLE_IDS')
# scatterSyntacticMeasures('FULL_ARTICLE_SET_STABLE_IDS', 'Tokens', 'Parse Tree Levels')
getSummaryAndPickleFromXML(
    folderName=["receipt-id-1423981-part-001 (biology)", "receipt-id-1451681-part-001 (literature)", 
                "receipt-id-1451701-part-001 (math)", "receipt-id-1451711-part-001 (sociology)"], 
    simple=True)