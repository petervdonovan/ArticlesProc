import matplotlib.pyplot as plt
import time
import pickle
import pandas as pd
from StatsAndVisualization.Difference import Difference, putDifferencesToExcel
from StatsAndVisualization.statsUtils import confidenceIntervalOfMean, getCombinedXNS
from Utils.textProcUtils import capitalizeFirstLetterEachWord
from Utils.timeUtils import getStringTimestamp

def getGranularStatisticalSummariesOfSetsDict(setsDict):
    return pd.concat([setsDict[set].getDescriptiveStatistics() for set in setsDict], keys=[set for set in setsDict])
def chartDifferencesInSubsetMeans(setsDict, statistic, minSampleSize=30):
    '''Returns a DataFrame with differences in subset means and boolean values for
    statistical significance at 0.95 and 0.99 confidence intervals, given h0 = no
    difference and two-sided t test.'''
    statistic = capitalizeFirstLetterEachWord(statistic)
    setNameList = [setName for setName in setsDict if setsDict[setName].getAnalyzableArticleCount() >= minSampleSize]
    sets = [setsDict[setName] for setName in setNameList]
    dimension = len(setNameList)
    data = [[None for _ in range(dimension)] for _ in range(dimension)]
    for j in range(dimension):
        for k in range(j):
            data[k][j] = Difference.comparePopulationMean(sets[j].getData().loc[:, statistic], sets[k].getData().loc[:, statistic], 0.05, 0.01)
            # Copy the data from one side of the diagonal to the other 
            # (before b was compared to a, now copy to a compared to b)
            data[j][k] = data[k][j].getInverted()
    return pd.DataFrame(data=data, index=setNameList, columns=setNameList)

