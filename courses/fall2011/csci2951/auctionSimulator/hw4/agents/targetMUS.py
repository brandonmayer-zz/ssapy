"""
this is /auctionSimulator/hw4/targetMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate targetMUS from Yoon and Wellman 2011.
This is just a wrapper around targetMVS and accepts a price prediction distribution
and calculates the mean(s) for price prediction
"""
from margDistPredictionAgent import *
from targetMVS import *

class targetMUS(margDistPredictionAgent):

    @staticmethod        
    def type():
        return "targetMUS"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        
        targetMUS assumes that "all goods outside the taget bundle
        are unavailable" (Yoon & Wellman 2011)
        """
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
                                                     
        expectedPrices = pricePrediction.expectedPrices(**kwargs)
        
        return targetMVS.SS( pointPricePrediction = expectedPrices,
                             bundles              = kwargs['bundles'],
                             l                    = kwargs['l'],
                             valuation            = kwargs['valuation'])