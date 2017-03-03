# this isn't right if you don't from __future__ import division
from collections import Counter
from ..linearAlgebra.matrice import shape
from ..linearAlgebra.matrice import get_column
from ..linearAlgebra.matrice import make_matrix
from ..linearAlgebra.vector import dot
from ..linearAlgebra.vector import sum_of_squares
import math
import matplotlib.pyplot as plt

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

def correlation_matrix(data):
    """returns the num_columns x num_columns matrix whose (i, j)th entry
    is the correlation between columns i and j of data"""
    _, num_columns = shape(data)#shap is a function in LinearAlgebra.matrices
    def matrix_entry(i, j):
        return correlation(get_column(data, i), get_column(data, j))
    return make_matrix(num_columns, num_columns, matrix_entry)
    
    
def scatter_plot_matrix(data):
    _, num_columns = shape(data)
    fig, ax = plt.subplots(num_columns, num_columns)
    for i in range(num_columns):
        for j in range(num_columns):
            # scatter column_j on the x-axis vs column_i on the y-axis
            if i != j: ax[i][j].scatter(get_column(data, j), get_column(data, i))
            # unless i == j, in which case show the series name
            else: ax[i][j].annotate("series " + str(i), (0.5, 0.5),
                                    xycoords='axes fraction',
                                    ha="center", va="center")
            # then hide axis labels except left and bottom charts
            if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
            if j > 0: ax[i][j].yaxis.set_visible(False)
            # fix the bottom right and top left axis labels, which are wrong because
            # their charts only have text in them
    ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
    ax[0][0].set_ylim(ax[0][1].get_ylim())
    plt.show()
    
'''Sampling>bootstrapping'''
def bootstrap_sample(data):
    """randomly samples len(data) elements with replacement"""
    return [random.choice(data) for _ in data]

'''
stat_fn is a function like median 
or variance which gets a list of list of(two list is not typo)
numbers and convert them to a list with num_samples elements
of numbers like the list of variances made by the bootstraped data
'''
def bootstrap_statistic(data, stats_fn, num_samples):
    """evaluates stats_fn on num_samples bootstrap samples from data"""
    return [stats_fn(bootstrap_sample(data))
        for _ in range(num_samples)]