class ArticleSet(object):
    """A set of articles to be analyzed."""
    figureCount = 0
    pd.set_option('display.max_rows', 500)
    def __add__(self, other):
        '''Return a new ArticleSet with a combination of the
        articles in this ArticleSet and the articles in 
        another ArticleSet.'''
        articles = set()
        for theirArticle in other.articles:
            found = False
            for myArticle in self.articles:
                if myArticle.isEquivalent(theirArticle):
                    myArticle.add(theirArticle)
                    found = True
                if theirArticle.isEquivalent(myArticle):
                    theirArticle.add(myArticle)
                    if found: break
            if not found:
                articles.add(theirArticle)
        articles = articles.union(self.articles)
        return ArticleSet(articles)
    def __init__(self, articles):
        self.articles = articles
        self.rawData = None
        self.descriptiveStatistics = None
        self.subsets = dict()
        plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})
        self.countOfInvalidForUnknownReason = None
    def getDescriptiveStatistics(self):
        '''Returns a DataFrame containing descriptive statistics.'''
        if self.descriptiveStatistics is None:
            self.descriptiveStatistics = pd.DataFrame([
            [data.size for (_, data) in self.getData().iteritems()],
            [data.mean() for (_, data) in self.getData().iteritems()],
            [confidenceIntervalOfMean(_, 0.05) for (name, data) in self.getData().iteritems()],
            [data.std for (_, data) in self.getData().iteritems()]
            ],
            columns=[name for (name, _) in self.getData().iteritems()],
            index=[
                'n',
                'mean',
                '0.95 CI',
                's'
            ])
        return self.descriptiveStatistics
    def pickleAllArticles(self, fileName="dataset"):
        '''Pickles all articles as their tuple representation.'''
        with open(fileName + "_" + getStringTimestamp(), 'ab') as file:
            pickle.dump([article.getSaveableData() for article in self.articles], file)
            print("data dumped to", fileName + "_" + getStringTimestamp())
    def pickleSelf(self, fileName="dataset"):
        '''Pickles the ArticleSet'''
        with open(fileName + "_" + getStringTimestamp(), 'ab') as file:
            pickle.dump(self, file)
            print("data dumped to", fileName + "_" + getStringTimestamp())
    def makeHists(self, bins=20):
        '''Show frequency distributions of each calculated article characteristic.'''
        # Create the chart
        if len(self.getData().columns) > 1:
            fig, ax1 = plt.subplots(len(self.getData().columns))
            title = "| "
            count = 0
            for (name, data) in self.getData().iteritems():
                ax1[count].hist(data.tolist(), bins=bins)
                title += name + ' | '
                count += 1
            fig.suptitle = title
        else:
            plt.hist(self.getData().iloc[:,0])
            plt.title = self.getData().columns[0]
        plt.show()
    def thinOut(self):
        self.articles = [article for article in self.articles if article.hasValidAbstract()]
    def getData(self, decimalPlaces=20, verbose=False, simple=True):
        lastTimeCheck = time.time()
        table = [] # 2D list to be converted into a DataFrame
        index = [] # list of tuples to be converted into a MultiIndex to be used in the DataFrame
        if self.rawData is None:
            for article in self.articles:
                if (simple and article.getEnglishAbstract() is not None) or (not simple and article.hasValidAbstract()):
                    if verbose:
                        # Print out the data
                        print(article.getPath())
                        if not simple:
                            print("\nTitle:", article.getTitle(),
                          '\nAll of the following data is per sentence.',
                          "\nMean tokens:", article.getTokensPerSentence())
                            print(
                          "Mean parse tree levels:", article.getMeanParseTreeLevels(),
                          '\nMean dependent clauses:', article.getMeanDependentClauses(),
                          '\nMean prepositional phrases:', article.getMeanPrepositionalPhrases())
                            print("Time to get parse tree levels, dependent clauses, and prepositional phrases:", time.time() - lastTimeCheck)
                    if not simple:
                        # Calculate secondary Article characteristics
                        lengthAdjustedSbar = article.getMeanDependentClauses() / article.getTokensPerSentence()
                        lengthAdjustedPp = article.getMeanPrepositionalPhrases() / article.getTokensPerSentence()
                        combinedAdjustedSbarPp = lengthAdjustedSbar + lengthAdjustedPp
                        # Save the data for the current Article in the table
                        table.append([
                            round(article.getTokensPerSentence(), decimalPlaces),
                            round(article.getMeanParseTreeLevels(), decimalPlaces),
                            round(article.getMeanDependentClauses(), decimalPlaces),
                            round(article.getMeanPrepositionalPhrases(), decimalPlaces),
                            round(lengthAdjustedSbar, decimalPlaces),
                            round(lengthAdjustedPp, decimalPlaces),
                            round(combinedAdjustedSbarPp, decimalPlaces)
                            ])
                        # Create row in the index, if applicable
                        index.append(article.getId())
                    elif article.getFullTokensPerSentence() is not None:
                        table.append([
                            round(article.getFullTokensPerSentence(), decimalPlaces)
                            ])
                        # Create row in the index, if applicable
                        index.append(article.getId())
            #print("Time to process article:", time.time() - lastTimeCheck)
            lastTimeCheck = time.time()
            # Save all data to self.rawData as a DataFrame
            if not simple:
                columnNames = ['Tokens', 'Parse Tree Levels', 'Dependent Clauses', 'Prepositional Phrases', 'Length Adjusted SBAR', 'Length Adjusted PP', 'Combined Adjusted SBAR PP', 'Full Abstract Tokens']
            else:
                columnNames = ['Full Abstract Tokens']
            self.rawData = pd.DataFrame(table, index=index, columns=columnNames)
        if verbose: print('Count of invalid abstracts for unknown reason:', self.countOfInvalidForUnknownReason)
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
        return self.getData().index
    def getSubsetsByDiscipline(self):
        return self.getSubsetsByArticleCharacteristic('discipline', lambda article: article.getDiscipline())
    def getSubsetsByJournal(self):
        return self.getSubsetsByArticleCharacteristic('journal', lambda article: article.getJournal())
    def getSubsetsByArticleCharacteristic(self, characteristicName, articleCharacteristicGetterFunction):
        '''Returns a dictionary of subsets that have the same value returned by 
        the articleCharacteristicGetterFunction. For instance, if the 
        articleCharacteristicGetterFunction returns the journal in which the article
        was published, then it returns a dictionary of subsets of articles that were
        published in the same journal.'''
        # Create the dictionary associated with this articleCharacteristicGetterFunction
        # in the subsets dictionary
        if not characteristicName in self.subsets:
            self.subsets[characteristicName] = dict()
            currentDict = self.subsets[characteristicName]
            # iterate over the articles and place them in the dictionary
            for article in self.articles:
                characteristicValue = articleCharacteristicGetterFunction(article)
                if characteristicValue in currentDict:
                    currentDict[characteristicValue].add(article)
                else:
                    currentDict[characteristicValue] = {article}
            # In-place conversion of all of the sets of articles into ArticleSets
            for subset in currentDict:
                currentDict[subset] = ArticleSet(currentDict[subset])
        return self.subsets[characteristicName]
    def getStatistic(self, statistic):
        '''Returns the mean value of some descriptive statistic. This statisic can
        be any of the statistics returned by getDescriptiveStatistics.'''
        return self.getDescriptiveStatistics().loc['mean', capitalizeFirstLetterEachWord(statistic)]
    def getCountOfInvalidForUnknownReason(self):
        if self.countOfInvalidForUnknownReason == None:
            self.countOfInvalidForUnknownReason = 0
            for article in self.articles:
                if article.getAbstractInvalidForUnknownReason():
                    print('found invalid')
                    self.countOfInvalidForUnknownReason += 1
        return self.countOfInvalidForUnknownReason
    def __len__(self):
        return len(self.articles)
    def getAnalyzableArticleCount(self):
        return len(self.getData().index)
    def putDisciplineWiseJournalComparisonToExcel(self, writer):
        '''Puts a sheet showing the difference between journals of a given
        discipline and journals of other disciplines to a separate sheet in 
        and Excel workbook.'''
        putDifferencesToExcel(writer, 'Discipline-Wise Journal Compari', self.getDisciplineWiseJournalComparison())
    def putDisciplineSummariesToExcel(self, writer):
        '''Puts summaries of syntactic characteristics of each discipline to a separate sheet
        in an Excel workbook.'''
        articleDataByDiscipline = getGranularStatisticalSummariesOfSetsDict(self.getSubsetsByDiscipline())
        articleDataByDiscipline.to_excel(writer, sheet_name='By Discipline')
    def putJournalSummariesToExcel(self, writer):
        '''Puts summaries of syntactic characteristics of each journal to a separate sheet in
        an Excel workbook.'''
        articleDataByJournal = getGranularStatisticalSummariesOfSetsDict(self.getSubsetsByJournal())
        articleDataByJournal.to_excel(writer, sheet_name='By Journal')
    def putDisciplineDiffsToExcel(self, writer):
        '''Puts a table of the differences between each discipline and every other discipline,
        with respect to the mean of a given statistic.'''
        self.putDiffsToExcel(writer, 'discipline', lambda article: article.getDiscipline())
    def putJournalDiffsToExcel(self, writer):
        '''Puts a table of the differences between each discipline and every other discipline,
        with respect to the mean of a given statistic.'''
        self.putDiffsToExcel(writer, 'journal', lambda article: article.getJournal())
    def putDiffsToExcel(self, writer, characteristicName, articleCharacteristicGetterFunction):
        statTypes = self.getData().columns
        for statType in statTypes:
            name = 'Differences by ' + capitalizeFirstLetterEachWord(characteristicName) + ' (' + capitalizeFirstLetterEachWord(statType) + ')'
            if len(name) > 31: name = name[:31]
            putDifferencesToExcel(
                writer, 
                name, 
                chartDifferencesInSubsetMeans(
                    self.getSubsetsByArticleCharacteristic(
                        characteristicName, 
                        articleCharacteristicGetterFunction
                        ),
                   statType)
                )
    def getStatsBySubset(self, 
                         characteristicName, articleCharacteristicGetterFunction, 
                         statNames=None):
        '''Returns a DataFrame whose columns correspond to article statistics 
        (listed in statNames) and whose rows correspond to subsets, 
        selected based on an article characteristic. Each cell contains an
        ordered pair: mean and n. Essentially, mean represents the value of 
        the characteristic for that subset, and the n is necessary to 
        evaluate how meaningful that statistic actually is.'''
        if statNames == None:
            statNames = self.getDescriptiveStatistics().columns
        statNames = [capitalizeFirstLetterEachWord(statName) for statName in statNames]
        subsets = self.getSubsetsByArticleCharacteristic(characteristicName, 
                                                         articleCharacteristicGetterFunction)
        data = \
            [
                [
                    (
                        subsets[subset].getDescriptiveStatistics().loc['mean', statName],
                        subsets[subset].getDescriptiveStatistics().loc['n', statName]
                    )
                    for statName in statNames
                ]
                for subset in subsets
            ]
        return pd.DataFrame(data=data,index=[subsetName for subsetName in subsets],columns=statNames)
    def getDisciplineWiseJournalComparison(self):
        '''Returns a DataFrame with statistics for each journal in each
        discipline, for comparison of journals across disciplines. 
        See getSubsetWiseSubsetComparison for details.'''
        return self.getSubsetWiseSubsetComparison('discipline', 
                                             lambda article: article.getDiscipline(),
                                             'journal', 
                                             lambda article: article.getJournal())
    def getSubsetWiseSubsetComparison(
        self, 
        characteristicName1, articleCharacteristicGetterFunction1,
        characteristicName2, articleCharacteristicGetterFunction2):
        '''Outputs an excel sheet consisting of a vertical stack of tables,
        in which each table represents subsets of the whole and 
        columns of each table represent subsets of the subsets, formed
        by a different criteria. For instance, if each table corresponds to a
        discipline, each column in the table could correspond to a journal.
        Each row in the table corresponds to a statistic by which the 
        sub-subsets, if you will, are measured. For instance, in the table 
        for discipline X, there is a column for journal Y, and each cell in
        the column for journal Y corresponds to the Difference between that cell
        and the corresponding cells for journals OUTSIDE of the table for 
        discipline X, in other tables. The intention of this spreadsheet is to
        potentially refute the null hypothesis that (for instance) a journal in 
        discipline X is not statistically different from journals in other 
        disciplines (or whatever other characteristic they are separated by)'''
        subsetsToCompare = self.getSubsetsByArticleCharacteristic(
            characteristicName1, articleCharacteristicGetterFunction1
            )
        # Get a list of lists of stat Series. Each of these Series has
        # and index with 3 labels: mean, n, and s.
        subsetTables = pd.concat([
            getGranularStatisticalSummariesOfSetsDict(
                getDictionaryWithNumbersAsKeys(
                    subsetsToCompare[subset].getSubsetsByArticleCharacteristic(
                        characteristicName2, articleCharacteristicGetterFunction2
                    )
                )
            ).unstack(0).append(pd.DataFrame(index=['t']))
            for subset in subsetsToCompare
            ], keys=[subset for subset in subsetsToCompare]).stack(level=0, dropna=False).reorder_levels([2, 0, 1]).sort_index()
        getGranularStatisticalSummariesOfSetsDict(
                getDictionaryWithNumbersAsKeys(
                    subsetsToCompare['math'].getSubsetsByArticleCharacteristic(
                        characteristicName2, articleCharacteristicGetterFunction2
                    )
                )
            ).to_excel('intermediate_' + getStringTimestamp() + '.xlsx')
        #, columns=subsetsToCompare[subset].getSubsetsByArticleCharacteristic(
        #                characteristicName2, articleCharacteristicGetterFunction2
        #            ).keys()
        #print('got subset tables:', subsetTables)
        #subsetTables.to_excel("554test.xlsx")
        # Now it is necessary to convert each stat series in 
        # the cells of each subsetTable to a Difference. In order to do 
        # that, it will be necesary to calculate a test statistic and 
        # determine statistical significance at a couple of alphas.
        #print(subsetTables)
        for currentSubset in subsetsToCompare:
            otherSubsets = list(subsetsToCompare.keys())
            otherSubsets.remove(currentSubset)
            otherArticles = set()
            for otherSubset in otherSubsets:
                otherArticles = otherArticles.union(subsetsToCompare[otherSubset].articles)
            otherSubsetSet = ArticleSet(otherArticles)
            otherSubsetDescriptiveStatistics = otherSubsetSet.getDescriptiveStatistics()
            print(otherSubsetDescriptiveStatistics)
            #print('length of otherSubsetTables:', len(otherSubsetTables))
            for stat in otherSubsetDescriptiveStatistics.columns:
                outsideCurrentSubsetXNS = otherSubsetDescriptiveStatistics[stat]
                #summariesOfOtherSubgroups = [
                #    getCombinedXNS(subsetTables.loc[otherSubsetTable, [stat]])
                #    for otherSubsetTable in otherSubsetTables
                #    ]
                ##print(summariesOfOtherSubgroups)
                #outsideCurrentSubsetXNS = getCombinedXNS(
                #    pd.DataFrame(data=summariesOfOtherSubgroups, index=summariesOfOtherSubgroups[0].index)
                #    )
                #print(outsideCurrentSubsetXNS)
                print(subsetTables.index)
                print(subsetTables.loc[stat])
                print(subsetTables.loc[(stat, currentSubset)])
                for _, column in subsetTables.loc[(stat, currentSubset)].iteritems():
                    print(column)
                    column['t'] = Difference.propComparePopulationMean(
                        column['n'],
                        outsideCurrentSubsetXNS.at['n'],
                        column['mean'],
                        outsideCurrentSubsetXNS.at['mean'],
                        column['s'],
                        outsideCurrentSubsetXNS.at['s'],
                        [0.05, 0.01]
                        )
                    print(column['t'])
        #print(subsetTables)
        print("Done getting subsettables.")
        return subsetTables
    def __iter__(self):
        return iter(self.articles)

def getDictionaryWithNumbersAsKeys(meaningfulKeysDict):
    '''Returns a dictionary that is a copy of the dictionary passed,
    except the keys are changed to numbers starting with zero.'''
    meaninglessKeysDict = {}
    count = 0
    for key in meaningfulKeysDict:
        meaninglessKeysDict[count] = meaningfulKeysDict[key]
        count += 1
    return meaninglessKeysDict