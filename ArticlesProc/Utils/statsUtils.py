from scipy import stats
import numpy as np
import math

def confidenceIntervalOfMean(series, alpha):
    '''Gets the confidence interval of a pandas series as a tuple.'''
    mean = series.mean()
    standardError = stats.sem(series.tolist())
    tSubAlphaOverTwo = stats.t.ppf(1 - alpha/2, series.size-1)
    return (mean - tSubAlphaOverTwo*standardError, mean + tSubAlphaOverTwo*standardError)
def differentPopulationMean(series1, series2, alpha):
    '''Returns -1 if series1 appears to have a lower mean,
    +1 if series1 appears to have a higher mean,
    and 0 if it is not possible to reject the possibility that the
    population mean is the same.'''
    xBar1 = series1.mean()
    xBar2 = series2.mean()
    s1 = series1.std()
    s2 = series2.std()
    n1 = series1.size
    n2 = series2.size
    a = s1*s1/n1
    b = s2*s2/n2
    t = (xBar1 - xBar2)/(math.sqrt(a + b))
    df = (a+b)*(a+b)/(a*a/(n1-1) + b*b/(n2-1))
    tSubAlphaOverTwo = stats.t.ppf(1 - alpha/2, df)
    if t > tSubAlphaOverTwo:
        return 1
    elif t < - tSubAlphaOverTwo:
        return -1
    return 0