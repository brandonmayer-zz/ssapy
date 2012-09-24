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
    def bundleBid(**kwargs):
        pricePrediction = kwargs['pointPricePrediction']
        
        bundle = kwargs['bundle']
        
        m = int(bundle.shape[0])
        
        allBundles = simYW.allBundles(m)
        
        marginalValueBid = []
        for idx in xrange(m):
            if bundle[idx] == 1:
                tempPriceInf = numpy.array(pricePrediction).astype(numpy.float)
                tempPriceInf[idx] = float('inf')
                tempPriceZero = numpy.array(pricePrediction).astype(numpy.float)
                tempPriceZero[idx] = 0
                
#                [optIdxInf, optBundleInf, predictedSurplusInf] = self.acq(tempPriceInf,validate=False)
#                [optIdxZero, optBundleZero, predictedSurplusZero] = self.acq(tempPriceZero,validate=False)

                optBundleInf, predictedSurplusInf = simYW.acqYW(bundles     = allBundles,
                                                                valuation   = kwargs['valuation'],
                                                                l           = kwargs['l'],
                                                                priceVector = tempPriceInf)
                
                optBundleZero, predictedSurplusZero = simYW.acqYW(bundles     = allBundles,
                                                                  valuation   = kwargs['valuation'],
                                                                  l           = kwargs['l'],
                                                                  priceVector = tempPriceZero)
                
                # this shouldn't happen but just in case       
                if predictedSurplusZero - predictedSurplusInf < 0:
                    marginalValueBid.append(0)
                else:
                    marginalValueBid.append(predictedSurplusZero-predictedSurplusInf)
                    
            else:
                marginalValueBid.append(0)
        
        return numpy.atleast_1d(marginalValueBid).astype('float')
        
        
        
        
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
            