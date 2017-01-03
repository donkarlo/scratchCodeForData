from __future__ import division
import math
from bernoulli import bernoulli_trial;
'''
the production of this is a variable that it's higher band is 
and the lower band is 0
   ''' 
def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))
    
def getSigma(n,p):
    return math.sqrt(p * (1 - p) * n)
    
def getMu(n,p):
    return p*n

'''based on Centeral theorem: 
Xi = sum of number times you get heads when you
flip a coin 1000 times for ith time
so if you repeat that experiment(filiping a conin 100 times)
100000 times you will have
X1 to X100000 and Xi would be between 1 too 1000

if you
flip a coin n=100 times and you repeat that
100000 times you will 
'''
def normal_approximation_to_binomial(n, p):
    """finds mu and sigma corresponding to a Binomial(n, p)"""
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma
