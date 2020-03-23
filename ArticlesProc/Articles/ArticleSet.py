import matplotlib.pyplot as plt
import time
import pickle
from datetime import datetime
import pandas as pd
from Utils.statsUtils import confidenceIntervalOfMean


class ArticleSet(object):
    """A set of articles to be analyzed."""
    figureCount = 0
    INDEX_BY=['discipline', 'journal', 'original id']
    pd.set_option('display.max_rows', 500)
    def __init__(self, articles=set()):
        self.articles = articles
        self.rawData = None
        #self.tokenCounts = []
        #self.parseLevels = []
        #self.dependentClauses = []
        #self.prepositionalPhrases = []
        plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})
        self.countOfInvalidForUnknownReason = 0
    def markGroups(self, discipline=''):
        '''Mark Articles as being members of certain groups for indexing.'''
        for article in self.articles:
            article.setGroup('journal', article.getJournal())
            if discipline:
                article.setGroup('discipline', discipline)
            article.setGroup('original id', article.id)
    def getSummariesByGroup(self, groupType=ArticleSet.INDEX_BY[0]):
        # Returns a DataFrame with summary statistics for all articles that fall under each group,
        # where the type of group (discipline, journal, etc.) is specified.
        levels = self.getData().levels
        names = self.getData().names
        depth = names.index(groupType)
    def getDescriptiveStatistics(self):
        '''Returns a DataFrame containing descriptive statistics.'''
        return pd.DataFrame([
            [self.rawData.loc[:,'Tokens'].size, self.rawData.loc[:,'Parse Tree Levels'].size,
                         self.rawData.loc[:,'Dependent Clauses'].size, self.rawData.loc[:,'Prepositional Phrases'].size],
            
            [self.rawData.loc[:,'Tokens'].mean(), self.rawData.loc[:,'Parse Tree Levels'].mean(),
                         self.rawData.loc[:,'Dependent Clauses'].mean(), self.rawData.loc[:,'Prepositional Phrases'].mean()],
            
            [confidenceIntervalOfMean(self.rawData.loc[:,'Tokens'], 0.95), confidenceIntervalOfMean(self.rawData.loc[:,'Parse Tree Levels'], 0.95),
                         confidenceIntervalOfMean(self.rawData.loc[:,'Dependent Clauses'], 0.95), confidenceIntervalOfMean(self.rawData.loc[:,'Prepositional Phrases'], 0.95)],

            [self.rawData.loc[:,'Tokens'].std(), self.rawData.loc[:,'Parse Tree Levels'].std(),
                         self.rawData.loc[:,'Dependent Clauses'].std(), self.rawData.loc[:,'Prepositional Phrases'].std()]
            ],
            columns=[
                'Tokens',
                'Parse Tree Levels',
                'Dependent Clauses',
                'Prepositional Phrases'
            ],
            index=[
                'n',
                'mean',
                '0.95 CI',
                's'
            ])
    def pickleAllArticles(self, fileName="dataset"):
        dbfile = open(fileName + "_" + datetime.now().strftime("%d-%b-%Y (%H_%M)"), 'ab')
        pickle.dump([article.getSaveableData() for article in self.articles], dbfile)
        print("data dumped to", fileName + "_" + datetime.now().strftime("%d-%b-%Y (%H_%M)"))
        dbfile.close()
    def makeHists(self, bins=20):
        # Create the chart
        fig, ax1 = plt.subplots(4)
        fig.suptitle = "Article Set Summary"
        ax1[0].hist(self.rawData.loc[:,'Tokens'].tolist(), bins=bins)
        ax1[1].hist(self.rawData.loc[:,'Parse Tree Levels'].tolist(), bins=bins)
        ax1[2].hist(self.rawData.loc[:,'Dependent Clauses'].tolist(), bins=bins)
        ax1[3].hist(self.rawData.loc[:,'Prepositional Phrases'].tolist(), bins=bins)
        plt.show()
    def getData(self, decimalPlaces=20, verbose=True):
        lastTimeCheck = time.time()
        table = [] # 2D list to be converted into a DataFrame
        index = [] # list of tuples to be converted into a MultiIndex to be used in the DataFrame
        if not self.rawData:
            for article in self.articles:
                if article.hasValidAbstract():
                    if verbose:
                        # Print out the data
                        print(article.getPath())
                        print("\nTitle:", article.getTitle(),
                      '\nAll of the following data is per sentence.',
                      "\nMean tokens:", article.getTokensPerSentence())
                        print(
                      "Mean parse tree levels:", article.getMeanParseTreeLevels(),
                      '\nMean dependent clauses:', article.getMeanDependentClauses(),
                      '\nMean prepositional phrases:', article.getMeanPrepositionalPhrases())
                        print("Time to get parse tree levels, dependent clauses, and prepositional phrases:", time.time() - lastTimeCheck)
                    # Save the data for the current Article in the table
                    table.append([
                        round(article.getTokensPerSentence(), decimalPlaces),
                        round(article.getMeanParseTreeLevels(), decimalPlaces),
                        round(article.getMeanDependentClauses(), decimalPlaces),
                        round(article.getMeanPrepositionalPhrases(), decimalPlaces)
                        ])
                    # Create row in the index, if applicable
                    indexOfCurrent = [] # temporary variable
                    for group in ArticleSet.INDEX_BY:
                        groupValue = article.getGroup(group)
                        # Convert lists to the hashable type tuple
                        if type(groupValue) == list:
                            indexOfCurrent.append(tuple(groupValue))
                        else:
                            indexOfCurrent.append(groupValue)
                    index.append(tuple(indexOfCurrent))
                # Make note if for some reason the current abstract is not parseable (necessary to make sure the data is valid)
                if article.getAbstractInvalidForUnknownReason():
                    print('-------------------------ABSTRACT INVALID FOR UNKNOWN REASON------------------------------')
                    self.countOfInvalidForUnknownReason += 1
                #print("Time to process article:", time.time() - lastTimeCheck)
                lastTimeCheck = time.time()
            # Save all data to self.rawData as a DataFrame
            columnNames = ['Tokens', 'Parse Tree Levels', 'Dependent Clauses', 'Prepositional Phrases']
            if len(index) > 0:
                self.rawData = pd.DataFrame(table, index=pd.MultiIndex.from_tuples(index, names=ArticleSet.INDEX_BY), columns=columnNames)
            else:
                self.rawData = pd.DataFrame(table, columns=columnNames)
            for i in range(len(index)):
                self.rawData = self.rawData.sort_index()
        print('Count of invalid abstracts for unknown reason:', self.countOfInvalidForUnknownReason)
        return self.rawData
    def getAllContributors(self):
        '''Gets set of the most detailed versions of the names of all of the contributors.'''
        allContributors = set()
        for article in articles:
            articleContributors = article.getContributors().copy()
            for (contributorToAdd, foundContributor) in zip(articleContributors, allContributors):
                if contributorToAdd > foundContributor:
                    # The new name (contributorToAdd) is more specific than the name that previously existed (foundContributor)
                    articleContributors.remove(contributorToAdd) # Remove the added contributor from the articleContributors
                    allContributors.remove(foundContributor) # Remove the duplicate contributor from allContributors
                    allContributors.add(contributorToAdd) # Replace the duplicate contributor with the more detailed contributor Name
                    print('A new name is more specific:', str(contributorToAdd), 'is more specific than', str(foundContributor))
                    break
                if foundContributor > contributorToAdd:
                    # The already found name is more specific
                    articleContributors.remove(contributorToAdd) # Remove the added contributor from the articleContributors
                    print('The already found name is more specific:', str(foundContributor), 'is more specific than', str(contributorToAdd))
                    break
            # Add leftover names that did not match anything
            print('The following names did not match any previously found names:', (str(contributorToAdd) for contributorToAdd in articleContributors))
            allContributors.add(articleContributors)
    def getLanguageDistribution(self):
        '''Gets the number of appearances of any given language as the dominant language in the abstract of an Article.'''
        distribution = {}
        for article in self.articles:
            language = article.getAbstractLanguage()
            if not language in distribution:
                distribution[language] = 1
            else:
                distribution[language] += 1
        return distribution
    def getIndex(self):
        return self.rawData.index