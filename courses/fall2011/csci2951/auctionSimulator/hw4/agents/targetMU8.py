"""
this is /auctionSimulator/hw4/agents/targetMU8.py

Author:    Brandon A. Mayer
Date:      12/5/2011

Specialized agent to bid by targetMU strategy but sampling from
marginal distributions using the inverse transform method using 8 samples
per marginal distribution
"""

from margDistPredictionAgent import *
from targetMV import *

class targetMU8(margDistPredictionAgent):
    """
    A concrete class for targetMU8
    """
    
    @staticmethod
    def type():
        return "targetMU8"
    
    @staticmethod
    def SS(**kwargs):        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        kwargs['pointPricePrediction'] = pricePrediction.expectedPrices(method   = 'iTsample',
                                                                        nSamples = 8)
        return targetMV.SS(**kwargs)
        
    def printSummary(self, **kwargs):
        if 'expectedPrices' not in kwargs:
            
            kwargs['method']   = 'iTsample'
            kwargs['nSamples'] = 8
            
        super(targetMU8,self).printSummary(**kwargs)