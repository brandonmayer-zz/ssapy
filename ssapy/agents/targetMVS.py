"""
this is /auctionSimulator/hw4/targetMVS.py

Author: Brandon Mayer
Date: 11/18/2011

Specialized agent class to replicate targetMV* (hence MVS stands for MV Star) from
Yoon and Wellman (2011)
"""
#from targetMV import *
from pointPredictionAgent import *

class targetMVS(pointPredictionAgent):
    """
    targetMVS assumes that "all goods outside the taget bundle
    are unavailable" (Yoon & Wellman 2011)
    """
    
    @staticmethod
    def type():
        return "targetMVS"
        
    @staticmethod
    def SS(**kwargs):
        """
        Calculate a vector of marginal values given a single bundle
        and price vector assuming the price off all goods not in the bundle
        are infinite (unobtainable).
        """
        
        pointPricePrediction = kwargs.get('pointPricePrediction')
        if pointPricePrediction == None:
            raise KeyError("targetMVS.SS(...) - must specify pricePrediction")
        
        bundles = kwargs.get('bundles')
        if bundles == None:
            raise KeyError("targetMVS.SS(...) - must specify bundles")
                
        valuation = kwargs.get('valuation')
        if valuation == None:
            raise KeyError("targetMVS - must specify valuation")
        
        l = kwargs.get('l')
        if l == None:
            raise KeyError("targetMVS - must specify l (target number of time slots)")
        
        if isinstance(pointPricePrediction, pointSCPP):
            pricePrediction = numpy.asarray(pointPricePrediction.data, dtype = numpy.float)
            
        elif isinstance(pointPricePrediction, numpy.ndarray):
            pricePrediction = pointPricePrediction
            
        else:
            raise ValueError("targetMVS - Unknown pointPricePrediction type")
               
#        [optBundleIdx, optBundle, optSurplus] = self.acq(pricePrediction,validate=False)
    
        optBundle, optSurplus = targetMVS.acqYW(bundles      = bundles,
                                                valuation    = valuation,
                                                l            = l,
                                                priceVector  = pricePrediction)
        
        
        
        pricePredictionCopy = pricePrediction.copy()
        pricePredictionCopy[~optBundle] = numpy.float('inf')
        
        n_goods = bundles.shape[1]
        bid = numpy.zeros(n_goods,dtype=numpy.float)
        
        for goodIdx, good in enumerate(optBundle):
            if good:
                bid[goodIdx] = simYW.marginalUtility(bundles, pricePredictionCopy, valuation, l, goodIdx)
                
        return bid        
            