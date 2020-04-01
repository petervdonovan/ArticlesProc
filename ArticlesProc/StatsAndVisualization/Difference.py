from StatsAndVisualization.visualizationUtils import zScoreToRGB
import math
from scipy import stats

class Difference(object):
    """Class representation a difference between samples, 
    described in terms of what it signifies about a difference
    between populations."""
    def __init__(self, testStatistic, significanceLevels):
        '''Initialize based on calculated values. Significance levels are
        pairs, where the first element is alpha and the second element is a
        boolean representing whether the statistic is significant at that
        alpha level.'''
        #print('hello, i am a difference and my test statistic is', testStatistic)
        self.testStatistic = testStatistic
        '''The test statistic (e.g., t, z)'''
        self.significanceLevels = {}
        for significanceLevel in significanceLevels:
            self.significanceLevels[significanceLevel[0]] = significanceLevel[1]
    # Factory methods
    @classmethod
    def comparePopulationMean(cls, series1, series2, *alphas):
        '''Returns -1 if series1 appears to have a lower mean,
        +1 if series1 appears to have a higher mean,
        and 0 if it is not possible to reject the possibility that the
        population mean is the same.'''
        n1 = series1.size
        n2 = series2.size
        if n1 <= 0 or n2 <= 0:
            return 0
        xBar1 = series1.mean()
        xBar2 = series2.mean()
        return propComparePopulationMean(cls, n1, n2, xBar1, xBar2, sigma1, sigma2, alphas)
    @classmethod
    def propComparePopulationMean(cls, n1, n2, xBar1, xBar2, s1, s2, alphas):
        if s1 is None or s2 is None or not n1 or not n2:
            return cls(None, [])
        a = s1*s1/n1
        b = s2*s2/n2
        t = (xBar1 - xBar2)/(math.sqrt(a + b))
        df = (a+b)*(a+b)/(a*a/(n1-1) + b*b/(n2-1))
        significanceLevels = []
        for alpha in alphas:
            if df and df > 0:
                tSubAlphaOverTwo = stats.t.ppf(1 - alpha/2, df)
                significanceLevels.append((alpha, abs(t) > tSubAlphaOverTwo))
        #print(t)
        #print('t is no!', t, n1, n2, xBar1, xBar2, s1, s2, alphas)
        return cls(t, significanceLevels)
    def __float__(self):
        return float(self.testStatistic)
    def __str__(self):
        return str(self.testStatistic)
    def getSignificance(self, alpha):
        '''Returns whether this Difference is known to be statistically
        significant for a given alpha value. Returns false if the answer
        cannot be determined, given the information with which the 
        Difference was initialized.'''
        for level in self.significanceLevels:
            if level <= alpha and self.significanceLevels[level] == True:
                return True
        return False
    def getStat(self):
        '''Returns the test statistic of this Difference.'''
        return self.testStatistic
    @staticmethod
    def testStatAsHSL(difference):
        '''Returns an HSL value in the form of a CSS rule based on the 
        test statistic.'''
        if not isinstance(difference, Difference) or difference.getStat() is None or math.isnan(difference.getStat()):
            return ''
        if not difference:
            return zScoreToRGB(0)
        return 'background-color: ' + zScoreToRGB(difference.getStat()) + ';'
    @staticmethod
    def formatBasedOnSignificance(difference):
        '''Returns a CSS rule based on the significance level.'''
        if not isinstance(difference, Difference) or difference.getStat() is None or math.isnan(difference.getStat()):
            return ''
        if not difference:
            return ''
        rule = ''
        if difference.getSignificance(0.05):
            rule += 'font-weight: bold;'
        if difference.getSignificance(0.01):
            rule += 'font-style: italic;'
        return rule
    def getInverted(self):
        testStatistic = self.testStatistic
        significanceLevels = [(level, self.significanceLevels[level]) 
                              for level in self.significanceLevels]
        return Difference(-testStatistic, significanceLevels)

# Supporting methods
def putDifferencesToExcel(writer, sheetName, chart):
    '''Puts a conditionally formatted description of the differences in subset means to an Excel sheet.'''
    styler = chart.round(2).style
    styler.applymap(Difference.testStatAsHSL).applymap(Difference.formatBasedOnSignificance)
    styler.to_excel(writer, sheet_name=sheetName)