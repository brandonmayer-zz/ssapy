"""
this is /auctionSimulator/hw4/agents/straightMU8.py

Author:    Brandon A. Mayer
Date:      12/5/2011

Specialized agent to bid by straightMU strategy but sampling from
marginal distributions using the inverse transform method using 8 samples
per marginal distribution
"""

from margDistPredictionAgent import *
from auctionSimulator.hw4.agents.straightMV import *

class straightMU8(margDistPredictionAgent):
    """
    A concrete class for straightMU8
    """
    @staticmethod
    def type():
        return "straightMU8"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected using inverse sampling method and 8 samples
        Then bid via straightMV with the resulting expected prices
        """
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        expectedPrices = pricePrediction.expectedPrices( method   = 'iTsample',
                                                         nSamples = 8)
        
        return straightMV.SS( pointPricePrediction = expectedPrices,
                              bundles              = kwargs['bundles'],
                              valuation            = kwargs['valuation'],
                              l                    = kwargs['l'])
        
        
        
    def printSummary(self,**kwargs):
        
        if 'expectedPrices' not in kwargs:
            
            kwargs['method']   = 'iTsample'
            kwargs['nSamples'] = 8
            
        super(straightMU8,self).printSummary(**kwargs)
                                              