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
    def bundleBid(**kwargs):
        pricePrediction = kwargs['pointPricePrediction']
        
        bundle = numpy.atleast_1d(kwargs['bundle'])
                                  
        valuation = kwargs['valuation']
        
        l = kwargs['l']
        
        pricePrediction = kwargs.get('pointPricePrediction')
        
        
        # set the price of all goods not in the optimal bundle to infinity
        # deep copy price to preserve original price vector
        pricePredictionInf = numpy.asarray(pricePrediction, dtype = numpy.float).copy()
        pricePredictionInf[ (numpy.atleast_1d(bundle) == 0) ] = float('inf')
        
        m = int(bundle.shape[0])
        
        allBundles = simYW.allBundles(m)
        
        marginalValueBid = []
        for idx in xrange(m):
            if bundle[idx] == 1:
                tempPriceInf = pricePredictionInf.copy()
                tempPriceInf[idx] = float('inf')
                tempPriceZero = pricePredictionInf.copy()
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
    def SS(**kwargs):
        """
        Calculate a vector of marginal values given a single bundle
        and price vector assuming the price off all goods not in the bundle
        are infinite (unobtainable).
        """
        
        numpy.testing.assert_('bundles' in kwargs,
                              msg = "Must provide bundles argument")
        
        numpy.testing.assert_('valuation' in kwargs,
                              msg = "Must provide valuation argument")
        
        numpy.testing.assert_('l' in kwargs,
                              msg = "Must provide l, target number of goods argument")
        
            
        assert isinstance(kwargs['pointPricePrediction'],pointSCPP) or\
                isinstance(kwargs['pointPricePrediction'], numpy.ndarray),\
               "kwargs['pointPricePrediction'] must be either a pointSCPP or numpy.ndarray"
            
            
        if isinstance(kwargs['pointPricePrediction'], pointSCPP):
                        
            pricePrediction = kwargs['pointPricePrediction'].data
            
        elif isinstance(kwargs['pointPricePrediction'],numpy.ndarray):
            
            pricePrediction = numpy.atleast_1d(kwargs['pointPricePrediction'])
            
        else:
            # this should never happen
            pricePrediction = None
            raise AssertionError
               
#        [optBundleIdx, optBundle, optSurplus] = self.acq(pricePrediction,validate=False)
    
        optBundle,optSurplus = targetMVS.acqYW(bundles      = kwargs['bundles'],
                                               valuation    = kwargs['valuation'],
                                               l            = kwargs['l'],
                                               priceVector  = pricePrediction)
        
        
        
                       
        return targetMVS.bundleBid(pointPricePrediction = pricePrediction,
                                   bundle               = optBundle,
                                   valuation            = kwargs['valuation'],
                                   l                    = kwargs['l'] )
        
            
        
            