from stanfordnlp.server import CoreNLPClient
from stanfordcorenlp import StanfordCoreNLP

from Citations.Citation import Citation
from Articles.ArticleSet import ArticleSet, getGranularStatisticalSummariesOfSetsDict, chartDifferencesInSubsetMeans
from Articles.ArticleSetBuilder import ArticleSetBuilder, getSummaryFromPickle, getSummaryAndPickleFromXML

from DevelopmentSets.citationRecognitionLiteratureSet681 import sampleLiteratureCitations
from DevelopmentSets.citationRecognitionBiologySet981 import sampleBiologyCitations

from Utils.timeUtils import getStringTimestamp
from Utils.textProcUtils import capitalizeFirstLetterEachWord

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
# StanfordCoreNLP('http://localhost', port=9000)
#with CoreNLPClient('http://localhost:9000') as client:
#from stanza.nlp.corenlp import CoreNLPClient
#with CoreNLPClient(server='http://localhost:9000', default_annotators=['ssplit', 'tokenize', 'lemma', 'pos', 'ner']) as client:

articles = ArticleSetBuilder(None).retrieveArticlesFromPickle('FULL_ARTICLE_SET_23-Mar-2020 (15_02)').getArticles()
print('articles retrieved')
articleSet = ArticleSet(articles)
getGranularStatisticalSummariesOfSetsDict(articleSet.getSubsetsByDiscipline()).unstack(0).append(pd.DataFrame(index=['t'])).to_excel('test_' + getStringTimestamp() + '.xlsx')
print('articleSet created')
articleSet.thinOut()
print('articleSet thinned')

workbookName = 'discipline-wise-journal-comparison_' + getStringTimestamp() + '.xlsx'
with pd.ExcelWriter(workbookName) as writer:
    articleSet.putDisciplineWiseJournalComparisonToExcel(writer)


#with CoreNLPClient(annotators=['tokenize', 'ssplit', 'parse'], be_quiet=True, memory='16G', threads=8, timeout=240000) as client:
    
    #workbookName = 'full_dataset_summary_' + getStringTimestamp() + '.xlsx'
    #with pd.ExcelWriter(workbookName) as writer:
    #    articleSet.putDisciplineSummariesToExcel(writer)
    #    articleSet.putJournalSummariesToExcel(writer)
    #    articleSet.putDisciplineDiffsToExcel(writer)
    #    articleSet.putJournalDiffsToExcel(writer)

