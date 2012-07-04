from auctionSimulator.hw4.auctions.simultaneousAuction import *
from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.straightMU import *
from auctionSimulator.hw4.agents.targetPriceDist import *

import unittest
import numpy
import tempfile

class testAuctions(unittest.TestCase):
    """
    Test cases for auctions
    """
    
    def test_simultaneousAuction(self):
        """
        test the simultaneous auction
        """
        self.m = 5
        self.randomPriceVector = numpy.random.random_integers(1,10,self.m)
        
        self.mu = [20,15,10,8,5]
#        self.sigma = [10]*self.m
        self.sigma = numpy.random.random_integers(1,15,self.m)
        self.randomPriceDist = []
        self.randomPriceCount = []
        for good in xrange(self.m):
            randomPrices = numpy.random.normal(loc=self.mu[good],scale=self.sigma[good],size=10000)
            self.randomPriceDist.append(numpy.histogram(randomPrices,bins=range(0,51),density=True))
            
        randomMargDist = margDistSCPP(self.randomPriceDist)
        
        #all agents are given the same valuations and lambda in order to 
        #directly observe differences in bidding
        riskAware1 = riskAware(margDistPricePrediction = randomMargDist)
        
        riskAware2 = riskAware(margDistPricePrediction = randomMargDist,
                               v = riskAware1.v,
                               l = riskAware1.l)
        
        riskAware2.A = 5
        
        riskAware3 = riskAware(margDistPricePrediction = randomMargDist,
                               v = riskAware1.v,
                               l = riskAware1.l)
        
        riskAware3.A = 20
        
        straightMU1 = straightMU8(margDistPricePrediction = randomMargDist, 
                                                        m = riskAware1.m, 
                                                        l = riskAware1.l, 
                                                        v = riskAware1.v)
        
        targetPriceDist1 = targetPrice8(margDistPricePrediction = randomMargDist,
                                                                 m = riskAware1.m,
                                                                 l = riskAware1.l,
                                                                 v = riskAware1.v)
        
        agentList = [riskAware1, riskAware2, riskAware3,straightMU1, targetPriceDist1]
        
        [agent.printSummary() for agent in agentList]
        
        auction = simultaneousAuction(agentList = agentList)
        
        print auction.agentList
        
        auction.removeAgent(riskAware3.id)
        
        print auction.agentList
        
        winners, finalPrices, winningBids = auction.runAuction()
        
        print 'Winners = {0}'.format(winners)
        
        print 'Final Prices = {0}'.format(finalPrices)
        
        print 'winningBids = {0}'.format(winningBids)
        
        
        auction.notifyAgents()
        
        
        
if __name__ == "__main__":
    unittest.main()