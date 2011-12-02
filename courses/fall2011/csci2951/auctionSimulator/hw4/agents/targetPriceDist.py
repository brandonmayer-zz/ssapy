"""
this is /auctionSimulator/hw4/agents/targetPriceDist.py

Author: Brandon Mayer
Date:   11/21/2011

Extends target price to bidding the expected values for goods
given a distirubtion price prediction, not a point price prediciton.
"""

from margDistPredictionAgent import *

class targetPriceDist(margDistPredictionAgent):
    
    @staticmethod
    def type():
        return "targetPriceDist"
    
    @staticmethod
    def SS(args={}):
        """
        Calculate and bid the expected value of marginal distributions
        """
        pricePrediction = margDistPredictionAgent.SS(args=args)
        
        method = None
        if 'method' in args:
            method = args['method']
        
        if not method or method == 'average':
            return pricePrediction.expectedPrices()
        
        if method == 'iTsample':
            assert 'nSamples' in args,\
                "Must specify the number of Samples."
            samples = numpy.atleast_2d(pricePrediction.iTsample(args['nSamples']))
            
            return numpy.mean(samples,0)
            