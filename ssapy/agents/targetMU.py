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
    def SS(**kwargs):
        """
        Calculate the expected marginal price vector given marginal distributions
        over good prices. 
        """
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
                                                     
        expectedPrices = pricePrediction.expectedPrices(**kwargs)
           
        return targetMV.SS( pointPricePrediction = expectedPrices,
                            bundles              = kwargs['bundles'],
                            valuation            = kwargs['valuation'],
                            l                    = kwargs['l'])     
        
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