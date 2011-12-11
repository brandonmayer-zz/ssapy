"""
this is /auctionSimulator/hw4/agents/targetPriceDist.py

Author: Brandon Mayer
Date:   11/21/2011

Extends target price to bidding the expected values for goods
given a distirubtion price prediction, not a point price prediciton.
"""

from margDistPredictionAgent import *
from auctionSimulator.hw4.agents.targetPrice import *

class targetPriceDist(margDistPredictionAgent):
    
    @staticmethod
    def type():
        return "targetPriceDist"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate and bid the expected value of marginal distributions
        """
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        


        return targetPrice.SS(bundles               = kwargs['bundles'],
                              valuation             = kwargs['valuation'],
                              l                     = kwargs['l'],
                              pointPricePrediction  = pricePrediction.expectedPrices())
            
        

            