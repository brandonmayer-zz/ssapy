"""
this is /auctionSimulator/hw4/agents/targetPriceDist.py

Author: Brandon Mayer
Date:   11/21/2011

Extends target price to bidding the expected values for goods
given a distirubtion price prediction, not a point price prediciton.
"""

from margDistPredictionAgent import *
from targetPrice import *

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
        
        expectedPrices = kwargs.get('expectedPrices',
                    pricePrediction.expectedPrices(method = 'average'))
        
        bundles = kwargs.get('bundles', simYW.allBundles(pricePrediction.m))
        
        return targetPrice.SS(bundles               = bundles,
                              valuation             = kwargs['valuation'],
                              l                     = kwargs['l'],
                              pointPricePrediction  = expectedPrices)
            
class targetPrice8(margDistPredictionAgent):
    @staticmethod
    def type():
        return "targetPrice8"
    
    @staticmethod
    def SS(**kwargs):
        """
        Interface for bid
        """
        pricePrediction = margDistPredictionAgent.SS(**kwargs)
        
        bundles = kwargs.get('bundles',simYW.allBundles(pricePrediction.m))
        
        expectedPrices = kwargs.get('expectedPrices',
            pricePrediction.expectedPrices(method   = 'iTsample', nSamples = 8))

        return targetPrice.SS(bundles              = bundles,
                              valuation            = kwargs['valuation'],
                              l                    = kwargs['l'],
                              pointPricePrediction = expectedPrices)       
        
class targetPrice64(margDistPredictionAgent):
    @staticmethod
    def type():
        return "targetPrice64"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = margDistPrediction.SS(**kwargs)
        
        bundles = kwargs.get('bundles', simYW.allBundles(pricePrediction.m))
        
        expectedPrices = kwargs.get('expectedPrices',
            pricePrediction.expectedPrices(method   = 'iTsample', nSamples = 64))
        
        return targetPrice.SS(bundles              = bundles,
                              valuation            = kwargs['valuation'],
                              l                    = kwargs['l'],
                              pointPricePrediction = expectedPrices)
        
class targetPrice256(margDistPredictionAgent):
    @staticmethod
    def type():
        return "targetPrice256"
    
    @staticmethod
    def SS(**kwargs):
        pricePrediction = margDistPrediction.SS(**kwargs)
        
        bundles = kwargs.get('bundles', simYW.allBundles(pricePrediction.m))
        
        expectedPrices = kwargs.get('expectedPrices',
            pricePrediction.expectedPrices(method   = 'iTsample', nSamples = 256))
        
        return targetPrice.SS(bundles              = bundles,
                              valuation            = kwargs['valuation'],
                              l                    = kwargs['l'],
                              pointPricePrediction = expectedPrices)