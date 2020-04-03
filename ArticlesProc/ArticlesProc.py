from stanfordnlp.server import CoreNLPClient
from stanfordcorenlp import StanfordCoreNLP

from Citations.Citation import Citation
from Articles.ArticleSet import ArticleSet, getGranularStatisticalSummariesOfSetsDict, chartDifferencesInSubsetMeans
from Articles.ArticleSetBuilder import ArticleSetBuilder, getSummaryFromPickle, getSummaryAndPickleFromXML

from DevelopmentSets.citationRecognitionLiteratureSet681 import sampleLiteratureCitations
from DevelopmentSets.citationRecognitionBiologySet981 import sampleBiologyCitations
from DevelopmentSets.citationRecognitionSociologySet711 import sampleSociologyCitations
from DevelopmentSets.citationRecognitionMathSet701 import sampleMathCitations

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

print(len(sampleMathCitations))
multipleYearsCount = 0
noYearsCount = 0
for raw in sampleMathCitations[::20][100:120]:
    citation = Citation(raw)
#    if len(citation.getYear()) > 1:
#        multipleYearsCount += 1
#    elif not citation.getYear():
#        noYearsCount += 1
#print('multiple years count:', multipleYearsCount)
#print('no years count:', noYearsCount)
    if citation.getNameList()[1]:
        print(raw[:115])
        print([str(name) for name in citation.getNames()])
        print()




#with CoreNLPClient(annotators=['tokenize', 'ssplit', 'parse'], be_quiet=True, memory='16G', threads=8, timeout=240000) as client:
def getSampleOfRawCitations(articles):
    for article in articles:
        for citation in article.getCitations():
            print('"' + escapeDoubleQuotes(str(citation)) + '", ')
