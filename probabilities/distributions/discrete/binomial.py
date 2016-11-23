from bernoulli import bernoulli_trial;
'''
the production of this is a variable that it's higher band is 
and the lower band is 0
   ''' 
def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))