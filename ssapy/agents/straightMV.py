"""
this is /auctionSimulator/hw4/straightMV.py

Author: Brandon Mayer
Date: 11/17/2011

Specialized agent class to replicate straightMV from
Yoon and Wellman (2011)
"""
from ssapy.agents.agentBase import agentBase
import ssapy

import numpy

def straightMV(**kwargs):
    pricePrediction = kwargs.get('pricePrediction')
    
    if pricePrediction == None:
        raise KeyError("Must specify pricePrediction")
    
    pricePrediction = numpy.atleast_1d(pricePrediction)
    
    bundles = kwargs.get('bundles')
    if bundles == None:
        raise KeyError("straightMV.SS(...) - must specify bundles")
                    
    valuation = kwargs.get('valuation')
    if valuation == None:
        raise KeyError("straightMV - must specify valuation")
    
    
    
    n_goods = bundles.shape[1]
    marginalValueBid = numpy.zeros(n_goods,dtype=numpy.float64)
    for goodIdx in xrange(n_goods):
        marginalValueBid[goodIdx] = \
                ssapy.marginalUtility(bundles, pricePrediction,
                                      valuation, goodIdx) 
    return marginalValueBid
         
    
#class straightMV(agentBase):
#    """
#    straightMV bids marginal values for all goods.
#    """
#    @staticmethod
#    def type():
#        return "straightMV"
#    
#    @staticmethod
#    def SS(**kwargs):
#        """
#        Calculate the marginal values of all goods for auction
#        given the predicted prices.
#        
#        NOTE:
#            Bid on all available goods, don't solve acq for overall best bundle.
#            
#        Parameters:
#            pointPricePrediction     A point price prediction
#            bundles                  The available bundles to bid on
#            valuation                A vector of valuations (one valuation per bundle)
#            l                        The target number of goods
#        """
#
#        pointPricePrediction = kwargs.get('pointPricePrediction')
#        
#        if pointPricePrediction == None:
#            raise KeyError("straightMV.SS(...) - must specify pricePrediction")
#        
#        pointPricePrediction = numpy.atleast_1d(pointPricePrediction)
#        
#        bundles = kwargs.get('bundles')
#        if bundles == None:
#            raise KeyError("straightMV.SS(...) - must specify bundles")
#                
#        valuation = kwargs.get('valuation')
#        if valuation == None:
#            raise KeyError("straightMV - must specify valuation")
#        
#             
#        n_goods = bundles.shape[1]
#        marginalValueBid = numpy.zeros(n_goods,dtype=numpy.float64)
#        for goodIdx in xrange(n_goods):
#            marginalValueBid[goodIdx] = \
#                    ssapy.marginalUtility(bundles, pointPricePrediction,
#                                          valuation, goodIdx) 
#                                          
#
#        return marginalValueBid
        
            