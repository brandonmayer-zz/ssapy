"""
this is /auctionSimulator/hw4/targetMU.py

Author: Brandon Mayer
Date:   11/21/2011

Specialized agent class to replicate targetMU from Yoon and Wellman 2011.
This is just a wrapper around targetMV and accepts a price prediction distribution
and calculates the mean(s) for price prediction
"""
from margDistPredictionAgent import *
from targetMV import *

class targetMU(margDistPredictionAgent):

    @staticmethod       
    def type():
        return "targetMU"
            
    @staticmethod
    def SS(args={}):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        """
        pricePrediction = margDistPredictionAgent.SS(args=args)
                                                     
        expectedPrices = pricePrediction.expectedPrices(args=args)
        
        return targetMV.SS({'pointPricePrediction' : expectedPrices,
                            'bundles'              : args['bundles'],
                            'l'                    : args['l'],
                            'valuation'            : args['valuation']})        