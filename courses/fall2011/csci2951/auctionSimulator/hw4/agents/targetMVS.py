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
    def bundleBid(args={}):
        pricePrediction = args['pointPricePrediction']
        
        bundle = args['bundle']
        
        valuation = args['valuation']
        
        l = args['l']
        
        # set the price of all goods not in the optimal bundle to infinity
        # deep copy price to preserve original price vector
        pricePredictionInf = numpy.array(pricePrediction).astype(numpy.float)
        pricePredictionInf[ (numpy.atleast_1d(bundle) == 0) ] = float('inf')
        
        m = int(bundle.shape[0])
        
        allBundles = simYW.allBundles(m)
        
        marginalValueBid = []
        for idx in xrange(m):
            if bundle[idx] == 1:
                tempPriceInf = pricePredictionInf.astype(numpy.float)
                tempPriceInf[idx] = float('inf')
                tempPriceZero = pricePredictionInf
                tempPriceZero[idx] = 0
                
                [optBundleInf, predictedSurplusInf]   = targetMVS.acqYW(bundles     = allBundles,
                                                                        valuation   = valuation,
                                                                        l           = l,
                                                                        priceVector = tempPriceInf)
                
                [optBundleZero, predictedSurplusZero] = targetMVS.acqYW(bundles     = allBundles,
                                                                        valuation   = valuation,
                                                                        l           = l,
                                                                        priceVector = tempPriceZero)
                #this shouldn't happend but just in case.
                if predictedSurplusZero - predictedSurplusInf < 0:
                    print '----WARNING----'
                    print 'targetMVS.SS() predictedSurplusZero - predictedSurplusInf < 0'
                    marginalValueBid.append(0)
                else:
                    marginalValueBid.append(predictedSurplusZero - predictedSurplusInf)
            else:
                marginalValueBid.append(0)
                
        return numpy.atleast_1d(marginalValueBid).astype('float')
    
    @staticmethod
    def SS(args = {}):
        """
        Calculate a vector of marginal values given a single bundle
        and price vector assuming the price off all goods not in the bundle
        are infinite (unobtainable).
        """
        
        assert 'pointPricePrediction' in args,\
            "Must specify pointPricePrediction in args parameter."
            
        assert isinstance(args['pointPricePrediction'],pointSCPP) or\
                isinstance(args['pointPricePrediction'], numpy.ndarray),\
               "args['pointPricePrediction'] must be either a pointSCPP or numpy.ndarray"
            
        assert 'bundles' in args,\
            "Must specify bundles in args parameter."
            
        assert 'valuation' in args,\
            "Must specify the valuation of each bundle in the args parameter."
            
        assert 'l' in args,\
            "Must specify l, the target number of goods in args parameter."
            
        if isinstance(args['pointPricePrediction'], pointSCPP):
                        
            pricePrediction = args['pointPricePrediction'].data
            
        elif isinstance(args['pointPricePrediction'],numpy.ndarray):
            
            pricePrediction = numpy.atleast_1d(args['pointPricePrediction'])
            
        else:
            # this should never happen
            pricePrediction = None
            raise AssertionError
               
#        [optBundleIdx, optBundle, optSurplus] = self.acq(pricePrediction,validate=False)
    
        optBundle,optSurplus = targetMVS.acqYW(bundles      = args['bundles'],
                                               valuation    = args['valuation'],
                                               l            = args['l'],
                                               priceVector  = pricePrediction)
        
        
        
                       
        return targetMVS.bundleBid({ 'pointPricePrediction' : pricePrediction,
                                     'bundle'               : optBundle,
                                     'valuation'            : args['valuation'],
                                     'l'                    : args['l'] })
        
            
        
            