"""
this is /auctionSimulator/hw4/targetPrice.py

Author: Brandon Mayer
Date: 11/17/2011

Specialized agent class to replicate targetPrice from
Yoon and Wellman (2011)
"""

from auctionSimulator.hw4.agents.pointPredictionAgent import *

class targetPrice(pointPredictionAgent):
        
    @staticmethod
    def type():
        return "targetPrice"
    
    @staticmethod
    def bundleBid(**kwargs):
        """
        Given a price prediciton and an optimal bundle,
        place construct a bid vector
        """
        pointPricePrediction = kwargs['pointPricePrediction']
        
        bundle = kwargs['bundle']
        
        numpy.testing.assert_(isinstance(bundle,numpy.ndarray))
        
        #bid the predicted prices for the optimal bundle
        bid = []
        for idx in xrange(bundle.shape[0]):
            if bundle[idx]:
                bid.append(pointPricePrediction[idx])
            else:
                bid.append(0)
                
        return numpy.atleast_1d(bid)
                      
    @staticmethod
    def SS(**kwargs):
            
        numpy.testing.assert_('pointPricePrediction' in kwargs, 
                              msg = "Must specify pointPricePrediciton.")
        
        numpy.testing.assert_('bundles' in kwargs,
                              msg = "Must specify bundles")
        
        numpy.testing.assert_('valuation' in kwargs,
                              msg = "Must specify the valuation of each bundle." )
        
        numpy.testing.assert_('l' in kwargs,
                              msg = "Must specify l, the number of goods.")

        # solve acq for optimal bundle
        # size checks of parameters will be done in acq
        [optBundle, optSurplus] = simYW.acqYW(bundles     = kwargs['bundles'],
                                              valuation   = kwargs['valuation'],
                                              l           = kwargs['l'],
                                              priceVector = kwargs['pointPricePrediction'])
                    
        return targetPrice.bundleBid(pointPricePrediction = kwargs['pointPricePrediction'],
                                     bundle               = optBundle)
        