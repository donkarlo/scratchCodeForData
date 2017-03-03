from __future__ import division
from collections import Counter
import math
import random
from matplotlib import pyplot as plt



def uniform_pdf(x):
    return 1 if x >= 0 and x < 1 else 0

def uniform_cdf(x):
    "returns the probability that a uniform random variable is <= x"
    if x < 0:
     return 0# uniform random is never less than 0
     
    elif x < 1: return x
     # e.g. P(X <= 0.4) = 0.4
    else:
        return 1# uniform random is always less than
     
def normal_pdf(x, mu=0, sigma=1):
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return (math.exp(-(x-mu) ** 2 / 2 / sigma ** 2) / (sqrt_two_pi * sigma))

#plotting normal destribution
xs = [x / 10.0 for x in range(-50, 50)]
plt.plot(xs,[normal_pdf(x,sigma=1) for x
 in xs],'-',label='mu=0,sigma=1')
plt.plot(xs,[normal_pdf(x,sigma=2) for x
 in xs],'--',label='mu=0,sigma=2')
plt.plot(xs,[normal_pdf(x,sigma=0.5) for
 x in xs],':',label='mu=0,sigma=0.5')
plt.plot(xs,[normal_pdf(x,mu=-1)
 for x
 in xs],'-.',label='mu=-1,sigma=1')
plt.legend()
plt.title("Various Normal pdfs")
plt.show()

#
def normal_cdf(x, mu=0,sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

#give it probability it will give you randiom variable bands
def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """find approximate inverse using binary search"""
    # if not standard, compute standard and rescale
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)
    low_z, low_p = -10.0, 0 # normal_cdf(-10) is (very close to) 0
    hi_z, hi_p = 10.0, 1 # normal_cdf(10) is (very close to) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2
         # consider the midpoint
        mid_p = normal_cdf(mid_z)
         # and the cdf's value there
        if mid_p < p:
            # midpoint is still too low, search above it
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            # midpoint is still too high, search below it
            hi_z, hi_p = mid_z, mid_p
        else:
            break
    return mid_z
    

#sample bernouli trial
def bernoulli_trial(p):
    return 1 if random.random() < p else 0
'''
the production of this is a variable that it's higher band is 
and the lower band is 0
   ''' 
def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))
    
    
'''sample bernouli trial'''
def bernoulli_trial(p):
    return 1 if random.random() < p else 0
'''
the production of this is a variable that it's higher band is 
and the lower band is 0
   ''' 
def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))
    
    
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
    
make_hist(0.75,100,1000000)





