from scipy import stats
import statistics
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

ZERO_STAND_IN = 1e-8

def showNormalTransformedQQ(iterable, bins, *transformation):
    '''Shows a normal quantile plot of an iterable of values
    that can be compared to each other.'''
    fig, ax1 = plt.subplots(max(len(transformation), 2))
    for i, trans in enumerate(transformation):
        transformed = [trans(x) for x in iterable if x != 0]
        stats.probplot(transformed, plot=ax1[i])
    if len(transformation) == 1:
        ax1[1].hist(transformed, bins=bins)
    plt.show()
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
def rmsZAndTheoreticalZDifference(series):
    '''Returns the root mean square difference between the 
    computed z score of each value and the theoretical
    z score of the value based on ppf (inverse cdf).'''
    n = len(series)
    series.sort()
    pairs = zip(
        stats.zscore(series), 
        [
            stats.norm.ppf((i+0.5)/n)
            for i in range(n)
        ]
        )
    return rmsDiff(pairs)
def rmsDiff(pairs):
    '''Returns the root mean square difference between the two
    values in each pair.'''
    return statistics.mean((a - b)**2 for a, b in pairs)**0.5
def findPowerOfMaxRmsNormality(series, guess=0, step=1, maxSteps=8, depth=4, points=None):
    '''Returns the power to which one could raise each element
    in the series to make the distribution of the series as 
    normal as possible. The distribution is considered as 
    normal as possible if there is no power to which it could 
    be raised that would give a lower rms difference between
    computed z score and theoretical percent-point-function-
    based z score.'''
    # This is a recursive function.
    if points==None:
        points = list()
    if depth == 0:
        unzipped = list(zip(*points))
        plt.scatter(unzipped[0], unzipped[1], s=8)
        plt.show()
        return guess
    power = guess
    radius = 0
    minRmsPower = guess
    minRms = 1e6
    for _ in range(maxSteps + 1):
        for sign in [-1, 1]:
            signedPower = sign*power
            if power == 0:
                transformed = [math.log(x) for x in series if x != 0]
            else:
                transformed = [max(x, ZERO_STAND_IN)**(signedPower) for x in series]
            print('Calculating RMS for the power', signedPower)
            rms = rmsZAndTheoreticalZDifference(transformed)
            print('Power:', signedPower, 'and RMS:', rms)
            if rms < minRms:
                minRms = rms
                minRmsPower = signedPower
            points.append((signedPower, rms))
        power += step
    print('Power of max normality, remaining depth=' + str(depth), ':', minRmsPower)
    print('Min RMS deviation from normal z score:', minRms)
    return findPowerOfMaxRmsNormality(
        series, 
        guess=minRmsPower, 
        step=step/maxSteps,
        maxSteps=maxSteps,
        depth=depth-1, 
        points=points
        )