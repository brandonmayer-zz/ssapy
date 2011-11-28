"""
This is /auctionSimulator/hw4/agents/pointPredictionAgent.py

Author:        Brandon A. Mayer
Date:          11/27/2011

A base class for agents who utilize a point price prediction.
"""

from pricePredictionAgent import *
from auctionSimulator.hw4.pricePrediction.pointSCPP import *

class pointPredictionAgent(pricePredictionAgent):
    def __init__(self,
                 m = 5,
                 v = None,
                 l = None,
                 vmin = 0,
                 vmax = 50,
                 pointPricePrediction = None,
                 name = "Anonymous"):
        
        super(pointPredictionAgent,self).__init__(m=m,
                                                  v=v,
                                                  l=l,
                                                  vmin=vmin,
                                                  vmax=vmax,
                                                  name=name,
                                                  pricePrediction=pointPricePrediction)
        
    @staticmethod
    def predictionType():
        return "pointSCPP"
    
    @staticmethod
    def type():
        return "pointPredictionAgent"
    
    def printSummary(self,args={}):
        """
        Print a summary of agent state to standard out.
        """
        super(pricePredictionAgent,self).printSummary()
        
        if self.pricePrediction != None:
            print 'Price Prediction = {0}'.format(self.pricePrediction.data)
            print 'Bundle | Valuation | Cost | Surplus'
            
            bundles = self.allBundles(self.m)
            
            valuation = self.valuation(bundles = bundles, 
                                       v = self.v, 
                                       l = self.l)
            
            cost = self.cost(bundles=bundles, 
                             price=self.pricePrediction.data)
            
            surplus = self.surplus(bundles=bundles, 
                                   valuation=valuation, 
                                   priceVector=self.pricePrediction.data)
            
            for i in xrange(bundles.shape[0]):
                print "{0}  {1:^5} {2:^5} {3:^5}".format( bundles[i].astype(numpy.int),
                                                          valuation[i],
                                                          cost[i],
                                                          surplus[i])
                
            [optBundle, optSurplus] = self.acq(priceVector=self.pricePrediction.data)
            
            print "Optimal Bundle (acq):      {0}".format(optBundle.astype(numpy.int))
            print "Surplus of Optimal Bundle: {0}".format(optSurplus)
            print "Bid:                       {0}".format(self.bid())
        else:
            print 'No Point Price Prediction loaded...'
            
            
        
        
        
    