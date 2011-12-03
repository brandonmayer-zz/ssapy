from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.hw4.agents.riskAware import *


import itertools
import numpy
import multiprocessing

import os
  
class randomAgent():
        def __init__(self):
            self.mybid = numpy.random.random()
        def bid(self):
            return self.mybid
        
if __name__ == '__main__':
    
    nAgents = 5
    
    auction = simultaneousAcution()
    
    #face price predicitons
    self.m = 5
    self.randomPriceVector = numpy.random.random_integers(1,10,self.m)
    
    self.mu = [5,3,2,1,1]
#        self.sigma = [10]*self.m
    self.sigma = numpy.random.random_integers(1,15,self.m)
    self.randomPriceDist = []
    self.randomPriceCount = []
    for good in xrange(self.m):
        randomPrices = numpy.random.normal(loc=self.mu[good],scale=self.sigma[good],size=10000)
        self.randomPriceDist.append(numpy.histogram(randomPrices,bins=range(0,51),density=True))
    
    randomMargDist = margDistSCPP()
    
    for i in xrange(nAgents):
        
        auciton.arrachAgents(riskAware())
        
    auciton.runAuction()
     
        
        
    