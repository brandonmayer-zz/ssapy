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
    def bundleBid(args={}):
        pricePrediction = args['pointPricePrediction']
        
        bundle = args['bundle']
        
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
                                                                valuation   = args['valuation'],
                                                                l           = args['l'],
                                                                priceVector = tempPriceInf)
                
                optBundleZero, predictedSurplusZero = simYW.acqYW(bundles     = allBundles,
                                                                  valuation   = args['valuation'],
                                                                  l           = args['l'],
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
    def SS(args={}):
        """
        Calculate a vector of marginal values given a price
        vector.
        """
        assert 'pointPricePrediction' in args,\
            "Must specify pointPricePrediciton in args parameter."
            
        assert isinstance(args['pointPricePrediction'],pointSCPP) or\
                isinstance(args['pointPricePrediction'], numpy.ndarray),\
               "args['pointPricePrediction'] must be either a pointSCPP or numpy.ndarray"
            
        assert 'bundles' in args,\
            "Must specify bundles in args parameter."
            
        assert 'valuation' in args,\
            "Must specify the valuation of each bundle in args parameter."
            
        assert 'l' in args,\
            "Must specify l, the target number of goods in args parameter."
        
        pricePrediction = None

        if isinstance(args['pointPricePrediction'], pointSCPP):
                        
            pricePrediction = args['pointPricePrediction'].data
            
        elif isinstance(args['pointPricePrediction'],numpy.ndarray):
            
            pricePrediction = numpy.atleast_1d(args['pointPricePrediction'])
            
        else:
            # this should never happen
            print 'Even HAL made mistakes...'
            raise AssertionError
        
                
        # solve acq for optimal bundle
        # size checks of parameters will be done in acq
        [optBundle, optSurplus] = simYW.acqYW(bundles       = args['bundles'],
                                              valuation     = args['valuation'],
                                              l             = args['l'],
                                              priceVector   = pricePrediction)
            
        return targetMV.bundleBid({'pointPricePrediction' : pricePrediction,
                                   'bundle'               : numpy.atleast_1d(optBundle),
                                   'valuation'            : args['valuation'],
                                   'l'                    : args['l']})
          