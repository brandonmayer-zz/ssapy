"""
this is /auctionSimulator/hw4/straightMV.py

Author: Brandon Mayer
Date: 11/17/2011

Specialized agent class to replicate straightMV from
Yoon and Wellman (2011)
"""
from auctionSimulator.hw4.agents.pointPredictionAgent import *

class straightMV(pointPredictionAgent):
    """
    straightMV bids marginal values for all goods.
    """
    @staticmethod
    def type():
        return "straightMV"
    
    @staticmethod
    def SS(args={}):
        """
        Calculate the marginal values of all goods for auction
        given the predicted prices.
        
        NOTE:
            Bid on all available goods, don't solve acq for overall best bundle.
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
        
        marginalValueBid = []
        for idx in xrange(args['bundles'].shape[1]):
            tempPriceInf = numpy.array(pricePrediction).astype(numpy.float)
            tempPriceInf[idx] = float('inf')
            tempPriceZero = numpy.array(pricePrediction)
            tempPriceZero[idx] = 0 
            
            optBundleInf, predictedSurplusInf = simYW.acqYW(bundles     = args['bundles'],
                                                            valuation   = args['valuation'],
                                                            l           = args['l'],
                                                            priceVector = tempPriceInf)
            
            optBundleZero, predictedSurplusZero = simYW.acqYW(bundles     = args['bundles'],
                                                              valuation   = args['valuation'],
                                                              l           = args['l'], 
                                                              priceVector = tempPriceZero)
                
            #this shouldn't happend but just in case.
            if predictedSurplusZero - predictedSurplusInf < 0:
                marginalValueBid.append(0)
            else:
                marginalValueBid.append(predictedSurplusZero - predictedSurplusInf)
            
        return numpy.atleast_1d(marginalValueBid).astype('float')
        
            