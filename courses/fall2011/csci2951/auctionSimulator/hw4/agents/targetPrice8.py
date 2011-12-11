"""
this is /auctionSimulator/hw4/agents/targetPriceDist.py

Author: Brandon Mayer
Date:   12/6/2011

Extends target price to bidding the expected values for goods
using 8 samples from each marginal distribution
"""
from auctionSimulator.hw4.agents.targetPrice import *
from auctionSimulator.hw4.agents.targetPriceDist import *

class targetPrice8(targetPriceDist):
    @staticmethod
    def type():
        return "targetPrice8"
    
    @staticmethod
    def SS(**kwargs):
        """
        Interface for bid
        """
        
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        expectedPrices = pricePrediction.expectedPrices(method   = 'iTsample',
                                                        nSamples = 8)

        return targetPrice.SS(bundles              = kwargs['bundles'],
                              valuation            = kwargs['valuation'],
                              l                    = kwargs['l'],
                              pointPricePrediction = expectedPrices)
        
        