"""
this is /auctionSimulator/hw4/targetPrice.py

Author: Brandon Mayer
Date: 11/17/2011

Specialized agent class to replicate targetPrice from
Yoon and Wellman (2011)
"""

from auctionSimulator.hw4.agents.pointPredictionAgent import *

class targetPrice(pointPredictionAgent):
#    def __init__(self,
#                 m = 5,
#                 v = None,
#                 l = None,
#                 vmin = 0,
#                 vmax = 50,
#                 pointPricePrediction = None,
#                 name = "Anonymous"):
#        super(targetPrice,self).__init__(m=m,
#                                         v=v,
#                                         l=l,
#                                         vmin=vmin,
#                                         vmax=vmax,
#                                         pointPricePrediction=pointPricePrediction,
#                                         name=name)
        
    @staticmethod
    def type():
        return "targetPrice"
    
    @staticmethod
    def bundleBid(args={}):
        """
        Given a price prediciton and an optimal bundle,
        place construct a bid vector
        """
        pointPricePrediction = args['pointPricePrediction']
        
        bundle = args['bundle']
        
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
    def SS(args={}):
        assert 'pointPricePrediction' in args,\
            "Must specify pointPricePrediciton in args parameter."
            
        assert 'bundles' in args,\
            "Must specify bundles in args parameter."
            
        assert 'valuation' in args,\
            "Must specify the valuation of each bundle in args parameter."
            
        assert 'l' in args,\
            "Must specify l, the target number of goods in args parameter."

        # solve acq for optimal bundle
        # size checks of parameters will be done in acq
        [optBundle, optSurplus] = simYW.acqYW(bundles=args['bundles'],
                                              valuation=args['valuation'],
                                              l=args['l'],
                                              priceVector=args['pointPricePrediction'])
                    
        return targetPrice.bundleBid({'pointPricePrediction' : args['pointPricePrediction'],
                                      'bundle'               : optBundle})
        