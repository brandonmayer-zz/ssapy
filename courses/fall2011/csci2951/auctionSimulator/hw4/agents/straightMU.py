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