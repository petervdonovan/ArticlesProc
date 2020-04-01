from scipy import stats
import numpy as np
import math
import pandas as pd

def confidenceIntervalOfMean(series, alpha):
    '''Gets the confidence interval of a pandas series as a tuple.'''
    df = series.size-1
    if df <= 0 or not df:
        return (None, None)
    mean = series.mean()
    standardError = stats.sem(series.tolist())
    tSubAlphaOverTwo = stats.t.ppf(1 - alpha/2, df)
    return (mean - tSubAlphaOverTwo*standardError, mean + tSubAlphaOverTwo*standardError)
def getCombinedS(snList):
    '''Returns the combined standard deviation based on
    a list of pairs of s values and corresponding n values'''
    # get total n
    nTotal = sum(n for (_, n) in snList)
    # return None if there is no valid data
    if not nTotal or nTotal <= 1:
        return None
    # get list of mean squared deviation
    deviationSquaredNList = [(s**2*(n)/(n-1), n) for (s, n) in snList]
    # get sum of deviation squared
    sumDeviationSquared = sum(dev2*n for (dev2, n) in deviationSquaredNList)
    # return s
    print(sumDeviationSquared, nTotal)
    return math.sqrt(sumDeviationSquared / (nTotal - 1))
def getCombinedXNS(xnsDataFrame):
    '''Based on a DataFrame, in which each column
    contains elements labeled mean (x), n, and s, creates one 
    combined Pandas Series of the same form as the columns that represents 
    the same sample as all of the Pandas Series in the
    DataFrame combined.'''
    xnsList = [
        (xnsSeries['mean'], xnsSeries['n'], xnsSeries['s'])
        for seriesName, xnsSeries in xnsDataFrame.iteritems()
        ]
    combinedS = getCombinedS([(s, n) for (x, n, s) in xnsList])
    combinedN = sum(n for (x, n, s) in xnsList)
    combinedX = sum(x*n for (x, n, s) in xnsList) / combinedN
    return pd.Series(
        data=(combinedX, combinedN, combinedS), 
        index=['mean','n','s']
        )