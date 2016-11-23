# this isn't right if you don't from __future__ import division
from collections import Counter
def mean(x):
    return sum(x) / len(x)

def median(v):
    """finds the 'middle-most' value of v"""
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2
    if n % 2 == 1:
        # if odd, return the middle value
        return sorted_v[midpoint]
    else:
        # if even, return the average of the middle values
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2


def quantile(dataList, percent):
    """returns the pth-percentile value in x"""
    p_index = int(percent * len(dataList))
    return sorted(dataList)[p_index]
    
def mode(x):
    """returns a list, might be more than one mode"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.iteritems()
        if count == max_count]
            
# "range" already means something in Python, so we'll use a different name
def data_range(x):
    return max(x) - min(x)

def de_mean(x):
    """translate x by subtracting its mean (so the result has mean 0)"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]
    
#variance from a sample population
def variance(x):
    """assumes x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)#sum of squares come from the vector package
    
def standard_deviation(x):
    return math.sqrt(variance(x))
'''
Both the range and the standard deviation have the same 
outlier problem that we saw
earlier for the mean.A more robust alternative computes 
the difference between the 75th percentile value
and the 25th percentile value:
which is quite plainly unaffected by a small number of outliers.
'''
def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)

def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)

def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0




