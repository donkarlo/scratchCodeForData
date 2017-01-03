from __future__ import division
import random
import statistics


class Dicing:
    x=range(1,7)
    def __init__(self):
        pass#instead of return
        
    @staticmethod#so you dont need to pass self
    def roll():
        return random.randint(1,6)
        
    def roll_n_times(self,n):
        return [self.roll() for _ in range(1,n)]
      
    def mu(self):#mu is 3
        return sum(self.x)/len(self.x)
        
    def sigma(self):#2.917
        return sum([((i-self.mu())**2)/(len(self.x)) for i in self.x])

    
dicing = Dicing()
print dicing.roll()