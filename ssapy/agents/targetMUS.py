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
        
class targetMUS8(margDistPredictionAgent):
    """
    A concrete class for targetMUS8
    """
    @staticmethod
    def type():
        return "targetMUS8"
    
    @staticmethod
    def SS(**kwargs):

        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        kwargs['pointPricePrediction'] = pricePrediction.expectedPrices( method   = 'iTsample',
                                                                         nSamples = 8)
        
        return targetMVS.SS(**kwargs)
        
    def printSummary(self, **kwargs):
        
        if 'expectedPrices' not in kwargs:
            kwargs['method']   = 'iTsample'
            kwargs['nSamples'] = 8
            
        super(targetMUS8,self).printSummary(**kwargs)
        
        
class targetMUS64(margDistPredictionAgent):
    @staticmethod
    def type():
        return "targetMUS64"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        tkwargs = dict(kwargs)
        
        tkwargs['pointPricePrediction'] = pricePrediction.expectedPrices(method   = 'iTsample',
                                                                         nSamples = 64)
        
        return targetMVS.SS(**tkwargs)
    
    def printSummary(self, **kwargs):
        tkwargs = dict(kwargs)
        
        if 'expectedPrices' not in tkwargs:
            tkwargs['method']   = 'iTsample'
            tkwargs['nSamples'] = 8
            
        super(targetMUS64,self).printSummary(**tkwargs)
        