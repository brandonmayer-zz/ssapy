"""
This is /auctionSimulator/hw4/agents/pointPredictionAgent.py

Author:        Brandon A. Mayer
Date:          11/27/2011

A base class for agents who utilize a distribution price prediction.
"""
from pricePredicitonAgent import *
from auctionSimulator.hw4.pricePrediction.margDistSCPP import *

class margDistPredictionAgent(pricePredictionAgent):
    def __init__(self,
                 m = 5,
                 v = None,
                 l = None,
                 vmin = 0,
                 vmax = 50,
                 margDistPricePrediction = None,
                 name = "Anonymous"):
        super(margDistPredictionAgent,self).__init__(m    = m,
                                                     v    = v,
                                                     l    = l,
                                                     vmin = vmin,
                                                     vmax = vmax,
                                                     name = name,
                                                     pricePrediction = margDistPricePrediction)
            
    @staticmethod
    def predictionType():
        return "margDistSCPP"
    
    @staticmethod
    def type():
        return "margDistPredictionAgent"
    
    def printSummary(self,args={}):
        """
        Print a summary of the agent's state to standard output.
        """
        super(margDistPredictionAgent,self).printSummary()
        
        assert 'margDistPricePrediction' in args or self.pricePrediction != None,\
            "Must specify a price prediction"
            
        pricePrediction = None
        
        if 'margDistPricePrediction' in args:
            
            assert isinstance(args['margDistPricePrediction'],margDistSCPP) or\
                isinstance(args['margDistPricePrediction'], tuple),\
                    "args['margDistPricePrediction'] must be a margDistSCPP or numpy.ndarray"
                    
            if isinstance(args['margDistPricePrediction'], margDistSCPP):
                
                pricePredicton = args['margDistPricePrediciton']
                
            elif isinstance(args['margDistPricePrediction'], tuple):
                
                pricePrediction = margDistSCPP(args['margDistPricePrediction'])
                
            else:
                print 'Should never get here'
                raise AssertionError
                
        else:
            pricePrediction = self.pricePrediction
            
        bundles = self.allBundles(self.m)
        
        valuation = self.valuation(bundles = bundles,
                                   v       = self.v,
                                   l       = self.l )
        
        expectePriceVector = pricePrediction.expectedPrices
        
        print 'Expected Price Vector = {0}'
        
                                   
                
                
                
                
                