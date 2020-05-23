from Citations.Citation import Citation
from Articles.ArticleSet import ArticleSet, getGranularStatisticalSummariesOfSetsDict, chartDifferencesInSubsetMeans
from Articles.ArticleSetBuilder import ArticleSetBuilder, getSummaryFromPickle, getSummaryAndPickleFromXML
from Articles.ArticlesDB import ArticlesDB
from Articles.RealArticle import RealArticle

from DevelopmentSets.citationRecognitionLiteratureSet681 import sampleLiteratureCitations
from DevelopmentSets.citationRecognitionBiologySet981 import sampleBiologyCitations
from DevelopmentSets.citationRecognitionSociologySet711 import sampleSociologyCitations
from DevelopmentSets.citationRecognitionMathSet701 import sampleMathCitations

from People.ContributorsDB import ContributorsDB
from People.Name import Name

from Themes.CitationGroup import CitationGroup
from Themes.AuthorshipGroup import AuthorshipGroup
from Themes.ThemeGroupSet import ThemeGroupSet

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

import sys
sys.setrecursionlimit(10**6)


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

def storeContributorDataFromArticles(articles, dbName):
    '''Stores both the contributor data and the article data (which 
    depends on the corresponding contributor data, because it includes
    names of the stored Contributors)'''
    timesToRecordContributors = []
    timesToEvaluateProperties = []    
    count = 1
    tstart = time.time()
    virtualArticles = set()
    for article in articles:
        print(count, "Article id", article.getId())
        count += 1

        lastTime = time.time()
        article.recordContributors()
        if time.time() - lastTime > 0.5:
            print('Article at', article.getFullPath(), 'took over 0.5 seconds to record contributors')
        print('Time to record contributors:', time.time() - lastTime)

        lastTime=time.time()
        citedArticles = set(citation.getArticle() for citation in article.getCitations())
        virtualArticles = virtualArticles.union(citedArticles)
        #article.recordCitations()
        if time.time() - lastTime > 0.5:
            print('Article at', article.getFullPath(), 'took over 0.5 seconds to record citations')
        print('Time to record citations:', time.time() - lastTime)
        ## Attempt to pickle progress
        #if count % 1000 == 0:
        #    ContributorsDB().pickle(fileName='biology_test_dbs_10^6_recursion/' + dbName)
    print('Total time:', time.time() - tstart)
    # print("mean record contributors time: ", sum(timesToRecordContributors) / len(timesToRecordContributors))
    # print("mean evaluate properties time: ", sum(timesToEvaluateProperties) / len(timesToEvaluateProperties))
    ArticleSet(articles.union(virtualArticles)).pickleAllArticles(fileName=dbName+'_articles')
    ContributorsDB().pickle(fileName=dbName+'_contributors')

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

def getNormalTransformationFunction(series):
    '''Returns a function that would transform the data to make it
    resemble a Gaussian distribution.'''
    #series = getSeriesOfMetric(pickleFileName, metric)
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
#getSummaryAndPickleFromXML(
#    folderName=["receipt-id-1423981-part-001 (biology)", "receipt-id-1451681-part-001 (literature)", 
#                "receipt-id-1451701-part-001 (math)", "receipt-id-1451711-part-001 (sociology)"], 
#    simple=True)
# getSummaryFromPickle("FULL_DATASET_receipt-id-1423981-part-001 (biology)_receipt-id-1451681-part-001 (literature)_receipt-id-1451701-part-001 (math)_receipt-id-1451711-part-001 (sociology)_08-May-2020 (13_06)")
def storeDisciplineData(discipline, folder):
    '''Store data about articles from the discipline.'''
    articles = ArticleSetBuilder().retrieveArticlesFromPickle('FULL_DATASET_biology_literature_math_sociology_10-May-2020 (00_00)').getArticles()
    disciplineArticles = ArticleSet(articles).getSubsetsByDiscipline()[discipline].articles
    ls = list()
    for article in disciplineArticles:
        if article.getId() % 10 == 0:
            ls.append(article.getId())
        if len(ls) == 10:
            print(ls)
            ls = list()
    storeContributorDataFromArticles(disciplineArticles, folder + '/' + discipline)

def makeArticlesDB(inPicklePath, outPicklePath):
    '''Based on a stored raw Articles data pickle, make a rapidly
    searchable ArticlesDB.'''
    articles = ArticleSetBuilder().retrieveArticlesFromPickle(inPicklePath).getArticles()
    for article in articles:
        ArticlesDB().add(article)
    ArticlesDB().pickle(outPicklePath)

