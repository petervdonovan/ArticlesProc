from stanfordnlp.server import CoreNLPClient
from stanfordcorenlp import StanfordCoreNLP

from Citations.Citation import Citation
from Articles.ArticleSet import ArticleSet, getGranularStatisticalSummariesOfSetsDict, chartDifferencesInSubsetMeans
from Articles.ArticleSetBuilder import ArticleSetBuilder, getSummaryFromPickle, getSummaryAndPickleFromXML

from DevelopmentSets.citationRecognitionLiteratureSet681 import sampleLiteratureCitations
from DevelopmentSets.citationRecognitionBiologySet981 import sampleBiologyCitations
from DevelopmentSets.citationRecognitionSociologySet711 import sampleSociologyCitations
from DevelopmentSets.citationRecognitionMathSet701 import sampleMathCitations

from People.ContributorsDB import ContributorsDB

from Utils.timeUtils import getStringTimestamp
from Utils.textProcUtils import capitalizeFirstLetterEachWord, escapeDoubleQuotes

from random import sample
import pandas as pd

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
articles = ArticleSetBuilder(None).retrieveArticlesFromPickle('FULL_ARTICLE_SET_STABLE_IDS').getArticles()
for article in sample(articles, 100):
    for citation in article.getCitations():
        citation.record()
        print(citation.raw)
    #citation.getArticle().print()
ContributorsDB().print()

#with CoreNLPClient(annotators=['tokenize', 'ssplit', 'parse'], be_quiet=True, memory='16G', threads=8, timeout=240000) as client:
def getSampleOfRawCitations(articles):
    for article in articles:
        for citation in article.getCitations():
            print('"' + escapeDoubleQuotes(str(citation)) + '", ')
