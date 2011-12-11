"""
this is /auctionSimulator/hw4/agents/straightMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate straightMU from Yoon and Wellman 2011.
This is just a wrapper around targetMV and accepts a price prediction distribution
and calculates the mean(s) for price prediction
"""
from margDistPredictionAgent import *
from straightMV import *

class straightMU(margDistPredictionAgent):
       
    @staticmethod
    def type():
        return "straightMU"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        
        We consider in the average, the price associated with a bin to be the
        bins center. The average is then calculated as summing the product 
        of the bin centers multiplied by the bin probability.
        """
        #check validity of args
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        #AGENT SPECIFIC LOGIC
        expectedPrices = pricePrediction.expectedPrices(**kwargs)

        return straightMV.SS(pointPricePrediction = expectedPrices,
                             bundles              = kwargs['bundles'],
                             l                    = kwargs['l'],
                             valuation            = kwargs['valuation'])