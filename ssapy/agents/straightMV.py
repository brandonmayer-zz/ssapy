"""
this is /auctionSimulator/hw4/straightMV.py

Author: Brandon Mayer
Date: 11/17/2011

Specialized agent class to replicate straightMV from
Yoon and Wellman (2011)
"""
#from auctionSimulator.hw4.agents.pointPredictionAgent import *
from pointPredictionAgent import *

import copy

class straightMV(pointPredictionAgent):
    """
    straightMV bids marginal values for all goods.
    """
    @staticmethod
    def type():
        return "straightMV"
    
    @staticmethod
    def SS(**kwargs):
        """
        Calculate the marginal values of all goods for auction
        given the predicted prices.
        
        NOTE:
            Bid on all available goods, don't solve acq for overall best bundle.
            
        Parameters:
            pointPricePrediction     A point price prediction
            bundles                  The available bundles to bid on
            valuation                A vector of valuations (one valuation per bundle)
            l                        The target number of goods
        """

        pointPricePrediction = kwargs.get('pointPricePrediction')
        if pointPricePrediction == None:
            raise KeyError("straightMV.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("straightMV.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("straightMV - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("straightMV - must specify l (target number of time slots)")
        
        if isinstance(pointPricePrediction, pointSCPP):
            pricePrediction = numpy.asarray(pointPricePrediction.data, dtype = numpy.float)
            
        elif isinstance(pointPricePrediction, numpy.ndarray):
            pricePrediction = pointPricePrediction
            
        else:
            raise ValueError("straightMV - Unknown pointPricePrediction type")
        
        marginalValueBid = []
        for idx in xrange(kwargs['bundles'].shape[1]):
            tempPriceInf = pricePrediction.copy()
            tempPriceInf[idx] = float('inf')
            tempPriceZero = pricePrediction.copy()
            tempPriceZero[idx] = 0 
            
            optBundleInf, predictedSurplusInf = simYW.acqYW(bundles     = bundles,
                                                            valuation   = valuation,
                                                            l           = l,
                                                            priceVector = tempPriceInf)
            
            optBundleZero, predictedSurplusZero = simYW.acqYW(bundles     = bundles,
                                                              valuation   = valuation,
                                                              l           = l, 
                                                              priceVector = tempPriceZero)
                
            #this shouldn't happend but just in case.
            if predictedSurplusZero - predictedSurplusInf < 0:
                marginalValueBid.append(0)
            else:
                marginalValueBid.append(predictedSurplusZero - predictedSurplusInf)
            
        return numpy.atleast_1d(marginalValueBid).astype('float')
        
            