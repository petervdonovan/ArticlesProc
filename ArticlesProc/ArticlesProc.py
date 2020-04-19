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

articles = ArticleSetBuilder().retrieveArticlesFromXML(folderName='receipt-id-1451701-part-001 (math)').getArticles()
timesToRecordContributors = []
timesToEvaluateProperties = []
for article in articles:
    lastTime = time.time()
    article.recordContributors()
    timesToRecordContributors.append(time.time() - lastTime)
    print('Time to record contributors:', time.time() - lastTime)
    lastTime = time.time()
    article.evaluateProperties()
    timesToEvaluateProperties.append(time.time() - lastTime)
    print('Time to evaluate properties:', time.time() - lastTime)
print("mean record contributors time: ", sum(timesToRecordContributors) / len(timesToRecordContributors))
print("mean evaluate properties time: ", sum(timesToEvaluateProperties) / len(timesToEvaluateProperties))
ArticleSet(articles).pickleSelf()
ContributorsDB().pickle()

#for article in ArticleSetBuilder(None).retrieveArticlesFromPickle('20_article_sample_18-Apr-2020 (17_41)').getArticles():
#    print(article.getFullPath())
#    print(article.properties)
#    article.print(verbose=True)
#showArticlesOfContributor('ContributorsDB_18-Apr-2020 (15_51)', Name(surname='Wang', givenName='Yafeng'))