from __future__ import division
from collections import Counter
import math
from matplotlib import pyplot as plt
'''
use this incase u dont have an __init__.py in continuos
import sys;
sys.path.append('probabilities/distributions/continuous') 
import normal
'''
from probabilities.distributions.continuous.normal import * 
from probabilities.distributions.discrete.binomial import * 

    
    
def make_hist(p, n, num_points):
    '''
    10000 times we record the sum of successes of 100 bernuli trial
    OR
    10000 times we will examine 100 bernouli trials to sotre the sum of successes
    '''
    data = [binomial(n, p) for _ in range(num_points)]
    # use a bar chart to show the actual binomial samples
    '''this line says how many times 76 was seen in 10000 
    times that we have thrown 100 times a coin
    a sample output:
    Counter({76: 908, 75: 895, 74: 871,
    77: 860, 73: 766, 72: 730, 78: 727,
    79: 616, 71: 615, 70: 504, 80: 504,
    81: 373, 69: 342, 82: 226, 68: 222,
    67: 190, 83: 172, 66: 113, 84: 101,
    65: 68, 85: 55, 64: 46, 86: 30, 63: 17,
    87: 15, 62: 11, 61: 7, 88: 6, 60: 4,
    89: 3, 59: 2, 90: 1})
    '''
    histogram = Counter(data)
    plt.bar([x - 0.4 for x in histogram.keys()],
        [v / num_points for v in histogram.values()],
        0.8,
        color='0.75')
    
    mu = p * n
    sigma = math.sqrt(n * p * (1 - p))
    
    # use a line chart to show the normal approximation
    
    xs = range(min(data), max(data) + 1)
    ys = [normal_cdf(i + 0.5, mu, sigma) - normal_cdf(i - 0.5, mu, sigma)
        for i in xs]
    plt.plot(xs,ys)
    
    plt.title("Binomial Distribution vs. Normal Approximation")
    plt.show()
    
make_hist(0.75,100,10000)