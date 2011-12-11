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
        
        assert 'pointPricePrediction' in kwargs,\
            "Must specify pointPricePrediciton in kwargs parameter."
            
        assert isinstance(kwargs['pointPricePrediction'],pointSCPP) or\
                isinstance(kwargs['pointPricePrediction'], numpy.ndarray),\
               "kwargs['pointPricePrediction'] must be either a pointSCPP or numpy.ndarray"
            
        assert 'bundles' in kwargs,\
            "Must specify bundles in kwargs parameter."
            
        assert 'valuation' in kwargs,\
            "Must specify the valuation of each bundle in kwargs parameter."
            
        assert 'l' in kwargs,\
            "Must specify l, the target number of goods in kwargs parameter."
        
        pricePrediction = None

        if isinstance(kwargs['pointPricePrediction'], pointSCPP):
                        
            pricePrediction = kwargs['pointPricePrediction'].data
            
        elif isinstance(kwargs['pointPricePrediction'],numpy.ndarray):
            
            pricePrediction = numpy.atleast_1d(kwargs['pointPricePrediction'])
            
        else:
            # this should never happen
            print 'Even HAL made mistakes...'
            raise AssertionError
        
                
        # solve acq for optimal bundle
        # size checks of parameters will be done in acq
        [optBundle, optSurplus] = simYW.acqYW(bundles       = kwargs['bundles'],
                                              valuation     = kwargs['valuation'],
                                              l             = kwargs['l'],
                                              priceVector   = pricePrediction)
            
        return targetMV.bundleBid(pointPricePrediction      = pricePrediction,
                                  bundle                    = numpy.atleast_1d(optBundle),
                                  valuation                 = kwargs['valuation'],
                                  l                         = kwargs['l'])
          