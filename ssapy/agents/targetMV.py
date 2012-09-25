"""
this is /auctionSimulator/hw4/targetMV.py

Author: Brandon Mayer
Date: 11/17/2011

Specialized agent class to replicate targetMV from
Yoon and Wellman (2011)
"""
from pointPredictionAgent import *

class targetMV(pointPredictionAgent):
        
    @staticmethod
    def type():
        return "targetMV"
              
    @staticmethod
    def SS(**kwargs):
        """
        Calculate a vector of marginal values given a price
        vector.
        """
        
        pointPricePrediction = kwargs.get('pointPricePrediction')
        if pointPricePrediction == None:
            raise KeyError("targetMV.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMV.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMV - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMV - must specify l (target number of time slots)")
        
        if isinstance(pointPricePrediction, pointSCPP):
            pricePrediction = numpy.asarray(pointPricePrediction.data, dtype = numpy.float)
            
        elif isinstance(pointPricePrediction, numpy.ndarray):
            pricePrediction = pointPricePrediction
            
        else:
            raise ValueError("targetMV - Unknown pointPricePrediction type")
        
                
        # solve acq for optimal bundle
        # size checks of parameters will be done in acq
        [optBundle, optSurplus] = simYW.acqYW(bundles       = bundles,
                                              valuation     = valuation,
                                              l             = l,
                                              priceVector   = pricePrediction)
        
        n_goods = bundles.shape[1]
        bid = numpy.zeros(n_goods,dtype=numpy.float)
        
        for goodIdx, good in enumerate(optBundle):
            if good:
                bid[goodIdx] = simYW.marginalUtility(bundles, pricePrediction, valuation, l, goodIdx)
        
            
        return bid
            