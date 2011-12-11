"""
this is /auctionSimulator/hw4/agents/riskAware.py

Author:    Brandon A. Mayer
Date:      12/6/2011
"""

from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.targetPrice import *
    
class riskAwareTP8(riskAware):
    
    @staticmethod        
    def type():
        return "riskAwareTP8"
        
    @staticmethod
    def SS(**kwargs):
        expectedPrices = kwargs['margDistPrediction'].expectedPrices( method   = 'iTsample',
                                                                      nSamples = 8)
        expectedSurplus = riskAware.surplus(kwargs['bundles'], kwargs['valuation'], expectedPrices)
        
        upperPartialStd = kwargs['margDistPrediction'].margUps(expectedPrices = expectedPrices)
        
        #optimalBundle
        optBundle, optups = riskAware.acqMups( bundles         = kwargs['bundles'], 
                                               l               = kwargs['l'],
                                               A               = kwargs['A'],
                                               upperPartialStd = upperPartialStd, 
                                               expectedSurplus = expectedSurplus )
        
        return targetPrice.bundleBid(pointPricePrediction = expectedPrices,
                                     bundle               = optBundle)
        
        
    def printSummary(self,**kwargs):
        """
        Print a summary of agent state to standard out.
        """
        if 'expectedPrices' not in kwargs:
            expectedPrices = self.pricePrediction.expectedPrices(method   = 'iTsample',
                                                                 nSamples = 8)
            
        super(riskAwareTP8,self).printSummary(expectedPrices = expectedPrices)
        
        
        
        
        
        
                                                            
                                                                    
        
    
    