from stanfordnlp.server import CoreNLPClient
from stanfordcorenlp import StanfordCoreNLP

from Citations.Citation import Citation
from Articles.ArticleSet import ArticleSet
from Articles.ArticleSetBuilder import ArticleSetBuilder, getSummaryFromPickle, getSummaryAndPickleFromXML

from DevelopmentSets.citationRecognitionLiteratureSet681 import sampleLiteratureCitations
from DevelopmentSets.citationRecognitionBiologySet981 import sampleBiologyCitations

from random import sample

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

with CoreNLPClient(annotators=['tokenize', 'ssplit', 'parse'], be_quiet=True, memory='16G', threads=8, timeout=240000) as client:
    mathArticles = ArticleSetBuilder(client).retrieveArticlesFromPickle('FULL_COMBINED_MATH_701_DATASET_18-Mar-2020 (15_18)').getArticles()
    sociologyArticles = ArticleSetBuilder(client).retrieveArticlesFromPickle('FULL_COMBINED_SOCIOLOGY_711_DATASET_19-Mar-2020 (14_34)').getArticles()
    literatureArticles = ArticleSetBuilder(client).retrieveArticlesFromPickle('FULL_DATASET_receipt-id-1451681-part-001 (literature)_19-Mar-2020 (16_55)').getArticles()
    biologyArticles = ArticleSetBuilder(client).retrieveArticlesFromPickle('FULL_DATASET_receipt-id-1423981-part-001 (biology)_20-Mar-2020 (01_37)').getArticles()
    
    ArticleSet(articles=mathArticles).markGroups(discipline='math')
    ArticleSet(articles=sociologyArticles).markGroups(discipline='sociology')
    ArticleSet(articles=literatureArticles).markGroups(discipline='literature')
    ArticleSet(articles=biologyArticles).markGroups(discipline='biology')

    allArticles = mathArticles + sociologyArticles + literatureArticles + scienceArticles
    fullArticleSet = ArticleSet(allArticles)
    fullArticleSet.getData(verbose=False)
    fullArticleSet.makeHists()
    fullArticleSet.pickleAllArticles(fileName="FULL_ARTICLE_SET_3_20")
    #literatureArticles = ArticleSetBuilder(client).retrieveArticlesFromPickle('FULL_DATASET_receipt-id-1451681-part-001 (literature)_19-Mar-2020 (16_55)').getArticles()
    #litArticleSet = ArticleSet(articles=sample(literatureArticles, 1000))
    #litArticleSet.markGroups(discipline='literature')
    #print(litArticleSet.getData(indexBy=['discipline', 'journal', 'id'], verbose=False))
    

#print('dataset size', len(sampleLiteratureCitations))
#for citation in sampleLiteratureCitations[::5][180:]:
#    print(Citation(citation).getNameList())