def repairArticlesRaw(inPicklePath, outPicklePath):
    articles = ArticleSetBuilder().retrieveArticlesFromPickle(inPicklePath).getArticles()
    for article in articles:
        if 'articlesThatCiteThis' in article.properties:
            article.properties['articlesThatCiteThis'] = [article.getId() for article in article.properties['articlesThatCiteThis']]
        if 'articlesThatThisCites' in article.properties:
            article.properties['articlesThatThisCites'] = [article.getId() for article in article.properties['articlesThatThisCites']]
    ArticleSet(articles).pickleAllArticles(fileName=outPicklePath)

def repairContributors(inPicklePath, outPicklePath):
    ContributorsDB().getFromPickle(inPicklePath)
    for contrib in ContributorsDB.instance.db:
        for article in contrib.getArticles().articles:
            if article is None:
                print('NONE ARTICLE*************************************************************')
    ContributorsDB().pickle(outPicklePath)



#ContributorsDB().getFromPickle('lit-pickles/literature_contributors_11-May-2020 (21_49)')
#contribs = ContributorsDB().getSample(40)
#print("Articles by the randomly selected contributors:")
#for contrib in contribs:
#    print()
#    print('*******************************************************')
#    print()
#    for article in contrib.getArticles():
#        print(article)
#ArticlesDB().getFromPickle('lit-pickles/lit-articles-db_15-May-2020 (19_55)')
#repairContributors('lit-pickles/lit_contributors_11-May-2020 (21_49)',
#                   'lit-pickles/lit_contributors')
#ArticlesDB().clear()

#ArticlesDB().getFromPickle('soc-pickles/soc-articles-db_16-May-2020 (13_25)')
#repairContributors('soc-pickles/soc_contributors_16-May-2020 (05_15)',
#                   'soc-pickles/soc_contributors')
#ArticlesDB().clear()

#ArticlesDB().getFromPickle('math-pickles/math-articles-db_15-May-2020 (19_48)')
#repairContributors('math-pickles/math_contributors_15-May-2020 (14_12)',
#                   'math-pickles/math_contributors')
#ArticlesDB().clear()

#ArticlesDB().getFromPickle('bio-pickles/bio-articles-db_15-May-2020 (20_05)')
#repairContributors('bio-pickles/bio_contributors_13-May-2020 (23_13)',
#                   'bio-pickles/bio_contributors')

#ArticlesDB().getFromPickle('lit-pickles/lit_articles_db_17-May-2020 (18_02)')
#print('length of articlesDB:', len(ArticlesDB.instance.db))
#articles = ArticleSetBuilder().retrieveArticlesFromPickle('lit-pickles/lit_articles_15-May-2020 (17_14)').getArticles()
#print('length of articles raws', len(articles))
#for article in articles:
#    if ArticlesDB().get(article.id) is None:
#        print("Did not find this article:")
#        print(article)
#        try:
#            print(article.getFullPath())
#        except:
#            pass
#makeArticlesDB('lit-pickles/lit_articles_15-May-2020 (17_14)', 'lit-pickles/lit_articles_db')
#ArticlesDB().clear()
#makeArticlesDB('soc-pickles/soc_articles_16-May-2020 (05_14)', 'soc-pickles/soc_articles_db')
#ArticlesDB().clear()
#makeArticlesDB('math-pickles/math_articles_15-May-2020 (17_11)', 'math-pickles/math-articles-db')
#ArticlesDB().clear()
#makeArticlesDB('bio-pickles/bio_articles_15-May-2020 (17_17)', 'bio-pickles/bio-articles-db')
#ArticlesDB().clear()

#ArticlesDB().getFromPickle('lit-pickles/lit-articles-db_15-May-2020 (19_55)')
#repairContributors('lit-pickles/lit_contributors_11-May-2020 (21_49)', 'lit-pickles/lit_contributors')
#ArticlesDB().clear()
#ArticlesDB().getFromPickle('soc-pickles/soc-articles-db_16-May-2020 (13_25)')
#repairContributors('soc-pickles/soc_contributors_16-May-2020 (05_15)', 'soc-pickles/soc_contributors')
#ArticlesDB().clear()
#ArticlesDB().getFromPickle('bio-pickles/bio-articles-db_15-May-2020 (20_05)')
#repairContributors('bio-pickles/bio_contributors_13-May-2020 (23_13)', 'bio-pickles/bio_contributors')
#ArticlesDB().clear()
#ArticlesDB().getFromPickle('math-pickles/math-articles-db_15-May-2020 (19_48)')
#repairContributors('math-pickles/math_contributors_15-May-2020 (14_12)', 'math-pickles/math_contributors')

