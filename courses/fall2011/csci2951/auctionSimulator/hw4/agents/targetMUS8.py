"""
this is /auctionSimulator/hw4/agents/targetMUS8.py

Author:    Brandon A. Mayer
Date:      12/5/2011

Specialized agent to bid by targetMUS strategy but sampling from
marginal distributions using the inverse transform method using 8 samples
per marginal distribution
"""

from auctionSimulator.hw4.agents.targetMVS import *
from margDistPredictionAgent import *

class targetMUS8(margDistPredictionAgent):
    """
    A concrete class for targetMUS8
    """
    @staticmethod
    def type():
        return "targetMUS8"
    
    @staticmethod
    def SS(**kwargs):

        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        kwargs['pointPricePrediction'] = pricePrediction.expectedPrices( method   = 'iTsample',
                                                                         nSamples = 8)
        
        return targetMVS.SS(**kwargs)
        
    def printSummary(self, **kwargs):
        
        if 'expectedPrices' not in kwargs:
            kwargs['method']   = 'iTsample'
            kwargs['nSamples'] = 8
            
        super(targetMUS8,self).printSummary(**kwargs)