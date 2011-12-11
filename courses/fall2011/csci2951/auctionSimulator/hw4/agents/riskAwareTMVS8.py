"""
this is /auctionSimulator/hw4/agents/riskAware.py

Author:    Brandon A. Mayer
Date:      12/6/2011
"""

from auctionSimulator.hw4.agents.riskAware import *
from auctionSimulator.hw4.agents.targetMVS import *

class riskAwareTMVS8(riskAware):
    @staticmethod
    def type():
        return "riskAwareMUS8"
    
    @staticmethod
    def SS(**kwargs):
        expectedPrices = kwargs['margDistPrediction'].expectedPrices( method   = 'iTsample',
                                                                    nSamples = 8)
        
        upperPartialStd = kwargs['margDistPrediction'].margUps(expectedPrices = expectedPrices)
        
        expectedSurplus = riskAware.surplus(kwargs['bundles'], kwargs['valuation'] , expectedPrices)
        
        #optimalBundle
        optBundle, optups = riskAware.acqMups( bundles         = kwargs['bundles'], 
                                               l               = kwargs['l'],
                                               A               = kwargs['A'],
                                               upperPartialStd = upperPartialStd, 
                                               expectedSurplus = expectedSurplus )
        
        return targetMVS.bundleBid(bundle               = optBundle,
                                   pointPricePrediction = expectedPrices,
                                   valuation            = kwargs['valuation'],
                                   l                    = kwargs['l'])
    def printSummary(self,**kwargs):
        """
        Print a summary of agent state to standard out.
        """
        if 'expectedPrices' not in kwargs:
            expectedPrices = self.pricePrediction.expectedPrices(method   = 'iTsample',
                                                                 nSamples = 8)
            
        super(riskAwareTMVS8,self).printSummary(expectedPrices = expectedPrices)
        