#ArticleSetBuilder().retrieveArticlesFromPickle('lit-pickles/literature_articles_19-May-2020 (23_30)')
##ArticlesDB().getFromPickle('lit-pickles/lit-articles-db_18-May-2020 (21_23)')
#ls = list()
#for article in ArticlesDB.instance.db:
#    if article.getId() % 10 == 0:
#        ls.append(article.getId())
#    if len(ls) == 10:
#        print(ls)
#        ls = list()
#for article in ArticlesDB.instance.db:
#    if not article.properties['contributors']:
#        try:
#            print(article.properties['citation'].raw)
#        except KeyError:
#            print('No contributors, no citation.')
#for id in range(47550, 47700):
#    print(id)
#    article = ArticlesDB().get(id)
#    print(article)
#    try:
#        print(article.properties)
#    except:
#        pass
#    try:
#        print(article.getFullPath())
#    except:
#        print('not real.')
#    try:
#        for citing in article.properties['articlesThatCiteThis']:
#            print(ArticlesDB().get(citing))
#            print(ArticlesDB().get(citing).properties)
#    except:
#        print('not cited.')
#    try:
#        for citing in article.properties['articlesThatThisCites']:
#            print(ArticlesDB().get(citing))
#            print(ArticlesDB().get(citing).properties)
#    except:
#        print('not citing.')
#    print()
#    print()
#print('________________________________________________________')
#print('________________________________________________________')
#print('________________________________________________________')
#length = len(ArticlesDB.instance.db)
#for id in range(length-150, 635600):
#    print(id)
#    article = ArticlesDB().get(id)
#    print(article)
#    try:
#        print(article.properties)
#    except:
#        pass
#    try:
#        print(article.getFullPath())
#    except:
#        print('not real.')
#    try:
#        for citing in article.properties['articlesThatCiteThis']:
#            print(ArticlesDB().get(citing))
#            print(ArticlesDB().get(citing).properties)
#    except:
#        print('not cited.')
#    try:
#        for citing in article.properties['articlesThatThisCites']:
#            print(ArticlesDB().get(citing))
#            print(ArticlesDB().get(citing).properties)
#    except:
#        print('not citing.')
#    print()
#    print()

#storeDisciplineData('literature', 'lit-pickles')
#ArticlesDB().pickle('lit-pickles/lit-articles-db')
def load(articlesPath, contributorsPath):
    '''Initialize the ArticlesDB from stored Article data 
    (not actual Article objects) and initialize the 
    ContributorsDB from the db file (list of Contributor 
    objects)'''
    # Clear the ArticlesDB
    ArticlesDB().clear()
    # Populate the ArticlesDB
    ArticleSetBuilder().retrieveArticlesFromPickle(articlesPath)
    # Clear the ContributorsDB
    ContributorsDB().clear()
    # Populate the ContibutorsDB
    ContributorsDB().getFromPickle(contributorsPath)

def showArticleAndCitationNumberDistribution():
    '''Shows the frequency distribution of articles and citations per Contributor.'''
    load('lit-pickles/literature_articles_19-May-2020 (23_30)', 'lit-pickles/literature_contributors_19-May-2020 (23_30)')
    plt.hist([
        len([
            article
            for article in contributor.getArticles()
            if isinstance(article, RealArticle)
            ])
        for contributor in ContributorsDB()
        ], bins=100)
    plt.show()
    plt.hist([
        sum([
            len(article.getArticlesThatCiteThis())
            for article in contributor.getArticles()
            ])
        for contributor in ContributorsDB()
        ], bins=99, range=(2, 100))
    plt.show()


#ArticlesDB().clear()
#ContributorsDB().clear()
#storeDisciplineData('math', 'math-pickles')
#ArticlesDB().pickle('math-pickles/math-articles-db')

#ArticlesDB().clear()
#ContributorsDB().clear()
#storeDisciplineData('biology', 'bio-pickles')
#ArticlesDB().pickle('bio-pickles/bio-articles-db')

#ArticlesDB().clear()
#ContributorsDB().clear()
#storeDisciplineData('sociology', 'soc-pickles')
#ArticlesDB().pickle('soc-pickles/soc-articles-db')

load('lit-pickles/literature_articles_19-May-2020 (23_30)', 'lit-pickles/literature_contributors_19-May-2020 (23_30)')
ThemeGroupSet(CitationGroup.setFactory()).pickle('lit-pickles/literature_theme_groups_citation')

load('lit-pickles/literature_articles_19-may-2020 (23_30)', 'lit-pickles/literature_contributors_19-may-2020 (23_30)')
ThemeGroupSet(AuthorshipGroup.setFactory()).pickle('lit-pickles/literature_theme_groups_authorship')

#load('lit-pickles/literature_articles_19-May-2020 (23_30)', 'lit-pickles/literature_contributors_19-May-2020 (23_30)')
#getNormalTransformationFunction([
#        sum([
#            len(article.getArticlesThatCiteThis())
#            for article in contributor.getArticles()
#            ])
#        for contributor in ContributorsDB()
#        ])

#showArticleAndCitationNumberDistribution()